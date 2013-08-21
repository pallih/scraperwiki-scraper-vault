require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'
require 'pp'
require 'uri'
require 'net/http'
require 'scraperwiki/datastore'
require 'httpclient'
require 'scraperwiki/scraper_require'


url = "http://andreascorrano88.altervista.org/andreascorrano88_0001.html"

doc = Nokogiri.HTML(open(url))
#puts doc

rows=doc.search('p a')
#puts rows

rows.each do |row|

link=row[:href]

url = link

doc = Nokogiri.HTML(open(url))

credit={}

credit[:artist_url]=url

  if doc.search('a.overview span').inner_text == "overview"
   
    credit[:check_overview]=1

  else

    credit[:check_overview]=0

  end #ends the if else condition 

ScraperWiki::save_sqlite([:artist_url], credit, table_name="Overview_check_presence", verbose=0)

end #ends iteration over links from altervista
