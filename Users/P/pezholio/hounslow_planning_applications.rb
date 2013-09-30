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

BASE_URL = 'http://planning.hounslow.gov.uk/'

def save_page_links(doc)
  apps = doc.xpath("//a[contains(@href,'Planning_CaseNo.aspx')]") 
  puts "Found #{apps.size} applications"
  
  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app[:href]
      record['uid'] = app.inner_text.strip
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)
      
  url = BASE_URL + "planning_summary.aspx?strWeekListType=SRCH&strRecTo=#{(until_date).strftime('%d/%m/%Y')}&strRecFrom=#{(until_date - 14).strftime('%d/%m/%Y')}&strStreet=ALL&strStreetTxt=All%20Streets&strWard=ALL&strAppTyp=ALL&strWardTxt=All%20Wards&strAppTypTxt=All%20Application%20Types&strArea=ALL&strAreaTxt=All%20Areas&strLimit=500"
      
  doc = Nokogiri.HTML(open(url, "Cookie" => 'LBHPlanningAccept=true' ))
    
  save_page_links(doc)
end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL LIMIT 500")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE start_date > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  url = app_info['url']

  doc = Nokogiri.HTML(open(url))

  details = app_info

  doc = Nokogiri.HTML(open(url, "Cookie" => 'LBHPlanningAccept=true' ))
  
  details_hash = doc.xpath("//table[@width=540][2]//tr").inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.force_encoding("BINARY").gsub("\xC2\xA0", " ").strip] = tr.search('td')[1] if tr.search('td').count > 1 ;hsh}
  
  applicant_hash = doc.xpath("//table[@width=540][3]//tr").inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.force_encoding("BINARY").gsub("\xC2\xA0", " ").strip] = tr.search('td')[1] if tr.search('td').count > 1 ;hsh}
  
  status_hash = doc.xpath("//table[@width=540][7]//tr").inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.force_encoding("BINARY").gsub("\xC2\xA0", " ").strip] = tr.search('td')[1] if tr.search('td').count > 1 ;hsh}
    
  details[:address] = details_hash["Site description"].inner_text.force_encoding("BINARY").split("\xC2\xA0")[0].strip.squeeze(' ')
  eastingnorthing = details_hash["Site description"].search('a')[0][:href].scan(/http:\/\/www.streetmap.co.uk\/newmap.srf\?x=([0-9]+.[0-9]+)&y=([0-9]+.[0-9]+)/)[0]
  details[:easting] = eastingnorthing[0]
  details[:northing] = eastingnorthing[1]
  details[:application_type] = details_hash["Application type"].inner_text.strip
  details[:date_received] = Date.parse(details_hash["Date received"].inner_text.strip)
  details[:start_date] = Date.parse(details_hash["Date received"].inner_text.strip)
  details[:description] = details_hash["Details"].inner_text.strip
  details[:ward_name] = details_hash["Ward"].inner_text.strip
  details[:case_officer] = details_hash["Officer"].inner_text.strip.squeeze(' ')
  details[:applicant_name] = applicant_hash["Name"].inner_text.strip.squeeze(' ')
  details[:applicant_address] = applicant_hash["Address"].inner_text.strip.squeeze(' ')
  details[:agent_name] = doc.search('#lbl_Agent_Name')[0].inner_text.strip.squeeze(' ')
  details[:agent_tel] = doc.search('#lbl_Agent_Phone')[0].inner_text.strip.squeeze(' ')
  details[:agent_address] = doc.search('#lbl_Agent_Address')[0].inner_text.strip.squeeze(' ')
  details[:status] = doc.search('#lbl_COMMDATETYPE')[0].inner_text.strip.squeeze(' ')
  
  details[:decision] = status_hash["Decision"].inner_text.strip
  details[:decision_issued_date] = Date.parse(status_hash["Decision Issued"].inner_text.strip) rescue nil
  details[:appeal_date] = Date.parse(status_hash["Appeal Lodged"].inner_text.strip) rescue nil
  details[:appeal_result] = status_hash["Appeal decision"].inner_text.strip
  details[:appeal_decision_date] = Date.parse(status_hash["Appeal decision date"].inner_text.strip) rescue nil
  details[:permission_expires_date] = Date.parse(status_hash["Expiry Date"].inner_text.strip) rescue nil
  
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

BASE_URL = 'http://planning.hounslow.gov.uk/'

def save_page_links(doc)
  apps = doc.xpath("//a[contains(@href,'Planning_CaseNo.aspx')]") 
  puts "Found #{apps.size} applications"
  
  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app[:href]
      record['uid'] = app.inner_text.strip
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)
      
  url = BASE_URL + "planning_summary.aspx?strWeekListType=SRCH&strRecTo=#{(until_date).strftime('%d/%m/%Y')}&strRecFrom=#{(until_date - 14).strftime('%d/%m/%Y')}&strStreet=ALL&strStreetTxt=All%20Streets&strWard=ALL&strAppTyp=ALL&strWardTxt=All%20Wards&strAppTypTxt=All%20Application%20Types&strArea=ALL&strAreaTxt=All%20Areas&strLimit=500"
      
  doc = Nokogiri.HTML(open(url, "Cookie" => 'LBHPlanningAccept=true' ))
    
  save_page_links(doc)
end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL LIMIT 500")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE start_date > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  url = app_info['url']

  doc = Nokogiri.HTML(open(url))

  details = app_info

  doc = Nokogiri.HTML(open(url, "Cookie" => 'LBHPlanningAccept=true' ))
  
  details_hash = doc.xpath("//table[@width=540][2]//tr").inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.force_encoding("BINARY").gsub("\xC2\xA0", " ").strip] = tr.search('td')[1] if tr.search('td').count > 1 ;hsh}
  
  applicant_hash = doc.xpath("//table[@width=540][3]//tr").inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.force_encoding("BINARY").gsub("\xC2\xA0", " ").strip] = tr.search('td')[1] if tr.search('td').count > 1 ;hsh}
  
  status_hash = doc.xpath("//table[@width=540][7]//tr").inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.force_encoding("BINARY").gsub("\xC2\xA0", " ").strip] = tr.search('td')[1] if tr.search('td').count > 1 ;hsh}
    
  details[:address] = details_hash["Site description"].inner_text.force_encoding("BINARY").split("\xC2\xA0")[0].strip.squeeze(' ')
  eastingnorthing = details_hash["Site description"].search('a')[0][:href].scan(/http:\/\/www.streetmap.co.uk\/newmap.srf\?x=([0-9]+.[0-9]+)&y=([0-9]+.[0-9]+)/)[0]
  details[:easting] = eastingnorthing[0]
  details[:northing] = eastingnorthing[1]
  details[:application_type] = details_hash["Application type"].inner_text.strip
  details[:date_received] = Date.parse(details_hash["Date received"].inner_text.strip)
  details[:start_date] = Date.parse(details_hash["Date received"].inner_text.strip)
  details[:description] = details_hash["Details"].inner_text.strip
  details[:ward_name] = details_hash["Ward"].inner_text.strip
  details[:case_officer] = details_hash["Officer"].inner_text.strip.squeeze(' ')
  details[:applicant_name] = applicant_hash["Name"].inner_text.strip.squeeze(' ')
  details[:applicant_address] = applicant_hash["Address"].inner_text.strip.squeeze(' ')
  details[:agent_name] = doc.search('#lbl_Agent_Name')[0].inner_text.strip.squeeze(' ')
  details[:agent_tel] = doc.search('#lbl_Agent_Phone')[0].inner_text.strip.squeeze(' ')
  details[:agent_address] = doc.search('#lbl_Agent_Address')[0].inner_text.strip.squeeze(' ')
  details[:status] = doc.search('#lbl_COMMDATETYPE')[0].inner_text.strip.squeeze(' ')
  
  details[:decision] = status_hash["Decision"].inner_text.strip
  details[:decision_issued_date] = Date.parse(status_hash["Decision Issued"].inner_text.strip) rescue nil
  details[:appeal_date] = Date.parse(status_hash["Appeal Lodged"].inner_text.strip) rescue nil
  details[:appeal_result] = status_hash["Appeal decision"].inner_text.strip
  details[:appeal_decision_date] = Date.parse(status_hash["Appeal decision date"].inner_text.strip) rescue nil
  details[:permission_expires_date] = Date.parse(status_hash["Expiry Date"].inner_text.strip) rescue nil
  
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
