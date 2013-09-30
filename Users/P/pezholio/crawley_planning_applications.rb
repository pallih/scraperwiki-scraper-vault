require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `address` text, `postcode` text, `applicant` text, `agent_name` text, `application_type` text, `description` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision` text, `start_date` text, `date_received` text, `consultation_end_date` text, `appeal_result` text, `decision_date` text, `appeal_date` text, `appeal_decision_date` text, `date_scraped` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://www.crawley.gov.uk'

def titleise(string)
  string.gsub(/\w+/) do |word|
    word.capitalize
  end
end

def save_page_links(link)
  doc = Nokogiri.HTML(open(link))
  application_links = doc.search('.mainarea table tr a')
  
  puts "Found #{application_links.size} applications"
  
  application_links.each do |link|
    begin
      record = {}
      record['url'] = BASE_URL + link[:href]
      record['uid'] = link.inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)

 search_url = "http://www.crawley.gov.uk/pw/Planning_and_Development/Planning_Permission___Applications/Planning_Applications_Search/index.htm?is_NextRow=1&accept=yes&strCSS=&pApplicationNo=&pProposal=&pLocation=&pPostcode=&pWard=&pDateType=received&pFromDate=#{(until_date - 14).strftime("%d%%2F%m%%2F%Y")}&pToDate=#{until_date.strftime("%d%%2F%m%%2F%Y")}&pExternalCode=&submit=Search"

  doc = Nokogiri.HTML(open(search_url))
  
  pages = doc.search('.mainarea p')
  total = pages[1].text.scan(/Displaying [0-9]+-[0-9]+ of ([0-9]+)/)[0][0].to_i
  
  save_page_links(search_url)
      
  pages = (total / 20)
  num = 1
  
  while num <= pages
    nextp = (num * 20) + 1
    save_page_links(search_url + "&is_NextRow=" + nextp.to_s)
    num += 1
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
  doc = Nokogiri.HTML(open(app_info['url']))
  
  details_hash = doc.search('.middle p').inject({}){|hsh,p| hsh[p.at('strong').inner_text.strip] = p.inner_text.gsub(p.at('strong').inner_text.strip, '') if p.at('strong');hsh}
  
  details = app_info
  
  details[:comment_url] = doc.search('.middle ul li a')[1][:href] rescue nil
  details[:address] = titleise(details_hash['Location:'].strip) 
  details[:postcode] = details_hash['Location Postcode:'].strip 
  details[:applicant_name] =  details_hash['Applicant Name:'].strip rescue nil
  details[:agent_name] = details_hash['Agent:'].strip rescue nil
  details[:agent_address] = details_hash['Agent Address:'].strip rescue nil
  details[:application_type] = details_hash['Application Type:'].strip rescue nil
  details[:description] = titleise(details_hash['Proposal:'].strip) rescue nil
  details[:case_officer] = details_hash['Case Officer:'].strip rescue nil
  details[:decision] = titleise(details_hash['Planning Application Decision:'].strip) rescue nil
  details[:appeal_result] = titleise(details_hash['Appeal Decision:'].strip) rescue nil
  
  details[:start_date] = Date.parse(details_hash['Received Date:'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-'))
  details[:date_received] = Date.parse(details_hash['Received Date:'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-'))
  
  dates = doc.search('.middle table tr')[1].search('td')
  
  details[:consultation_end_date] = Date.parse(dates[1].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:decision_date] = Date.parse(dates[2].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:appeal_date] = Date.parse(dates[3].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:appeal_decision_date] = Date.parse(dates[4].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil

  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)

  rescue Exception => e
    puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

#52.times do |i| 
 #search_for_new_applications(Date.today - (10*(i+i)))
#end

search_for_new_applications
update_stale_applicationsrequire 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `address` text, `postcode` text, `applicant` text, `agent_name` text, `application_type` text, `description` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision` text, `start_date` text, `date_received` text, `consultation_end_date` text, `appeal_result` text, `decision_date` text, `appeal_date` text, `appeal_decision_date` text, `date_scraped` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://www.crawley.gov.uk'

def titleise(string)
  string.gsub(/\w+/) do |word|
    word.capitalize
  end
end

def save_page_links(link)
  doc = Nokogiri.HTML(open(link))
  application_links = doc.search('.mainarea table tr a')
  
  puts "Found #{application_links.size} applications"
  
  application_links.each do |link|
    begin
      record = {}
      record['url'] = BASE_URL + link[:href]
      record['uid'] = link.inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)

 search_url = "http://www.crawley.gov.uk/pw/Planning_and_Development/Planning_Permission___Applications/Planning_Applications_Search/index.htm?is_NextRow=1&accept=yes&strCSS=&pApplicationNo=&pProposal=&pLocation=&pPostcode=&pWard=&pDateType=received&pFromDate=#{(until_date - 14).strftime("%d%%2F%m%%2F%Y")}&pToDate=#{until_date.strftime("%d%%2F%m%%2F%Y")}&pExternalCode=&submit=Search"

  doc = Nokogiri.HTML(open(search_url))
  
  pages = doc.search('.mainarea p')
  total = pages[1].text.scan(/Displaying [0-9]+-[0-9]+ of ([0-9]+)/)[0][0].to_i
  
  save_page_links(search_url)
      
  pages = (total / 20)
  num = 1
  
  while num <= pages
    nextp = (num * 20) + 1
    save_page_links(search_url + "&is_NextRow=" + nextp.to_s)
    num += 1
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
  doc = Nokogiri.HTML(open(app_info['url']))
  
  details_hash = doc.search('.middle p').inject({}){|hsh,p| hsh[p.at('strong').inner_text.strip] = p.inner_text.gsub(p.at('strong').inner_text.strip, '') if p.at('strong');hsh}
  
  details = app_info
  
  details[:comment_url] = doc.search('.middle ul li a')[1][:href] rescue nil
  details[:address] = titleise(details_hash['Location:'].strip) 
  details[:postcode] = details_hash['Location Postcode:'].strip 
  details[:applicant_name] =  details_hash['Applicant Name:'].strip rescue nil
  details[:agent_name] = details_hash['Agent:'].strip rescue nil
  details[:agent_address] = details_hash['Agent Address:'].strip rescue nil
  details[:application_type] = details_hash['Application Type:'].strip rescue nil
  details[:description] = titleise(details_hash['Proposal:'].strip) rescue nil
  details[:case_officer] = details_hash['Case Officer:'].strip rescue nil
  details[:decision] = titleise(details_hash['Planning Application Decision:'].strip) rescue nil
  details[:appeal_result] = titleise(details_hash['Appeal Decision:'].strip) rescue nil
  
  details[:start_date] = Date.parse(details_hash['Received Date:'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-'))
  details[:date_received] = Date.parse(details_hash['Received Date:'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-'))
  
  dates = doc.search('.middle table tr')[1].search('td')
  
  details[:consultation_end_date] = Date.parse(dates[1].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:decision_date] = Date.parse(dates[2].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:appeal_date] = Date.parse(dates[3].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:appeal_decision_date] = Date.parse(dates[4].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil

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