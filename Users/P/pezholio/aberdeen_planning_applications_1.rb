require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `application_type` text, `decision` text, `date_received` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `associated_application_uid` text, `decision_date` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://planning.aberdeencity.gov.uk'

def save_page_links(link)
  doc = Nokogiri.HTML(open(link, "cookie" => "AcceptedCookies=Y;accept=YES"))
  application_links = doc.search('table a[@href*="PlanningDetail.asp?ref="]') #only want details
  puts "Found #{application_links.size} applications"
  
  application_links.each do |link|
    begin
      record = {}
      record['url'] = BASE_URL + '/' + link[:href]
      record['uid'] = link[:href].scan(/ref=(\d+)/).flatten.first
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)
  search_url = BASE_URL + '/PlanningList.asp?ReferenceNumber=&PADescription=&ApplicationType=ANY&Address=&WardCode=ANY&Agent=&Applicant=&CaseOfficer=ANY&Decision=3'  
  search_url += "&RecDateFrom=#{(until_date - 14).strftime("%Y-%m-%d")}&RecDateTo=#{until_date.strftime("%Y-%m-%d")}&RegDateFrom=&RegDateTo=&DecDateFrom=&DecDateTo=&AppealDateFrom=&AppealDateTo=&SearchType=A&Submit2=Submit"
  
  doc = Nokogiri.HTML(open(search_url, "cookie" => "AcceptedCookies=Y;accept=YES"))

  pages = doc.search('#content p:nth-child(5)')
  total = pages[0].text.scan(/page [0-9]+ of ([0-9]+) pages./)[0][0].to_i
  
  num = 1

  while num <= total
    save_page_links(search_url + "&page=" + num.to_s)
    num += 1
  end

end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL OR postcode IS NULL")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE date_received > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  doc=Nokogiri.HTML(open(app_info['url'], "cookie" => "AcceptedCookies=Y;accept=YES"))
  details_hash = doc.search('table [@summary="Planning Application Details"] tr').inject({}){|hsh,tr| hsh[tr.at('th').inner_text.strip] = tr.search('td').last if tr.at('th');hsh}
  address_hash = doc.search('table [@summary="Planning Application Address"] tr').inject({}){|hsh,tr| hsh[tr.at('th').inner_text.strip] = tr.search('td').last if tr.at('th');hsh}
  status_hash = doc.search('table [@summary="Planning Application Status and Key Dates"] tr').inject({}){|hsh,tr| hsh[tr.at('th').inner_text.strip] = tr.search('td').last if tr.at('th');hsh}
  applicant_hash = doc.search('table [@summary="Planning Application Applicant, Agent and Case Officer Details"] tr').inject({}){|hsh,tr| hsh[tr.at('th').inner_text.strip] = tr.search('td').last if tr.at('th');hsh}
 
  details = app_info 
  details[:address] = address_hash['Address:'].inner_html.gsub("<br>", " ").squeeze(' ').strip #address is required
  details[:postcode] = address_hash['Post code:'].inner_html.strip
  applicant = applicant_hash['Applicant:'].inner_html.split("<br>")
  details[:applicant_name] = applicant.shift.squeeze(' ').strip rescue nil
  details[:applicant_address] = applicant.join(" ").squeeze(' ').strip rescue nil
  details[:application_type] = details_hash['Application type:'].inner_text.squeeze(' ').strip rescue nil
  details[:description] = details_hash['Proposal Description:'].inner_text.squeeze(' ').strip rescue nil
  details[:ward_name] = address_hash['Ward:'].inner_text.split("(").shift.squeeze(' ').strip rescue nil
  
  details[:status] = status_hash['Status:'].inner_text.squeeze(' ').strip rescue nil
  details[:decision] = status_hash['Decision:'].inner_text.strip rescue nil
  
  details[:start_date] = Date.parse(status_hash['Date application received:'].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) # Required
  details[:date_received] = Date.parse(status_hash['Date application received:'].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:date_validated] = Date.parse(status_hash['Date application Registered:'].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:decision_date] = Date.parse(status_hash['Decision date:'].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  
  if agent = applicant_hash['Agent:']
    agent = applicant_hash['Agent:'].inner_html.split("<br>")
    details[:agent_name] = agent.shift.squeeze.strip rescue nil
   details[:agent_address] = agent.join(" ").squeeze(' ').strip rescue nil
  end
  
  details[:comment_url] = BASE_URL + "/" + doc.at('a[text()*="Comment on this"]')[:href] rescue nil
  details[:case_officer] = applicant_hash['Officer:'].inner_text.squeeze(' ').strip rescue nil
  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

def format_date(date)
  date.strftime('%d/%m/%Y').gsub('/','%2F')
end

#52.times do |i| 
  #search_for_new_applications(Date.today - (10*(i+i)))
#end

search_for_new_applications
update_stale_applications