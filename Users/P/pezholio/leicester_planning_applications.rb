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

BASE_URL = 'http://rcweb.leicester.gov.uk/planning/onlinequery/'

def save_page_links(doc)
  apps = doc.search("table#ctl00_ContentPlaceHolder1_GridView1 tr") 
  apps.shift
  puts "Found #{apps.size} applications"
  
  apps.each do |app|
    begin
      record = {}
      link = app.search('a')[0]
      unless link[:href].scan(/javascript:/).length > 0
        record['url'] = BASE_URL + link[:href]
        record['uid'] = link.inner_text.strip
        ScraperWiki.save(["uid"], record) # use uid as primary key
      end
    rescue
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)
  url = BASE_URL + "ResultSet.aspx?AppNo=&Address=&UPRN=&Wrd=&AppType=&DateRecFrm=#{(until_date - 14).strftime('%d/%m/%Y')}&DateRecTo=#{(until_date).strftime('%d/%m/%Y')}&DateDecfrm=&DateDecTo=&Proposal=&DecisionType="
      
  doc = Nokogiri.HTML(open(url))
    
  save_page_links(doc)

  if doc.search("table#ctl00_ContentPlaceHolder1_GridView1 tr")[0]["bgcolor"] == "LightGoldenrodYellow"

    agent = Mechanize.new
            
    data = {
      '__EVENTTARGET' => "ctl00$ContentPlaceHolder1$GridView1",
      '__EVENTARGUMENT' => "Page$2",
      '__VIEWSTATE' => doc.search('#__VIEWSTATE')[0][:value],
      '__EVENTVALIDATION' => doc.search('#__EVENTVALIDATION')[0][:value]
    }
    
    page = agent.post(url, data)
    
    doc = Nokogiri.HTML(page.content)
        
    save_page_links(doc)
    
  end
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

  details[:address] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_locationLabel')[0].inner_text
  
  # Sometimes data isn't entered, so we don't save on this occassion
  unless details[:address] == "DATA NOT ENTERED"
  
    details[:description] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_proposalLabel')[0].inner_text
    details[:application_type] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_Label17')[0].inner_text rescue nil
    details[:ward_name] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_ward_descriptionLabel')[0].inner_text rescue nil
    details[:date_received] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_received_dateLabel')[0].inner_text)
    details[:start_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_received_dateLabel')[0].inner_text)
    details[:date_validated] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_received_complete_dateLabel')[0].inner_text) rescue nil
    details[:neighbour_consultation_start_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_neighbour_letter_dateLabel')[0].inner_text) rescue nil
    details[:neighbour_consultation_end_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_neighbour_expiry_dateLabel')[0].inner_text) rescue nil
    details[:applicant_name] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_Label2')[0].inner_text rescue nil
    details[:applicant_address] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_applicants_addressLabel')[0].inner_text rescue nil
    details[:agent_name] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_agentLabel')[0].inner_text rescue nil
    details[:agent_address] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_agents_addressLabel')[0].inner_text rescue nil
    details[:case_officer] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_case_officerLabel')[0].inner_text rescue nil
    details[:decision] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_decision_descriptionLabel')[0].inner_text rescue nil
    details[:meeting_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_committee_dateLabel')[0].inner_text) rescue nil
    details[:decision_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_decision_dateLabel')[0].inner_text) rescue nil
    details[:appeal_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_appeal_lodged_dateLabel')[0].inner_text) rescue nil
    details[:decision_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_decision_dateLabel')[0].inner_text) rescue nil
    details[:appeal_decision_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_appeal_decision_dateLabel')[0].inner_text) rescue nil
    details[:appeal_result] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_appeal_decisionLabel')[0].inner_text rescue nil
    details[:date_scraped] = Time.now
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
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `date_scraped` text,`start_date` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://rcweb.leicester.gov.uk/planning/onlinequery/'

def save_page_links(doc)
  apps = doc.search("table#ctl00_ContentPlaceHolder1_GridView1 tr") 
  apps.shift
  puts "Found #{apps.size} applications"
  
  apps.each do |app|
    begin
      record = {}
      link = app.search('a')[0]
      unless link[:href].scan(/javascript:/).length > 0
        record['url'] = BASE_URL + link[:href]
        record['uid'] = link.inner_text.strip
        ScraperWiki.save(["uid"], record) # use uid as primary key
      end
    rescue
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)
  url = BASE_URL + "ResultSet.aspx?AppNo=&Address=&UPRN=&Wrd=&AppType=&DateRecFrm=#{(until_date - 14).strftime('%d/%m/%Y')}&DateRecTo=#{(until_date).strftime('%d/%m/%Y')}&DateDecfrm=&DateDecTo=&Proposal=&DecisionType="
      
  doc = Nokogiri.HTML(open(url))
    
  save_page_links(doc)

  if doc.search("table#ctl00_ContentPlaceHolder1_GridView1 tr")[0]["bgcolor"] == "LightGoldenrodYellow"

    agent = Mechanize.new
            
    data = {
      '__EVENTTARGET' => "ctl00$ContentPlaceHolder1$GridView1",
      '__EVENTARGUMENT' => "Page$2",
      '__VIEWSTATE' => doc.search('#__VIEWSTATE')[0][:value],
      '__EVENTVALIDATION' => doc.search('#__EVENTVALIDATION')[0][:value]
    }
    
    page = agent.post(url, data)
    
    doc = Nokogiri.HTML(page.content)
        
    save_page_links(doc)
    
  end
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

  details[:address] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_locationLabel')[0].inner_text
  
  # Sometimes data isn't entered, so we don't save on this occassion
  unless details[:address] == "DATA NOT ENTERED"
  
    details[:description] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_proposalLabel')[0].inner_text
    details[:application_type] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_Label17')[0].inner_text rescue nil
    details[:ward_name] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_ward_descriptionLabel')[0].inner_text rescue nil
    details[:date_received] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_received_dateLabel')[0].inner_text)
    details[:start_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_received_dateLabel')[0].inner_text)
    details[:date_validated] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_received_complete_dateLabel')[0].inner_text) rescue nil
    details[:neighbour_consultation_start_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_neighbour_letter_dateLabel')[0].inner_text) rescue nil
    details[:neighbour_consultation_end_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_neighbour_expiry_dateLabel')[0].inner_text) rescue nil
    details[:applicant_name] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_Label2')[0].inner_text rescue nil
    details[:applicant_address] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_applicants_addressLabel')[0].inner_text rescue nil
    details[:agent_name] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_agentLabel')[0].inner_text rescue nil
    details[:agent_address] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_agents_addressLabel')[0].inner_text rescue nil
    details[:case_officer] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_case_officerLabel')[0].inner_text rescue nil
    details[:decision] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_decision_descriptionLabel')[0].inner_text rescue nil
    details[:meeting_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_committee_dateLabel')[0].inner_text) rescue nil
    details[:decision_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_decision_dateLabel')[0].inner_text) rescue nil
    details[:appeal_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_appeal_lodged_dateLabel')[0].inner_text) rescue nil
    details[:decision_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_decision_dateLabel')[0].inner_text) rescue nil
    details[:appeal_decision_date] = Date.parse(doc.search('#ctl00_ContentPlaceHolder1_FormView1_appeal_decision_dateLabel')[0].inner_text) rescue nil
    details[:appeal_result] = doc.search('#ctl00_ContentPlaceHolder1_FormView1_appeal_decisionLabel')[0].inner_text rescue nil
    details[:date_scraped] = Time.now
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
