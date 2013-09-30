require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `decision` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `os_grid_ref` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

def numeric?(object)
  true if Float(object) rescue false
end

def save_page_links(link)
  puts link
  doc = Nokogiri.HTML(open(link))
  apps = doc.search('h3.resultsnavbar') #only want details
  puts "Found #{apps.size} applications"
  
  apps.each do |app|
    begin
      record = {}
      record['uid'] = app.inner_text.gsub('Application No: ', '')
      record['url'] = 'http://www.calderdale.gov.uk/environment/planning/search-applications/planapps.jsp?app=' + record['uid']
      puts record['url']
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)

  search_url = "http://www.calderdale.gov.uk/environment/planning/search-applications/planapps.jsp?date2=#{until_date.strftime("%d%%2F%m%%2F%Y")}&date1=#{(until_date - 14).strftime("%d%%2F%m%%2F%Y")}"
    
  doc = Nokogiri.HTML(open(search_url))

  pages = doc.search('.resultbot li')
  total = 0
  pages.each do |list|
    if numeric?(list.inner_text)
      total += 1
    end
  end
    
  num = 0

  while num < total
    offset = num * 20
    save_page_links(search_url + "&offset=" + offset.to_s)
    num += 1
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
  doc=Nokogiri.HTML(open(app_info['url']))
  
  details_hash = doc.search('div.boxcontainer p').inject({}){|hsh,p| hsh[p.at('strong').inner_text.strip] = p.inner_text.gsub(p.at('strong').inner_text.strip, '') if p.at('strong');hsh}
  
  details = app_info 

  details[:comment_url] = "http://www.calderdale.gov.uk/environment/planning/comment/index.jsp?app=#{app_info['uid']}"
  details[:address] = details_hash['Address of proposal:'].gsub("\r", " ").strip
  details[:applicant_name] = details_hash['Applicant:'].strip rescue nil
  details[:applicant_address] = details_hash['Applicant Address:'].gsub("\r", " ").strip rescue nil
  details[:description] = details_hash['Proposal:'].strip rescue nil
  
  if details_hash.has_key?('Ward:')
    if details_hash['Ward:'].include? "Parish:"
      wardparish = details_hash['Ward:'].split("Parish:")
      details[:ward_name] = wardparish[0].strip.force_encoding("ASCII-8BIT").chomp(" \xC2\xA0").strip
      details[:parish] = wardparish[1].strip
    else
      details[:ward_name] = details_hash['Ward:'].strip rescue nil
    end
  end
  
  details[:status] = details_hash['Status:'].strip rescue nil
  details[:decision] = details_hash['Decision type:'].strip rescue nil
  details[:agent_name] = details_hash['Agent:'].strip rescue nil
  details[:agent_address] = details_hash['Agent Address:'].gsub("\r", " ").strip rescue nil
  details[:case_officer] = details_hash['Case Officer:'].strip rescue nil
  details[:os_grid_ref] = details_hash['Grid Reference:'].strip rescue nil
  
  details[:start_date] = Date.parse(details_hash['Valid Date:'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) # Required
  details[:date_validated] = Date.parse(details_hash['Valid Date:'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:decision_date] = Date.parse(details_hash['Decision Date:'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil

  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

#52.times do |i| 
 #search_for_new_applications(Date.today - (10*(i+i)))
#end
#search_for_new_applications
update_stale_applicationsrequire 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `decision` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `decision_date` text, `os_grid_ref` text, `date_validated` text, `parish` text, `start_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

def numeric?(object)
  true if Float(object) rescue false
end

def save_page_links(link)
  puts link
  doc = Nokogiri.HTML(open(link))
  apps = doc.search('h3.resultsnavbar') #only want details
  puts "Found #{apps.size} applications"
  
  apps.each do |app|
    begin
      record = {}
      record['uid'] = app.inner_text.gsub('Application No: ', '')
      record['url'] = 'http://www.calderdale.gov.uk/environment/planning/search-applications/planapps.jsp?app=' + record['uid']
      puts record['url']
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)

  search_url = "http://www.calderdale.gov.uk/environment/planning/search-applications/planapps.jsp?date2=#{until_date.strftime("%d%%2F%m%%2F%Y")}&date1=#{(until_date - 14).strftime("%d%%2F%m%%2F%Y")}"
    
  doc = Nokogiri.HTML(open(search_url))

  pages = doc.search('.resultbot li')
  total = 0
  pages.each do |list|
    if numeric?(list.inner_text)
      total += 1
    end
  end
    
  num = 0

  while num < total
    offset = num * 20
    save_page_links(search_url + "&offset=" + offset.to_s)
    num += 1
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
  doc=Nokogiri.HTML(open(app_info['url']))
  
  details_hash = doc.search('div.boxcontainer p').inject({}){|hsh,p| hsh[p.at('strong').inner_text.strip] = p.inner_text.gsub(p.at('strong').inner_text.strip, '') if p.at('strong');hsh}
  
  details = app_info 

  details[:comment_url] = "http://www.calderdale.gov.uk/environment/planning/comment/index.jsp?app=#{app_info['uid']}"
  details[:address] = details_hash['Address of proposal:'].gsub("\r", " ").strip
  details[:applicant_name] = details_hash['Applicant:'].strip rescue nil
  details[:applicant_address] = details_hash['Applicant Address:'].gsub("\r", " ").strip rescue nil
  details[:description] = details_hash['Proposal:'].strip rescue nil
  
  if details_hash.has_key?('Ward:')
    if details_hash['Ward:'].include? "Parish:"
      wardparish = details_hash['Ward:'].split("Parish:")
      details[:ward_name] = wardparish[0].strip.force_encoding("ASCII-8BIT").chomp(" \xC2\xA0").strip
      details[:parish] = wardparish[1].strip
    else
      details[:ward_name] = details_hash['Ward:'].strip rescue nil
    end
  end
  
  details[:status] = details_hash['Status:'].strip rescue nil
  details[:decision] = details_hash['Decision type:'].strip rescue nil
  details[:agent_name] = details_hash['Agent:'].strip rescue nil
  details[:agent_address] = details_hash['Agent Address:'].gsub("\r", " ").strip rescue nil
  details[:case_officer] = details_hash['Case Officer:'].strip rescue nil
  details[:os_grid_ref] = details_hash['Grid Reference:'].strip rescue nil
  
  details[:start_date] = Date.parse(details_hash['Valid Date:'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) # Required
  details[:date_validated] = Date.parse(details_hash['Valid Date:'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
  details[:decision_date] = Date.parse(details_hash['Decision Date:'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil

  details[:date_scraped] = Time.now

  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

#52.times do |i| 
 #search_for_new_applications(Date.today - (10*(i+i)))
#end
#search_for_new_applications
update_stale_applications