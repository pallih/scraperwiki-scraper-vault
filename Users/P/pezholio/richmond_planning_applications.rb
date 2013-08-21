require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `date_scraped` text,`start_date` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://www2.richmond.gov.uk/PlanData2/'

def save_page_links(doc)
  apps = doc.search("table.blueCellBorders tbody tr") 
  puts "Found #{apps.size} applications"
  
  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app.search('a')[0][:href]
      record['uid'] = app.search('td')[1].inner_text.strip
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + "planning_summary.aspx?strWeekListType=SRCH&strDecFrom=&strDecTo=&strRecFrom=#{(until_date - 14).strftime('%d-%b-%Y')}&strRecTo=#{(until_date).strftime('%d-%b-%Y')}&strWard=ALL&strAppTyp=ALL&strWardTxt=All%20Wards&strAppTypTxt=ALL%20-%20all%20applications&strAppStat=ALL&strAppStatTxt=All%20Applications&strStreet=ALL&strStreetTxt=All%20Streets&strLimit=350&strOrder=REC_DEC&strOrderTxt=Most%20recently%20received%20first"
    
  doc = Nokogiri.HTML(open(url))
    
  save_page_links(doc)

end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE date_validated > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  url = app_info['url']

  doc = Nokogiri.HTML(open(url))

  details = app_info

  latlng = doc.search('#amap')[0][:href].scan(/http:\/\/maps.google.com\/\?q=(-?[0-9]+.[0-9]+),(-?[0-9]+.[0-9]+)&z=24&output=embed/)[0] rescue nil
  
  details[:date_received] = Date.parse(doc.search('#cd_ap_stage1 .date')[0].inner_text)
  details[:start_date] = Date.parse(doc.search('#cd_ap_stage1 .date')[0].inner_text)
  details[:date_validated] = Date.parse(doc.search('#cd_ap_stage2 .date')[0].inner_text) rescue nil
  details[:consultation_start_date] = Date.parse(doc.search('#cd_ap_stage3 .date')[0].inner_text) rescue nil
  details[:consultation_end_date] = Date.parse(doc.search('#cd_ap_stage4 .date')[0].inner_text) rescue nil
  details[:decision_issued_date] = Date.parse(doc.search('#cd_ap_stage7 .date')[0].inner_text) rescue nil
  details[:status] = doc.search('#ctl00_PageContent_lbl_Status')[0].inner_text rescue nil
  details[:applicant_name] = doc.search('#ctl00_PageContent_lbl_Applic_Name')[0].inner_text..gsub(/\r/," ") rescue nil
  details[:agent_name] = doc.search('#ctl00_PageContent_lbl_Agent_Name')[0].inner_text.strip rescue nil
  details[:applicant_address] = doc.search('#ctl00_PageContent_lbl_Applic_Address')[0].inner_text.gsub(/\r/," ") rescue nil
  details[:agent_address] = doc.search('#ctl00_PageContent_lbl_Agent_Address')[0].inner_text.gsub(/\r/," ") rescue nil
  details[:description] = doc.search('#ctl00_PageContent_lbl_Proposal')[0].inner_text.gsub(/\r/," ") rescue nil
  details[:address] = doc.search('#ctl00_PageContent_lbl_Site_description')[0].inner_text.gsub(/\r/," ") rescue nil
  details[:lat] = latlng[0]
  details[:lng] = latlng[1]
  details[:application_type] = doc.search('#ctl00_PageContent_lbl_App_Type')[0].inner_text rescue nil
  details[:case_officer] = doc.search('#ctl00_PageContent_lbl_Officer')[0].inner_text rescue nil
  details[:ward_name] = doc.search('#ctl00_PageContent_lbl_Ward')[0].inner_text rescue nil
  
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
