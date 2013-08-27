#!/usr/bin/ruby -Ku
# Ruby code to download the list of senator



senadoresyelecto={}, senadores={}, electo={}

html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html")
puts html 


i=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'iso-8859-1')
doc.search('ul> li').each do |senadoryelecto|
  temp= senadoryelecto.inner_html
  puts temp
  temp=temp.gsub(/<\/?[^>]*>/,"") #con  la  función  gsub hacemos un remplazo utilizando expresiones  regulares,  see  http://en.wikipedia.org/wiki/Regular_expression, y  quitamos todo  el  html
  puts temp  
  senadoresyelecto=temp.split(".")
  senadores[i]=senadoresyelecto[0]
  electo[i]=senadoresyelecto[1] 
  i=i+1
end
#!/usr/bin/ruby -Ku
# Ruby code to download the list of senator



senadoresyelecto={}, senadores={}, electo={}

html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html")
puts html 


i=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'iso-8859-1')
doc.search('ul> li').each do |senadoryelecto|
  temp= senadoryelecto.inner_html
  puts temp
  temp=temp.gsub(/<\/?[^>]*>/,"") #con  la  función  gsub hacemos un remplazo utilizando expresiones  regulares,  see  http://en.wikipedia.org/wiki/Regular_expression, y  quitamos todo  el  html
  puts temp  
  senadoresyelecto=temp.split(".")
  senadores[i]=senadoresyelecto[0]
  electo[i]=senadoresyelecto[1] 
  i=i+1
end
#!/usr/bin/ruby -Ku
# Ruby code to download the list of senator



senadoresyelecto={}, senadores={}, electo={}

html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html")
puts html 


i=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'iso-8859-1')
doc.search('ul> li').each do |senadoryelecto|
  temp= senadoryelecto.inner_html
  puts temp
  temp=temp.gsub(/<\/?[^>]*>/,"") #con  la  función  gsub hacemos un remplazo utilizando expresiones  regulares,  see  http://en.wikipedia.org/wiki/Regular_expression, y  quitamos todo  el  html
  puts temp  
  senadoresyelecto=temp.split(".")
  senadores[i]=senadoresyelecto[0]
  electo[i]=senadoresyelecto[1] 
  i=i+1
end
