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
  
  # find everything within <tbody> tags
  #doc.search('tbody').each do |tbody|
  #  p tbody.inner_html
  #end
  
  #doc.search('h4').each do |h4|
  #  ScraperWiki.save([:data], {data: h4.inner_html})
  #end

  # store all contents of <tbody> tags
  doc.search('tbody').each do |tbody|
    h4 = doc.search('h4')
    ScraperWiki.save([:data], {data: h4.inner_html})
    ScraperWiki.save([:data], {data: url})
    #p = doc.search('p')
    #ScraperWiki.save([:operatorID], {operatorID: p.inner_html})
    ScraperWiki.save([:data], {data: tbody.inner_html})
  end

end

###########################################
# EXECUTION STARTS HERE
###########################################


# read in my list of operator IDs from Dropbox, building an array of strings
data = ScraperWiki.scrape 'http://dl.dropboxusercontent.com/u/6126475/IDsindata.csv'
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
  
  # find everything within <tbody> tags
  #doc.search('tbody').each do |tbody|
  #  p tbody.inner_html
  #end
  
  #doc.search('h4').each do |h4|
  #  ScraperWiki.save([:data], {data: h4.inner_html})
  #end

  # store all contents of <tbody> tags
  doc.search('tbody').each do |tbody|
    h4 = doc.search('h4')
    ScraperWiki.save([:data], {data: h4.inner_html})
    ScraperWiki.save([:data], {data: url})
    #p = doc.search('p')
    #ScraperWiki.save([:operatorID], {operatorID: p.inner_html})
    ScraperWiki.save([:data], {data: tbody.inner_html})
  end

end

###########################################
# EXECUTION STARTS HERE
###########################################


# read in my list of operator IDs from Dropbox, building an array of strings
data = ScraperWiki.scrape 'http://dl.dropboxusercontent.com/u/6126475/IDsindata.csv'
csv = CSV.new(data)
opIDs = csv.read().flatten

# loop through each operator ID, throwing to the page scrape function
opIDs.each do |opID|
  url = BASE_URL + opID + '.html?nocache='
  scrape_page(url)
end

