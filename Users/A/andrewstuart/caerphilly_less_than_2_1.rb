require 'nokogiri'
require 'mechanize'
require 'open-uri'
require 'date'
require 'json'

def get_postcode(code)
  url = "http://mapit.mysociety.org/postcode/#{code.gsub(' ', '')}"
  data = JSON.parse(open(url).string)
  result = {}
  result[:lat] = data["wgs84_lat"]
  result[:lng] = data["wgs84_lon"]
  return result
  
  rescue
    result = "error"
    return result
end

def get_details(doc)

  rows = doc.search('.uxMainResults tbody tr')

  rows.each do |row|
    details = {}
    details[:name] = row.search('a')[0].inner_text
    details[:id] = row.search('td')[0].search('input')[0][:value]
    details[:link] = row.search('a')[0][:href]
    details[:address] = row.search('.resultAddress')[0].inner_text.strip
    details[:postcode] = row.search('.resultPostcode')[0].inner_text.strip
    details[:rating] = row.search('.resultScore img')[0][:title].scan(/Food hygiene rating is '([0-9]+)': [A-Za-z ]+/)[0][0] rescue "Exempt"
    details[:date] = Date.parse(row.search('td')[2].inner_text.strip)
    details[:rss_date] =  details[:date].strftime("%A, %d %b %Y %H:%M:%S %Z")
    latlng = get_postcode(details[:postcode])
    if latlng != "error"
      details[:lat] = latlng[:lat]
      details[:lng] = latlng[:lng]
    end
    ScraperWiki.save(["id"], details)
  end
  
end

def search(url)
  a = Mechanize.new
  a.get(url) do |page|
    doc = Nokogiri.HTML(page.body)
    get_details(doc)
    
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
      get_details(doc)
      num += 1
    end
  end
end

url = ("http://ratings.food.gov.uk/advanced-search/en-GB?s=2&so=LessThanOrEqual&st=1&pi=0&las=338")

search(url)