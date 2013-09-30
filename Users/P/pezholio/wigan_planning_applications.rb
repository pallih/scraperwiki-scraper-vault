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

BASE_URL = 'http://kinnear.wigan.gov.uk/planapps/'

def save_page_links(doc)

  apps = doc.search('//a[contains(@href,"PlanAppsDetails.asp?passAppNo=")]')
  
  puts "Found #{apps.count} applications"
  
  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app[:href]
      record['uid'] = app.inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end

end

def search_for_new_applications(until_date=Date.today)

  data = {
    'txtAppNo' => nil,
    'txtApplicant' => nil,
    'txtSiteAddress' => nil,
    'txtProposal' => nil,
    'selNewWard' => nil,
    'selOldWard' => '%',
    'selAppTyp' => '%',
    'selAppStat' => '%',
    'selAppDecsn' => '%',
    'txtAgentName' => nil,
    'txtAppRecFromDate' => (until_date - 14).strftime("%d/%m/%Y"),
    'txtAppRecToDate' => (until_date).strftime("%d/%m/%Y"),
    'btnSearch' => 'Search'  
  }
  
  response  = Typhoeus::Request.post(BASE_URL + 'PlanAppsResults.asp', :params => data)
  
  doc = Nokogiri.HTML(response.body)
  
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

  doc = Nokogiri.HTML(open(url))
  
  labels = doc.search('td.minor')
  contents = doc.search('//td[not(@class)]')
  
  i = 0
  details_hash = {}
  
  labels.each do |label|
    details_hash[label.inner_text.strip] = contents[i].inner_text.strip
    i += 1
  end
  
  details[:date_received] = Date.parse(details_hash["Date Application Received"])
  details[:start_date] = Date.parse(details_hash["Date Application Received"])
  details[:target_decision_date] = Date.parse(details_hash["Decision Target Date"]) rescue nil
  details[:decision_date] = Date.parse(details_hash["Date Decision Made"]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(details_hash["Neighbour Consultations sent"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(details_hash["Neighbour Consultation expires"]) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash["Standard Consultations sent"]) rescue nil
  details[:consultation_end_date] = Date.parse(details_hash["Standard Consultation expires"]) rescue nil
  details[:decision_issued_date] = Date.parse(details_hash["Date Decision Issued"]) rescue nil
  details[:permission_expires_date] = Date.parse(details_hash["Permission Expires on"]) rescue nil
  
  details[:date_validated] = Date.parse(details_hash["Date Application Validated"]) rescue nil
  details[:address] = details_hash["Address of Proposal"] rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:description] = details_hash["Proposal"] rescue nil
  details[:application_type] = details_hash["Type of Application"] rescue nil
  details[:status] = details_hash["Status"] rescue nil
  details[:decision] = details_hash["Decision"] rescue nil
  details[:case_officer] = details_hash["Case Officer"] rescue nil
  details[:ward_name] = details_hash["Ward"] rescue nil
  details[:applicant_name] = details_hash["Applicant's Name"] rescue nil
  details[:applicant_address] = details_hash["Applicant's Address"] rescue nil
  details[:agent_name] = details_hash["Agent's Name"] rescue nil
  details[:agent_address] = details_hash["Agent's Address"] rescue nil
  
  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

#52.times do |i| 
# search_for_new_applications(Date.today - (10*(i+i)))
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

BASE_URL = 'http://kinnear.wigan.gov.uk/planapps/'

def save_page_links(doc)

  apps = doc.search('//a[contains(@href,"PlanAppsDetails.asp?passAppNo=")]')
  
  puts "Found #{apps.count} applications"
  
  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app[:href]
      record['uid'] = app.inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end

end

def search_for_new_applications(until_date=Date.today)

  data = {
    'txtAppNo' => nil,
    'txtApplicant' => nil,
    'txtSiteAddress' => nil,
    'txtProposal' => nil,
    'selNewWard' => nil,
    'selOldWard' => '%',
    'selAppTyp' => '%',
    'selAppStat' => '%',
    'selAppDecsn' => '%',
    'txtAgentName' => nil,
    'txtAppRecFromDate' => (until_date - 14).strftime("%d/%m/%Y"),
    'txtAppRecToDate' => (until_date).strftime("%d/%m/%Y"),
    'btnSearch' => 'Search'  
  }
  
  response  = Typhoeus::Request.post(BASE_URL + 'PlanAppsResults.asp', :params => data)
  
  doc = Nokogiri.HTML(response.body)
  
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

  doc = Nokogiri.HTML(open(url))
  
  labels = doc.search('td.minor')
  contents = doc.search('//td[not(@class)]')
  
  i = 0
  details_hash = {}
  
  labels.each do |label|
    details_hash[label.inner_text.strip] = contents[i].inner_text.strip
    i += 1
  end
  
  details[:date_received] = Date.parse(details_hash["Date Application Received"])
  details[:start_date] = Date.parse(details_hash["Date Application Received"])
  details[:target_decision_date] = Date.parse(details_hash["Decision Target Date"]) rescue nil
  details[:decision_date] = Date.parse(details_hash["Date Decision Made"]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(details_hash["Neighbour Consultations sent"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(details_hash["Neighbour Consultation expires"]) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash["Standard Consultations sent"]) rescue nil
  details[:consultation_end_date] = Date.parse(details_hash["Standard Consultation expires"]) rescue nil
  details[:decision_issued_date] = Date.parse(details_hash["Date Decision Issued"]) rescue nil
  details[:permission_expires_date] = Date.parse(details_hash["Permission Expires on"]) rescue nil
  
  details[:date_validated] = Date.parse(details_hash["Date Application Validated"]) rescue nil
  details[:address] = details_hash["Address of Proposal"] rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:description] = details_hash["Proposal"] rescue nil
  details[:application_type] = details_hash["Type of Application"] rescue nil
  details[:status] = details_hash["Status"] rescue nil
  details[:decision] = details_hash["Decision"] rescue nil
  details[:case_officer] = details_hash["Case Officer"] rescue nil
  details[:ward_name] = details_hash["Ward"] rescue nil
  details[:applicant_name] = details_hash["Applicant's Name"] rescue nil
  details[:applicant_address] = details_hash["Applicant's Address"] rescue nil
  details[:agent_name] = details_hash["Agent's Name"] rescue nil
  details[:agent_address] = details_hash["Agent's Address"] rescue nil
  
  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

#52.times do |i| 
# search_for_new_applications(Date.today - (10*(i+i)))
#end

search_for_new_applications
update_stale_applications
