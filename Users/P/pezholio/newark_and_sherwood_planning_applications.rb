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

BASE_URL = 'http://www.nsdc.info/eplanning/'

def save_page_links(doc)
  apps = doc.search('#_ctl0_DataGridList tr')
  apps.shift
  apps.pop
  
  puts "Found #{apps.count} applications"
  
  apps.each do |app|
    begin
      record = {}
      link = app.search('a')[0]
      record['url'] = BASE_URL + link[:href]
      record['uid'] = link.inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end

end

def search_for_new_applications(until_date=Date.today)
  url = BASE_URL + "default.aspx?sid=1&sindex=1&id=1&limit=0&start=#{(until_date - 14).strftime("%d/%m/%Y")}&end=#{(until_date).strftime("%d/%m/%Y")}"
  
  agent = Mechanize.new do |browser|
    browser.user_agent_alias = 'Linux Firefox'
    end
    
    page = agent.get(url)
    
    page.form_with(:name => 'Form1') do |f|
      f['__EVENTTARGET'] = ''
      f['__EVENTARGUMENT'] = ''
      f['_ctl0:pgsize'] = 150
      f['_ctl0:Button1'] = 'Change Pagesize'
      page = f.submit()
    end
    
    doc = Nokogiri.HTML(page.body)
      
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

  labels = doc.search('.label')
  contents = doc.search('.field')
  
  i = 0
  details_hash = {}
  
  labels.each do |label|
    unless label.inner_text == "Case Officer" || label.inner_text.force_encoding("BINARY") == "Tel\xC2\xA0"
      details_hash[label.inner_text.force_encoding("BINARY").strip.gsub("\xC2\xA0", " ")] = contents[i].inner_text.strip rescue nil
    end
    unless label.inner_text.force_encoding("BINARY") == "Tel\xC2\xA0"
      i += 1
    end
  end
  
  details[:date_received] = Date.parse(details_hash["Date Received"]) 
  details[:start_date] = Date.parse(details_hash["Date Received"])
  details[:date_validated] = Date.parse(details_hash["Date Validated"]) rescue nil
  details[:target_decision_date] = Date.parse(details_hash["Decision Target Date"]) rescue nil
  details[:decision_date] = Date.parse(details_hash["Date of Decision"]) rescue nil
  
  details[:description] = details_hash["Proposal"] rescue nil
  details[:status] = details_hash["Status"] rescue nil
  details[:applicant_name] = details_hash["Applicants Name"] rescue nil
  details[:applicant_address] = details_hash["Applicants Address"] rescue nil
  details[:agent_name] = details_hash["Agents Name"] rescue nil
  details[:agent_address] = details_hash["Agents Address"] rescue nil
  details[:address] = details_hash["Site Address"] rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:application_type] = details_hash["Type of Application"] rescue nil
  details[:parish] = details_hash["Parish"] rescue nil
  details[:ward_name] = details_hash["Ward"] rescue nil
  details[:os_grid_ref] = details_hash["OS Grid Reference"] rescue nil
  details[:planning_portal_id] = details_hash["Planning Portal Reference"] rescue nil
  
  details[:comment_url] = BASE_URL + doc.search('#_ctl0_DcComments1_LabelCommentLink a')[0][:href] rescue nil
  
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

BASE_URL = 'http://www.nsdc.info/eplanning/'

def save_page_links(doc)
  apps = doc.search('#_ctl0_DataGridList tr')
  apps.shift
  apps.pop
  
  puts "Found #{apps.count} applications"
  
  apps.each do |app|
    begin
      record = {}
      link = app.search('a')[0]
      record['url'] = BASE_URL + link[:href]
      record['uid'] = link.inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end

end

def search_for_new_applications(until_date=Date.today)
  url = BASE_URL + "default.aspx?sid=1&sindex=1&id=1&limit=0&start=#{(until_date - 14).strftime("%d/%m/%Y")}&end=#{(until_date).strftime("%d/%m/%Y")}"
  
  agent = Mechanize.new do |browser|
    browser.user_agent_alias = 'Linux Firefox'
    end
    
    page = agent.get(url)
    
    page.form_with(:name => 'Form1') do |f|
      f['__EVENTTARGET'] = ''
      f['__EVENTARGUMENT'] = ''
      f['_ctl0:pgsize'] = 150
      f['_ctl0:Button1'] = 'Change Pagesize'
      page = f.submit()
    end
    
    doc = Nokogiri.HTML(page.body)
      
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

  labels = doc.search('.label')
  contents = doc.search('.field')
  
  i = 0
  details_hash = {}
  
  labels.each do |label|
    unless label.inner_text == "Case Officer" || label.inner_text.force_encoding("BINARY") == "Tel\xC2\xA0"
      details_hash[label.inner_text.force_encoding("BINARY").strip.gsub("\xC2\xA0", " ")] = contents[i].inner_text.strip rescue nil
    end
    unless label.inner_text.force_encoding("BINARY") == "Tel\xC2\xA0"
      i += 1
    end
  end
  
  details[:date_received] = Date.parse(details_hash["Date Received"]) 
  details[:start_date] = Date.parse(details_hash["Date Received"])
  details[:date_validated] = Date.parse(details_hash["Date Validated"]) rescue nil
  details[:target_decision_date] = Date.parse(details_hash["Decision Target Date"]) rescue nil
  details[:decision_date] = Date.parse(details_hash["Date of Decision"]) rescue nil
  
  details[:description] = details_hash["Proposal"] rescue nil
  details[:status] = details_hash["Status"] rescue nil
  details[:applicant_name] = details_hash["Applicants Name"] rescue nil
  details[:applicant_address] = details_hash["Applicants Address"] rescue nil
  details[:agent_name] = details_hash["Agents Name"] rescue nil
  details[:agent_address] = details_hash["Agents Address"] rescue nil
  details[:address] = details_hash["Site Address"] rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:application_type] = details_hash["Type of Application"] rescue nil
  details[:parish] = details_hash["Parish"] rescue nil
  details[:ward_name] = details_hash["Ward"] rescue nil
  details[:os_grid_ref] = details_hash["OS Grid Reference"] rescue nil
  details[:planning_portal_id] = details_hash["Planning Portal Reference"] rescue nil
  
  details[:comment_url] = BASE_URL + doc.search('#_ctl0_DcComments1_LabelCommentLink a')[0][:href] rescue nil
  
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
