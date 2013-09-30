require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'
 
def submit(page)
  page.forms[0].submit
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during submit"
  retry
end

def extract(page)
  scraped = 0
  saved = 0

  page_number = 1
  save_metadata('page_number', page_number)
  puts "Scraping page #{page_number}"

  page.parser.css('#filings tr:gt(1)').each do |tr|
    scraped += 1
    br = tr.css('br')
    ##a = tds[0].at_css('a')
    company_name = tds[1].text.strip
    location = tds[2].text.strip
    entity_type = tds[3].text.strip
    company_number = tds[4].text.strip
    record = {
      'CompanyName'   => company_name,
      'Location'      => location,
      'EntityType'   => entity_type,
      'CompanyNumber' => company_number
      ##'RegistryUrl'   => a[:href]
    }
    begin
      ScraperWiki.save(['CompanyNumber'], record)
      saved += 1
    rescue Timeout::Error => e
      puts "ERROR: #{e.inspect} during save(#{record.inspect})"
      retry
    end
  end
  if scraped != saved
    puts "WARNING: Missed #{scraped - saved} records!"
  end
  if scraped % 20 != 0
    puts "WARNING: Didn't scrape all records (#{scraped})!"
  end
end
 
##Mechanize.html_parser = Nokogiri::HTML
agent = Mechanize.new
agent.user_agent_alias = 'Linux Firefox'

page = agent.get('http://www.oera.li/hrweb/eng/Suchformular.htm')
page.form['Name'] = 'her'
s = page.form('form1')
page = agent.submit(s)

extract page

require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'
 
def submit(page)
  page.forms[0].submit
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during submit"
  retry
end

def extract(page)
  scraped = 0
  saved = 0

  page_number = 1
  save_metadata('page_number', page_number)
  puts "Scraping page #{page_number}"

  page.parser.css('#filings tr:gt(1)').each do |tr|
    scraped += 1
    br = tr.css('br')
    ##a = tds[0].at_css('a')
    company_name = tds[1].text.strip
    location = tds[2].text.strip
    entity_type = tds[3].text.strip
    company_number = tds[4].text.strip
    record = {
      'CompanyName'   => company_name,
      'Location'      => location,
      'EntityType'   => entity_type,
      'CompanyNumber' => company_number
      ##'RegistryUrl'   => a[:href]
    }
    begin
      ScraperWiki.save(['CompanyNumber'], record)
      saved += 1
    rescue Timeout::Error => e
      puts "ERROR: #{e.inspect} during save(#{record.inspect})"
      retry
    end
  end
  if scraped != saved
    puts "WARNING: Missed #{scraped - saved} records!"
  end
  if scraped % 20 != 0
    puts "WARNING: Didn't scrape all records (#{scraped})!"
  end
end
 
##Mechanize.html_parser = Nokogiri::HTML
agent = Mechanize.new
agent.user_agent_alias = 'Linux Firefox'

page = agent.get('http://www.oera.li/hrweb/eng/Suchformular.htm')
page.form['Name'] = 'her'
s = page.form('form1')
page = agent.submit(s)

extract page

