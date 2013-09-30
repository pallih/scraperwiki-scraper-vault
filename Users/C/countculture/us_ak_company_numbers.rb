require 'rubygems'
require 'open-uri'
require 'nokogiri'
require 'mechanize'

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

Mechanize.html_parser = Nokogiri::HTML
agent = Mechanize.new do |b|
  b.user_agent_alias = 'Mac Safari'
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
end

offset = get_metadata('offset', 0).to_i
puts "Starting at offset #{offset}"

scraped = 0
saved = 0

while 1
  puts "Scraping offset #{offset}"

  begin
    page = agent.get("https://myalaska.state.ak.us/business/soskb/SearchResults.asp?FormName=CorpNameSearch&Words=Starting&SearchStr=&TopRec=#{offset}&Pos=Next%2050%20%3E%3E")
  rescue Timeout::Error => e
    puts "ERROR: #{e.inspect} during scrape(\"https://myalaska.state.ak.us/business/soskb/SearchResults.asp?FormName=CorpNameSearch&Words=Starting&SearchStr=&TopRec=#{offset}&Pos=Next%2050%20%3E%3E\")"
    retry
  end

  page.parser.css('table table table td:not([align]) table tr:gt(3)').each do |tr|
    scraped += 1
    # Company Number is sometimes empty!
    a = tr.at_css('td:eq(1) a')
    company_name = a.text.strip.sub(/DBA.+$/,'') # strip out trading names
    record = {
      'CompanyNumber' => tr.at_css('td:eq(2)').text.strip,
      'RegistryUrl'   => 'https://myalaska.state.ak.us/business/soskb/' + a[:href],
      'CompanyName'   => company_name,
      'EntityType'    => tr.at_css('td:eq(3)').text.strip,
      'Status'        => tr.at_css('td:eq(4)').text.strip,
      'IncorporationDate'  => tr.at_css('td:eq(5)').text.strip,
      'EntityID'      => a[:href][/\d+\Z/],
    }
    begin
      ScraperWiki.save(['EntityID'], record)
      saved += 1
    rescue Timeout::Error => e
      puts "ERROR: #{e.inspect} during save(#{record.inspect})"
      retry
    end
  end

  if scraped != saved
    puts "WARNING: Missed #{scraped - saved} records!"
  end
  if scraped % 50 != 0
    puts "WARNING: Didn't scrape all records (#{scraped})!"
  end

  if page.parser.at_css('input[value="Next 50 >>"]')
    offset += 50
    save_metadata('offset', offset)
  else
    save_metadata('offset', 0)
    break
  end
end
require 'rubygems'
require 'open-uri'
require 'nokogiri'
require 'mechanize'

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

Mechanize.html_parser = Nokogiri::HTML
agent = Mechanize.new do |b|
  b.user_agent_alias = 'Mac Safari'
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
end

offset = get_metadata('offset', 0).to_i
puts "Starting at offset #{offset}"

scraped = 0
saved = 0

while 1
  puts "Scraping offset #{offset}"

  begin
    page = agent.get("https://myalaska.state.ak.us/business/soskb/SearchResults.asp?FormName=CorpNameSearch&Words=Starting&SearchStr=&TopRec=#{offset}&Pos=Next%2050%20%3E%3E")
  rescue Timeout::Error => e
    puts "ERROR: #{e.inspect} during scrape(\"https://myalaska.state.ak.us/business/soskb/SearchResults.asp?FormName=CorpNameSearch&Words=Starting&SearchStr=&TopRec=#{offset}&Pos=Next%2050%20%3E%3E\")"
    retry
  end

  page.parser.css('table table table td:not([align]) table tr:gt(3)').each do |tr|
    scraped += 1
    # Company Number is sometimes empty!
    a = tr.at_css('td:eq(1) a')
    company_name = a.text.strip.sub(/DBA.+$/,'') # strip out trading names
    record = {
      'CompanyNumber' => tr.at_css('td:eq(2)').text.strip,
      'RegistryUrl'   => 'https://myalaska.state.ak.us/business/soskb/' + a[:href],
      'CompanyName'   => company_name,
      'EntityType'    => tr.at_css('td:eq(3)').text.strip,
      'Status'        => tr.at_css('td:eq(4)').text.strip,
      'IncorporationDate'  => tr.at_css('td:eq(5)').text.strip,
      'EntityID'      => a[:href][/\d+\Z/],
    }
    begin
      ScraperWiki.save(['EntityID'], record)
      saved += 1
    rescue Timeout::Error => e
      puts "ERROR: #{e.inspect} during save(#{record.inspect})"
      retry
    end
  end

  if scraped != saved
    puts "WARNING: Missed #{scraped - saved} records!"
  end
  if scraped % 50 != 0
    puts "WARNING: Didn't scrape all records (#{scraped})!"
  end

  if page.parser.at_css('input[value="Next 50 >>"]')
    offset += 50
    save_metadata('offset', offset)
  else
    save_metadata('offset', 0)
    break
  end
end
