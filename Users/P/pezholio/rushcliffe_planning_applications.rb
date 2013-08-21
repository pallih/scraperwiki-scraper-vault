require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `date_scraped` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

ROOT_URL = "http://www.document1.co.uk/blueprint/"

def numeric?(object)
  true if Float(object) rescue false
end

def save_page_links(doc)
  apps = doc.search('#innercolumn .boxlist li:last-child a') #only want details
  puts "Found #{apps.size} applications"
  
  apps.each do |app|
    begin
      record = {}
      record['uid'] = app.inner_text
      record['url'] = 'http://www.document1.co.uk/blueprint/' + app[:href]
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)

  url = ROOT_URL + "copyright.asp?Acpt=&QueryType=5"
  
  a = Mechanize.new
  
  p = a.post(url, {
    'AppType' => 'DC',
  'advDaten3' => (until_date - 14).strftime("%d/%m/%Y") ,
  'advDaten4' => until_date.strftime("%d/%m/%Y") ,
  'AppType' => 'DC',
  'advDatee7' => 'All',
  'locality' => 'All',
  'street' => 'All Streets',
  'property' => 'Enter name or number',
  'startdate' => (until_date - 14).strftime("%d/%m/%Y") ,
  'enddate' => until_date.strftime("%d/%m/%Y") ,
  'Apps' => 'Rec',
  'UndApps' => '',
  'Wards' => ''
  })
  
  page = a.click(p.link_with(:text => /I have read and accept the copyright notice and disclaimer/))
    
  doc = Nokogiri.HTML(page.body)

  pages = doc.search('#pages a:last-child').inner_text.to_i
    
  num = 1
  
  save_page_links(doc)

  while num < pages
    start = (num * 5) + 1
    num += 1
    uri = page.uri.to_s + "&StartingRecord=#{start}&StartPage=#{start}&Page=#{num}"
    doc = Nokogiri.HTML(a.get(uri).body)
    save_page_links(doc)
  end
end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL LIMIT 50")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE start_date > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 50")
  current_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)

  doc = Nokogiri.HTML(open(app_info["url"]).read.encode("utf-8", :invalid => :replace, :undef => :replace))
  
  details_hash = doc.search('.style2 li').inject({}){|hsh,li| hsh[li.at('strong').inner_text.strip] = li.inner_text.gsub(li.at('strong').inner_text.strip, '').strip if li.at('strong');hsh}
    
  details = app_info
  
  details[:address] = details_hash["Address of proposal:"].gsub("(View other applications made for this address)", "").strip
  details[:applicant_address] = details_hash["Address of applicant:"]
  details[:applicant_name] = details_hash["Name of applicant:"]
  details[:start_date] = Date.parse(details_hash["Date received:"])
  details[:date_received] = Date.parse(details_hash["Date received:"])
  details[:description] = details_hash["Proposal:"]
  details[:agent_address] = details_hash["Address of agent:"]
  details[:agent_name] = details_hash["Name of agent:"]
  details[:application_type] = details_hash["Type of application:"]
  details[:case_officer] = details_hash["Case officer:"]
  details[:comment_url] = ROOT_URL + doc.search('#innercolumn a[@href*="Comments.asp?Acpt="]')[0][:href] rescue nil
  details[:consultation_end_date] = Date.parse(details_hash["Consultation period expected to end:"]) rescue nil
  details[:decision] = details_hash["Decision:"]
  details[:decision_date] = Date.parse(details_hash["Date of decision:"]) rescue nil
  details[:easting] = details_hash["OS map references:"].scan(/Easting ([0-9]+); Northing ([0-9]+);/)[0][0]
  details[:northing] = details_hash["OS map references:"].scan(/Easting ([0-9]+); Northing ([0-9]+);/)[0][1]
  details[:parish] = details_hash["Parish:"]
  details[:status] = details_hash["Current status:"]
  details[:ward_name] = details_hash["Ward:"].gsub("(view details of Councillors for this ward)", "").strip
  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)

end

#52.times do |i| 
 #search_for_new_applications(Date.today - (10*(i+i)))
#end

search_for_new_applications
update_stale_applications
