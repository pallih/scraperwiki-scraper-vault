require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `date_scraped` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

#ScraperWiki.sqliteexecute('ALTER TABLE swdata RENAME TO swdata2')
#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `date_scraped` text, `status` text, `target_decision_date` text, `agent_name` text, `postcode` text, `address` text, `case_officer` text, `consultation_end_date` text, `start_date` text, `description` text, `decision_date` text, `decision_issued_date` text, `decision` text)')
#ScraperWiki.sqliteexecute('INSERT INTO swdata(url, uid, date_scraped, status, target_decision_date, agent_name, postcode, address, case_officer, consultation_end_date, start_date, description, decision_date, decision_issued_date, decision) SELECT url, uid, date_scraped, status, target_decision_date, agent, postcode, address, case_officer, consultation_end_date, start_date, description, decision_date, decision_issued_date, decision FROM swdata2;')
#exit

BASE_URL = 'http://www.rbwm.gov.uk/pam/'

def save_page_links(doc)
  rows = doc.search('.srg_tab_container table tr')
  rows.shift
  rows.shift
  
  puts "Found #{rows.size} applications"
    
  rows.each do |row|
    begin
      record = {}
      link = row.search('a')[0]
      record['url'] = BASE_URL + link[:href]
      record['uid'] = link.inner_text
      puts record['uid']
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + 'search_results.jsp'
  
  a = Mechanize.new
  
  page = a.post(url, {
    'app_id' => nil,
  'validated_start_date' => (until_date - 14).strftime("%d-%b-%Y") ,
  'validated_end_date' => until_date.strftime("%d-%b-%Y") ,
  })
  
  doc = Nokogiri.HTML(page.body)
  
  pages = doc.search('.srg_tab_container table tfoot tr td')
  total = pages[0].inner_html.scan(/Results [0-9]+ - [0-9]+ of ([0-9]+)<br>/)[0][0].to_i
  
  save_page_links(doc)
      
  pages = (total / 15)
  num = 1
  
  while num <= pages
    uri = url + "?pageno=" + num.to_s
    save_page_links(a.get(uri))
    num += 1
  end

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

  doc=Nokogiri.HTML(open(app_info["url"]))
  
  details_hash = doc.search('table[@summary="Planning Application Details"] tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text.strip if tr.at('td');hsh}
  
  progress_hash = doc.search('table[@align="center"] tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.gsub("-", "").strip] = tr.search('td')[1].inner_text.strip if tr.search('td')[1];hsh}
  
  details = app_info

  details[:address] = details_hash['Address'].strip rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:status] = details_hash['Status'].strip rescue nil
  details[:decision] = details_hash['Decision'].strip unless details_hash['Decision'].strip == "-" rescue nil
  details[:agent_name] = details_hash['Agent Name'].strip rescue nil
  details[:description] = details_hash['Proposal'].strip rescue nil
  details[:case_officer] = details_hash['Planning Officer'].strip rescue nil
  details[:target_decision_date] = Date.parse(progress_hash['Decision expected by']) rescue nil
  details[:start_date] = Date.parse(progress_hash['Application was registered on'])
  details[:consultation_end_date] = Date.parse(progress_hash['Consultations were completed on']) rescue nil
  details[:decision_date] = Date.parse(progress_hash['Decision was made on']) rescue nil
  details[:decision_issued_date] = Date.parse(progress_hash['Decision was issued on']) rescue nil
  details[:date_scraped] = Time.now
  
  ScraperWiki.save([:uid], details)  

end

#52.times do |i| 
 #search_for_new_applications(Date.today - (10*(i+i)))
#end

search_for_new_applications
update_stale_applicationsrequire 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `date_scraped` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

#ScraperWiki.sqliteexecute('ALTER TABLE swdata RENAME TO swdata2')
#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `date_scraped` text, `status` text, `target_decision_date` text, `agent_name` text, `postcode` text, `address` text, `case_officer` text, `consultation_end_date` text, `start_date` text, `description` text, `decision_date` text, `decision_issued_date` text, `decision` text)')
#ScraperWiki.sqliteexecute('INSERT INTO swdata(url, uid, date_scraped, status, target_decision_date, agent_name, postcode, address, case_officer, consultation_end_date, start_date, description, decision_date, decision_issued_date, decision) SELECT url, uid, date_scraped, status, target_decision_date, agent, postcode, address, case_officer, consultation_end_date, start_date, description, decision_date, decision_issued_date, decision FROM swdata2;')
#exit

BASE_URL = 'http://www.rbwm.gov.uk/pam/'

def save_page_links(doc)
  rows = doc.search('.srg_tab_container table tr')
  rows.shift
  rows.shift
  
  puts "Found #{rows.size} applications"
    
  rows.each do |row|
    begin
      record = {}
      link = row.search('a')[0]
      record['url'] = BASE_URL + link[:href]
      record['uid'] = link.inner_text
      puts record['uid']
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + 'search_results.jsp'
  
  a = Mechanize.new
  
  page = a.post(url, {
    'app_id' => nil,
  'validated_start_date' => (until_date - 14).strftime("%d-%b-%Y") ,
  'validated_end_date' => until_date.strftime("%d-%b-%Y") ,
  })
  
  doc = Nokogiri.HTML(page.body)
  
  pages = doc.search('.srg_tab_container table tfoot tr td')
  total = pages[0].inner_html.scan(/Results [0-9]+ - [0-9]+ of ([0-9]+)<br>/)[0][0].to_i
  
  save_page_links(doc)
      
  pages = (total / 15)
  num = 1
  
  while num <= pages
    uri = url + "?pageno=" + num.to_s
    save_page_links(a.get(uri))
    num += 1
  end

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

  doc=Nokogiri.HTML(open(app_info["url"]))
  
  details_hash = doc.search('table[@summary="Planning Application Details"] tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text.strip if tr.at('td');hsh}
  
  progress_hash = doc.search('table[@align="center"] tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.gsub("-", "").strip] = tr.search('td')[1].inner_text.strip if tr.search('td')[1];hsh}
  
  details = app_info

  details[:address] = details_hash['Address'].strip rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:status] = details_hash['Status'].strip rescue nil
  details[:decision] = details_hash['Decision'].strip unless details_hash['Decision'].strip == "-" rescue nil
  details[:agent_name] = details_hash['Agent Name'].strip rescue nil
  details[:description] = details_hash['Proposal'].strip rescue nil
  details[:case_officer] = details_hash['Planning Officer'].strip rescue nil
  details[:target_decision_date] = Date.parse(progress_hash['Decision expected by']) rescue nil
  details[:start_date] = Date.parse(progress_hash['Application was registered on'])
  details[:consultation_end_date] = Date.parse(progress_hash['Consultations were completed on']) rescue nil
  details[:decision_date] = Date.parse(progress_hash['Decision was made on']) rescue nil
  details[:decision_issued_date] = Date.parse(progress_hash['Decision was issued on']) rescue nil
  details[:date_scraped] = Time.now
  
  ScraperWiki.save([:uid], details)  

end

#52.times do |i| 
 #search_for_new_applications(Date.today - (10*(i+i)))
#end

search_for_new_applications
update_stale_applications