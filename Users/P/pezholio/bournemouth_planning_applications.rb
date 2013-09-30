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

BASE_URL = 'http://planning.bournemouth.gov.uk/RealTimeRegister/'

def save_page_links(doc)

  apps = doc.search('#MainContent_grdResults_ctl00 tbody tr')
  
  puts "Found #{apps.count} applications"
  
  apps.each do |app|
    begin
      record = {}
      link = app.search('a')[0]
      record['uid'] = link.inner_text.strip
      record['url'] = BASE_URL + link[:href]
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end

end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + 'planappsrch.aspx'
  
  doc = Nokogiri.HTML(open(url))
  
  viewstate = doc.search('#__VIEWSTATE')[0]["value"]
  eventvalidation = doc.search('#__EVENTVALIDATION')[0]["value"]
  
  agent = Mechanize.new  
  
  data = {
    '__EVENTTARGET' => nil,
    '__EVENTARGUMENT' => nil,
    '__VIEWSTATE' => viewstate,
    '__EVENTVALIDATION' => eventvalidation,
    'ctl00$ctl00$MainContent$MainContent$txtAppNumber' => "",
    'ctl00$ctl00$MainContent$MainContent$RadStreetName' => "",
    'MainContent_MainContent_RadStreetName_ClientState' => "",
    'ctl00$ctl00$MainContent$MainContent$txtAddress' => "",
    'ctl00$ctl00$MainContent$MainContent$ddlWard' => "",
    'ctl00$ctl00$MainContent$MainContent$txtDateReceivedFrom' => (until_date - 14).strftime("%d/%m/%Y"),
    'ctl00$ctl00$MainContent$MainContent$txtDateReceivedTo' => until_date.strftime("%d/%m/%Y"),
    'ctl00$ctl00$MainContent$MainContent$txtDateIssuedFrom' => "",
    'ctl00$ctl00$MainContent$MainContent$txtDateIssuedTo' => "",
    'ctl00$ctl00$MainContent$MainContent$txtAgentsName' => "",
    'ctl00$ctl00$MainContent$MainContent$ddlApplicationType' => "",
    'ctl00$ctl00$MainContent$MainContent$btnSearch' => 'Search'
  }  

  page = agent.post(url, data)
  
  doc = Nokogiri.HTML(page.content)
  
  results = Float(doc.search('#contenttext b')[0].inner_text.to_i)
    
  pages = ((results - 10) / 10).ceil
  
  save_page_links(doc)
  
  pages.times do
    form = agent.page.form_with(:id => "form1")
    button = form.button_with(:class => "rgPageNext")
    page = agent.submit(form, button)
    doc = Nokogiri.HTML(page.content)
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

  doc = Nokogiri.HTML(open(url))
  
  labels = doc.search('#MainContent_MainContent_RadMultiPage1 label')
  contents = doc.search('//*[@readonly="readonly"]')
  
  i = 0
  details_hash = {}
  
  labels.each do |label|
    unless contents[i].nil? 
      if contents[i].name == "textarea"
        details_hash[label.inner_text.strip] = contents[i].inner_text
      elsif contents[i].name == "input"
        details_hash[label.inner_text.strip] = contents[i][:value]
      else
        details_hash[label.inner_text.strip] = ""
      end
      i += 1
    end
  end
  
  details[:application_type] = details_hash["Type"] rescue nil
  details[:applicant_name] = details_hash["Applicant"] rescue nil
  details[:agent_name] = details_hash["Agent"] rescue nil
  details[:description] = details_hash["Proposal"].strip rescue nil
  details[:date_received] = Date.parse(details_hash["Received Date"])
  details[:start_date] = Date.parse(details_hash["Received Date"])
  details[:date_validated] = Date.parse(details_hash["Valid Date"]) rescue nil
  details[:latest_advertisement_expiry_date] = Date.parse(details_hash["Advert Expiry"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(details_hash["Neighbour Expiry"]) rescue nil
  details[:meeting_date] = Date.parse(details_hash["Committee/Delegated Date"]) rescue nil
  details[:decision_issued_date] = Date.parse(details_hash["Issue Date"]) rescue nil
  details[:decision_date] = Date.parse(details_hash["Decision Date"]) rescue nil
  details[:decision] = details_hash["Decision"] rescue nil
  details[:address] = details_hash["Address"].strip rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:ward_name] = details_hash["Ward"] rescue nil
  details[:parish] = doc.search('#MainContent_MainContent_txtParish')[0][:value] rescue nil
  details[:easting] = doc.search('#MainContent_MainContent_txtEasting')[0][:value] rescue nil
  details[:northing] = doc.search('#MainContent_MainContent_txtNorthing')[0][:value] rescue nil 
  
  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

52.times do |i| 
 search_for_new_applications(Date.today - (10*(i+i)))
end

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

BASE_URL = 'http://planning.bournemouth.gov.uk/RealTimeRegister/'

def save_page_links(doc)

  apps = doc.search('#MainContent_grdResults_ctl00 tbody tr')
  
  puts "Found #{apps.count} applications"
  
  apps.each do |app|
    begin
      record = {}
      link = app.search('a')[0]
      record['uid'] = link.inner_text.strip
      record['url'] = BASE_URL + link[:href]
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end

end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + 'planappsrch.aspx'
  
  doc = Nokogiri.HTML(open(url))
  
  viewstate = doc.search('#__VIEWSTATE')[0]["value"]
  eventvalidation = doc.search('#__EVENTVALIDATION')[0]["value"]
  
  agent = Mechanize.new  
  
  data = {
    '__EVENTTARGET' => nil,
    '__EVENTARGUMENT' => nil,
    '__VIEWSTATE' => viewstate,
    '__EVENTVALIDATION' => eventvalidation,
    'ctl00$ctl00$MainContent$MainContent$txtAppNumber' => "",
    'ctl00$ctl00$MainContent$MainContent$RadStreetName' => "",
    'MainContent_MainContent_RadStreetName_ClientState' => "",
    'ctl00$ctl00$MainContent$MainContent$txtAddress' => "",
    'ctl00$ctl00$MainContent$MainContent$ddlWard' => "",
    'ctl00$ctl00$MainContent$MainContent$txtDateReceivedFrom' => (until_date - 14).strftime("%d/%m/%Y"),
    'ctl00$ctl00$MainContent$MainContent$txtDateReceivedTo' => until_date.strftime("%d/%m/%Y"),
    'ctl00$ctl00$MainContent$MainContent$txtDateIssuedFrom' => "",
    'ctl00$ctl00$MainContent$MainContent$txtDateIssuedTo' => "",
    'ctl00$ctl00$MainContent$MainContent$txtAgentsName' => "",
    'ctl00$ctl00$MainContent$MainContent$ddlApplicationType' => "",
    'ctl00$ctl00$MainContent$MainContent$btnSearch' => 'Search'
  }  

  page = agent.post(url, data)
  
  doc = Nokogiri.HTML(page.content)
  
  results = Float(doc.search('#contenttext b')[0].inner_text.to_i)
    
  pages = ((results - 10) / 10).ceil
  
  save_page_links(doc)
  
  pages.times do
    form = agent.page.form_with(:id => "form1")
    button = form.button_with(:class => "rgPageNext")
    page = agent.submit(form, button)
    doc = Nokogiri.HTML(page.content)
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

  doc = Nokogiri.HTML(open(url))
  
  labels = doc.search('#MainContent_MainContent_RadMultiPage1 label')
  contents = doc.search('//*[@readonly="readonly"]')
  
  i = 0
  details_hash = {}
  
  labels.each do |label|
    unless contents[i].nil? 
      if contents[i].name == "textarea"
        details_hash[label.inner_text.strip] = contents[i].inner_text
      elsif contents[i].name == "input"
        details_hash[label.inner_text.strip] = contents[i][:value]
      else
        details_hash[label.inner_text.strip] = ""
      end
      i += 1
    end
  end
  
  details[:application_type] = details_hash["Type"] rescue nil
  details[:applicant_name] = details_hash["Applicant"] rescue nil
  details[:agent_name] = details_hash["Agent"] rescue nil
  details[:description] = details_hash["Proposal"].strip rescue nil
  details[:date_received] = Date.parse(details_hash["Received Date"])
  details[:start_date] = Date.parse(details_hash["Received Date"])
  details[:date_validated] = Date.parse(details_hash["Valid Date"]) rescue nil
  details[:latest_advertisement_expiry_date] = Date.parse(details_hash["Advert Expiry"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(details_hash["Neighbour Expiry"]) rescue nil
  details[:meeting_date] = Date.parse(details_hash["Committee/Delegated Date"]) rescue nil
  details[:decision_issued_date] = Date.parse(details_hash["Issue Date"]) rescue nil
  details[:decision_date] = Date.parse(details_hash["Decision Date"]) rescue nil
  details[:decision] = details_hash["Decision"] rescue nil
  details[:address] = details_hash["Address"].strip rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:ward_name] = details_hash["Ward"] rescue nil
  details[:parish] = doc.search('#MainContent_MainContent_txtParish')[0][:value] rescue nil
  details[:easting] = doc.search('#MainContent_MainContent_txtEasting')[0][:value] rescue nil
  details[:northing] = doc.search('#MainContent_MainContent_txtNorthing')[0][:value] rescue nil 
  
  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

52.times do |i| 
 search_for_new_applications(Date.today - (10*(i+i)))
end

search_for_new_applications
update_stale_applications
