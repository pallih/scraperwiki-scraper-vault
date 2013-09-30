require 'nokogiri'
require 'open-uri'
require 'csv'

# declare some useful variables
BASE_URL = 'http://primis.phmsa.dot.gov/comm/reports/operator/OperatorIM_opid_'

###########################################
# this function scrapes a single page
###########################################
def scrape_page(url)

  # open single PHMSA operator data page
  html = ScraperWiki.scrape url
   
  # create a variable to hold the website, parsed with nokogiri
  doc = Nokogiri::HTML(html)
  
  # store all data
  doc.search('tbody').each do |tbody|
    h4 = doc.search('h4')
    ScraperWiki.save([:name, :urls, :data], {name:h4.inner_html, urls:url, data:tbody.inner_html})
  end

  # clear variables
  doc = nil
  html = nil
  h4 = nil

end

###########################################
# EXECUTION STARTS HERE
###########################################


# read in my list of operator IDs from Dropbox, building an array of strings
data = ScraperWiki.scrape 'http://dl.dropboxusercontent.com/u/6126475/just_IDs.csv'
csv = CSV.new(data)
opIDs = csv.read().flatten

# loop through each operator ID, throwing to the page scrape function
opIDs.each do |opID|
  url = BASE_URL + opID + '.html?nocache='
  scrape_page(url)
end

require 'nokogiri'
require 'open-uri'
require 'csv'

# declare some useful variables
BASE_URL = 'http://primis.phmsa.dot.gov/comm/reports/operator/OperatorIM_opid_'

###########################################
# this function scrapes a single page
###########################################
def scrape_page(url)

  # open single PHMSA operator data page
  html = ScraperWiki.scrape url
   
  # create a variable to hold the website, parsed with nokogiri
  doc = Nokogiri::HTML(html)
  
  # store all data
  doc.search('tbody').each do |tbody|
    h4 = doc.search('h4')
    ScraperWiki.save([:name, :urls, :data], {name:h4.inner_html, urls:url, data:tbody.inner_html})
  end

  # clear variables
  doc = nil
  html = nil
  h4 = nil

end

###########################################
# EXECUTION STARTS HERE
###########################################


# read in my list of operator IDs from Dropbox, building an array of strings
data = ScraperWiki.scrape 'http://dl.dropboxusercontent.com/u/6126475/just_IDs.csv'
csv = CSV.new(data)
opIDs = csv.read().flatten

# loop through each operator ID, throwing to the page scrape function
opIDs.each do |opID|
  url = BASE_URL + opID + '.html?nocache='
  scrape_page(url)
end

