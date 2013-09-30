html = ScraperWiki.scrape("http://www.sfsu.edu/~upd/crimelog/index.html")

require 'nokogiri'
doc = Nokogiri::HTML(html)
doc.search(".brief").each do |brief|
  #push to console
  puts brief.css("h3:nth-child(3) , p:nth-child(4), h3:nth-child(4), p:nth-child(5)").text

  #save in sql  
  ScraperWiki.save_sqlite(['data'], {'data' => brief.css("h3:nth-child(3) , p:nth-child(4), h3:nth-child(4), p:nth-child(5)").text})
endhtml = ScraperWiki.scrape("http://www.sfsu.edu/~upd/crimelog/index.html")

require 'nokogiri'
doc = Nokogiri::HTML(html)
doc.search(".brief").each do |brief|
  #push to console
  puts brief.css("h3:nth-child(3) , p:nth-child(4), h3:nth-child(4), p:nth-child(5)").text

  #save in sql  
  ScraperWiki.save_sqlite(['data'], {'data' => brief.css("h3:nth-child(3) , p:nth-child(4), h3:nth-child(4), p:nth-child(5)").text})
end