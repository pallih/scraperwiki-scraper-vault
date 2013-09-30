######################################
# Business entity search for the state of Georgia 
#
# SOURCE: http://corp.sos.state.ga.us/corp/soskb/
######################################

require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

URL_BASE = 'http://corp.sos.state.ga.us/corp/soskb/'

# Names of the columns on a searc results page
COLUMNS = ['Business Entity Name', 'Control No', 'Type', 'Status', 'Entity Creation Date']

# An array of characters and numbers used for generating search terms
CHARACTERS = ('a'..'z').to_a + ('0'..'9').to_a

#ScraperWiki.save_var('term', 'aaa')
#ScraperWiki.save_var('add', '')
#ScraperWiki.save_var('t2', '')
#ScraperWiki.save_var('t1', '')

# Load all of the results for a given search url
# This could timeout if there are too many results
def search_and_load(start_url)
  agent = Mechanize.new
  puts start_url

  # Initialize results page
  results_page = agent.get(start_url)

  # Load the results for that page
  load_results(results_page)

  # Get the 'Next' button if it exists
  form = results_page.forms.first
  buttons = form ? form.buttons_with(:value => /Next/) : []

  # While there are more pages
  while buttons.length > 0
    puts "Next"

    # Get the next results page
    results_page = agent.submit(form, buttons.first)

    # Load the results for that page
    load_results(results_page)

    # Get the 'Next' button if it exists
    form = results_page.forms.first
    buttons = form ? form.buttons_with(:value => /Next/) : []
  end
end

# Load each results company information
def load_results(results_page)
  puts "load results"
  page = Nokogiri::HTML(results_page.body)

  # For each row in the table
  page.css('table tr').collect { |x| x.css('td') }.reject{ |x|

    # Don't do anything, if the row is not a properly formatted result
    x.length == 0 or x.length != COLUMNS.size() or x.css('td')[0].css('a').length != 1 or
    not x.css('td')[0].css('a')[0]['href'].include?('Corp.asp?')

  }.each do | row | # These rows should all be properly formatted

    record = Hash.new

    # the link is in the first columns 'a' tag
    record['Link'] = URL_BASE + row.css('td')[0].css('a')[0]['href']

    # Set the key/value pair for each column in the table
    (0..COLUMNS.size()-1).each do |i|
      record[COLUMNS[i]] = row.css('td')[i].inner_text.strip
    end

    # Map the expected columns to opencorporates standard
    record['CompanyName']   = record['Business Entity Name']
    record['CompanyNumber'] = record['Control No']
    #record['Status']        = record['Status']
    record['EntityType']    = record['Type']
    record['RegistryUrl']   = record['Link']
    record['DateScraped']   = Time.now

    puts record.to_yaml

    # Save the record
    begin
       ScraperWiki.save_sqlite(unique_keys=['Control No'], record)
    rescue Exception => e
       puts "Exception (#{e.inspect}) raised saving record #{record.inspect}"
    end
  end

end

# Given a term of the form [a-z0-9]+ produce the next term 
# in the sequence while maintaining the same length.
# In this case lower order positions are at the higher indexes
def increment_term(term)
  term = String.new(term) # Ruby doesn't pass by value

  # Reset to lowest possible value when ceiling is hit
  if term == '9' * term.length
    return 'a' * term.length
  end

  # Initialize index to that of lowest order position
  index = term.length-1

  # Increment the lowest order position
  term[index] = increment_char(term[index].chr)
  
  # Increment higher order positions when a lower order one hits the ceiling
  while index > 0 and term[index].chr == 'a'
   index = index - 1
   term[index] = increment_char(term[index].chr)
  end

  return term
end

# Increments a character to its next higher value, wraps at max
# For this scraper characters are in the range [a-z0-9] and rated 
# from low to high in that order
def increment_char(c)
  return CHARACTERS[ (CHARACTERS.index(c) + 1) % (CHARACTERS.length) ]
end

# Generate a search url
def get_search_url(search_term)
    args = "SearchResults.asp?FormName=CorpNameSearch&Words=Starting&SearchStr=#{search_term}&SearchType=Search"
    return URL_BASE + args
end

##################
## Start Here
##################

puts "Starting Load"

## Searching is not affected by spaces

# Initialize search term
term = ScraperWiki.get_var('term', 'aaa')
add  = ScraperWiki.get_var('add', '') # Additional letters for the search term
t1   = ScraperWiki.get_var('t1', '')  # Try 1
t2   = ScraperWiki.get_var('t2', '')  # Try 2

error_count = 0

# For each possible term
while term != '999'

  begin
 
    # Extend the term addition if the term/add combo has been tried multiple times
    if term + add == t1 and term + add == t2 and error_count == 0
      puts "Increment term addition"
      add = add + 'a'
      ScraperWiki.save_var('add', add)
    end

    # Search failed to complete, use additional letters 
    if add != ''
      puts "Search with term addition"
  
      # For each possible additional letter
      while add != '9'*add.length
        t2 = term + add if term + add == t1
        t1 = term + add
        ScraperWiki.save_var('t2', t2)
        ScraperWiki.save_var('t1', t1)

        # Download all results
        search_and_load(get_search_url(term + add))
        error_count = 0

        # Increment and save the addition
        add = increment_term(add)
        ScraperWiki.save_var('add', add)
      end

      # Reset addition, increment and save the search term
      add = ''
      term = increment_term(term)
      ScraperWiki.save_var('add', add)
      ScraperWiki.save_var('term', term)
    end

    t2 = term if term == t1
    t1 = term
    ScraperWiki.save_var('t2', t2)
    ScraperWiki.save_var('t1', t1)

    # Download all results
    search_and_load(get_search_url(term))
    error_count = 0

    # Increment and save the search term
    term = increment_term(term)
    ScraperWiki.save_var('term', term)

  rescue Exception, Timeout::Error => e
    puts "xxxxxxxxxxxxxxxxx\nAn error occured: #{e.inspect}\n#{e.backtrace}"

    # Stop if error happens twice in a row
    break if error_count == 1
    error_count = 1
    sleep 30
  end
end

# Reset term state
if term == '999' and add == ''
  ScraperWiki.save_var('term', 'aaa')
end
######################################
# Business entity search for the state of Georgia 
#
# SOURCE: http://corp.sos.state.ga.us/corp/soskb/
######################################

require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

URL_BASE = 'http://corp.sos.state.ga.us/corp/soskb/'

# Names of the columns on a searc results page
COLUMNS = ['Business Entity Name', 'Control No', 'Type', 'Status', 'Entity Creation Date']

# An array of characters and numbers used for generating search terms
CHARACTERS = ('a'..'z').to_a + ('0'..'9').to_a

#ScraperWiki.save_var('term', 'aaa')
#ScraperWiki.save_var('add', '')
#ScraperWiki.save_var('t2', '')
#ScraperWiki.save_var('t1', '')

# Load all of the results for a given search url
# This could timeout if there are too many results
def search_and_load(start_url)
  agent = Mechanize.new
  puts start_url

  # Initialize results page
  results_page = agent.get(start_url)

  # Load the results for that page
  load_results(results_page)

  # Get the 'Next' button if it exists
  form = results_page.forms.first
  buttons = form ? form.buttons_with(:value => /Next/) : []

  # While there are more pages
  while buttons.length > 0
    puts "Next"

    # Get the next results page
    results_page = agent.submit(form, buttons.first)

    # Load the results for that page
    load_results(results_page)

    # Get the 'Next' button if it exists
    form = results_page.forms.first
    buttons = form ? form.buttons_with(:value => /Next/) : []
  end
end

# Load each results company information
def load_results(results_page)
  puts "load results"
  page = Nokogiri::HTML(results_page.body)

  # For each row in the table
  page.css('table tr').collect { |x| x.css('td') }.reject{ |x|

    # Don't do anything, if the row is not a properly formatted result
    x.length == 0 or x.length != COLUMNS.size() or x.css('td')[0].css('a').length != 1 or
    not x.css('td')[0].css('a')[0]['href'].include?('Corp.asp?')

  }.each do | row | # These rows should all be properly formatted

    record = Hash.new

    # the link is in the first columns 'a' tag
    record['Link'] = URL_BASE + row.css('td')[0].css('a')[0]['href']

    # Set the key/value pair for each column in the table
    (0..COLUMNS.size()-1).each do |i|
      record[COLUMNS[i]] = row.css('td')[i].inner_text.strip
    end

    # Map the expected columns to opencorporates standard
    record['CompanyName']   = record['Business Entity Name']
    record['CompanyNumber'] = record['Control No']
    #record['Status']        = record['Status']
    record['EntityType']    = record['Type']
    record['RegistryUrl']   = record['Link']
    record['DateScraped']   = Time.now

    puts record.to_yaml

    # Save the record
    begin
       ScraperWiki.save_sqlite(unique_keys=['Control No'], record)
    rescue Exception => e
       puts "Exception (#{e.inspect}) raised saving record #{record.inspect}"
    end
  end

end

# Given a term of the form [a-z0-9]+ produce the next term 
# in the sequence while maintaining the same length.
# In this case lower order positions are at the higher indexes
def increment_term(term)
  term = String.new(term) # Ruby doesn't pass by value

  # Reset to lowest possible value when ceiling is hit
  if term == '9' * term.length
    return 'a' * term.length
  end

  # Initialize index to that of lowest order position
  index = term.length-1

  # Increment the lowest order position
  term[index] = increment_char(term[index].chr)
  
  # Increment higher order positions when a lower order one hits the ceiling
  while index > 0 and term[index].chr == 'a'
   index = index - 1
   term[index] = increment_char(term[index].chr)
  end

  return term
end

# Increments a character to its next higher value, wraps at max
# For this scraper characters are in the range [a-z0-9] and rated 
# from low to high in that order
def increment_char(c)
  return CHARACTERS[ (CHARACTERS.index(c) + 1) % (CHARACTERS.length) ]
end

# Generate a search url
def get_search_url(search_term)
    args = "SearchResults.asp?FormName=CorpNameSearch&Words=Starting&SearchStr=#{search_term}&SearchType=Search"
    return URL_BASE + args
end

##################
## Start Here
##################

puts "Starting Load"

## Searching is not affected by spaces

# Initialize search term
term = ScraperWiki.get_var('term', 'aaa')
add  = ScraperWiki.get_var('add', '') # Additional letters for the search term
t1   = ScraperWiki.get_var('t1', '')  # Try 1
t2   = ScraperWiki.get_var('t2', '')  # Try 2

error_count = 0

# For each possible term
while term != '999'

  begin
 
    # Extend the term addition if the term/add combo has been tried multiple times
    if term + add == t1 and term + add == t2 and error_count == 0
      puts "Increment term addition"
      add = add + 'a'
      ScraperWiki.save_var('add', add)
    end

    # Search failed to complete, use additional letters 
    if add != ''
      puts "Search with term addition"
  
      # For each possible additional letter
      while add != '9'*add.length
        t2 = term + add if term + add == t1
        t1 = term + add
        ScraperWiki.save_var('t2', t2)
        ScraperWiki.save_var('t1', t1)

        # Download all results
        search_and_load(get_search_url(term + add))
        error_count = 0

        # Increment and save the addition
        add = increment_term(add)
        ScraperWiki.save_var('add', add)
      end

      # Reset addition, increment and save the search term
      add = ''
      term = increment_term(term)
      ScraperWiki.save_var('add', add)
      ScraperWiki.save_var('term', term)
    end

    t2 = term if term == t1
    t1 = term
    ScraperWiki.save_var('t2', t2)
    ScraperWiki.save_var('t1', t1)

    # Download all results
    search_and_load(get_search_url(term))
    error_count = 0

    # Increment and save the search term
    term = increment_term(term)
    ScraperWiki.save_var('term', term)

  rescue Exception, Timeout::Error => e
    puts "xxxxxxxxxxxxxxxxx\nAn error occured: #{e.inspect}\n#{e.backtrace}"

    # Stop if error happens twice in a row
    break if error_count == 1
    error_count = 1
    sleep 30
  end
end

# Reset term state
if term == '999' and add == ''
  ScraperWiki.save_var('term', 'aaa')
end
