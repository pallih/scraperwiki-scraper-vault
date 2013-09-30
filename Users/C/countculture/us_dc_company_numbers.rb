require 'rubygems'
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://mblr.dc.gov/corp/lookup/'

# scrape_table function: gets passed an individual page to scrape
def scrape_table(url)
  doc = Nokogiri::HTML(open(url))
  data_table = doc.css('#aForm tr')[1..-1].collect do |row|
    record = {}
    tds = row.css('td')
    record['CompanyName']   = tds[1].at('a').inner_text.strip
    record['CompanyNumber'] = row.css('td')[4].inner_text.strip
    record['RegistryUrl'] = BASE_URL + tds[1].at('a')[:href]
    record['date_scraped'] = Time.now
    next unless record['CompanyNumber']
    ScraperWiki.save(["CompanyNumber"], record)
  end
  rescue Exception, Timeout::Error => e
  puts "Exception raised while getting or parsing data: #{e.inspect}"
end
        
# Scrape page
def get_results_and_extract_data_for(letter)
  start_page_number = ScraperWiki.get_var('page_number', 0)
  url = BASE_URL + "results.asp?algorithm=mtphn1&rec_limit=&search_type=1&clp_mod=2&keywords=#{letter}&page=0"
  end_page_number = Nokogiri::HTML(open(url)).at('#aForm div.default_div img[src*="rr-arrows.gif"]').parent[:href].scan(/page=(\d+)/).to_s.to_i rescue 0
  puts "About to start getting data for companies beginning with #{letter}, pages #{start_page_number}-#{end_page_number}"
  (start_page_number..end_page_number).each do |page_number|
    url = BASE_URL + "results.asp?algorithm=mtphn1&rec_limit=&search_type=1&clp_mod=2&keywords=#{letter}&page=" + page_number.to_s
    scrape_table(open(url))
    ScraperWiki.save_var('page_number', page_number) # save page_number in case scraper gets killed
  end
rescue Exception, Timeout::Error => e #timeout errors all too common, but as this is being run daily, don't worry about missing a few entries
  puts "Exception raised while getting data: #{e.inspect}"
end

# This is where the script proper starts

initial_chars = (0..9).to_a + ('A'..'Z').to_a
start_position = initial_chars.index ScraperWiki.get_var('letter', 0)

initial_chars[start_position..-1].each do |letter|
  begin
    get_results_and_extract_data_for(letter)
    puts "\nFinished getting details for companies beginning with '#{letter}'\n"
  rescue Exception, Timeout::Error => e #timeout errors all too common, but as this is being run daily, don't worry about missing a few entries
    puts "Exception raised while getting first page of search: #{e.inspect}"
  end
  ScraperWiki.save_var('page_number', 0) # reset page number
  meta_data_letter = (letter == 'Z') ? 0 : letter #reset to beginning if we get to end
  ScraperWiki.save_var('letter', meta_data_letter) # save letter in case scraper gets killed
end
require 'rubygems'
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://mblr.dc.gov/corp/lookup/'

# scrape_table function: gets passed an individual page to scrape
def scrape_table(url)
  doc = Nokogiri::HTML(open(url))
  data_table = doc.css('#aForm tr')[1..-1].collect do |row|
    record = {}
    tds = row.css('td')
    record['CompanyName']   = tds[1].at('a').inner_text.strip
    record['CompanyNumber'] = row.css('td')[4].inner_text.strip
    record['RegistryUrl'] = BASE_URL + tds[1].at('a')[:href]
    record['date_scraped'] = Time.now
    next unless record['CompanyNumber']
    ScraperWiki.save(["CompanyNumber"], record)
  end
  rescue Exception, Timeout::Error => e
  puts "Exception raised while getting or parsing data: #{e.inspect}"
end
        
# Scrape page
def get_results_and_extract_data_for(letter)
  start_page_number = ScraperWiki.get_var('page_number', 0)
  url = BASE_URL + "results.asp?algorithm=mtphn1&rec_limit=&search_type=1&clp_mod=2&keywords=#{letter}&page=0"
  end_page_number = Nokogiri::HTML(open(url)).at('#aForm div.default_div img[src*="rr-arrows.gif"]').parent[:href].scan(/page=(\d+)/).to_s.to_i rescue 0
  puts "About to start getting data for companies beginning with #{letter}, pages #{start_page_number}-#{end_page_number}"
  (start_page_number..end_page_number).each do |page_number|
    url = BASE_URL + "results.asp?algorithm=mtphn1&rec_limit=&search_type=1&clp_mod=2&keywords=#{letter}&page=" + page_number.to_s
    scrape_table(open(url))
    ScraperWiki.save_var('page_number', page_number) # save page_number in case scraper gets killed
  end
rescue Exception, Timeout::Error => e #timeout errors all too common, but as this is being run daily, don't worry about missing a few entries
  puts "Exception raised while getting data: #{e.inspect}"
end

# This is where the script proper starts

initial_chars = (0..9).to_a + ('A'..'Z').to_a
start_position = initial_chars.index ScraperWiki.get_var('letter', 0)

initial_chars[start_position..-1].each do |letter|
  begin
    get_results_and_extract_data_for(letter)
    puts "\nFinished getting details for companies beginning with '#{letter}'\n"
  rescue Exception, Timeout::Error => e #timeout errors all too common, but as this is being run daily, don't worry about missing a few entries
    puts "Exception raised while getting first page of search: #{e.inspect}"
  end
  ScraperWiki.save_var('page_number', 0) # reset page number
  meta_data_letter = (letter == 'Z') ? 0 : letter #reset to beginning if we get to end
  ScraperWiki.save_var('letter', meta_data_letter) # save letter in case scraper gets killed
end
