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

BASE_URL = 'http://www.southoxon.gov.uk/ccm/support/'

def save_page_links(doc)
  apps = doc.search(".tablediv .rowdiv a") 
  puts "Found #{apps.size} applications"
  
  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app[:href]
      record['uid'] = app.inner_text.strip
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue => e
      puts "Exception #{e.inspect} raised getting basic data from #{app}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + "Main.jsp?MODULE=ApplicationCriteriaList&TYPE=Application&PARISH=ABG&AREA=A&TXTSEARCH=&APP_TYPE=&APP_STATUS=&SDAY=#{(until_date - 14).strftime('%e')}&SMONTH=#{(until_date - 14).strftime('%-m')}&SYEAR=#{(until_date - 14).strftime('%Y')}&EDAY=#{(until_date).strftime('%e')}&EMONTH=#{(until_date).strftime('%-m')}&EYEAR=#{(until_date).strftime('%Y')}&Submit=Search".gsub(" ", "")
        
  doc = Nokogiri.HTML(open(url))
    
  save_page_links(doc)

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
  url = app_info['url']

  doc = Nokogiri.HTML(open(url))

  details = app_info

  details_hash = doc.search('.tablediv .rowdiv').inject({}){|hsh,tr| hsh[tr.search('.leftcelldiv')[0].inner_text.strip] = tr.search('.rightcelldiv')[0] ;hsh}
  dates_hash = details_hash["Application Progress"].search('table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text.force_encoding("BINARY").strip.gsub(/\xC2\xA0/, '') ;hsh}
  
  details[:date_received] = Date.parse(dates_hash["Date Received"])
  details[:start_date] = Date.parse(dates_hash["Date Received"])
  details[:date_validated] = Date.parse(dates_hash["Registration Date"]) rescue nil
  details[:consultation_start_date] = Date.parse(dates_hash["Start Consultation Period"]) rescue nil
  details[:consultation_end_date] = Date.parse(dates_hash["End Consultation Period"]) rescue nil
  details[:target_decision_date] = Date.parse(dates_hash["Target Decision Date"]) rescue nil
  details[:application_type] = details_hash["Application Type"].inner_text.strip rescue nil
  details[:description] = details_hash["Description"].inner_text
  details[:address] = details_hash["Location"].inner_text
  eastingnorthing = details_hash["Grid Reference"].inner_text.scan(/([0-9]+)\/([0-9]+)/)[0] rescue nil
  details[:easting] = eastingnorthing[0] rescue nil
  details[:northing] = eastingnorthing[1] rescue nil
  applicant = details_hash["Applicant"].inner_text.split(/\r?\n/) rescue nil
  details[:applicant_name] = applicant.shift rescue nil
  details[:applicant_address] = applicant.join("\r\n") rescue nil
  agent = details_hash["Agent"].search('pre')[0].inner_text.split(/\r?\n/) rescue nil
  details[:agent_name] = agent.shift rescue nil
  details[:agent_address] = agent.join("\r\n") rescue nil
  details[:case_officer] = details_hash["Case Officer"].inner_html.split("<br>")[0] rescue nil
  
  unless details_hash["Decision"].inner_text.strip == "No decision Issued"
    decision = details_hash["Decision"].inner_text.scan(/([a-z ]+) on ([0-9]+[a-z]+ [a-z]+ [0-9]+)/i)[0] rescue nil
    details[:decision] = decision[0] rescue nil
    details[:decision_date] = Date.parse(decision[1]) rescue nil
  end  
  
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
