require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

def get_metadata(key, default)
  ScraperWiki.get_metadata(key, default)
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
  retry
end

def save_metadata(key, value)
  ScraperWiki.save_metadata(key, value)
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
  retry
end

def submit(page)
  page.forms[0].submit
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during submit"
  retry
end

def extract(page)
  scraped = 0
  saved = 0

  page_number = page.forms[0]['ctl00$contentMain$txtHeaderCurrentPage']
  save_metadata('page_number', page_number)
  puts "Scraping page #{page_number}"

  page.parser.css('#filings tr:gt(1)').each do |tr|
    scraped += 1
    tds = tr.css('td')
    a = tds[0].at_css('a')
    record = {
      'CompanyNumber' => a.text.strip,
      'RegistryUrl'   => 'https://wyobiz.wy.gov/Business/' + a[:href],
      'EntityType'    => tds[1].text.strip,
      'CompanyName'   => tds[2].text.strip,
      'FilingDate'    => tds[3].text.strip,
      'Status'        => tds[4].text.strip,
      'TaxStanding'   => tds[5].text.strip,
      'RAStanding'    => tds[6].text.strip,
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

  # Advance to the next page, or restart.
  if page.parser.at_css('#ctl00_contentMain_lbtnNextHeader')
    page.forms[0]['__EVENTTARGET'] = 'ctl00$contentMain$lbtnNextHeader'
    extract submit(page)
  else
    save_metadata('page_number', '1')
  end
end

Mechanize.html_parser = Nokogiri::HTML
agent = Mechanize.new do |b|
  b.user_agent_alias = 'Mac Safari'
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
end

# Searching for punctuation returns all records!
page = agent.get 'https://wyobiz.wy.gov/Business/FilingSearch.aspx'
page.forms[0]['ctl00$contentMain$txtFilingName'] = '.'
page.forms[0]['ctl00$contentMain$searchOpt'] = 'chkSearchStartWith'
page.forms[0]['ctl00$contentMain$cmdSearch'] = 'Search'

# Resume from last visited page.
page_number = get_metadata('page_number', '1')
puts "Starting on page #{page_number}"

if page_number != '1'
  page = submit(page)
  page.forms[0]['ctl00$contentMain$txtHeaderCurrentPage'] = page_number
  page.forms[0]['__EVENTTARGET'] = 'ctl00$contentMain$txtHeaderCurrentPage'
end

extract submit(page)

