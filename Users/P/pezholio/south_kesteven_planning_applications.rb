require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `date_scraped` text,`start_date` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://www.southkesteven.gov.uk/'

def save_page_links(doc)
  apps = doc.search(".PlanningApplication h4 a") 
  puts "Found #{apps.size} applications"
  
  apps.each do |app|
    begin
      record = {}
      record['url'] = BASE_URL + app[:href]
      record['uid'] = app[:href].scan(/index.aspx\?articleid=2230&ApplicationNumber=(S[0-9]+\/[0-9]+)/)[0][0]
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)

  url = BASE_URL + 'index.aspx?articleid=1640'
  
  agent = Mechanize.new
  
  data = {
    'ShowAdvancedSearch' => 'true',
    'CompleteAddress' => '',
    'Proposal' => '',
    'ApplicantName' => '',
    'AgentName' => '',
    'DatePresets' => 'None',
    'ApplicationState' => 'ReceivedDate',
    'DateStart' => (until_date - 14).strftime("%d/%m/%Y"),
    'DateEnd' => until_date.strftime("%d/%m/%Y"),
    'ResultSize' => '100',
    'ViewName' => 'ViewList',
    'searchFilter' => 'Search'
  }
  
  page = agent.post(url, data)
  
  doc = Nokogiri.HTML(page.content)
  
  results = doc.search('.cmxform p strong')[0].inner_text.to_i
  
  pages = (Float(results) / 100).ceil
  
  pages.times do |page|
    data['searchResults_Page'] = page + 1
    data['Page'] = page
    page = agent.post(url, data)
    save_page_links(Nokogiri.HTML(page.content))
  end

end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL LIMIT 5000")
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

  details_hash = doc.search('.ReferenceInformation tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text if tr.search('td').count > 1;hsh}
  
  details[:address] = details_hash['Location']
  details[:description] = details_hash['Proposal']
  details[:date_received] = Date.parse(details_hash['Received on'])
  details[:start_date] = Date.parse(details_hash['Received on'])
  details[:application_type] = details_hash['Type']
  details[:decision] = details_hash['Decision']
  details[:decision_date] = Date.parse(details_hash['Decision made']) rescue nil
  details[:applicant_name] = details_hash['Applicant']
  details[:agent_name] = details_hash['Agent'] rescue nil
  
  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{details.inspect}). Backtrace:\n#{e.backtrace}"
end

#52.times do |i| 
 #search_for_new_applications(Date.today - (10*(i+i)))
#end

search_for_new_applications
update_stale_applications
