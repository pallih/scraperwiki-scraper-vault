###############################################################################
# This is a scraper to look for additional information of spanish senators
# from each of the senate web site
###############################################################################
require 'open-uri'

html = ScraperWiki.scrape("http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado&idDiputado=72&idLegislatura=8")
puts html


# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.
require 'nokogiri'
 
doc = Nokogiri::HTML(html)

name=doc.css('div[@class= "nombre_dip"]').first
puts name.content

provincia = doc.css('div[@class= "dip_rojo"]').first
puts provincia.content

grupo = doc.css('div[@class= "dip_rojo"] > a').first
puts grupo.content

i=1
desc={}
doc.css('div[@class= "texto_dip"] > ul > li').each do |name|
  desc[i]=name.content
  i=i+1
end

puts desc[2]
puts desc[3]
