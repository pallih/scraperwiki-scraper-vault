require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'
require 'date'
require 'yaml'

ROOT_URL = 'http://legacy.chesterfield.gov.uk/environment/planning2012/'

def save_page_links(doc)
  apps = doc.search(".DataListData a")
  
  apps.each do |app|
    begin
      record = {}
      record['url'] = ROOT_URL + app[:href]
      record['uid'] = app.inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)

  url = ROOT_URL + "PlanningSearchResults.aspx"
  
  a = Mechanize.new
  
  p = a.post(url, {
    '__EVENTTARGET' => '',
    '__EVENTARGUMENT' => '',
  'txtFrom' => (until_date - 14).strftime("%d/%m/%Y") ,
  'txtTo' => until_date.strftime("%d/%m/%Y") ,
  'Txtb_ApplicationNumber' => '',
  'Txtb_Location' => '',
  'Sel_WardList' => '',
  'Rad_Filter' => 'all',
  'But_Submit' => 'Search Planning Applications'
  })
        
  doc = Nokogiri.HTML(p.body)
  save_page_links(doc)
  
  pages = Float(doc.search("#lblCurrentPage")[0].inner_text.scan(/ planning applications: 1 to [0-9]+ of ([0-9]+)/)[0][0])
  
  viewstate = doc.search("#__VIEWSTATE")[0][:value]
   
  pages = ((pages / 10).ceil) - 1
  
  pages.times do
  
    a = Mechanize.new
  
    p = a.post(url, {
    '__EVENTTARGET' => '',
    '__EVENTARGUMENT' => '',
    '__LASTFOCUS' => '',
    '__VIEWSTATE' => viewstate,
    'txtFrom' => (until_date - 14).strftime("%d/%m/%Y") ,
    'txtTo' => until_date.strftime("%d/%m/%Y") ,
    'cmdNextTop' => '>>',
    'DDL_AppsPerPage' => '10',
    'Txtb_Location' => '',
    'Txtb_ApplicationNumber' => '',
    'Sel_WardList' => '',
    'Rad_Filter' => 'all'
    })
        
    doc = Nokogiri.HTML(p.body)
    save_page_links(doc)
    
    viewstate = doc.search("#__VIEWSTATE")[0][:value]
    
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
  
  details_hash = doc.search('div.DataListDataWrapper').inject({}){|hsh,div| hsh[div.search('.DataListLabelabel')[0].inner_text.strip] = div.search('.DataListData')[0].inner_text.gsub("\r", " ").strip if div.search('.DataListLabelabel');hsh}
  
  details[:address] = details_hash["Location:"] rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:agent_name] = details_hash["Agent:"] rescue nil
  details[:application_type] = details_hash["Type:"] rescue nil
  details[:applicant_name] = details_hash["Applicant:"] rescue nil
  details[:ward_name] = details_hash["Ward:"] rescue nil
  details[:description] = details_hash["Proposal:"] rescue nil
  details[:date_received] = Date.parse(details_hash["Application Date:"])
  details[:start_date] = Date.parse(details_hash["Application Date:"])
  details[:date_validated] = Date.parse(details_hash["Validation Date:"]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(details_hash["Neighbours Consulted:"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(details_hash["Neighbours Expiry:"]) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash["Standard Consultation Sent Date:"]) rescue nil
  details[:decision] = details_hash["Decision:"] rescue nil
  details[:decision_date] = Date.parse(details_hash["Determination Date:"]) rescue nil
  details[:case_officer] = details_hash["Case Officer:"] rescue nil

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
require 'nokogiri'
require 'mechanize'
require 'open-uri'
require 'date'
require 'yaml'

ROOT_URL = 'http://legacy.chesterfield.gov.uk/environment/planning2012/'

def save_page_links(doc)
  apps = doc.search(".DataListData a")
  
  apps.each do |app|
    begin
      record = {}
      record['url'] = ROOT_URL + app[:href]
      record['uid'] = app.inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)

  url = ROOT_URL + "PlanningSearchResults.aspx"
  
  a = Mechanize.new
  
  p = a.post(url, {
    '__EVENTTARGET' => '',
    '__EVENTARGUMENT' => '',
  'txtFrom' => (until_date - 14).strftime("%d/%m/%Y") ,
  'txtTo' => until_date.strftime("%d/%m/%Y") ,
  'Txtb_ApplicationNumber' => '',
  'Txtb_Location' => '',
  'Sel_WardList' => '',
  'Rad_Filter' => 'all',
  'But_Submit' => 'Search Planning Applications'
  })
        
  doc = Nokogiri.HTML(p.body)
  save_page_links(doc)
  
  pages = Float(doc.search("#lblCurrentPage")[0].inner_text.scan(/ planning applications: 1 to [0-9]+ of ([0-9]+)/)[0][0])
  
  viewstate = doc.search("#__VIEWSTATE")[0][:value]
   
  pages = ((pages / 10).ceil) - 1
  
  pages.times do
  
    a = Mechanize.new
  
    p = a.post(url, {
    '__EVENTTARGET' => '',
    '__EVENTARGUMENT' => '',
    '__LASTFOCUS' => '',
    '__VIEWSTATE' => viewstate,
    'txtFrom' => (until_date - 14).strftime("%d/%m/%Y") ,
    'txtTo' => until_date.strftime("%d/%m/%Y") ,
    'cmdNextTop' => '>>',
    'DDL_AppsPerPage' => '10',
    'Txtb_Location' => '',
    'Txtb_ApplicationNumber' => '',
    'Sel_WardList' => '',
    'Rad_Filter' => 'all'
    })
        
    doc = Nokogiri.HTML(p.body)
    save_page_links(doc)
    
    viewstate = doc.search("#__VIEWSTATE")[0][:value]
    
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
  
  details_hash = doc.search('div.DataListDataWrapper').inject({}){|hsh,div| hsh[div.search('.DataListLabelabel')[0].inner_text.strip] = div.search('.DataListData')[0].inner_text.gsub("\r", " ").strip if div.search('.DataListLabelabel');hsh}
  
  details[:address] = details_hash["Location:"] rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:agent_name] = details_hash["Agent:"] rescue nil
  details[:application_type] = details_hash["Type:"] rescue nil
  details[:applicant_name] = details_hash["Applicant:"] rescue nil
  details[:ward_name] = details_hash["Ward:"] rescue nil
  details[:description] = details_hash["Proposal:"] rescue nil
  details[:date_received] = Date.parse(details_hash["Application Date:"])
  details[:start_date] = Date.parse(details_hash["Application Date:"])
  details[:date_validated] = Date.parse(details_hash["Validation Date:"]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(details_hash["Neighbours Consulted:"]) rescue nil
  details[:neighbour_consultation_end_date] = Date.parse(details_hash["Neighbours Expiry:"]) rescue nil
  details[:consultation_start_date] = Date.parse(details_hash["Standard Consultation Sent Date:"]) rescue nil
  details[:decision] = details_hash["Decision:"] rescue nil
  details[:decision_date] = Date.parse(details_hash["Determination Date:"]) rescue nil
  details[:case_officer] = details_hash["Case Officer:"] rescue nil

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
