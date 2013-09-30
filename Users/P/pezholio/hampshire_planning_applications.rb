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

BASE_URL = 'http://www3.hants.gov.uk/mineralsandwaste/'

def save_page_links(apps)

  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app.search('a')[0][:href]
      record['uid'] = app.search('a')[0].inner_text
      #puts record.to_yaml
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{app}"
    end
  end

end

def get_all_applications

  url = BASE_URL + "application-search-results.htm?show=100&search=yes"

  doc = Nokogiri.HTML(open(url))

  results = Float(doc.search('.maincopy strong')[0].inner_text.scan(/([0-9]+) application\(s\) found./)[0][0])

  pages = (results / 100).ceil

  pages.times do |i|    
    doc = Nokogiri.HTML(open(url + "&page=#{i + 1}"))

    table = doc.search('.simpletable')[1]
    apps = table.search('tr')
    apps.shift
    
    save_page_links(apps)
  end

end

def search_for_new_applications
  count = ScraperWiki.sqliteexecute('select count(*) from `swdata`')["data"][0][0]

  url = BASE_URL + "application-search-results.htm?show=100&search=yes"

  doc = Nokogiri.HTML(open(url))

  current = Float(doc.search('.maincopy strong')[0].inner_text.scan(/([0-9]+) application\(s\) found./)[0][0])

  num = (count - current).to_i

  table = doc.search('.simpletable')[1]

  apps = []

  num.times do |i|
    apps[i] = table.search('tr')[i]
  end

  save_page_links(apps)  
end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE start_date > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    populate_application_details(app)
  end
  unaddressed_applications = ScraperWiki.select("* from swdata WHERE address is NULL")
  unaddressed_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  url = app_info['url']

  doc = Nokogiri.HTML(open(url))

  details = app_info

  details_hash = doc.search('.applicationDetails tr').inject({}){|hsh,tr| hsh[tr.search('th').inner_text.strip.encode("ISO-8859-1", :invalid => :replace, :undef => :replace, :replace => "'")] = tr.search('td').inner_text.strip if tr.search('td').count > 0;hsh}
  
  details[:address] = details_hash["Location:"]
  details[:description] = details_hash["Proposal:"]
  details[:date_received] = Date.parse(details_hash["Received:"])
  details[:start_date] = Date.parse(details_hash["Received:"])
  details[:date_validated] = Date.parse(details_hash["Validated:"]) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash["Start of Public Consultation:"]) rescue nil
  details[:consultation_end_date] = Date.parse(details_hash["Public Consultation Expiry:"]) rescue nil
  details[:decision] = details_hash["Decision:"] rescue nil
  details[:decision_date] = Date.parse(details_hash["Decision date:"]) rescue nil
  details[:appeal_result] = details_hash["Appeal Status:"] rescue nil
  details[:case_officer] = details_hash["Case Officer:"] rescue nil
  details[:applicant_name] = details_hash["Applicant's Name:"] rescue nil
  details[:applicant_address] = details_hash["Applicant's Address:"] rescue nil
  details[:agent_name] = details_hash["Agent's Name:"] rescue nil
  details[:agent_address] = details_hash["Agent's Address:"] rescue nil
  
  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

#get_all_applications
search_for_new_applications
update_stale_applications

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

BASE_URL = 'http://www3.hants.gov.uk/mineralsandwaste/'

def save_page_links(apps)

  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app.search('a')[0][:href]
      record['uid'] = app.search('a')[0].inner_text
      #puts record.to_yaml
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{app}"
    end
  end

end

def get_all_applications

  url = BASE_URL + "application-search-results.htm?show=100&search=yes"

  doc = Nokogiri.HTML(open(url))

  results = Float(doc.search('.maincopy strong')[0].inner_text.scan(/([0-9]+) application\(s\) found./)[0][0])

  pages = (results / 100).ceil

  pages.times do |i|    
    doc = Nokogiri.HTML(open(url + "&page=#{i + 1}"))

    table = doc.search('.simpletable')[1]
    apps = table.search('tr')
    apps.shift
    
    save_page_links(apps)
  end

end

def search_for_new_applications
  count = ScraperWiki.sqliteexecute('select count(*) from `swdata`')["data"][0][0]

  url = BASE_URL + "application-search-results.htm?show=100&search=yes"

  doc = Nokogiri.HTML(open(url))

  current = Float(doc.search('.maincopy strong')[0].inner_text.scan(/([0-9]+) application\(s\) found./)[0][0])

  num = (count - current).to_i

  table = doc.search('.simpletable')[1]

  apps = []

  num.times do |i|
    apps[i] = table.search('tr')[i]
  end

  save_page_links(apps)  
end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE start_date > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    populate_application_details(app)
  end
  unaddressed_applications = ScraperWiki.select("* from swdata WHERE address is NULL")
  unaddressed_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  url = app_info['url']

  doc = Nokogiri.HTML(open(url))

  details = app_info

  details_hash = doc.search('.applicationDetails tr').inject({}){|hsh,tr| hsh[tr.search('th').inner_text.strip.encode("ISO-8859-1", :invalid => :replace, :undef => :replace, :replace => "'")] = tr.search('td').inner_text.strip if tr.search('td').count > 0;hsh}
  
  details[:address] = details_hash["Location:"]
  details[:description] = details_hash["Proposal:"]
  details[:date_received] = Date.parse(details_hash["Received:"])
  details[:start_date] = Date.parse(details_hash["Received:"])
  details[:date_validated] = Date.parse(details_hash["Validated:"]) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash["Start of Public Consultation:"]) rescue nil
  details[:consultation_end_date] = Date.parse(details_hash["Public Consultation Expiry:"]) rescue nil
  details[:decision] = details_hash["Decision:"] rescue nil
  details[:decision_date] = Date.parse(details_hash["Decision date:"]) rescue nil
  details[:appeal_result] = details_hash["Appeal Status:"] rescue nil
  details[:case_officer] = details_hash["Case Officer:"] rescue nil
  details[:applicant_name] = details_hash["Applicant's Name:"] rescue nil
  details[:applicant_address] = details_hash["Applicant's Address:"] rescue nil
  details[:agent_name] = details_hash["Agent's Name:"] rescue nil
  details[:agent_address] = details_hash["Agent's Address:"] rescue nil
  
  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

#get_all_applications
search_for_new_applications
update_stale_applications

