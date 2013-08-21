require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://www.reigate-banstead.gov.uk/Planit2/planit2.jsp?'

def save_page_links(doc)
  apps = doc.search('.contentgreenback .result')

  puts "Found #{apps.count} applications"
  
  apps.each do |app|
    begin
      record = {}
      link = app.search('a')[0]
      record['uid'] = link.inner_text.strip
      record['url'] = BASE_URL + "Controller=p2Controller&Action=FindApplicationByRefvalAction&REFVAL=" + record['uid']
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end

end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + "Controller=p2Controller&Action=FindApplicationsByDatesAction&START_DD=#{(until_date - 14).strftime("%d")}&START_MMM=#{(until_date - 14).strftime("%b")}&START_YYYY=#{(until_date - 14).strftime("%Y")}&END_DD=#{(until_date).strftime("%d")}&END_MMM=#{(until_date).strftime("%b")}&END_YYYY=#{(until_date).strftime("%Y")}&WARD=ALL&areabutton=Search"
  
  doc = Nokogiri.HTML(open(url))
  
  results = Float(doc.search('.resultsbox h3').inner_text.scan(/Applications [0-9]+ to [0-9]+ of ([0-9]+)/)[0][0])
  
  save_page_links(doc)
  
  pages = ((results - 10) / 10).ceil
  
  pages.times do |i|
    url = BASE_URL + "Controller=p2Controller&Action=FindApplicationsByDatesAction&START_DD=#{(until_date - 14).strftime("%d")}&START_MMM=#{(until_date - 14).strftime("%b")}&START_YYYY=#{(until_date - 14).strftime("%Y")}&END_DD=#{(until_date).strftime("%d")}&END_MMM=#{(until_date).strftime("%b")}&END_YYYY=#{(until_date).strftime("%Y")}&WARD=ALL&CURR=&DECSN=&START_ROW=#{i * 10}&FIRST_TEN_SHOWN=Y&SEARCH_DIRECTION=F"
    
    doc = Nokogiri.HTML(open(url))
    
    save_page_links(doc)
  end

end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE date_received > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  url = app_info['url']

  doc = Nokogiri.HTML(open(url))

  details = app_info
  
  details_hash = doc.search('#planitdetails-table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1] if tr.search('td').count > 1;hsh}
  
  datesurl = url.gsub('FindApplicationByRefvalAction', 'ShowApplicationDetailsDates')
  
  datesdoc = Nokogiri.HTML(open(datesurl))
  
  labels = datesdoc.search('.label')
  content = datesdoc.search('.details')
  
  i = 0
  dates_hash = {}
  
  labels.each do |label|
    dates_hash[label.inner_text] = content[i].inner_text
    i += 1
  end
  
  details[:date_received] = Date.parse(details_hash["Date Valid"].inner_text)
  details[:start_date] = Date.parse(details_hash["Date Valid"].inner_text)
  
  details[:ward_name] = details_hash["Ward"].inner_text rescue nil
  details[:address] = doc.search('.contentgreenback h3')[0].inner_text.gsub("Address: ", "").gsub("\r", " ").strip
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:description] = doc.search('.contentgreenback h3')[1].inner_text.gsub("Proposal: ", "") rescue nil
  applicant = details_hash["Applicant"].inner_html.split("<br>") rescue nil
  details[:applicant_name] = applicant[0] rescue nil
  details[:applicant_address] = applicant[1].gsub("\r", " ").strip rescue nil
  agent = details_hash["Agent"].inner_html.split("<br>") rescue nil
  details[:agent_name] = agent[0] rescue nil
  details[:agent_address] = agent[1].gsub("\r", " ").strip rescue nil
  details[:decision_date] = Date.parse(details_hash["Decision Date"].inner_text) rescue nil
  details[:decision] = details_hash["Decision"].inner_text rescue nil
  details[:appeal_date] = Date.parse(details_hash["Appeal Date"].inner_text) rescue nil 
  details[:target_decision_date] = Date.parse(dates_hash["Target Determination Date:"]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(dates_hash["Neighbour Notifications sent on:"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(dates_hash["Expiry Date for Neighbour Notifications:"]) rescue nil
  details[:consultation_start_date] = Date.parse(dates_hash["Standard Consultations sent on:"]) rescue nil
  details[:consultation_end_date] = Date.parse(dates_hash["Expiry Date for Standard Consultations:"]) rescue nil
  details[:last_advertised_date] = Date.parse(dates_hash["Last Advertised in press:"]) rescue nil
  details[:latest_advertisement_expiry_date] = Date.parse(dates_hash["Expiry Date for Latest Advertisement:"]) rescue nil
  
  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

#52.times do |i| 
 #search_for_new_applications(Date.today - (10*(i+i)))
#end

search_for_new_applications
update_stale_applications