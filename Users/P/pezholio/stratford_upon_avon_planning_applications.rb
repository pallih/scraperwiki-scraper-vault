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

BASE_URL = "http://apps.stratford.gov.uk/eplanning/"

def save_page_links(doc)

  apps = doc.search('#dgdSearchResult tr')
    
  apps.shift
  apps.shift
  apps.pop
  
  puts "Found #{apps.count} applications"
  
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

def search_for_new_applications(until_date=Date.today)
  url = BASE_URL + "AppSearchResult.aspx?searchby=advanced&appnumber=&apptype=All&status=All&decision=All&ward=All&parish=All&agent=All&datereceivedfrom=#{(until_date - 14).strftime("%d%%2F%m%%2F%Y")}&datereceivedto=#{(until_date).strftime("%d%%2F%m%%2F%Y")}&datevalidatedfrom=&datevalidatedto=&dateissuedfrom=&dateissuedto=&appealstatus=All&appealdecision=All&"
            
  doc = Nokogiri.HTML(open(url))
  
  save_page_links(doc)
  
  results = Float(doc.search('#lbResult strong')[0].inner_text)
  
  pages = ((results - 15) / 15).ceil
  
  pages.times do |i|
      
    agent = Mechanize.new
            
    data = {
      '__EVENTTARGET' => "dgdSearchResult$ctl19$ctl0#{i + 1}",
      '__EVENTARGUMENT' => nil,
      '__VIEWSTATE' => doc.search('#__VIEWSTATE')[0][:value],
    }
    
    page = agent.post(url, data)
    
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

  
  application_hash = doc.search('#tabApplication table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text.strip.encode("UTF-8", :invalid => :replace, :undef => :replace, :replace => "") if tr.search('td').count > 1;hsh}
  
  dates1 = doc.search('#tabDates table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text if tr.search('td').count > 1;hsh}
  
  dates2 = doc.search('#tabDates table tr').inject({}){|hsh,tr| hsh[tr.search('td')[3].inner_text.strip] = tr.search('td')[4].inner_text if tr.search('td').count > 1;hsh}
  
  applicant_hash = doc.search('#tabApplicant table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text.strip.encode("UTF-8", :invalid => :replace, :undef => :replace, :replace => "") if tr.search('td').count > 1;hsh}
  
  agent_hash = doc.search('#tabAgent table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text.strip.encode("UTF-8", :invalid => :replace, :undef => :replace, :replace => "") if tr.search('td').count > 1;hsh}
  
  details_hash = application_hash.merge(dates1).merge(dates2).merge(applicant_hash).merge(agent_hash)
  
  details[:address] = details_hash["Address"] rescue nil
  details[:description] = details_hash["Proposal"] rescue nil
  details[:application_type] = details_hash["Application Type"] rescue nil
  details[:status] = details_hash["Status"] rescue nil
  details[:decision] = details_hash["Proposal"] rescue nil
  details[:decision_issued_date] = Date.parse(details_hash["Date Decision Issued"]) rescue nil
  details[:case_officer] = details_hash["Case Officer"] rescue nil
  details[:parish] = details_hash["Parish"] rescue nil
  details[:ward_name] = details_hash["Current Ward"] rescue nil
  details[:date_received] = Date.parse(details_hash["Application Received"])
  details[:start_date] = Date.parse(details_hash["Application Received"])
  details[:date_validated] = Date.parse(details_hash["Application Valid"]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(details_hash["Neighbour Notifications sent on"]) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash["Standard Consultations sent on"]) rescue nil
  details[:last_advertised_date] = Date.parse(details_hash["Last Advertised on"]) rescue nil
  details[:permission_expires_date] = Date.parse(details_hash["Permission Expiry Date"]) rescue nil
  details[:target_decision_date] = Date.parse(details_hash["Target Date for Determination"]) rescue nil
  details[:meeting_date] = Date.parse(details_hash["Committee Date"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(details_hash["Expiry Date for Neighbour Notifications"]) rescue nil
  details[:consultation_end_date] = Date.parse(details_hash["Expiry Date for Standard Consultations"]) rescue nil
  details[:latest_advertisement_expiry_date] = Date.parse(details_hash["Site Notice Expires"]) rescue nil
  details[:applicant_name] = details_hash["Applicant Name"] rescue nil
  details[:applicant_address] = details_hash["Applicant Address"] rescue nil
  details[:agent_name] = details_hash["Agent's Name"] rescue nil
  details[:agent_address] = details_hash["Agent's Address"] rescue nil
  details[:agent_tel] = details_hash["Agent's Phone"] rescue nil
  
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

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `date_scraped` text,`start_date` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = "http://apps.stratford.gov.uk/eplanning/"

def save_page_links(doc)

  apps = doc.search('#dgdSearchResult tr')
    
  apps.shift
  apps.shift
  apps.pop
  
  puts "Found #{apps.count} applications"
  
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

def search_for_new_applications(until_date=Date.today)
  url = BASE_URL + "AppSearchResult.aspx?searchby=advanced&appnumber=&apptype=All&status=All&decision=All&ward=All&parish=All&agent=All&datereceivedfrom=#{(until_date - 14).strftime("%d%%2F%m%%2F%Y")}&datereceivedto=#{(until_date).strftime("%d%%2F%m%%2F%Y")}&datevalidatedfrom=&datevalidatedto=&dateissuedfrom=&dateissuedto=&appealstatus=All&appealdecision=All&"
            
  doc = Nokogiri.HTML(open(url))
  
  save_page_links(doc)
  
  results = Float(doc.search('#lbResult strong')[0].inner_text)
  
  pages = ((results - 15) / 15).ceil
  
  pages.times do |i|
      
    agent = Mechanize.new
            
    data = {
      '__EVENTTARGET' => "dgdSearchResult$ctl19$ctl0#{i + 1}",
      '__EVENTARGUMENT' => nil,
      '__VIEWSTATE' => doc.search('#__VIEWSTATE')[0][:value],
    }
    
    page = agent.post(url, data)
    
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

  
  application_hash = doc.search('#tabApplication table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text.strip.encode("UTF-8", :invalid => :replace, :undef => :replace, :replace => "") if tr.search('td').count > 1;hsh}
  
  dates1 = doc.search('#tabDates table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text if tr.search('td').count > 1;hsh}
  
  dates2 = doc.search('#tabDates table tr').inject({}){|hsh,tr| hsh[tr.search('td')[3].inner_text.strip] = tr.search('td')[4].inner_text if tr.search('td').count > 1;hsh}
  
  applicant_hash = doc.search('#tabApplicant table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text.strip.encode("UTF-8", :invalid => :replace, :undef => :replace, :replace => "") if tr.search('td').count > 1;hsh}
  
  agent_hash = doc.search('#tabAgent table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text.strip.encode("UTF-8", :invalid => :replace, :undef => :replace, :replace => "") if tr.search('td').count > 1;hsh}
  
  details_hash = application_hash.merge(dates1).merge(dates2).merge(applicant_hash).merge(agent_hash)
  
  details[:address] = details_hash["Address"] rescue nil
  details[:description] = details_hash["Proposal"] rescue nil
  details[:application_type] = details_hash["Application Type"] rescue nil
  details[:status] = details_hash["Status"] rescue nil
  details[:decision] = details_hash["Proposal"] rescue nil
  details[:decision_issued_date] = Date.parse(details_hash["Date Decision Issued"]) rescue nil
  details[:case_officer] = details_hash["Case Officer"] rescue nil
  details[:parish] = details_hash["Parish"] rescue nil
  details[:ward_name] = details_hash["Current Ward"] rescue nil
  details[:date_received] = Date.parse(details_hash["Application Received"])
  details[:start_date] = Date.parse(details_hash["Application Received"])
  details[:date_validated] = Date.parse(details_hash["Application Valid"]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(details_hash["Neighbour Notifications sent on"]) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash["Standard Consultations sent on"]) rescue nil
  details[:last_advertised_date] = Date.parse(details_hash["Last Advertised on"]) rescue nil
  details[:permission_expires_date] = Date.parse(details_hash["Permission Expiry Date"]) rescue nil
  details[:target_decision_date] = Date.parse(details_hash["Target Date for Determination"]) rescue nil
  details[:meeting_date] = Date.parse(details_hash["Committee Date"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(details_hash["Expiry Date for Neighbour Notifications"]) rescue nil
  details[:consultation_end_date] = Date.parse(details_hash["Expiry Date for Standard Consultations"]) rescue nil
  details[:latest_advertisement_expiry_date] = Date.parse(details_hash["Site Notice Expires"]) rescue nil
  details[:applicant_name] = details_hash["Applicant Name"] rescue nil
  details[:applicant_address] = details_hash["Applicant Address"] rescue nil
  details[:agent_name] = details_hash["Agent's Name"] rescue nil
  details[:agent_address] = details_hash["Agent's Address"] rescue nil
  details[:agent_tel] = details_hash["Agent's Phone"] rescue nil
  
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
