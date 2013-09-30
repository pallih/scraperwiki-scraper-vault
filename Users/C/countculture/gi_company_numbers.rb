require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://www.companieshouse.gi/4DCGI/Verify'

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page_body)
  return unless data_table = Nokogiri::HTML(page_body).css('table[@cellpadding="2"] tr')[1..-1]
  data_table.collect do |row|
    tds = row.css('td')
    next unless tds.first.inner_text.match(/Company/)
    record = {}
    record['CompanyNumber'] = stripped_inner_text(tds[1])
    record['CompanyName']   = stripped_inner_text(tds[2])
    record['Status']        = stripped_inner_text(tds[3])
    record['LastAnnualReturnDate'] = stripped_inner_text(tds[5])
    record['CompanyType']   = stripped_inner_text(tds[6])
    record['date_scraped']   = Time.now
    next if record['CompanyName'].match(/\(Former Name\)|^VOID/)
    begin
      ScraperWiki.save(["CompanyNumber"], record)
    rescue Exception=>e
      puts "Exception (#{e.inspect}) raised saving company record:#{record.inspect}"
    end
  end
end
        
# Scrape page
def get_results_and_extract_data_for(term)
  @page = @br.post('http://www.companieshouse.gi/4DCGI/NSearch', 'OK'=>'Search','VNAME'=>term)
  scrape_table(@page.body)
#rescue Exception => e
  #puts "Exception raised while getting data: #{e.inspect}\n#{e.backtrace}"
rescue Timeout::Error => e #timeout errors all too common, but as this is being run daily, don't worry about missing a few entries
  puts "Timeout exception raised while getting data: #{e.inspect}"
  raise e unless @catch_timeout_errors
end

def stripped_inner_text(td_element)
  return unless td_element
  td_element.inner_text.strip.gsub(/&nbsp/,'')
end

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

# @catch_timeout_errors = true #server seems to run out of steam and throw lots of Timeout::Error halfway through run so we don't necessarily want to catch them

# starting_url = BASE_URL + 'search/CompanySearch.aspx'
@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
}


# get first page to pick up cookies etc
@br.post(BASE_URL,'OK'=>'Enter') # verify with no credentials

initial_first_letter = ScraperWiki.get_var('first_letter', '0')
initial_middle_letter = ScraperWiki.get_var('middle_letter', '0')

initial_first_letter, initial_middle_letter = ['0','0'] if [initial_first_letter, initial_middle_letter] == ['9','9']
(initial_first_letter..'9').each do |first_letter|
  (initial_middle_letter..'9').each do |middle_letter|
    begin
      letters = first_letter + middle_letter
      get_results_and_extract_data_for(letters)
      puts "\nFinished getting details for '#{letters}'\n"
    rescue Exception => e
      puts "Exception raised while getting data for #{letters}: #{e.inspect}"
    rescue Timeout::Error => e #timeout errors all too common, but as this is being run daily, don't worry about missing a few entries
      puts "Timeout::Error raised while getting data for #{letters}: #{e.inspect}"
      raise e #unless @catch_timeout_errors
    end
    ScraperWiki.save_var('middle_letter', middle_letter)
    initial_middle_letter = '0' if middle_letter == '9'
  end
  ScraperWiki.save_var('first_letter', first_letter)
end
require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://www.companieshouse.gi/4DCGI/Verify'

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page_body)
  return unless data_table = Nokogiri::HTML(page_body).css('table[@cellpadding="2"] tr')[1..-1]
  data_table.collect do |row|
    tds = row.css('td')
    next unless tds.first.inner_text.match(/Company/)
    record = {}
    record['CompanyNumber'] = stripped_inner_text(tds[1])
    record['CompanyName']   = stripped_inner_text(tds[2])
    record['Status']        = stripped_inner_text(tds[3])
    record['LastAnnualReturnDate'] = stripped_inner_text(tds[5])
    record['CompanyType']   = stripped_inner_text(tds[6])
    record['date_scraped']   = Time.now
    next if record['CompanyName'].match(/\(Former Name\)|^VOID/)
    begin
      ScraperWiki.save(["CompanyNumber"], record)
    rescue Exception=>e
      puts "Exception (#{e.inspect}) raised saving company record:#{record.inspect}"
    end
  end
end
        
# Scrape page
def get_results_and_extract_data_for(term)
  @page = @br.post('http://www.companieshouse.gi/4DCGI/NSearch', 'OK'=>'Search','VNAME'=>term)
  scrape_table(@page.body)
#rescue Exception => e
  #puts "Exception raised while getting data: #{e.inspect}\n#{e.backtrace}"
rescue Timeout::Error => e #timeout errors all too common, but as this is being run daily, don't worry about missing a few entries
  puts "Timeout exception raised while getting data: #{e.inspect}"
  raise e unless @catch_timeout_errors
end

def stripped_inner_text(td_element)
  return unless td_element
  td_element.inner_text.strip.gsub(/&nbsp/,'')
end

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

# @catch_timeout_errors = true #server seems to run out of steam and throw lots of Timeout::Error halfway through run so we don't necessarily want to catch them

# starting_url = BASE_URL + 'search/CompanySearch.aspx'
@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
}


# get first page to pick up cookies etc
@br.post(BASE_URL,'OK'=>'Enter') # verify with no credentials

initial_first_letter = ScraperWiki.get_var('first_letter', '0')
initial_middle_letter = ScraperWiki.get_var('middle_letter', '0')

initial_first_letter, initial_middle_letter = ['0','0'] if [initial_first_letter, initial_middle_letter] == ['9','9']
(initial_first_letter..'9').each do |first_letter|
  (initial_middle_letter..'9').each do |middle_letter|
    begin
      letters = first_letter + middle_letter
      get_results_and_extract_data_for(letters)
      puts "\nFinished getting details for '#{letters}'\n"
    rescue Exception => e
      puts "Exception raised while getting data for #{letters}: #{e.inspect}"
    rescue Timeout::Error => e #timeout errors all too common, but as this is being run daily, don't worry about missing a few entries
      puts "Timeout::Error raised while getting data for #{letters}: #{e.inspect}"
      raise e #unless @catch_timeout_errors
    end
    ScraperWiki.save_var('middle_letter', middle_letter)
    initial_middle_letter = '0' if middle_letter == '9'
  end
  ScraperWiki.save_var('first_letter', first_letter)
end
