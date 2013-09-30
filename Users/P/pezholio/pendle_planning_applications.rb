require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text,  `address` text, `description` text, `postcode` text, `applicant_name` text, `case_officer` text, `comment_url` text, `decision_date` text, `start_date` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://pendle.jdi-consult.net'

def save_page_links(url, page)

  doc = Nokogiri.HTML(open(url))
  
  apps = doc.search('.item table tr')
  apps.shift
  
  puts "Found #{apps.count} applications"

  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app.search('a')[0][:href]
      record['uid'] = app.search('td')[0].inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end

  if doc.search("//a[text()='next']").count == 1
    url = url + "&page=#{page}"
    page += 1
    save_page_links(url, page)
  end
end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + "/mapping/search.php?action=search&mapid=41&searcharea=&DESCRIPTIO=&SITE_ADDRE=&APPNAME=&DATEREGstartdate=#{(until_date - 14).strftime("%d/%m/%Y")}&DATEREGenddate=#{until_date.strftime("%d/%m/%Y")}&DATECOMMstartdate=&DATECOMMenddate=&DECISION=&DECISION_Dstartdate=&DECISION_Denddate="
      
  save_page_links(url, 2)

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
  url = app_info['url']

  doc = Nokogiri.HTML(open(url))

  details = app_info

  doc = Nokogiri.HTML(open(url))
  
  details_hash = doc.search('table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text.strip if tr.search('td').count > 1;hsh}
  
  details[:date_received] = Date.parse(details_hash["Registered Date:"])
  details[:start_date] = Date.parse(details_hash["Registered Date:"])
  details[:address] = details_hash["Address:"].strip rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:description] = details_hash["Proposal:"]
  details[:applicant_name] = details_hash["Applicant Name:"] rescue nil
  details[:case_officer] = details_hash["Officer Name:"] rescue nil
  details[:meeting_date] = Date.parse(details_hash["Committee Date:"]) rescue nil
  details[:status] = details_hash["Status:"].gsub(" [Comment on this application]", "") rescue nil
  details[:decision_date] = Date.parse(details_hash["Decision Date:"]) rescue nil
  details[:comment_url] = "http://bopdoccip.pendle.gov.uk/PlanApp/jsp/PlanObjection.jsp?PlanningApplicationNumber=#{details[:uid]}"
  
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

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text,  `address` text, `description` text, `postcode` text, `applicant_name` text, `case_officer` text, `comment_url` text, `decision_date` text, `start_date` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://pendle.jdi-consult.net'

def save_page_links(url, page)

  doc = Nokogiri.HTML(open(url))
  
  apps = doc.search('.item table tr')
  apps.shift
  
  puts "Found #{apps.count} applications"

  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app.search('a')[0][:href]
      record['uid'] = app.search('td')[0].inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end

  if doc.search("//a[text()='next']").count == 1
    url = url + "&page=#{page}"
    page += 1
    save_page_links(url, page)
  end
end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + "/mapping/search.php?action=search&mapid=41&searcharea=&DESCRIPTIO=&SITE_ADDRE=&APPNAME=&DATEREGstartdate=#{(until_date - 14).strftime("%d/%m/%Y")}&DATEREGenddate=#{until_date.strftime("%d/%m/%Y")}&DATECOMMstartdate=&DATECOMMenddate=&DECISION=&DECISION_Dstartdate=&DECISION_Denddate="
      
  save_page_links(url, 2)

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
  url = app_info['url']

  doc = Nokogiri.HTML(open(url))

  details = app_info

  doc = Nokogiri.HTML(open(url))
  
  details_hash = doc.search('table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text.strip if tr.search('td').count > 1;hsh}
  
  details[:date_received] = Date.parse(details_hash["Registered Date:"])
  details[:start_date] = Date.parse(details_hash["Registered Date:"])
  details[:address] = details_hash["Address:"].strip rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:description] = details_hash["Proposal:"]
  details[:applicant_name] = details_hash["Applicant Name:"] rescue nil
  details[:case_officer] = details_hash["Officer Name:"] rescue nil
  details[:meeting_date] = Date.parse(details_hash["Committee Date:"]) rescue nil
  details[:status] = details_hash["Status:"].gsub(" [Comment on this application]", "") rescue nil
  details[:decision_date] = Date.parse(details_hash["Decision Date:"]) rescue nil
  details[:comment_url] = "http://bopdoccip.pendle.gov.uk/PlanApp/jsp/PlanObjection.jsp?PlanningApplicationNumber=#{details[:uid]}"
  
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
