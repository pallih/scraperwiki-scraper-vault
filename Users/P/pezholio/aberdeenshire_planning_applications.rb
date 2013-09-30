require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `application_type` text, `decision` text, `date_received` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `associated_application_uid` text, `decision_date` text, `easting` integer, `northing` integer, `parish` text, `meeting_date` text, `start_date` text, `date_validated` text, `decision_issued` text, `comment_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('ALTER TABLE swdata ADD COLUMN date_scraped')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://www.aberdeenshire.gov.uk/planning/apps'

def save_page_links(link)
  doc = Nokogiri.HTML(open(link))
  application_links = doc.search('table a[@href*="detail.asp?ref_no="]') #only want details
  puts "Found #{application_links.size} applications"
  
  application_links.each do |link|
    begin
      record = {}
      record['url'] = BASE_URL + '/' + link[:href]
      record['uid'] = link.inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)
  search_url = BASE_URL + "/search.asp?ref_no=&site_postcode=&site_address=&area=&ward=&parish=&agent_name=&applicant=&startValidDate=#{(until_date - 14).strftime("%d%%2F%m%%2F%Y")}&endValidDate=#{until_date.strftime("%d%%2F%m%%2F%Y")}&x=17&y=7"
    
  doc = Nokogiri.HTML(open(search_url))

  pages = doc.search('#leftCol p:nth-of-type(2)')
  total = pages[0].text.scan(/Displaying page [0-9]+ of ([0-9]+) pages./)[0][0].to_i
  
  num = 1

  while num <= total
    save_page_links(search_url + "&pagenum=" + num.to_s)
    num += 1
  end
end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL LIMIT 500")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE date_received > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  doc=Nokogiri.HTML(open(app_info['url']))
details_hash = doc.search('table [@border="0"] tr').inject({}){|hsh,tr| hsh[tr.at('th').inner_text.gsub(/[^0-9a-z ]/i, '').strip] = tr.search('td') if tr.at('th');hsh}

details = app_info

details[:address] = details_hash['Site Address'].inner_html.gsub("\r\n", " ").gsub("<br>", " ").gsub(/<\/?[^>]*>/, "").squeeze(' ').force_encoding("ASCII-8BIT").gsub(/[\x80-\xff]/, " ").gsub('-->', '').strip
details[:description] =  doc.search('//a[@id="proposal"]/../following-sibling::p[1]').inner_text

eastingnorthing = details_hash['Map Ref'].inner_text.split(',')

details[:easting] = eastingnorthing[0].strip.to_i
details[:northing] = eastingnorthing[1].strip.to_i
details[:ward_name] = details_hash['Ward'].inner_html.split("<br>")[0].gsub(/<\/?[^>]*>/, "").strip
details[:parish] = details_hash['Parish'].inner_html.gsub(/<\/?[^>]*>/, "").force_encoding("ASCII-8BIT").gsub(/[\x80-\xff]/, " ").strip
details[:case_officer] = doc.search('//a[@id="proposal"]/../following-sibling::table[1]/tr[2]/td[1]').inner_text

applicant = doc.search('//a[@id="proposal"]/../following-sibling::table[2]/tr[2]/td[1]').inner_text.split("/r/n")

details[:applicant_name] = applicant[0].force_encoding("ASCII-8BIT").gsub(/[\x80-\xff]/, " ").squeeze(' ').strip rescue nil
details[:applicant_address] = applicant[1].force_encoding("ASCII-8BIT").gsub(/[\x80-\xff]/, " ").strip rescue nil

agent = doc.search('//a[@id="proposal"]/../following-sibling::table[2]/tr[2]/td[2]').inner_html.split("<br>")

details[:agent_name] = agent.shift.force_encoding("ASCII-8BIT").gsub(/[\x80-\xff]/, " ").strip rescue nil
details[:agent_address] = agent.join(" ").strip rescue nil

dates = doc.search('//a[@id="proposal"]/../following-sibling::table[3]/tr[2]/td')

details[:start_date] = dates[0].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')
details[:date_received] = Date.parse(dates[0].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-'))
details[:date_validated] = dates[1].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil
details[:meeting_date] = dates[2].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil

decision = doc.search('//a[@id="proposal"]/../following-sibling::table[4]/tr[2]/td')

details[:decision_date] = decision[0].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil
details[:decision_issued_date] = decision[0].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil
details[:decision] = decision[2].inner_text.force_encoding("ASCII-8BIT").gsub("\xC2\xA0", " ").strip

details[:comment_url] = BASE_URL + "/" + doc.search('#comment a[@href*="comment.asp?ref_no="]')[0][:href]
details[:comment_date] = doc.search('//a[@id="publiccomment"]/../following-sibling::p[1]').inner_text.gsub("Expiry Date:", "").strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil
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
update_stale_applicationsrequire 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'date'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `status` text, `date_scraped` text, `application_type` text, `decision` text, `date_received` text, `applicant_address` text, `address` text, `description` text, `agent_name` text, `applicant_name` text, `agent_address` text, `case_officer` text, `comment_url` text, `associated_application_uid` text, `decision_date` text, `easting` integer, `northing` integer, `parish` text, `meeting_date` text, `start_date` text, `date_validated` text, `decision_issued` text, `comment_date` text, `ward_name` text)')
#ScraperWiki.sqliteexecute('ALTER TABLE swdata ADD COLUMN date_scraped')
#ScraperWiki.sqliteexecute('CREATE INDEX date_scraped ON swdata (date_scraped)')
#exit

BASE_URL = 'http://www.aberdeenshire.gov.uk/planning/apps'

def save_page_links(link)
  doc = Nokogiri.HTML(open(link))
  application_links = doc.search('table a[@href*="detail.asp?ref_no="]') #only want details
  puts "Found #{application_links.size} applications"
  
  application_links.each do |link|
    begin
      record = {}
      record['url'] = BASE_URL + '/' + link[:href]
      record['uid'] = link.inner_text
      ScraperWiki.save(["uid"], record) # use uid as primary key
    rescue Exception => e
      puts "Exception #{e.inspect} raised getting basic data from #{link}"
    end
  end
end

def search_for_new_applications(until_date=Date.today)
  search_url = BASE_URL + "/search.asp?ref_no=&site_postcode=&site_address=&area=&ward=&parish=&agent_name=&applicant=&startValidDate=#{(until_date - 14).strftime("%d%%2F%m%%2F%Y")}&endValidDate=#{until_date.strftime("%d%%2F%m%%2F%Y")}&x=17&y=7"
    
  doc = Nokogiri.HTML(open(search_url))

  pages = doc.search('#leftCol p:nth-of-type(2)')
  total = pages[0].text.scan(/Displaying page [0-9]+ of ([0-9]+) pages./)[0][0].to_i
  
  num = 1

  while num <= total
    save_page_links(search_url + "&pagenum=" + num.to_s)
    num += 1
  end
end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL LIMIT 500")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE date_received > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  doc=Nokogiri.HTML(open(app_info['url']))
details_hash = doc.search('table [@border="0"] tr').inject({}){|hsh,tr| hsh[tr.at('th').inner_text.gsub(/[^0-9a-z ]/i, '').strip] = tr.search('td') if tr.at('th');hsh}

details = app_info

details[:address] = details_hash['Site Address'].inner_html.gsub("\r\n", " ").gsub("<br>", " ").gsub(/<\/?[^>]*>/, "").squeeze(' ').force_encoding("ASCII-8BIT").gsub(/[\x80-\xff]/, " ").gsub('-->', '').strip
details[:description] =  doc.search('//a[@id="proposal"]/../following-sibling::p[1]').inner_text

eastingnorthing = details_hash['Map Ref'].inner_text.split(',')

details[:easting] = eastingnorthing[0].strip.to_i
details[:northing] = eastingnorthing[1].strip.to_i
details[:ward_name] = details_hash['Ward'].inner_html.split("<br>")[0].gsub(/<\/?[^>]*>/, "").strip
details[:parish] = details_hash['Parish'].inner_html.gsub(/<\/?[^>]*>/, "").force_encoding("ASCII-8BIT").gsub(/[\x80-\xff]/, " ").strip
details[:case_officer] = doc.search('//a[@id="proposal"]/../following-sibling::table[1]/tr[2]/td[1]').inner_text

applicant = doc.search('//a[@id="proposal"]/../following-sibling::table[2]/tr[2]/td[1]').inner_text.split("/r/n")

details[:applicant_name] = applicant[0].force_encoding("ASCII-8BIT").gsub(/[\x80-\xff]/, " ").squeeze(' ').strip rescue nil
details[:applicant_address] = applicant[1].force_encoding("ASCII-8BIT").gsub(/[\x80-\xff]/, " ").strip rescue nil

agent = doc.search('//a[@id="proposal"]/../following-sibling::table[2]/tr[2]/td[2]').inner_html.split("<br>")

details[:agent_name] = agent.shift.force_encoding("ASCII-8BIT").gsub(/[\x80-\xff]/, " ").strip rescue nil
details[:agent_address] = agent.join(" ").strip rescue nil

dates = doc.search('//a[@id="proposal"]/../following-sibling::table[3]/tr[2]/td')

details[:start_date] = dates[0].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')
details[:date_received] = Date.parse(dates[0].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-'))
details[:date_validated] = dates[1].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil
details[:meeting_date] = dates[2].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil

decision = doc.search('//a[@id="proposal"]/../following-sibling::table[4]/tr[2]/td')

details[:decision_date] = decision[0].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil
details[:decision_issued_date] = decision[0].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil
details[:decision] = decision[2].inner_text.force_encoding("ASCII-8BIT").gsub("\xC2\xA0", " ").strip

details[:comment_url] = BASE_URL + "/" + doc.search('#comment a[@href*="comment.asp?ref_no="]')[0][:href]
details[:comment_date] = doc.search('//a[@id="publiccomment"]/../following-sibling::p[1]').inner_text.gsub("Expiry Date:", "").strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-') rescue nil
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