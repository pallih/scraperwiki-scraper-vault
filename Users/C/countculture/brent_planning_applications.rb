require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'https://forms.brent.gov.uk/servlet/ep.ext'

def search_for_new_applications(until_date=Date.today)
  search_url = BASE_URL + '?print=Y&byStreet=N&instructions=Enter+a+date+range&extId=101149&other4Label=Other4&queried=Y&other5Label=Other5&periodLabel=From&byPostcode=N&byAddress=N&byPeriod=Y&byHouseNumber=N&byFormat=N&auth=402&periodUnits=day&periodMultiples=14&displayTitle=Search+by+Application+Date&st=PL&other1Label=Other1&byOther5=N&byOther4=N&byOther3=N&other2Label=Other2&byOther2=N&byOther1=N&addressLabel=Select+Address&other3Label=Other3'
  search_url += "&from=#{format_date(until_date - 14)}&until=#{format_date(until_date)}"
  doc = Nokogiri.HTML(open(search_url, :ssl_verify_mode => OpenSSL::SSL::VERIFY_NONE))
  application_links = doc.search('form a[@href*="https://forms.brent.gov.uk/servlet/ep.ext"]') #only want details
  puts "Found #{application_links.size} applications"
  
  application_links.each do |link|
    begin
      record = {}
      record['url'] = link[:href]
      record['uid'] = link[:href].scan(/reference=(\d+)/).flatten.first.unpack('A2A4').join('/')
      ScraperWiki.save(["uid"], record) # use uid as primary key NB save overwrites any other data apart from url and uid
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def update_stale_applications
  current_applications = ScraperWiki.select("* from swdata WHERE date_received > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 200")
  current_applications.each do |app|
    populate_application_details(app)
  end
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL limit 600")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  doc=Nokogiri.HTML(open(app_info['url'] + '&print=Y', :ssl_verify_mode => OpenSSL::SSL::VERIFY_NONE))
  details_hash = doc.search('#detailsDiv table tr').inject({}){|hsh,tr| hsh[tr.at('td strong').inner_text.strip] = tr.search('td').last if tr.at('td strong');hsh}
  details = app_info
  details[:address] = details_hash['Location:'].inner_text.strip #address is required
  details[:applicant_name] = details_hash['Applicant:'].at('strong').remove.inner_text.strip rescue nil
  details[:applicant_address] = details_hash['Applicant:'].inner_text.sub(/^[,\s]+/,'').strip rescue nil
  details[:application_type] = details_hash['Application Type:'].inner_text.strip rescue nil
  details[:description] = details_hash['Proposal:'].inner_text.strip rescue nil
  details[:status] = details_hash['Status:'].inner_text.strip rescue nil
  details[:decision] = details_hash['Decision:'].inner_text.strip rescue nil
  date_received = details_hash['Received Date:'].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil
  # put dates in iso 8601 date format so we can sort by them
  details[:date_received] = Date.parse(date_received) rescue nil
  decision_date = details_hash['Decision Date:'].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil
  details[:decision_date] = Date.parse(decision_date) rescue nil
  if agent = details_hash['Agent:']
    details[:agent_name] = agent.at('strong').inner_text.strip rescue nil
    details[:agent_address] = agent.at('strong').next.inner_text.strip.gsub(/[\s]{3,}/,', ').sub(/^[\s,]+/,'').strip rescue nil
  end
  details[:comment_url] = doc.at('a[text()*="Comment on this"]')[:href] rescue nil
  details[:associated_application_uid] = details_hash['Associated application:'].inner_text.strip rescue nil
  details[:case_officer] = details_hash["Case Officer:"].inner_text.split("\n").first.strip rescue nil
  details[:date_scraped] = Time.now
  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

def format_date(date)
  date.strftime('%d/%m/%Y').gsub('/','%2F')
end

def make_iso_dates(field)
  current_applications = ScraperWiki.select("uid, " + field + " from swdata WHERE " + field + " like '%/%/%' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    app[field] = app[field].split('/').reverse.join('-')
    #ScraperWiki.execute("update swdata SET " + field + " = '" + app[field] + "' WHERE uid = '" + app['uid'] + "'")
    #ScraperWiki.commit()
  end
end

# get from 3 years ago working forward in fortnights
#78.times do |i| 
#  search_for_new_applications(Date.today - (79*14) + (i*14))
#end
#make_iso_dates('decision_date')
search_for_new_applications
update_stale_applicationsrequire 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'https://forms.brent.gov.uk/servlet/ep.ext'

def search_for_new_applications(until_date=Date.today)
  search_url = BASE_URL + '?print=Y&byStreet=N&instructions=Enter+a+date+range&extId=101149&other4Label=Other4&queried=Y&other5Label=Other5&periodLabel=From&byPostcode=N&byAddress=N&byPeriod=Y&byHouseNumber=N&byFormat=N&auth=402&periodUnits=day&periodMultiples=14&displayTitle=Search+by+Application+Date&st=PL&other1Label=Other1&byOther5=N&byOther4=N&byOther3=N&other2Label=Other2&byOther2=N&byOther1=N&addressLabel=Select+Address&other3Label=Other3'
  search_url += "&from=#{format_date(until_date - 14)}&until=#{format_date(until_date)}"
  doc = Nokogiri.HTML(open(search_url, :ssl_verify_mode => OpenSSL::SSL::VERIFY_NONE))
  application_links = doc.search('form a[@href*="https://forms.brent.gov.uk/servlet/ep.ext"]') #only want details
  puts "Found #{application_links.size} applications"
  
  application_links.each do |link|
    begin
      record = {}
      record['url'] = link[:href]
      record['uid'] = link[:href].scan(/reference=(\d+)/).flatten.first.unpack('A2A4').join('/')
      ScraperWiki.save(["uid"], record) # use uid as primary key NB save overwrites any other data apart from url and uid
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def update_stale_applications
  current_applications = ScraperWiki.select("* from swdata WHERE date_received > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 200")
  current_applications.each do |app|
    populate_application_details(app)
  end
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL limit 600")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  doc=Nokogiri.HTML(open(app_info['url'] + '&print=Y', :ssl_verify_mode => OpenSSL::SSL::VERIFY_NONE))
  details_hash = doc.search('#detailsDiv table tr').inject({}){|hsh,tr| hsh[tr.at('td strong').inner_text.strip] = tr.search('td').last if tr.at('td strong');hsh}
  details = app_info
  details[:address] = details_hash['Location:'].inner_text.strip #address is required
  details[:applicant_name] = details_hash['Applicant:'].at('strong').remove.inner_text.strip rescue nil
  details[:applicant_address] = details_hash['Applicant:'].inner_text.sub(/^[,\s]+/,'').strip rescue nil
  details[:application_type] = details_hash['Application Type:'].inner_text.strip rescue nil
  details[:description] = details_hash['Proposal:'].inner_text.strip rescue nil
  details[:status] = details_hash['Status:'].inner_text.strip rescue nil
  details[:decision] = details_hash['Decision:'].inner_text.strip rescue nil
  date_received = details_hash['Received Date:'].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil
  # put dates in iso 8601 date format so we can sort by them
  details[:date_received] = Date.parse(date_received) rescue nil
  decision_date = details_hash['Decision Date:'].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil
  details[:decision_date] = Date.parse(decision_date) rescue nil
  if agent = details_hash['Agent:']
    details[:agent_name] = agent.at('strong').inner_text.strip rescue nil
    details[:agent_address] = agent.at('strong').next.inner_text.strip.gsub(/[\s]{3,}/,', ').sub(/^[\s,]+/,'').strip rescue nil
  end
  details[:comment_url] = doc.at('a[text()*="Comment on this"]')[:href] rescue nil
  details[:associated_application_uid] = details_hash['Associated application:'].inner_text.strip rescue nil
  details[:case_officer] = details_hash["Case Officer:"].inner_text.split("\n").first.strip rescue nil
  details[:date_scraped] = Time.now
  ScraperWiki.save([:uid], details)
rescue Exception => e
  puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

def format_date(date)
  date.strftime('%d/%m/%Y').gsub('/','%2F')
end

def make_iso_dates(field)
  current_applications = ScraperWiki.select("uid, " + field + " from swdata WHERE " + field + " like '%/%/%' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    app[field] = app[field].split('/').reverse.join('-')
    #ScraperWiki.execute("update swdata SET " + field + " = '" + app[field] + "' WHERE uid = '" + app['uid'] + "'")
    #ScraperWiki.commit()
  end
end

# get from 3 years ago working forward in fortnights
#78.times do |i| 
#  search_for_new_applications(Date.today - (79*14) + (i*14))
#end
#make_iso_dates('decision_date')
search_for_new_applications
update_stale_applications