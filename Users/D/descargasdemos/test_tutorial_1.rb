# Blank Ruby

#html = ScraperWiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
 html = ScraperWiki.scrape("http://www.contratosdegalicia.es/licitacion?N=14005&PA=1&ID=0&lang=es")
puts html
#SeccionCampo

require 'nokogiri'
doc = Nokogiri::HTML(html)
for v in doc.search("span[@class='SeccionCampo']")
  
  data = {
    'id' => v.inner_html,
    'texto' => v.inner_html
  }
  #puts data.to_json
  ScraperWiki.save_sqlite(unique_keys=['country'], data=data)

end



# puts html

# Blank Ruby

#html = ScraperWiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
 html = ScraperWiki.scrape("http://www.contratosdegalicia.es/licitacion?N=14005&PA=1&ID=0&lang=es")
puts html
#SeccionCampo

require 'nokogiri'
doc = Nokogiri::HTML(html)
for v in doc.search("span[@class='SeccionCampo']")
  
  data = {
    'id' => v.inner_html,
    'texto' => v.inner_html
  }
  #puts data.to_json
  ScraperWiki.save_sqlite(unique_keys=['country'], data=data)

end



# puts html

