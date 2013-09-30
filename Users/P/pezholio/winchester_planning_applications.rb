require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('BEGIN TRANSACTION;')
#ScraperWiki.sqliteexecute('ALTER TABLE swdata RENAME TO swdata2;');
#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text, `postcode` text, `target_decision_date` text, `planning_portal_id` text, `date_received` text, `agent_tel` text)')
#ScraperWiki.sqliteexecute('INSERT INTO swdata (url, uid, status, date_scraped, applicant_address, address, description, agent_name, applicant_name, agent_address, case_officer, comment_url, decision_date, date_validated, parish, start_date, ward_name, postcode, target_decision_date, planning_portal_id, date_received, agent_tel) SELECT url, uid, status, date_scraped, applicant_address, address, description, agent_name, applicant_name, agent_address, case_officer, comment_url, decision_date, date_validated, parish, start_date, ward_name, postcode, target_decision_date, planning_portal_id, date_recieved, agent_tel FROM swdata2')
#ScraperWiki.sqliteexecute('DROP TABLE swdata2;')
#ScraperWiki.sqliteexecute('COMMIT;')
#exit

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://planningapplications.winchester.gov.uk/PlanningWeb/'

def save_page_links(url)
  doc = Nokogiri.HTML(open(url))
  apps = doc.xpath("//div[contains(@id, 'ctl00_midColumn_results1_results_DC_multiple1_Repeater')]") #only want details
  puts "Found #{apps.size} applications"
  
  apps.each do |app|
    begin
      record = {}
      link = app.search('a')[0]
      record['url'] = BASE_URL + link[:href]
      record['uid'] = link.inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)
  
  url = BASE_URL + "results.aspx?dateapprec1=#{(until_date - 14).strftime("%d/%m/%Y")}&dateapprec2=#{until_date.strftime("%d/%m/%Y")}"
  
  doc = Nokogiri.HTML(open(url))
  
  pages = doc.search('#ctl00_midColumn_results1_results_DC_multiple1_results_DC_multiple_GoToPage1_lblPageTotal').inner_text.to_i
  
  num = 1
  
  while num <= pages
      save_page_links(url + "&PAGE=" + num.to_s)
      num += 1
  end
      
end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL LIMIT 500")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE date_validated > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  
  ref = app_info['uid']

  page = []
  num = 0
  hash = {}
  
  page[0] = "#ctl00_midColumn_results1_results_DC_single1_results_DC_single_ApplicationDetails1_panelDetails"
  page[1] = "#ctl00_midColumn_results1_results_DC_single1_pnlImportantDates"
  page[2] = "#ctl00_midColumn_results1_results_DC_single1_pnlApplicantDetails"
  page[3] = "#ctl00_midColumn_results1_results_DC_single1_pnlAgentDetails"
  
  page.each do |id|
    url = "http://planningapplications.winchester.gov.uk/PlanningWeb/Results.aspx?ID=#{ref}&tab=#{num}"
    
    doc = Nokogiri.HTML(open(url))
    
    details = doc.search(id + ' table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1] if tr.search('td').count > 1;hsh}
    
    details.each do |key,value|
      if value.search('input').count > 0
        hash[key] = value.search('input')[0][:value].strip rescue nil
      else
        hash[key] = value.search('textarea')[0].inner_text.strip rescue nil
      end
    end
    
    num += 1
  end
  
  url = "http://planningapplications.winchester.gov.uk/PlanningWeb/Results.aspx?ID=#{ref}&tab=0"
    
  doc = Nokogiri.HTML(open(url))
  
  details = app_info
  
  details[:date_received] = Date.parse(hash['Date Application Received:']) rescue nil

  unless details[:date_received].nil? 
    details[:start_date] = Date.parse(hash['Date Application Received:'])  
    details[:decision_date] = Date.parse(hash['Decision Date:']) rescue nil
    details[:address] = hash['Address of Proposal:'].gsub("\r", " ").strip rescue nil
    details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
    details[:status] = hash['Status:'].strip rescue nil
    details[:description] = hash['Proposal:'].strip rescue nil
    details[:case_officer] = hash['Case Officer:'].strip rescue nil
    details[:target_decision_date] = Date.parse(hash['Target Decision Date:']) rescue nil
    details[:parish] = hash['Parish:'].strip rescue nil
    details[:ward_name] = hash['Ward:'].strip rescue nil
    details[:planning_portal_id] = hash['Planning Portal Reference:'].strip rescue nil
    details[:applicant_name] = hash['Applicant\'s Name:'].strip rescue nil
    details[:applicant_address] = hash['Applicant\'s Address:'].gsub("\r", " ").strip rescue nil
    details[:agent_name] = hash['Agent\'s Name:'].strip rescue nil
    details[:agent_address] = hash['Address:'].gsub("\r", " ").strip rescue nil
    details[:agent_tel] = hash['Phone Number:'].strip rescue nil
    details[:comment_url] = "http://planningapplications.winchester.gov.uk/PlanningWeb/MakeRepresentation.aspx?id=#{ref}"
  
    details[:date_scraped] = Time.now
  
    ScraperWiki.save([:uid], details)
  end

rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

  #unpopulated_applications = ScraperWiki.select("* from swdata WHERE start_date IS NULL")
  #unpopulated_applications.each do |app|
   # populate_application_details(app)
  #end

#52.times do |i| 
 #search_for_new_applications(Date.today - (10*(i+i)))
#end

search_for_new_applications
update_stale_applications
require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('BEGIN TRANSACTION;')
#ScraperWiki.sqliteexecute('ALTER TABLE swdata RENAME TO swdata2;');
#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text, `postcode` text, `target_decision_date` text, `planning_portal_id` text, `date_received` text, `agent_tel` text)')
#ScraperWiki.sqliteexecute('INSERT INTO swdata (url, uid, status, date_scraped, applicant_address, address, description, agent_name, applicant_name, agent_address, case_officer, comment_url, decision_date, date_validated, parish, start_date, ward_name, postcode, target_decision_date, planning_portal_id, date_received, agent_tel) SELECT url, uid, status, date_scraped, applicant_address, address, description, agent_name, applicant_name, agent_address, case_officer, comment_url, decision_date, date_validated, parish, start_date, ward_name, postcode, target_decision_date, planning_portal_id, date_recieved, agent_tel FROM swdata2')
#ScraperWiki.sqliteexecute('DROP TABLE swdata2;')
#ScraperWiki.sqliteexecute('COMMIT;')
#exit

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://planningapplications.winchester.gov.uk/PlanningWeb/'

def save_page_links(url)
  doc = Nokogiri.HTML(open(url))
  apps = doc.xpath("//div[contains(@id, 'ctl00_midColumn_results1_results_DC_multiple1_Repeater')]") #only want details
  puts "Found #{apps.size} applications"
  
  apps.each do |app|
    begin
      record = {}
      link = app.search('a')[0]
      record['url'] = BASE_URL + link[:href]
      record['uid'] = link.inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)
  
  url = BASE_URL + "results.aspx?dateapprec1=#{(until_date - 14).strftime("%d/%m/%Y")}&dateapprec2=#{until_date.strftime("%d/%m/%Y")}"
  
  doc = Nokogiri.HTML(open(url))
  
  pages = doc.search('#ctl00_midColumn_results1_results_DC_multiple1_results_DC_multiple_GoToPage1_lblPageTotal').inner_text.to_i
  
  num = 1
  
  while num <= pages
      save_page_links(url + "&PAGE=" + num.to_s)
      num += 1
  end
      
end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL LIMIT 500")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE date_validated > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  
  ref = app_info['uid']

  page = []
  num = 0
  hash = {}
  
  page[0] = "#ctl00_midColumn_results1_results_DC_single1_results_DC_single_ApplicationDetails1_panelDetails"
  page[1] = "#ctl00_midColumn_results1_results_DC_single1_pnlImportantDates"
  page[2] = "#ctl00_midColumn_results1_results_DC_single1_pnlApplicantDetails"
  page[3] = "#ctl00_midColumn_results1_results_DC_single1_pnlAgentDetails"
  
  page.each do |id|
    url = "http://planningapplications.winchester.gov.uk/PlanningWeb/Results.aspx?ID=#{ref}&tab=#{num}"
    
    doc = Nokogiri.HTML(open(url))
    
    details = doc.search(id + ' table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1] if tr.search('td').count > 1;hsh}
    
    details.each do |key,value|
      if value.search('input').count > 0
        hash[key] = value.search('input')[0][:value].strip rescue nil
      else
        hash[key] = value.search('textarea')[0].inner_text.strip rescue nil
      end
    end
    
    num += 1
  end
  
  url = "http://planningapplications.winchester.gov.uk/PlanningWeb/Results.aspx?ID=#{ref}&tab=0"
    
  doc = Nokogiri.HTML(open(url))
  
  details = app_info
  
  details[:date_received] = Date.parse(hash['Date Application Received:']) rescue nil

  unless details[:date_received].nil? 
    details[:start_date] = Date.parse(hash['Date Application Received:'])  
    details[:decision_date] = Date.parse(hash['Decision Date:']) rescue nil
    details[:address] = hash['Address of Proposal:'].gsub("\r", " ").strip rescue nil
    details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
    details[:status] = hash['Status:'].strip rescue nil
    details[:description] = hash['Proposal:'].strip rescue nil
    details[:case_officer] = hash['Case Officer:'].strip rescue nil
    details[:target_decision_date] = Date.parse(hash['Target Decision Date:']) rescue nil
    details[:parish] = hash['Parish:'].strip rescue nil
    details[:ward_name] = hash['Ward:'].strip rescue nil
    details[:planning_portal_id] = hash['Planning Portal Reference:'].strip rescue nil
    details[:applicant_name] = hash['Applicant\'s Name:'].strip rescue nil
    details[:applicant_address] = hash['Applicant\'s Address:'].gsub("\r", " ").strip rescue nil
    details[:agent_name] = hash['Agent\'s Name:'].strip rescue nil
    details[:agent_address] = hash['Address:'].gsub("\r", " ").strip rescue nil
    details[:agent_tel] = hash['Phone Number:'].strip rescue nil
    details[:comment_url] = "http://planningapplications.winchester.gov.uk/PlanningWeb/MakeRepresentation.aspx?id=#{ref}"
  
    details[:date_scraped] = Time.now
  
    ScraperWiki.save([:uid], details)
  end

rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

  #unpopulated_applications = ScraperWiki.select("* from swdata WHERE start_date IS NULL")
  #unpopulated_applications.each do |app|
   # populate_application_details(app)
  #end

#52.times do |i| 
 #search_for_new_applications(Date.today - (10*(i+i)))
#end

search_for_new_applications
update_stale_applications
