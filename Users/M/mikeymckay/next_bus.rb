###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

starting_url = 'http://wmata.nextbus.com/customStopSelector/fancyNewPredictionLayer.jsp?a=wmata&r=42&d=42_42_1&s=6113&ts=6225'
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)

(first,second,third) = doc.search('div')

ScraperWiki.save_var("first", first.content)
ScraperWiki.save_var("second", second.content)
ScraperWiki.save_var("third", third.content)


###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

starting_url = 'http://wmata.nextbus.com/customStopSelector/fancyNewPredictionLayer.jsp?a=wmata&r=42&d=42_42_1&s=6113&ts=6225'
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)

(first,second,third) = doc.search('div')

ScraperWiki.save_var("first", first.content)
ScraperWiki.save_var("second", second.content)
ScraperWiki.save_var("third", third.content)


