require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = "http://maps.rochford.gov.uk/DevelopmentControl.aspx?"

def save_page_links(doc)
  apps = doc.search('//a[contains(@href,"Filter=^REFVAL^")]')
    
  apps.each do |app|
    begin
      record = {}
      record['url'] = app[:href]
      record['uid'] = record['url'].scan(/Filter=\^REFVAL\^='([0-9\/A-Z]+)'/)[0][0]
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
  
end

def search_for_new_applications(until_date=Date.today)
  
  url = BASE_URL + "requesttype=parsetemplate&template=DevelopmentControlResults.tmplt&filter=%5Eq%5E%20ILIKE%20%27%25%20Enter%20an%20application%20number%20or%20address%25%27%5E%2C%5EDCSTAT%5E=%27%2C%27%5E%2C%5EDATEAPRECV%5E%20between%20%27#{(until_date).strftime("%Y-%m-%d")}%27%20AND%20%27#{(until_date - 14).strftime("%Y-%m-%d")}%27%5E&pagerecs=10&useSearch=true&order=DATEAPRECV%3ADESCENDING&maxrecords=100&basepage=DevelopmentControl.aspx&pageno=1"
    
  doc = Nokogiri.HTML(open(url))

  pages = doc.search('//div[@id="atSearchAgain"]/following::div[1]/a[last()]').inner_text.to_i
  
  num = 1
  
  pages.times do  
    url = BASE_URL + "requesttype=parsetemplate&template=DevelopmentControlResults.tmplt&filter=%5Eq%5E%20ILIKE%20%27%25%20Enter%20an%20application%20number%20or%20address%25%27%5E%2C%5EDCSTAT%5E=%27%2C%27%5E%2C%5EDATEAPRECV%5E%20between%20%27#{(until_date).strftime("%Y-%m-%d")}%27%20AND%20%27#{(until_date - 14).strftime("%Y-%m-%d")}%27%5E&pagerecs=10&useSearch=true&order=DATEAPRECV%3ADESCENDING&maxrecords=100&basepage=DevelopmentControl.aspx&pageno=#{num}"
        
    doc = Nokogiri.HTML(open(url))  
    save_page_links(doc)
    
    num += 1
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
  url = app_info['url'].gsub('^', '%5E')

  doc = Nokogiri.HTML(open(url))
  
  details = app_info
  
  dts = doc.search('#atTabs dt')
  dds = doc.search('#atTabs dd')
  
  i = 0
  details_hash = {}
  
  dts.each do |dt|
    details_hash[dt.inner_text] = dds[i].inner_text
    i += 1
  end
  
  details[:planning_portal_id] = details_hash["Planning Portal Reference Number:"] rescue nil
  details[:address] = details_hash["Address Of Proposal:"] rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:description] = details_hash["Proposal:"] rescue nil
  details[:application_type] = details_hash["Type of Application:"] rescue nil
  details[:status] = details_hash["Status:"] rescue nil
  details[:decision] = details_hash["Decision:"] rescue nil
  details[:appeal_result] = details_hash["Appeal Status:"] rescue nil
  details[:case_officer] = details_hash["Case Officer:"] rescue nil
  details[:ward_name] = details_hash["Ward:"] rescue nil
  details[:parish] = details_hash["Parish:"] rescue nil
  details[:applicant_name] = details_hash["Applicant Name:"] rescue nil
  details[:agent_name] = details_hash["Agent Name:"] rescue nil
  details[:agent_address] = details_hash["Agent Address:"] rescue nil
  details[:applicant_address] = details_hash["Applicants' Address:"] rescue nil
  details[:date_received] = Date.parse(details_hash["Date Application Received:"])
  details[:start_date] = Date.parse(details_hash["Date Application Received:"])
  details[:date_validated] = Date.parse(details_hash["Date Application Validated:"]) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash["Standard Consultations sent on:"]) rescue nil
  details[:consultation_end_date] = Date.parse(details_hash["Expiry Date for Standard Consultations:"]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(details_hash["Neighbourhood Consultations sent on:"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(details_hash["Expiry Date for Neighbour Consultations:"]) rescue nil
  details[:decision_date] = Date.parse(details_hash["Date Decision Made:"]) rescue nil
  details[:target_decision_date] = Date.parse(details_hash["Target Decision Date"]) rescue nil
  details[:appeal_date] = Date.parse(details_hash["Appeal Start Date:"]) rescue nil
  details[:appeal_decision_date] = Date.parse(details_hash["Appeal Decision Date:"]) rescue nil
  details[:last_advertised_date] = Date.parse(details_hash["Last advertised on:"]) rescue nil
  details[:latest_advertisement_expiry_date] = Date.parse(details_hash["Expiry Date for Latest Advertisement:"]) rescue nil
  details[:decision_date] = Date.parse(details_hash["Date Decision Made:"]) rescue nil
  details[:decision_issued_date] = Date.parse(details_hash["Date Decision Issued:"]) rescue nil
  details[:permission_expires_date] = Date.parse(details_hash["Permission Expiry Date:"]) rescue nil

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
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = "http://maps.rochford.gov.uk/DevelopmentControl.aspx?"

def save_page_links(doc)
  apps = doc.search('//a[contains(@href,"Filter=^REFVAL^")]')
    
  apps.each do |app|
    begin
      record = {}
      record['url'] = app[:href]
      record['uid'] = record['url'].scan(/Filter=\^REFVAL\^='([0-9\/A-Z]+)'/)[0][0]
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
  
end

def search_for_new_applications(until_date=Date.today)
  
  url = BASE_URL + "requesttype=parsetemplate&template=DevelopmentControlResults.tmplt&filter=%5Eq%5E%20ILIKE%20%27%25%20Enter%20an%20application%20number%20or%20address%25%27%5E%2C%5EDCSTAT%5E=%27%2C%27%5E%2C%5EDATEAPRECV%5E%20between%20%27#{(until_date).strftime("%Y-%m-%d")}%27%20AND%20%27#{(until_date - 14).strftime("%Y-%m-%d")}%27%5E&pagerecs=10&useSearch=true&order=DATEAPRECV%3ADESCENDING&maxrecords=100&basepage=DevelopmentControl.aspx&pageno=1"
    
  doc = Nokogiri.HTML(open(url))

  pages = doc.search('//div[@id="atSearchAgain"]/following::div[1]/a[last()]').inner_text.to_i
  
  num = 1
  
  pages.times do  
    url = BASE_URL + "requesttype=parsetemplate&template=DevelopmentControlResults.tmplt&filter=%5Eq%5E%20ILIKE%20%27%25%20Enter%20an%20application%20number%20or%20address%25%27%5E%2C%5EDCSTAT%5E=%27%2C%27%5E%2C%5EDATEAPRECV%5E%20between%20%27#{(until_date).strftime("%Y-%m-%d")}%27%20AND%20%27#{(until_date - 14).strftime("%Y-%m-%d")}%27%5E&pagerecs=10&useSearch=true&order=DATEAPRECV%3ADESCENDING&maxrecords=100&basepage=DevelopmentControl.aspx&pageno=#{num}"
        
    doc = Nokogiri.HTML(open(url))  
    save_page_links(doc)
    
    num += 1
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
  url = app_info['url'].gsub('^', '%5E')

  doc = Nokogiri.HTML(open(url))
  
  details = app_info
  
  dts = doc.search('#atTabs dt')
  dds = doc.search('#atTabs dd')
  
  i = 0
  details_hash = {}
  
  dts.each do |dt|
    details_hash[dt.inner_text] = dds[i].inner_text
    i += 1
  end
  
  details[:planning_portal_id] = details_hash["Planning Portal Reference Number:"] rescue nil
  details[:address] = details_hash["Address Of Proposal:"] rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:description] = details_hash["Proposal:"] rescue nil
  details[:application_type] = details_hash["Type of Application:"] rescue nil
  details[:status] = details_hash["Status:"] rescue nil
  details[:decision] = details_hash["Decision:"] rescue nil
  details[:appeal_result] = details_hash["Appeal Status:"] rescue nil
  details[:case_officer] = details_hash["Case Officer:"] rescue nil
  details[:ward_name] = details_hash["Ward:"] rescue nil
  details[:parish] = details_hash["Parish:"] rescue nil
  details[:applicant_name] = details_hash["Applicant Name:"] rescue nil
  details[:agent_name] = details_hash["Agent Name:"] rescue nil
  details[:agent_address] = details_hash["Agent Address:"] rescue nil
  details[:applicant_address] = details_hash["Applicants' Address:"] rescue nil
  details[:date_received] = Date.parse(details_hash["Date Application Received:"])
  details[:start_date] = Date.parse(details_hash["Date Application Received:"])
  details[:date_validated] = Date.parse(details_hash["Date Application Validated:"]) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash["Standard Consultations sent on:"]) rescue nil
  details[:consultation_end_date] = Date.parse(details_hash["Expiry Date for Standard Consultations:"]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(details_hash["Neighbourhood Consultations sent on:"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(details_hash["Expiry Date for Neighbour Consultations:"]) rescue nil
  details[:decision_date] = Date.parse(details_hash["Date Decision Made:"]) rescue nil
  details[:target_decision_date] = Date.parse(details_hash["Target Decision Date"]) rescue nil
  details[:appeal_date] = Date.parse(details_hash["Appeal Start Date:"]) rescue nil
  details[:appeal_decision_date] = Date.parse(details_hash["Appeal Decision Date:"]) rescue nil
  details[:last_advertised_date] = Date.parse(details_hash["Last advertised on:"]) rescue nil
  details[:latest_advertisement_expiry_date] = Date.parse(details_hash["Expiry Date for Latest Advertisement:"]) rescue nil
  details[:decision_date] = Date.parse(details_hash["Date Decision Made:"]) rescue nil
  details[:decision_issued_date] = Date.parse(details_hash["Date Decision Issued:"]) rescue nil
  details[:permission_expires_date] = Date.parse(details_hash["Permission Expiry Date:"]) rescue nil

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
