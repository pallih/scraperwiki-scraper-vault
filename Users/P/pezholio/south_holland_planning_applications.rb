require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://www.sholland.gov.uk/doitonline/plandev/'

def save_page_links(doc)
  apps = doc.search('fieldset.searchresults')
  
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

  url = BASE_URL + "plansearch.aspx?lo=24&st=1&sn=&ty=0&ad=5&sd=#{(until_date - 14).strftime("%Y%m%d")}&ed=#{(until_date).strftime("%Y%m%d")}"

  doc = Nokogiri.HTML(open(url))

  num = (Float(doc.search('.searchcriteria')[0].inner_text) / 25).ceil
  
  num.times do |i|
  
    url = BASE_URL + "plansearch.aspx?lo=24&st=#{i * 25}&sn=&ty=0&ad=5&sd=#{(until_date - 14).strftime("%Y%m%d")}&ed=#{(until_date).strftime("%Y%m%d")}"
    
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
  
  labels = doc.search('.fieldlabels')
  contents = doc.search('.fields')
  
  i = 0
  details_hash = {}
  
  labels.each do |label|
    details_hash[label.inner_text] = contents[i]
    i += 1
  end
    
  details[:date_received] = Date.parse(details_hash["Received on"].inner_text)
  details[:start_date] = Date.parse(details_hash["Received on"].inner_text)
  details[:date_validated] = Date.parse(details_hash["Validated on"].inner_text) rescue nil
  details[:target_decision_date] = Date.parse(details_hash["Decision due by"].inner_text) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(details_hash["Neighbour Consultations Sent on"].inner_text) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(details_hash["Neighbour Comments due by"].inner_text) rescue nil
  details[:decision_date] = Date.parse(details_hash["Date of Decision"].inner_text) rescue nil
  details[:decision_issued_date] = Date.parse(details_hash["Decision Issued"].inner_text) rescue nil
  details[:permission_expires_date] = Date.parse(details_hash["Permission Expires on"].inner_text) rescue nil
  
  details[:description] = details_hash["Proposal"].inner_text.strip rescue nil
  details[:status] = details_hash["Status"].inner_text.strip rescue nil
  details[:applicant_name] = details_hash["Applicant"].inner_text.strip rescue nil
  details[:agent_name] = details_hash["Agent"].inner_text.strip rescue nil
  details[:address] = details_hash["Site Address"].inner_html.gsub("<br>", " ").gsub(%r{</?[^>]+?>}, '').force_encoding("BINARY").gsub(0xA0.chr,"").gsub("  ", " ") rescue nil
  details[:postcode] = details_hash["Site Address"].search('#SitePostcodeLbl')[0].inner_text rescue nil
  details[:applicant_address] = details_hash["Applicant Address"].inner_html.gsub("<br>", " ").gsub(%r{</?[^>]+?>}, '').force_encoding("BINARY").gsub(0xA0.chr,"").gsub("  ", " ") rescue nil
  details[:agent_address] = details_hash["Agent Address"].inner_html.gsub("<br>", " ").gsub(%r{</?[^>]+?>}, '').force_encoding("BINARY").gsub(0xA0.chr,"").gsub("  ", " ") rescue nil
  details[:case_officer] = details_hash["Name"].inner_text rescue nil

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