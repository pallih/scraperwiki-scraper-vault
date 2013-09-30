require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://planning.broxtowe.gov.uk/'

def save_page_links(doc)
  apps = doc.search('#ctl00_cph_Body_dlSearchResults .tg2general')
  
  puts "Found #{apps.count} applications"

  apps.each do |app|
    begin
      record = {}
      uid = app.search('.tg2middleright')[0].inner_text
      record['url'] = BASE_URL + "ApplicationDetail.aspx?RefVal=#{uid}"
      record['uid'] = uid
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)
  friday = (until_date..(until_date+7)).find{|d| d.cwday == 5}
  
  url = BASE_URL + '/ApplicationSearch.aspx'
  
  agent = Mechanize.new  
  page = agent.get url
  uri = page.uri
      
  doc = Nokogiri.HTML(page.content)
  
  viewstate = doc.search('#__VIEWSTATE')[0][:value]
  eventvalidation = doc.search('#__EVENTVALIDATION')[0][:value]
  
  data = {
    '__EVENTTARGET' => nil,
    '__EVENTARGUMENT' => nil,
    '__LASTFOCUS' => nil,
    '__VIEWSTATE' => viewstate,
    '__EVENTVALIDATION' => eventvalidation,
    'ctl00$cph_Body$SearchType' => 'rbWeekly',
    'ctl00$cph_Body$ddlWeeklyList' => friday.strftime("%d/%m/%Y"),
    'ctl00$cph_Body$ddlResultsPerPageWeeklyList' => 50,
    'ctl00$cph_Body$cmdWeeklyList' => 'Search'
  }
    
  response = agent.post(uri.to_s, data)
  
  doc = Nokogiri.HTML(response.content)
  
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

  main_detail = doc.search('#ctl00_cph_Body_tblMainDetail tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1] if tr.search('td').count > 1;hsh}
  
  agent_detail = doc.search('#ctl00_cph_Body_tblAgentdetail tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1] if tr.search('td').count > 1;hsh}
  
  application_detail = doc.search('#ctl00_cph_Body_tblApplicationDetail tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text if tr.search('td').count > 1 ;hsh[tr.search('td')[2].inner_text.strip] = tr.search('td')[3].inner_text if tr.search('td').count > 2 ;hsh}
  
  consult_detail = doc.search('#ctl00_cph_Body_Table3 tr').inject({}){|hsh,tr| hsh["Start " + tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text if tr.search('td').count > 2;hsh["End " + tr.search('td')[0].inner_text.strip] = tr.search('td')[2].inner_text if tr.search('td').count > 2;hsh}
  
  details[:date_received] = Date.parse(application_detail["Date Received:"])
  details[:start_date] = Date.parse(application_detail["Date Received:"])
  details[:date_validated] = Date.parse(application_detail["Date Validated:"]) rescue nil
  
  details[:applicant_name] = main_detail["Applicant:"].inner_text rescue nil
  details[:address] = main_detail["Site Address:"].inner_text.gsub("\r", " ").strip rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:description] = main_detail["Proposal:"].inner_text rescue nil
  details[:agent_name] = agent_detail["Name:"].inner_text rescue nil
  details[:agent_address] = agent_detail["Address:"].inner_text.gsub("\r", " ").strip rescue nil
  details[:agent_tel] = agent_detail["Telephone No:"].inner_text rescue nil
  details[:case_officer] = application_detail["Officer Dealing:"] rescue nil
  details[:status] = application_detail["Status:"] rescue nil
  details[:decision_date] = Date.parse(application_detail["Decision Date:"]) rescue nil
  details[:consultation_start_date] = Date.parse(consult_detail["Start Consultees:"]) rescue nil
  details[:consultation_end_date] = Date.parse(consult_detail["End Consultees:"]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(consult_detail["Start Neighbours:"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(consult_detail["End Neighbours:"]) rescue nil
  details[:last_advertised_date] = Date.parse(consult_detail["Start Press Advert:"]) rescue nil
  details[:latest_advertisement_expiry_date] = Date.parse(consult_detail["End Press Advert:"]) rescue nil
  
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
require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://planning.broxtowe.gov.uk/'

def save_page_links(doc)
  apps = doc.search('#ctl00_cph_Body_dlSearchResults .tg2general')
  
  puts "Found #{apps.count} applications"

  apps.each do |app|
    begin
      record = {}
      uid = app.search('.tg2middleright')[0].inner_text
      record['url'] = BASE_URL + "ApplicationDetail.aspx?RefVal=#{uid}"
      record['uid'] = uid
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)
  friday = (until_date..(until_date+7)).find{|d| d.cwday == 5}
  
  url = BASE_URL + '/ApplicationSearch.aspx'
  
  agent = Mechanize.new  
  page = agent.get url
  uri = page.uri
      
  doc = Nokogiri.HTML(page.content)
  
  viewstate = doc.search('#__VIEWSTATE')[0][:value]
  eventvalidation = doc.search('#__EVENTVALIDATION')[0][:value]
  
  data = {
    '__EVENTTARGET' => nil,
    '__EVENTARGUMENT' => nil,
    '__LASTFOCUS' => nil,
    '__VIEWSTATE' => viewstate,
    '__EVENTVALIDATION' => eventvalidation,
    'ctl00$cph_Body$SearchType' => 'rbWeekly',
    'ctl00$cph_Body$ddlWeeklyList' => friday.strftime("%d/%m/%Y"),
    'ctl00$cph_Body$ddlResultsPerPageWeeklyList' => 50,
    'ctl00$cph_Body$cmdWeeklyList' => 'Search'
  }
    
  response = agent.post(uri.to_s, data)
  
  doc = Nokogiri.HTML(response.content)
  
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

  main_detail = doc.search('#ctl00_cph_Body_tblMainDetail tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1] if tr.search('td').count > 1;hsh}
  
  agent_detail = doc.search('#ctl00_cph_Body_tblAgentdetail tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1] if tr.search('td').count > 1;hsh}
  
  application_detail = doc.search('#ctl00_cph_Body_tblApplicationDetail tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text if tr.search('td').count > 1 ;hsh[tr.search('td')[2].inner_text.strip] = tr.search('td')[3].inner_text if tr.search('td').count > 2 ;hsh}
  
  consult_detail = doc.search('#ctl00_cph_Body_Table3 tr').inject({}){|hsh,tr| hsh["Start " + tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text if tr.search('td').count > 2;hsh["End " + tr.search('td')[0].inner_text.strip] = tr.search('td')[2].inner_text if tr.search('td').count > 2;hsh}
  
  details[:date_received] = Date.parse(application_detail["Date Received:"])
  details[:start_date] = Date.parse(application_detail["Date Received:"])
  details[:date_validated] = Date.parse(application_detail["Date Validated:"]) rescue nil
  
  details[:applicant_name] = main_detail["Applicant:"].inner_text rescue nil
  details[:address] = main_detail["Site Address:"].inner_text.gsub("\r", " ").strip rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:description] = main_detail["Proposal:"].inner_text rescue nil
  details[:agent_name] = agent_detail["Name:"].inner_text rescue nil
  details[:agent_address] = agent_detail["Address:"].inner_text.gsub("\r", " ").strip rescue nil
  details[:agent_tel] = agent_detail["Telephone No:"].inner_text rescue nil
  details[:case_officer] = application_detail["Officer Dealing:"] rescue nil
  details[:status] = application_detail["Status:"] rescue nil
  details[:decision_date] = Date.parse(application_detail["Decision Date:"]) rescue nil
  details[:consultation_start_date] = Date.parse(consult_detail["Start Consultees:"]) rescue nil
  details[:consultation_end_date] = Date.parse(consult_detail["End Consultees:"]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(consult_detail["Start Neighbours:"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(consult_detail["End Neighbours:"]) rescue nil
  details[:last_advertised_date] = Date.parse(consult_detail["Start Press Advert:"]) rescue nil
  details[:latest_advertisement_expiry_date] = Date.parse(consult_detail["End Press Advert:"]) rescue nil
  
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
