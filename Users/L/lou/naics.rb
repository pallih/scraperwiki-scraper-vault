# NAICS Scraper

require 'nokogiri'
require 'openURI'

# set URLs to retrieve a list of codes from NAICS API
naics_api      = 'http://naics-api.herokuapp.com/v0/q?year='
naics_2007_url = naics_api + '2007'
naics_2012_url = naics_api + '2012'

open(naics_2007_url) {|f|
  f.each_line {|line| p line}
}

# eventually we need to go through and pull the census page for each code

#html = ScraperWiki::scrape("http://www.census.gov/cgi-bin/sssd/naics/naicsrch?code=541430&search=2012%20NAICS%20Search")
html = ScraperWiki::scrape("http://www.census.gov/cgi-bin/sssd/naics/naicsrch?code=541&search=2012%20NAICS%20Search")

# parse the HTML document

doc = Nokogiri::HTML html
content = doc.css("#middle-column table")
puts content

data = {
  info: content[0].inner_html
}

# save the data

ScraperWiki::save_sqlite(['info'], data)
# NAICS Scraper

require 'nokogiri'
require 'openURI'

# set URLs to retrieve a list of codes from NAICS API
naics_api      = 'http://naics-api.herokuapp.com/v0/q?year='
naics_2007_url = naics_api + '2007'
naics_2012_url = naics_api + '2012'

open(naics_2007_url) {|f|
  f.each_line {|line| p line}
}

# eventually we need to go through and pull the census page for each code

#html = ScraperWiki::scrape("http://www.census.gov/cgi-bin/sssd/naics/naicsrch?code=541430&search=2012%20NAICS%20Search")
html = ScraperWiki::scrape("http://www.census.gov/cgi-bin/sssd/naics/naicsrch?code=541&search=2012%20NAICS%20Search")

# parse the HTML document

doc = Nokogiri::HTML html
content = doc.css("#middle-column table")
puts content

data = {
  info: content[0].inner_html
}

# save the data

ScraperWiki::save_sqlite(['info'], data)
