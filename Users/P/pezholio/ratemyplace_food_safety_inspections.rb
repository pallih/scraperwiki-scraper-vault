require 'nokogiri'
require 'mechanize'
require 'open-uri'
require 'date'
require 'json'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`id` text, `date` text, `date_scraped` text)')
#ScraperWiki.sqliteexecute('UPDATE `swdata` SET date_scraped = NULL WHERE category is NULL')
#exit


def get_postcode(code)
  url = "http://www.uk-postcodes.com/postcode/#{code.gsub(' ', '')}.json"
  data = JSON.parse(open(url).string)
  result = {}
  result[:lat] = data["geo"]["lat"]
  result[:lng] = data["geo"]["lng"]
  return result
  
  rescue
    result = "error"
    return result
end

def get_inspection_page(doc, id)

  rows = doc.search('.uxMainResults tbody tr')

  inspections = []

  rows.each do |row|
    details = {}
    details[:id] = row.search('td')[0].search('input')[0][:value]
    details[:councilid] = id
    details[:date] = Date.parse(row.search('td')[2].inner_text.strip)
    details[:name] = row.search('a')[0].inner_text
    details[:link] = row.search('a')[0][:href]
    details[:address] = row.search('.resultAddress')[0].inner_text.strip
    details[:postcode] = row.search('.resultPostcode')[0].inner_text.strip
    details[:rating] = row.search('.resultScore img')[0][:title].scan(/Food hygiene rating is '([0-9]+)': [A-Za-z ]+/)[0][0] rescue "Exempt"
    details[:rss_date] =  details[:date].strftime("%A, %d %b %Y %H:%M:%S %Z")
    inspections << details
  end

  return inspections

rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating inspection details"
  
end

def get_inspection_detail(details)
    page = Nokogiri.HTML(open(details["link"]))
 
    latlng = get_postcode(details[:postcode])
    if latlng != "error"
      details[:lat] = latlng[:lat]
      details[:lng] = latlng[:lng]
    end
 
    details[:address1] = page.search('#ctl00_ContentPlaceHolder1_uxBusinessAddress1')[0].inner_text.strip rescue nil
    details[:address2] = page.search('#ctl00_ContentPlaceHolder1_uxBusinessAddress2')[0].inner_text.strip rescue nil
    details[:address3] = page.search('#ctl00_ContentPlaceHolder1_uxBusinessAddress3')[0].inner_text.strip rescue nil
    details[:address4] = page.search('#ctl00_ContentPlaceHolder1_uxBusinessAddress4')[0].inner_text.strip rescue nil

    details[:category] = page.search('#ctl00_ContentPlaceHolder1_uxBusinessType')[0].inner_text.strip rescue nil

    details[:date_scraped] = Time.now

    ScraperWiki.save(["id"], details)

rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating inspection details for #{details['link']}"

end

def update_stale_inspections
  unpopulated_inspections = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL LIMIT 500")
  unpopulated_inspections.each do |app|
    get_inspection_detail(app)
  end
end

def search(url, id)
  a = Mechanize.new

  a.get(url) do |page|
    doc = Nokogiri.HTML(page.body)
    
    scraped = []
    
    scraped << get_inspection_page(doc, id)
    
    viewstate = doc.search('#__VIEWSTATE')[0][:value]
    eventvalidation = doc.search('#__EVENTVALIDATION')[0][:value]
    
    total = doc.search('#ctl00_ContentPlaceHolder1_uxResults_labelStatusMessage')[0].inner_text.scan(/The search took [0-9]+.[0-9]+ seconds and returned ([0-9]+) items./)[0][0].to_i
    pages = total / 10
    num = 1
    
    while num <= pages
      page = a.post(url, {
        "__VIEWSTATE" => viewstate,
        "__EVENTVALIDATION" => eventvalidation,
        "ctl00$ContentPlaceHolder1$uxResults$lnkNext" => "Next >",
        "ctl00$ContentPlaceHolder1$hiddenDialogClose" => "Close",
        "ctl00$ContentPlaceHolder1$hiddenDialogClose" => num
      })
      doc = Nokogiri.HTML(page.body)
      viewstate = doc.search('#__VIEWSTATE')[0][:value]
      eventvalidation = doc.search('#__EVENTVALIDATION')[0][:value]
      scraped << get_inspection_page(doc, id)
      num += 1
    end

    old = Hash.new
    ScraperWiki.select("id, date from swdata").each { |i| old[i["id"]] = i["date"]}

    puts scraped.to_yaml

    scraped.flatten.each do |i|
      if old.has_key?(i[:id].to_s) === FALSE
        get_inspection_detail(i)
        puts "Adding new inspection for #{i[:name]}"
      elsif old[i[:id]] != i[:date].to_s
        get_inspection_detail(i)
        puts "Updating inspection for #{i[:name]}"
      end
    end

  end
end

update_stale_inspections

#ids = ["382","364"]
#ids.each do |id|
 # url = ("http://ratings.food.gov.uk/advanced-search/en-GB?st=1&las=#{id}")
 # search(url, id)
#end