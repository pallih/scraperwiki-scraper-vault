require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

#ScraperWiki.sqliteexecute('create INDEX date_scraped_index on swdata (date_scraped);')
#exit
# ScraperWiki.save_var('prefix','A5M')
#ScraperWiki.sqliteexecute('UPDATE swdata SET Status = NULL;')
#ScraperWiki.commit

# ScraperWiki.save_var('register','Existing')

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://www.cro.ie/'
REGISTERS = %w(Existing Previous) 
ALPHA_PLUS_DIGITS = ("A".."Z").to_a + ("0".."9").to_a
@starting_url = BASE_URL + 'search/CompanySearch.aspx'


# scrape_table function: gets passed an individual page to scrape
def scrape_table(page_body, register)
  doc = Nokogiri::HTML(page_body)
  return if doc.at('#labelResultsMessage').inner_text.match(/More than 500 rows/) # to trigger increase in prefix size
  return true unless data_rows = doc.css('table#GridView1 tr')[1..-1] # silently skip if no results
  data_table = data_rows.collect do |row|
    record = {}
    address = row.css('td')[2].inner_text.strip
    record['CompanyName']   = row.css('td')[0].inner_text.strip
    record['CompanyNumber']     = row.css('td')[1].inner_text.strip
    # record['Status']     = (register == 'Previous' ? 'Dissolved' : 'Active') . # we can't trust status
    record['RegisteredAddress'] = address.match(/NO ADDRESS/) ? nil : address 
    record['date_scraped'] = Time.now
    ScraperWiki.save(["CompanyNumber"], record)
  end
end
        
# Scrape page
def get_results_and_extract_data_for(prefix, register)
  sleep 2 # give their server a break
  get_start_page if @refetch_start_page
  puts "Searching for #{register} companies with prefix '#{prefix}'"
  @page.form_with(:name => 'form1') do |f|
    f.radiobutton_with(:name=>'radioSearchFor', :value=>'C').check
    f.radiobutton_with(:name=>'radioSearchOptions', :value=>'2').check
    f.radiobutton_with(:name=>'radioExPrevious', :value=>register).check
    f['Button1'] = 'Search'
    f['textAlphaSort'] = prefix
    @page = f.submit
  end
  unless scrape_table(@page.body, register)
    ALPHA_PLUS_DIGITS.each{|letter| get_results_and_extract_data_for(prefix + letter, register) }
  end
  @refetch_start_page = false
  @consec_error_count = 0 # reset if we're getting info ok
rescue Exception, Timeout::Error => e
  @consec_error_count += 1
  puts "xxxxxx An error occured (happened #{@consec_error_count} times, sleeping now for #{(60 * @consec_error_count)} seconds): #{e.inspect}#{e.backtrace} (happened #{@consec_error_count} times)"
  sleep (60 * @consec_error_count)
  exit if @consec_error_count > 4
  @refetch_start_page = true
  get_results_and_extract_data_for(prefix, register)
end

def get_start_page
  @page = @br.get(@starting_url) # get starting url again
end

# increments a string. like String#succ but includes 0..9, so ABZ increments to AB0 and AB9 to ACA. position is position from right, with 0 the rightmost
def increment_string(string, given_position=0)
  chars = string.chars.to_a
  position = -1 - given_position
  char_to_increment = chars[position]
  incremented_char = char_to_increment&&char_to_increment.succ #if nil it's because we need to add a new char at the front of the array
  case incremented_char
  when 'AA'
    chars[position] = '0'
  when '10'
    chars[position] = 'A'
    chars = increment_string(chars.join, given_position+1)
  when nil
    chars.unshift('A')
  else
    chars[position] = incremented_char
  end
  chars.is_a?(String) ? chars : chars.join
end

def run_from(prefix, register)
  consec_error_count = 0
  loop do
    ScraperWiki.save_var('prefix', prefix) # save before getting results, so we start back here if scraper killed/fails
    get_results_and_extract_data_for(prefix, register)
    if prefix == '999'
      #register = (register ==  REGISTERS.first ? REGISTERS.last : REGISTERS.first)
      #ScraperWiki.save_var('register', register)
      prefix = 'AAA'
    else
      prefix = increment_string(prefix)
    end
  end
end

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

prefix = ScraperWiki.get_var('prefix', 'AAA')
#register = ScraperWiki.get_var('register', REGISTERS.first)
register = "Existing"
@consec_error_count = 0

@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
}
# get first page to pick up cookies etc
get_start_page

run_from(prefix, register)
require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

#ScraperWiki.sqliteexecute('create INDEX date_scraped_index on swdata (date_scraped);')
#exit
# ScraperWiki.save_var('prefix','A5M')
#ScraperWiki.sqliteexecute('UPDATE swdata SET Status = NULL;')
#ScraperWiki.commit

# ScraperWiki.save_var('register','Existing')

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://www.cro.ie/'
REGISTERS = %w(Existing Previous) 
ALPHA_PLUS_DIGITS = ("A".."Z").to_a + ("0".."9").to_a
@starting_url = BASE_URL + 'search/CompanySearch.aspx'


# scrape_table function: gets passed an individual page to scrape
def scrape_table(page_body, register)
  doc = Nokogiri::HTML(page_body)
  return if doc.at('#labelResultsMessage').inner_text.match(/More than 500 rows/) # to trigger increase in prefix size
  return true unless data_rows = doc.css('table#GridView1 tr')[1..-1] # silently skip if no results
  data_table = data_rows.collect do |row|
    record = {}
    address = row.css('td')[2].inner_text.strip
    record['CompanyName']   = row.css('td')[0].inner_text.strip
    record['CompanyNumber']     = row.css('td')[1].inner_text.strip
    # record['Status']     = (register == 'Previous' ? 'Dissolved' : 'Active') . # we can't trust status
    record['RegisteredAddress'] = address.match(/NO ADDRESS/) ? nil : address 
    record['date_scraped'] = Time.now
    ScraperWiki.save(["CompanyNumber"], record)
  end
end
        
# Scrape page
def get_results_and_extract_data_for(prefix, register)
  sleep 2 # give their server a break
  get_start_page if @refetch_start_page
  puts "Searching for #{register} companies with prefix '#{prefix}'"
  @page.form_with(:name => 'form1') do |f|
    f.radiobutton_with(:name=>'radioSearchFor', :value=>'C').check
    f.radiobutton_with(:name=>'radioSearchOptions', :value=>'2').check
    f.radiobutton_with(:name=>'radioExPrevious', :value=>register).check
    f['Button1'] = 'Search'
    f['textAlphaSort'] = prefix
    @page = f.submit
  end
  unless scrape_table(@page.body, register)
    ALPHA_PLUS_DIGITS.each{|letter| get_results_and_extract_data_for(prefix + letter, register) }
  end
  @refetch_start_page = false
  @consec_error_count = 0 # reset if we're getting info ok
rescue Exception, Timeout::Error => e
  @consec_error_count += 1
  puts "xxxxxx An error occured (happened #{@consec_error_count} times, sleeping now for #{(60 * @consec_error_count)} seconds): #{e.inspect}#{e.backtrace} (happened #{@consec_error_count} times)"
  sleep (60 * @consec_error_count)
  exit if @consec_error_count > 4
  @refetch_start_page = true
  get_results_and_extract_data_for(prefix, register)
end

def get_start_page
  @page = @br.get(@starting_url) # get starting url again
end

# increments a string. like String#succ but includes 0..9, so ABZ increments to AB0 and AB9 to ACA. position is position from right, with 0 the rightmost
def increment_string(string, given_position=0)
  chars = string.chars.to_a
  position = -1 - given_position
  char_to_increment = chars[position]
  incremented_char = char_to_increment&&char_to_increment.succ #if nil it's because we need to add a new char at the front of the array
  case incremented_char
  when 'AA'
    chars[position] = '0'
  when '10'
    chars[position] = 'A'
    chars = increment_string(chars.join, given_position+1)
  when nil
    chars.unshift('A')
  else
    chars[position] = incremented_char
  end
  chars.is_a?(String) ? chars : chars.join
end

def run_from(prefix, register)
  consec_error_count = 0
  loop do
    ScraperWiki.save_var('prefix', prefix) # save before getting results, so we start back here if scraper killed/fails
    get_results_and_extract_data_for(prefix, register)
    if prefix == '999'
      #register = (register ==  REGISTERS.first ? REGISTERS.last : REGISTERS.first)
      #ScraperWiki.save_var('register', register)
      prefix = 'AAA'
    else
      prefix = increment_string(prefix)
    end
  end
end

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

prefix = ScraperWiki.get_var('prefix', 'AAA')
#register = ScraperWiki.get_var('register', REGISTERS.first)
register = "Existing"
@consec_error_count = 0

@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
}
# get first page to pick up cookies etc
get_start_page

run_from(prefix, register)
