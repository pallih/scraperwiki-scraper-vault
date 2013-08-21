#############################################
# A Scraper for Incorporations, Cooperatives, Banks and Insurance Companies in the state of Arkansas.
#
# SOURCE: http://www.sos.arkansas.gov/corps/search_corps.php
#############################################

require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

SEARCH_BASE = 'http://www.sos.arkansas.gov/corps/search_corps.php'
DETAIL_BASE = 'http://www.sos.arkansas.gov/corps/'

# Names of the values stored on the page
COLUMNS = ['Corporation Name', 'Fictitious Names', 'Filing #', 'Filing Type', 'Filed under Act', 'Status', 'Principal Address', 'Reg. Agent', 'Agent Address', 'Date Filed', 'Officers', 'Foreign Name', 'Foreign Address', 'State of Origin']

## Variable Names
TYPE_ID = 'type_id' # From the 'Corporation Type' drop down
PAGE    = 'page'    # A page number for the search results
INDEX   = 'index'   # An index into the search results page
ERROR_COUNT = 'error_count'

#ScraperWiki.save_var(TYPE_ID, 1)
#ScraperWiki.save_var(PAGE, 4)
#ScraperWiki.save_var(INDEX, 0)

# Create a table to store result links
if ScraperWiki.show_tables()['links'] == nil
  ScraperWiki.sqliteexecute("CREATE TABLE links (link STRING PRIMARY KEY)")
end

# Load the company details of all the companies of a particular type
def load(agent, type_id)
  page = ScraperWiki.get_var(PAGE, 0)
  url = SEARCH_BASE + "?SEARCH=1&run=#{page}&corp_type_id=#{type_id}"
  puts url

  # Finish loading and processing current results
  results_page = agent.get(url)
  reset_error_count()
  load_results(results_page)
  process_results(agent)

  # Move on to the next page
  while results_page.link_with(:href => /^search_corps\.php\?SEARCH/, :text => /^Next/)
    puts "Next"
    page = page + 1
    ScraperWiki.save_var(PAGE, page)

    # Load and process results
    results_page = results_page.link_with(:href => /^search_corps\.php\?SEARCH/, :text => /^Next/).click
    load_results(results_page)
    process_results(agent)
  end

  page = 0  # Reset page to 0
  ScraperWiki.save_var(PAGE, page)
end

# Loads all the detail page links for the given results page.
# Uses the INDEX variable to prevent duplicate work for a given page.
def load_results(results_page)
  puts "load results"

  # Get all the links on the page
  links = results_page.links_with(:href => /^search_corps\.php\?DETAIL/)

  # Get the index of the last loaded link, or 0
  index = ScraperWiki.get_var(INDEX, 0)

  # Finish loading the rest of the links onthe page
  while index < links.length   
    link = DETAIL_BASE + links[index].href
    puts "load link " + link

    # Load the current link
    begin
      ScraperWiki.sqliteexecute("INSERT INTO links (link) VALUES (?)", [link])
      ScraperWiki.commit()
    rescue Exception => e
      puts "Exception (#{e.inspect}) raised saving record #{link}"
    end

    # Increment and save the index
    index = index + 1
    ScraperWiki.save_var(INDEX, index)
  end
end

# Loads the details of a particular company from it's detail page
# Assumes details are stored in a two column, table layout
def load_details(agent, url)
  puts "load details - " + url

  details_page = agent.get(url)
  page = Nokogiri::HTML(details_page.body)

  record = Hash.new
  record['Link'] = url
  
  # For each row in the table, if the first column has one of the expected keys
  # get the value from the second column and add it to the record
  page.css('table tr').collect {|x| x.css('td')}.each do | row |
    key = row[0].content.strip if row[0]
    val = row[1].content.strip if row[1]
    if COLUMNS.include?(key)
      if key == 'Filing #' # Modify key for storage in db
        key = 'Filing Number'
      end
      record[key] = val
    end
  end

  # Map the expected columns to opencorporates standard
  record['CompanyName']   = record['Corporation Name']
  record['CompanyNumber'] = record['Filing Number']
  #record['Status']        = record['Status']
  record['EntityType']    = record['Filing Type']
  record['RegistryUrl']   = record['Link']
  record['DateScraped']   = Time.now

  puts record.to_yaml

  # Save the record
  begin
    ScraperWiki.save_sqlite(unique_keys=['Filing Number'], record)
  rescue Exception => e
    puts "Exception (#{e.inspect}) raised saving record #{record.inspect}"
  end
end

# Removes a link from the link table
def delete_link(link)
  puts "Removing link: " + link
  ScraperWiki.sqliteexecute("DELETE FROM links WHERE link = '#{link}'")
  ScraperWiki.commit()
end

# Loads the details for each link in the link table, then removes the link
def process_results(agent)
  links = ScraperWiki.select("link FROM links")
  links.collect{ |x| x['link'] }.each do | link |
    load_details(agent, link)
    delete_link(link)
    sleep 10
  end
  ScraperWiki.save_var(INDEX, 0)
end

def reset_error_count()
  ScraperWiki.save_var(ERROR_COUNT, 0)
end

##################
## Start Here
##################

puts "Starting Load"
agent = Mechanize.new

# Restore/Initialize state
type_id = ScraperWiki.get_var(TYPE_ID, 1)
reset_error_count()

# For each company type
while type_id <= 31

  begin 

    # Load info for type
    load(agent, type_id)

    # Move on to next type
    type_id = type_id + 1 
    ScraperWiki.save_var(TYPE_ID, type_id)

  rescue Exception, Timeout::Error => e
      error_count = 0
    begin
      error_count = ScraperWiki.get_var(ERROR_COUNT, 0)
      puts "xxxxxxxxxxxxxxxxx\nAn error occured #{error_count} times: #{e.inspect}\n#{e.backtrace}"
      # Stop if error happens five times in a row
      break if error_count == 5
      error_count = error_count + 1
      ScraperWiki.save_var(ERROR_COUNT, error_count)
    rescue Exception => e
      puts "xxxxxxxxxxxxxxxxx\nA ScraperWiki error occured: #{e.inspect}\n#{e.backtrace}"
    end
    sleep (error_count + 1) * 60
  end

end 

if type_id > 31
  ScraperWiki.save_var(TYPE_ID, 1) # Reset type to 1
  ScraperWiki.save_var(PAGE, 0)    # Reset page to 0
end

puts "Done!"
