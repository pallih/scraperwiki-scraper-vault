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

BASE_URL = 'http://apps.staffordshire.gov.uk/CPLand/'

def save_page_links(doc)
  
  apps = doc.search("#ContentPlaceHolder1_tblResults a") 
  puts "Found #{apps.size} applications"
  
  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app[:href]
      record['uid'] = app.inner_text.scan(/Proposal Details \((.+)\)/)[0][0]
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end

end

def get_all_applications

  url = BASE_URL + 'search.aspx'
  
  a = Mechanize.new
  a.get(url)
  form = a.page.form_with(:action=>/search.aspx/)  
  form.submit(form.button_with(:value=>'Search'))
    
  doc = Nokogiri.HTML(a.page.body)
  
  save_page_links(doc)
    
  pages = doc.search('.dtlcontent b').inner_text.scan(/Page[\W]+[0-9]+[\W]+of[\W]+([0-9]+)/)[0][0].to_i - 1
      
  pages.times do

    form = a.page.form_with(:action=>/search.aspx/)  
    form.submit(form.button_with(:name=>'ctl00$ContentPlaceHolder1$imgButtonNext'))
    
    doc = Nokogiri.HTML(a.page.body)
    
    save_page_links(doc)
  
  end
  
end

def search_for_new_applications
  
  count = ScraperWiki.sqliteexecute('select count(*) from `swdata`')["data"][0][0]

  url = BASE_URL + 'search.aspx'
  
  a = Mechanize.new
  a.get(url)
  form = a.page.form_with(:action=>/search.aspx/)  
  form.submit(form.button_with(:value=>'Search'))
    
  doc = Nokogiri.HTML(a.page.body)
  
  save_page_links(doc)
  
  apps = Float(doc.search('.dtlcontent')[2].inner_text.scan(/Total matches for search:[\W]+([0-9]+)/)[0][0].to_i)
  
  new = apps - count
  
  pages = (new / 5).ceil - 1
  
  form = a.page.form_with(:action=>/search.aspx/)  
  form.submit(form.button_with(:name=>'ctl00$ContentPlaceHolder1$imgButtonLast'))
  
  pages.times do
  
    form = a.page.form_with(:action=>/search.aspx/)  
    form.submit(form.button_with(:name=>'ctl00$ContentPlaceHolder1$imgButtonBack'))
    
    doc = Nokogiri.HTML(a.page.body)
  
    save_page_links(doc)
  
  end
    
end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE date_received > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  url = app_info['url']

  doc = Nokogiri.HTML(open(url))

  details = app_info

  labels = doc.search('#ContentPlaceHolder1_tblSummary .dtlcontent3')
  contents = doc.search('#ContentPlaceHolder1_tblSummary .dtlcontent2')
  
  i = 0
  details_hash = {}
  
  labels.each do |label|
  details_hash[label.inner_text.strip] = contents[i]
  i += 1
  end
  
  details[:case_officer] = details_hash["Case Officer"].inner_text
  details[:address] = details_hash["Location"].inner_text
  eastingnorthing = details_hash["Site Map"].search('a')[0][:href].scan(/http:\/\/localview.staffordshire.gov.uk\/lvplanning\/OnTheMap.aspx\?e=([0-9]+)&n=([0-9]+)/)[0] rescue nil
  details[:easting] = eastingnorthing[0] rescue nil
  details[:northing] = eastingnorthing[1] rescue nil
  details[:description] = details_hash["Proposal"].inner_text
  details[:applicant_address] = details_hash["Applicant"].inner_text
  details[:agent_address] = details_hash["Agent"].inner_text
  details[:date_received] = Date.parse(details_hash["Received"].inner_text)
  details[:start_date] = Date.parse(details_hash["Received"].inner_text)
  details[:target_decision_date] = Date.parse(details_hash["Target"].inner_text) rescue nil
  details[:decision] = details_hash["Committee Decision"].inner_text
  if details[:decision] == "" # If not committee decision, it's been delegated
  details[:decision] = details_hash["Delegated Decision"].inner_text
  end
  details[:decision_date] = Date.parse(details_hash["Decision Date"].inner_text) rescue nil
  details[:application_type] = details_hash["Type"].inner_text 
  
  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

#get_all_applications

search_for_new_applications
update_stale_applications
