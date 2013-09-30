require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'
require 'httpclient'

OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = "https://ppc.ipswich.gov.uk/"

def save_page_links(doc)

  apps = doc.search('.resulttable tr')
  
  apps.shift
  
  puts "Found #{apps.count} applications"

  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app.search('a')[0][:href]
      record['uid'] = app.search('td')[0].inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{app}"
    end
  end

end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + "appnresults.asp?txtValStartDate=#{(until_date - 14).strftime("%d%%2F%m%%2F%Y")}&txtValEndDate=#{until_date.strftime("%d%%2F%m%%2F%Y")}&pnlAdvancedOpen=1"
    
  doc = Nokogiri.HTML(open(url))
  
  results = Float(doc.search('#pnlHeader p')[0].inner_text.scan(/([0-9]+) applications found based on the following search criteria/)[0][0])
    
  save_page_links(doc)
  
  pages = ((results - 10) / 10).ceil
    
  pages.times do |i|
    url = url + "pageNumber=#{i + 1}"
    
    doc = Nokogiri.HTML(open(url))
    
    save_page_links(doc)
  end

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
  
  labels = doc.search('.formtable th')
  contents = doc.search('.formtable .formbox')
  
  i = 0
  details_hash = {}
  
  labels.each do |label|
    unless contents[i].nil? 
      if contents[i].name == "textarea"
        details_hash[label.inner_text.strip] = contents[i].inner_text.gsub(/\r/," ")
      elsif contents[i].name == "input"
        details_hash[label.inner_text.strip] = contents[i][:value].strip
      else
        details_hash[label.inner_text.strip] = ""
      end
      i += 1
    end
  end
  
  details[:address] = details_hash["Address Of Proposal"].strip rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:description] = details_hash["Proposal"] rescue nil
  details[:application_type] = details_hash["Type of Application"] rescue nil
  details[:status] = details_hash["Status"] rescue nil
  details[:appeal_result] = details_hash["Appeal Decision"] rescue nil
  details[:case_officer] = details_hash["Case Officer"] rescue nil
  details[:ward_name] = details_hash["Current Ward"] rescue nil
  details[:date_received] = Date.parse(details_hash["Date Application Received"])
  details[:start_date] = Date.parse(details_hash["Date Application Received"])
  details[:date_validated] = Date.parse(details_hash["Date Application Validated"]) rescue nil
  details[:target_decision_date] = Date.parse(details_hash["Eight Week Target Date"]) rescue nil
  details[:meeting_date] = Date.parse(details_hash["Actual Committee Date"]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(details_hash["Neighbour Consultations sent on"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(details_hash["Expiry Date for Neighbour Consultations"]) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash["Standard Consultations sent on"]) rescue nil
  details[:consultation_end_date] = Date.parse(details_hash["Expiry Date for Standard Consultations"]) rescue nil
  details[:last_advertised_date] = Date.parse(details_hash["Advertised on"]) rescue nil
  details[:latest_advertisement_expiry_date] = Date.parse(details_hash["Expiry Date for Advertisement"]) rescue nil
  details[:decision_date] = Date.parse(details_hash["Date Decision Made"]) rescue nil
  details[:appeal_date] = Date.parse(details_hash["Date Appeal Lodged"]) rescue nil
  details[:appeal_decision_date] = Date.parse(details_hash["Date of Decision on Appeal"]) rescue nil
  details[:applicant_name] = details_hash["Applicant's Name"] rescue nil
  details[:applicant_address] = details_hash["Applicant's Name"] rescue nil
  details[:agent_name] = details_hash["Agent's Name"] rescue nil
  details[:agent_address] = details_hash["Agent's Address"] rescue nil
  details[:agent_tel] = details_hash["Agent's Phone Number"] rescue nil
  
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
require 'httpclient'

OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = "https://ppc.ipswich.gov.uk/"

def save_page_links(doc)

  apps = doc.search('.resulttable tr')
  
  apps.shift
  
  puts "Found #{apps.count} applications"

  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app.search('a')[0][:href]
      record['uid'] = app.search('td')[0].inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{app}"
    end
  end

end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + "appnresults.asp?txtValStartDate=#{(until_date - 14).strftime("%d%%2F%m%%2F%Y")}&txtValEndDate=#{until_date.strftime("%d%%2F%m%%2F%Y")}&pnlAdvancedOpen=1"
    
  doc = Nokogiri.HTML(open(url))
  
  results = Float(doc.search('#pnlHeader p')[0].inner_text.scan(/([0-9]+) applications found based on the following search criteria/)[0][0])
    
  save_page_links(doc)
  
  pages = ((results - 10) / 10).ceil
    
  pages.times do |i|
    url = url + "pageNumber=#{i + 1}"
    
    doc = Nokogiri.HTML(open(url))
    
    save_page_links(doc)
  end

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
  
  labels = doc.search('.formtable th')
  contents = doc.search('.formtable .formbox')
  
  i = 0
  details_hash = {}
  
  labels.each do |label|
    unless contents[i].nil? 
      if contents[i].name == "textarea"
        details_hash[label.inner_text.strip] = contents[i].inner_text.gsub(/\r/," ")
      elsif contents[i].name == "input"
        details_hash[label.inner_text.strip] = contents[i][:value].strip
      else
        details_hash[label.inner_text.strip] = ""
      end
      i += 1
    end
  end
  
  details[:address] = details_hash["Address Of Proposal"].strip rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:description] = details_hash["Proposal"] rescue nil
  details[:application_type] = details_hash["Type of Application"] rescue nil
  details[:status] = details_hash["Status"] rescue nil
  details[:appeal_result] = details_hash["Appeal Decision"] rescue nil
  details[:case_officer] = details_hash["Case Officer"] rescue nil
  details[:ward_name] = details_hash["Current Ward"] rescue nil
  details[:date_received] = Date.parse(details_hash["Date Application Received"])
  details[:start_date] = Date.parse(details_hash["Date Application Received"])
  details[:date_validated] = Date.parse(details_hash["Date Application Validated"]) rescue nil
  details[:target_decision_date] = Date.parse(details_hash["Eight Week Target Date"]) rescue nil
  details[:meeting_date] = Date.parse(details_hash["Actual Committee Date"]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(details_hash["Neighbour Consultations sent on"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(details_hash["Expiry Date for Neighbour Consultations"]) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash["Standard Consultations sent on"]) rescue nil
  details[:consultation_end_date] = Date.parse(details_hash["Expiry Date for Standard Consultations"]) rescue nil
  details[:last_advertised_date] = Date.parse(details_hash["Advertised on"]) rescue nil
  details[:latest_advertisement_expiry_date] = Date.parse(details_hash["Expiry Date for Advertisement"]) rescue nil
  details[:decision_date] = Date.parse(details_hash["Date Decision Made"]) rescue nil
  details[:appeal_date] = Date.parse(details_hash["Date Appeal Lodged"]) rescue nil
  details[:appeal_decision_date] = Date.parse(details_hash["Date of Decision on Appeal"]) rescue nil
  details[:applicant_name] = details_hash["Applicant's Name"] rescue nil
  details[:applicant_address] = details_hash["Applicant's Name"] rescue nil
  details[:agent_name] = details_hash["Agent's Name"] rescue nil
  details[:agent_address] = details_hash["Agent's Address"] rescue nil
  details[:agent_tel] = details_hash["Agent's Phone Number"] rescue nil
  
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
