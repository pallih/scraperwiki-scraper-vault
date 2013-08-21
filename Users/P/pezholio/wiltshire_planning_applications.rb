require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `date_validated` text, `parish` text, `start_date` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = "http://www.wiltshire.gov.uk/planninganddevelopment/"

def save_page_links(doc)
  apps = doc.search('#article dl a')
  
  if apps.count > 0
    
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

end

def search_for_new_applications(until_date=Date.today)
  url = BASE_URL + "planningadvancedsearch.htm"
  
  doc = Nokogiri.HTML(open(url))
  
  parishes = doc.search("#MultiSiteParish option")
  
  parishes.each do |parish|
  
    url = BASE_URL + "planningsearchresults.htm?MultiSiteParish=#{URI::encode(parish.inner_text)}&DateReceivedFrom=#{(until_date - 14).strftime("%d%%2F%m%%2F%Y")}&DateReceivedTo=#{(until_date).strftime("%d%%2F%m%%2F%Y")}&DecisionNoticeDateFrom=&DecisionNoticeDateTo=&SearchType=Multi"
    
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

  labels = doc.search('#article dl dt')
  contents = doc.search('#article dl dd')
  
  i = 0
  details_hash = {}
  
  labels.each do |label|
    details_hash[label.inner_text.strip] = contents[i].inner_html.strip
    i += 1
  end
  
  eastingnorthing = details_hash["Grid reference"].scan(/Easting : ([0-9]+)<br>Northing: ([0-9]+)/)[0] rescue nil
  consultations = doc.search('.progress')[0].inner_text.scan(/Public consultation started ([0-9]+ [A-Za-z]+ [0-9]+) and (ends|ended) ([0-9]+ [A-Za-z]+ [0-9]+)/)[0] rescue nil
  applicant = details_hash["Applicant's name"].split('<br>') rescue nil
  agent = details_hash["Agent's name"].split('<br>') rescue nil
  
  details[:date_received] = Date.parse(doc.search('.progress')[0].inner_text.scan(/Application received on ([0-9]+ [A-Za-z]+ [0-9]+)/)[0][0])
  details[:start_date] = Date.parse(doc.search('.progress')[0].inner_text.scan(/Application received on ([0-9]+ [A-Za-z]+ [0-9]+)/)[0][0])
  details[:date_validated] = Date.parse(doc.search('.progress')[0].inner_text.scan(/Application registered on ([0-9]+ [A-Za-z]+ [0-9]+)/)[0][0]) rescue nil
  details[:consultation_start_date] = Date.parse(consultations[0]) rescue nil
  details[:consultation_end_date] = Date.parse(consultations[2]) rescue nil
  details[:target_decision_date] = Date.parse(doc.search('.progress')[0].inner_text.scan(/Decision expected before ([0-9]+ [A-Za-z]+ [0-9]+)/)[0][0]) rescue nil
  details[:decision_date] = Date.parse(doc.search('.progress')[0].inner_text.scan(/Decision of [A-Za-z<>\/]+ made on ([0-9]+ [A-Za-z]+ [0-9]+)/)[0][0]) rescue nil
  details[:case_officer] = details_hash["Case officer"] rescue nil
  details[:application_type] = details_hash["Application type"] rescue nil
  details[:description] = CGI.unescapeHTML(details_hash["Proposed development"]) rescue nil
  details[:address] = CGI.unescapeHTML(details_hash["Site address"]) rescue nil
  details[:applicant_name] = CGI.unescapeHTML(applicant[0]) rescue nil
  details[:applicant_address] = CGI.unescapeHTML(applicant[1]) rescue nil
  details[:agent_name] = CGI.unescapeHTML(agent[0]) rescue nil
  details[:agent_address] = CGI.unescapeHTML(agent[1]) rescue nil
  details[:parish] = CGI.unescapeHTML(details_hash["Parish"]) rescue nil
  details[:easting] = eastingnorthing[0].to_i rescue nil
  details[:northing] = eastingnorthing[1].to_i rescue nil
  details[:decision] = details_hash["Decision"] rescue nil
  
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
