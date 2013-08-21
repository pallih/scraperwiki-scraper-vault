require 'nokogiri'
require 'open-uri'
require 'csv'

# declare some useful variables
BASE_URL = 'http://primis.phmsa.dot.gov/comm/reports/operator/OperatorIM_opid_'

###########################################
# this function scrapes a single page
###########################################
def scrape_page(url)
   
  # create a variable to hold the website, parsed with nokogiri
  doc = Nokogiri::HTML(open(url))
  
  # scrape what we're interested in, using xpath and nokogiri
  title=doc.search('h4').inner_html
  allcommod=doc.xpath('//div[@id="MileagebyCommodity_tab_1"]//div[@class="reporttablewrap"]//table[@class="sortable tabular"]//tbody//tr//td')
  total=doc.xpath('//div[@id="MileagebyCommodity_tab_1"]//div[@class="reporttablewrap"]//table[@class="sortable tabular"]//tbody//tr[@class="total sortbottom"]//td')
  
  # save all data for this page
  ScraperWiki.save([:title, :allcommod, :total, :url], {title:title, allcommod:allcommod.inner_html, total:total.inner_html, url:url})

  # clear variables
  doc = nil
  html = nil
  allcommod=nil
  total=nil
  url=nil
  title=nil

end

###########################################
# EXECUTION STARTS HERE
###########################################


# read in my list of operator IDs from Dropbox, building an array of strings
csv = CSV.new(open("http://dl.dropboxusercontent.com/u/6126475/just_IDs.csv"))
opIDs = csv.read().flatten

#opID = '300'
#opID = '4906'

# loop through each operator ID, throwing to the page scrape function
opIDs.each do |opID|
  url = BASE_URL + opID + '.html?nocache='
  scrape_page(url)
end