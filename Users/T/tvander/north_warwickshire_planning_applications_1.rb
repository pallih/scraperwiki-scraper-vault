require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'
require 'date'
require 'yaml'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `date_scraped` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://www.winnipeg.ca/cao/media/news/nr_2012/nr_201201_toc.stm'

def save_page_links(doc)
  rows = doc.search('#central table')[0].search('tr')
  rows.shift
  
  puts "Found #{rows.size} applications"
  
  rows.each do |row|
    begin
      record = {}
      link = row.search('a')[0]
      record['url'] = link[:href].gsub('..', BASE_URL)
      record['uid'] = link.inner_text
      ScraperWiki.save(["uid"], record)
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
    
end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + "/servlets/ApplicationSearchServlet"
  
  a = Mechanize.new

  page = a.post(url, {
  'ReceivedDateFrom' => (until_date - 7).strftime("%d-%b-%Y") ,
  'ReceivedDateTo' => until_date.strftime("%d-%b-%Y") ,
  'button' => 'Search'
  })
  
  doc = Nokogiri.HTML(page.body)
  
  save_page_links(doc)

  if doc.search('input[name="forward"]')
  
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
  doc = Nokogiri.HTML(open(app_info['url']))
    
  details_hash = doc.search('#central table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip.encode('UTF-8')] = tr.search('td')[1].inner_text.strip.encode('UTF-8') if tr.search('td')[1];hsh}

  details = app_info
  
  details[:address] = doc.search('#central table tr')[4].search('td')[1].inner_html.encode('UTF-8').gsub('<br>', ' ')
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:decision] = details_hash['Decision'].strip rescue nil
  details[:agent_name] = details_hash['Agent name'].strip rescue nil
  details[:applicant] = details_hash['Applicant Name'].strip rescue nil
  details[:description] = details_hash['Proposal'].strip rescue nil
  details[:case_officer] = details_hash['Case Officer'].strip rescue nil
  details[:ward_name] = details_hash['Ward'].strip rescue nil
  details[:parish] = details_hash['Parish'].strip rescue nil
  details[:start_date] = Date.parse(details_hash['Received Date'])
  details[:decision_date] = Date.parse(details_hash['Decision Date']) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash['Public Consultation End Date']) rescue nil
  details[:consultation_end_date] = Date.parse(details_hash['Public Consultation Start Date']) rescue nil
  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)

  rescue Exception => e
    puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

52.times do |i| 
 search_for_new_applications(Date.today - (10*(i+i)))
end

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

BASE_URL = 'http://www.winnipeg.ca/cao/media/news/nr_2012/nr_201201_toc.stm'

def save_page_links(doc)
  rows = doc.search('#central table')[0].search('tr')
  rows.shift
  
  puts "Found #{rows.size} applications"
  
  rows.each do |row|
    begin
      record = {}
      link = row.search('a')[0]
      record['url'] = link[:href].gsub('..', BASE_URL)
      record['uid'] = link.inner_text
      ScraperWiki.save(["uid"], record)
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
    
end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + "/servlets/ApplicationSearchServlet"
  
  a = Mechanize.new

  page = a.post(url, {
  'ReceivedDateFrom' => (until_date - 7).strftime("%d-%b-%Y") ,
  'ReceivedDateTo' => until_date.strftime("%d-%b-%Y") ,
  'button' => 'Search'
  })
  
  doc = Nokogiri.HTML(page.body)
  
  save_page_links(doc)

  if doc.search('input[name="forward"]')
  
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
  doc = Nokogiri.HTML(open(app_info['url']))
    
  details_hash = doc.search('#central table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip.encode('UTF-8')] = tr.search('td')[1].inner_text.strip.encode('UTF-8') if tr.search('td')[1];hsh}

  details = app_info
  
  details[:address] = doc.search('#central table tr')[4].search('td')[1].inner_html.encode('UTF-8').gsub('<br>', ' ')
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:decision] = details_hash['Decision'].strip rescue nil
  details[:agent_name] = details_hash['Agent name'].strip rescue nil
  details[:applicant] = details_hash['Applicant Name'].strip rescue nil
  details[:description] = details_hash['Proposal'].strip rescue nil
  details[:case_officer] = details_hash['Case Officer'].strip rescue nil
  details[:ward_name] = details_hash['Ward'].strip rescue nil
  details[:parish] = details_hash['Parish'].strip rescue nil
  details[:start_date] = Date.parse(details_hash['Received Date'])
  details[:decision_date] = Date.parse(details_hash['Decision Date']) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash['Public Consultation End Date']) rescue nil
  details[:consultation_end_date] = Date.parse(details_hash['Public Consultation Start Date']) rescue nil
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