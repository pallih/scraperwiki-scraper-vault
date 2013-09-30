require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `address` text, `description` text, `start_date` text, `date_validated` text, `application_type` text, `planning_portal_id` text, `case_officer` text, `os_grid_ref` text, `parish` text, `ward_name` text, `decision` text, `decision_date` text, `appeal_result` text, `appeal_decision_date` text, `agent_name` text, `agent_address` text, `applicant_name` text, `applicant_address` text, `date_scraped` text, `date_received` text, `consultation_end_date` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

def titleise(string)
  string.gsub(/\w+/) do |word|
    word.capitalize
  end
end

BASE_URL = 'http://online.carmarthenshire.gov.uk/eaccessv2/'

def save_page_links(link)
  doc = Nokogiri.HTML(open(link))
  rows = doc.search('#TableResults tr')
  rows.shift
  application_links = rows.search('a')
  
  puts "Found #{application_links.size} applications"
  
  application_links.each do |link|
    begin
      record = {}
      record['url'] = BASE_URL + link[:href]
      record['uid'] = link.inner_text
      puts record['uid']
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
  sleep 30
end

def search_for_new_applications(until_date=Date.today)
  search_url = "http://online.carmarthenshire.gov.uk/eaccessv2/SearchAllPCByDetailsResults.aspx?txtPlanningKeywords=&dlPlanningParishs=&dlPlanningWard=&ddlPlanningapplicationtype=0&DCdatefrom=#{(until_date - 14).strftime("%d-%m-%Y")}&DCdateto=#{until_date.strftime("%d-%m-%Y")}&txtDCAgent=&txtDCApplicant=&PageSizeDropDown=10&Sortby=ApplicationNumber"
  
  doc = Nokogiri.HTML(open(search_url))
  
  pages = doc.search('#lblNowShowingTop')
    
  total = pages.text.scan(/Showing [0-9]+ to  [0-9]+ of ([0-9]+) items/)[0][0].to_i

  save_page_links(search_url)

  pages = (total / 10) 
  num = 1
  
  while num <= pages
    save_page_links(search_url + "&PageNumber=" + (num + 1).to_s)
    num += 1
  end

end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL LIMIT 100")
  num = 1
  unpopulated_applications.each do |app|
    populate_application_details(app)
    if num == 10
      sleep 240
      num = 1
    else
      sleep 30 # Trying to ease the load on the server!
      num += 1
    end
  end
  sleep 240
  current_applications = ScraperWiki.select("* from swdata WHERE date_validated > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 100")
  num = 1
  current_applications.each do |app|
    populate_application_details(app)
    if num == 10
      sleep 240
      num = 1
    else
      sleep 30 # Trying to ease the load on the server!
      num += 1
    end
  end
end

def populate_application_details(app_info)
  doc = Nokogiri.HTML(open(app_info['url']))
  
  details_hash = doc.search('.informationarea table tr').inject({}){|hsh,tr| hsh[tr.at('th').inner_text.strip] = tr.search('td').inner_text.strip if tr.at('th');hsh}
  
  details = app_info
  
  details[:address] = titleise(details_hash['Site address']) rescue nil
  details[:description] = titleise(details_hash['Descripton of proposal']) rescue nil
  details[:date_validated] = Date.parse(details_hash['Date valid'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:application_type] = details_hash['Application type'] rescue nil
  details[:planning_portal_id] = details_hash['Planning portal reference'] rescue nil
  details[:case_officer] = details_hash['Case officer'] rescue nil
  details[:os_grid_ref] = details_hash['Grid reference'].gsub(/[\r][\n]/, "").gsub(/[\t]/, "").squeeze rescue nil
  details[:parish] = details_hash['Parish'] rescue nil
  details[:ward_name] = details_hash['Ward'] rescue nil
  details[:decision] = details_hash['Decision'] rescue nil
  details[:decision_date] = Date.parse(details_hash['Decision date'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:appeal_result] = details_hash['Appeal decision'] rescue nil
  details[:appeal_decision_date] = Date.parse(details_hash['Appeal decision date'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:agent_name] = titleise(details_hash['Agent']) rescue nil
  details[:agent_address] = titleise(details_hash['Agent address']) rescue nil
  details[:applicant_name] = titleise(details_hash['Applicant']) rescue nil
  details[:applicant_address] = titleise(details_hash['Applicant address']) rescue nil

  url = doc.search('.nav ul li:last-child a')[0][:href]
  
  dates = Nokogiri.HTML(open(BASE_URL + url))

  dates = dates.search('.informationarea table tr').inject({}){|hsh,tr| hsh[tr.at('th').inner_text.strip] = tr.search('td').inner_text.strip if tr.at('th');hsh}
  
  details[:date_received] = Date.parse(dates['Application Received'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:start_date] = Date.parse(dates['Application Received'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:consultation_end_date] = Date.parse(dates['Consultation expiry date'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil

  details[:date_scraped] = Time.now
  
  unless details[:start_date].nil? 
    ScraperWiki.save([:uid], details)
  end

  rescue Exception => e
    puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

#52.times do |i| 
 #search_for_new_applications(Date.today - (10*(i+i)))
#end

search_for_new_applications
update_stale_applications
require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `address` text, `description` text, `start_date` text, `date_validated` text, `application_type` text, `planning_portal_id` text, `case_officer` text, `os_grid_ref` text, `parish` text, `ward_name` text, `decision` text, `decision_date` text, `appeal_result` text, `appeal_decision_date` text, `agent_name` text, `agent_address` text, `applicant_name` text, `applicant_address` text, `date_scraped` text, `date_received` text, `consultation_end_date` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

def titleise(string)
  string.gsub(/\w+/) do |word|
    word.capitalize
  end
end

BASE_URL = 'http://online.carmarthenshire.gov.uk/eaccessv2/'

def save_page_links(link)
  doc = Nokogiri.HTML(open(link))
  rows = doc.search('#TableResults tr')
  rows.shift
  application_links = rows.search('a')
  
  puts "Found #{application_links.size} applications"
  
  application_links.each do |link|
    begin
      record = {}
      record['url'] = BASE_URL + link[:href]
      record['uid'] = link.inner_text
      puts record['uid']
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
  sleep 30
end

def search_for_new_applications(until_date=Date.today)
  search_url = "http://online.carmarthenshire.gov.uk/eaccessv2/SearchAllPCByDetailsResults.aspx?txtPlanningKeywords=&dlPlanningParishs=&dlPlanningWard=&ddlPlanningapplicationtype=0&DCdatefrom=#{(until_date - 14).strftime("%d-%m-%Y")}&DCdateto=#{until_date.strftime("%d-%m-%Y")}&txtDCAgent=&txtDCApplicant=&PageSizeDropDown=10&Sortby=ApplicationNumber"
  
  doc = Nokogiri.HTML(open(search_url))
  
  pages = doc.search('#lblNowShowingTop')
    
  total = pages.text.scan(/Showing [0-9]+ to  [0-9]+ of ([0-9]+) items/)[0][0].to_i

  save_page_links(search_url)

  pages = (total / 10) 
  num = 1
  
  while num <= pages
    save_page_links(search_url + "&PageNumber=" + (num + 1).to_s)
    num += 1
  end

end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL LIMIT 100")
  num = 1
  unpopulated_applications.each do |app|
    populate_application_details(app)
    if num == 10
      sleep 240
      num = 1
    else
      sleep 30 # Trying to ease the load on the server!
      num += 1
    end
  end
  sleep 240
  current_applications = ScraperWiki.select("* from swdata WHERE date_validated > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 100")
  num = 1
  current_applications.each do |app|
    populate_application_details(app)
    if num == 10
      sleep 240
      num = 1
    else
      sleep 30 # Trying to ease the load on the server!
      num += 1
    end
  end
end

def populate_application_details(app_info)
  doc = Nokogiri.HTML(open(app_info['url']))
  
  details_hash = doc.search('.informationarea table tr').inject({}){|hsh,tr| hsh[tr.at('th').inner_text.strip] = tr.search('td').inner_text.strip if tr.at('th');hsh}
  
  details = app_info
  
  details[:address] = titleise(details_hash['Site address']) rescue nil
  details[:description] = titleise(details_hash['Descripton of proposal']) rescue nil
  details[:date_validated] = Date.parse(details_hash['Date valid'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:application_type] = details_hash['Application type'] rescue nil
  details[:planning_portal_id] = details_hash['Planning portal reference'] rescue nil
  details[:case_officer] = details_hash['Case officer'] rescue nil
  details[:os_grid_ref] = details_hash['Grid reference'].gsub(/[\r][\n]/, "").gsub(/[\t]/, "").squeeze rescue nil
  details[:parish] = details_hash['Parish'] rescue nil
  details[:ward_name] = details_hash['Ward'] rescue nil
  details[:decision] = details_hash['Decision'] rescue nil
  details[:decision_date] = Date.parse(details_hash['Decision date'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:appeal_result] = details_hash['Appeal decision'] rescue nil
  details[:appeal_decision_date] = Date.parse(details_hash['Appeal decision date'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:agent_name] = titleise(details_hash['Agent']) rescue nil
  details[:agent_address] = titleise(details_hash['Agent address']) rescue nil
  details[:applicant_name] = titleise(details_hash['Applicant']) rescue nil
  details[:applicant_address] = titleise(details_hash['Applicant address']) rescue nil

  url = doc.search('.nav ul li:last-child a')[0][:href]
  
  dates = Nokogiri.HTML(open(BASE_URL + url))

  dates = dates.search('.informationarea table tr').inject({}){|hsh,tr| hsh[tr.at('th').inner_text.strip] = tr.search('td').inner_text.strip if tr.at('th');hsh}
  
  details[:date_received] = Date.parse(dates['Application Received'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:start_date] = Date.parse(dates['Application Received'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:consultation_end_date] = Date.parse(dates['Consultation expiry date'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil

  details[:date_scraped] = Time.now
  
  unless details[:start_date].nil? 
    ScraperWiki.save([:uid], details)
  end

  rescue Exception => e
    puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

#52.times do |i| 
 #search_for_new_applications(Date.today - (10*(i+i)))
#end

search_for_new_applications
update_stale_applications
