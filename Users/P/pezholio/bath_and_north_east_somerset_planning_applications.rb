require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'

#BASE_URL = "http://isharemaps.bathnes.gov.uk/ishare42/projects/bathnes/developmentcontrol/default.aspx?"
BASE_URL = "http://isharemaps.bathnes.gov.uk/projects/bathnes/developmentcontrol/default.aspx?" # new URL

def save_page_links(doc, from_date)
  apps = doc.search('.atSearchResults > div:not(.atPagination)')
  
  apps.each do |app|
    dateRef = app.search('.atDateDetails')[0].inner_text.scan(/Application reference: ([0-9]+\/[0-9]+\/[A-Z0-9]+) received on ([0-9\/]+)/)
    if Date.strptime(dateRef[0][1], '%d/%m/%Y') >= from_date 
      begin
        record = {}
        link = app.search('a')[0]
        record['url'] = link[:href]
        record['uid'] = dateRef[0][0]
        ScraperWiki.save(["uid"], record) # use uid as primary key
      rescue
        puts "Exception #{e.inspect} raised getting basic data from #{link}"
      end
    end
  end
  
end

def search_for_new_applications(until_date=Date.today)
  
  for i in 1..10 do  
    url = BASE_URL + "template=DevelopmentControlResults.tmplt&requestType=parseTemplate&usesearch=true&order=DATEAPRECV%3ADESCENDING&q%3ALIKE=&DCAPPTYP%3ASRCH=&DCSTAT%3ASRCH=&APSTAT%3ASRCH=&WARD%3ASRCH=&PARISH%3ASRCH=&DATEAPVAL%3AFROM%3ADATE=#{(until_date - 14).strftime("%d/%m/%Y")}&DATEAPVAL%3ATO%3ADATE=#{until_date.strftime("%d/%m/%Y")}&DATEACTCOM%3AFROM%3ADATE=&DATEDECISN%3AFROM%3ADATE=&DAPLSTART%3AFROM%3ADATE=&DATEAPPDEC%3AFROM%3ADATE=&pagerecs=10&maxrecords=100&pageno=#{i}"
    doc = Nokogiri.HTML(open(url))
      
    save_page_links(doc, until_date - 14)
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
  url = app_info['url'].gsub('^', '%5E')
  
  doc = Nokogiri.HTML(open(url))
  
  details = app_info
  
  details_hash = doc.search('#atTab1 table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text if tr.search('td').count > 1;hsh}
  dates = doc.search('#atTab2 table tr').inject({}){|hsh,tr| hsh[tr.search('td')[0].inner_text.strip] = tr.search('td')[1].inner_text if tr.search('td').count > 1;hsh}
  
  details[:date_received] = Date.parse(dates["Date Application Received:"])
  details[:start_date] = Date.parse(dates["Date Application Received:"])
  details[:date_validated] = Date.parse(dates["Date Application Validated:"]) rescue nil
  details[:consultation_end_date] = Date.parse(dates["Expiry Date for Consultation :"].match(/[0-9\/]+/)[0]) rescue nil
  details[:neighbour_consultation_start_date] = Date.parse(dates["Neighbourhood Consultations sent on:"]) rescue nil
  details[:decision_date] = Date.parse(dates["Date Decision Made:"]) rescue nil
  details[:target_decision_date] = Date.parse(dates["Target Decision Date"]) rescue nil
  details[:appeal_date] = Date.parse(dates["Appeal Start Date:"]) rescue nil
  details[:appeal_decision_date] = Date.parse(dates["Appeal Decision Date:"]) rescue nil
  details[:address] = details_hash["Address Of Proposal:"] rescue nil
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0] rescue nil
  details[:easting] = doc.search('.atPublisherTemplate script')[2].inner_text.scan(/var easting = '([0-9]+)';/)[0][0]
  details[:northing] = doc.search('.atPublisherTemplate script')[2].inner_text.scan(/var northing = '([0-9]+)';/)[0][0]
  details[:status] = details_hash["Status:"] rescue nil
  details[:description] = details_hash["Proposal:"] rescue nil
  details[:case_officer] = details_hash["Case Officer Name:"] rescue nil
  details[:target_decision_date] = Date.parse(dates["Target Decision Date:"]) rescue nil
  details[:ward_name] = details_hash["Ward:"] rescue nil
  details[:planning_portal_id] = details_hash["Planning Portal Reference Number:"] rescue nil
  details[:applicant_name] = details_hash["Applicant Name:"] rescue nil
  details[:decision] = details_hash["Decision:"] rescue nil
  details[:agent_name] = details_hash["Agent Name:"] rescue nil
  details[:agent_address] = details_hash["Agent Address:"] rescue nil
  details[:appeal_result] = details_hash["Appeal Status:"] rescue nil
  details[:comment_url] = doc.search('h3 a')[0][:href] rescue nil

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
