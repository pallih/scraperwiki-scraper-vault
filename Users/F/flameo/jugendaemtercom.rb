html = ScraperWiki.scrape("http://www.jugendaemter.com/index.php/jugendamt-aachen/")

puts html


require 'nokogiri'

doc = Nokogiri::HTML(html)

doc.search(".p").each do |entry|

  name = entry.css("strong").first.inner_html
  data = entry.css("p.data").first.inner_html.split("<br>").map(&:'strip')
  tel = entry.at_css(".action").inner_text.match(/^([0-9 ()]+) /)[1] + entry.css(".action img").collect{|i|i['src'][-5,1]}.join

 something = "#{name},#{data[0]},#{data[1][0..4]},#{data[1][5..-1]},#{tel}"


    ScraperWiki.save(['data'], {'data' => something})
end

html = ScraperWiki.scrape("http://www.jugendaemter.com/index.php/jugendamt-aachen/")

puts html


require 'nokogiri'

doc = Nokogiri::HTML(html)

doc.search(".p").each do |entry|

  name = entry.css("strong").first.inner_html
  data = entry.css("p.data").first.inner_html.split("<br>").map(&:'strip')
  tel = entry.at_css(".action").inner_text.match(/^([0-9 ()]+) /)[1] + entry.css(".action img").collect{|i|i['src'][-5,1]}.join

 something = "#{name},#{data[0]},#{data[1][0..4]},#{data[1][5..-1]},#{tel}"


    ScraperWiki.save(['data'], {'data' => something})
end

