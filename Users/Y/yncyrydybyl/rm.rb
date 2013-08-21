# Blank Ruby
# html = ScraperWiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
url = "http://eifon.raumobil.de/search/result?isSubmit=true&commodityType=mobile&mobile.requestType=SUPPLY&mobile.startLocation.displayCountry=Deutschland&mobile.startLocation.country=DE&mobile.startLocation.zipCode=&mobile.startLocation.city=berlin&mobile.endLocation.displayCountry=Deutschland&mobile.endLocation.country=DE&mobile.endLocation.zipCode=&mobile.endLocation.city=Berlin&mobile.date=13.07.11&mobile.dayTolerance=5&v=1&lang=en&layoutTheme=m2_iphonenat&layout=ajax"

html = ScraperWiki.scrape(url)
require 'nokogiri'
doc = Nokogiri::HTML(html) 
content = doc.search("li[@class='arrow']")

puts content
