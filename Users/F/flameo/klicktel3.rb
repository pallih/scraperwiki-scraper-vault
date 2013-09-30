html = ScraperWiki.scrape("http://www.klicktel.de/branchenbuch/index/search?method=searchSimple&location_id=&trade_id=3302742&_dvform_posted=1&trade=Jugend%C3%A4mter&name=Name&zipCity=m%C3%BCnster&street=Stra%C3%9Fe&streetNumber=Nr.&radial=50%20km")

puts html


require 'nokogiri'

doc = Nokogiri::HTML(html)

doc.search('li.standard').each do |entry|

  name = entry.css(".fn").first.inner_html
  data = entry.css("p.data").first.inner_html.split("<br>").map(&:'strip')
  tel = entry.at_css(".action").inner_text.match(/^([0-9 ()]+) /)[1] + entry.css(".action img").collect{|i|i['src'][-5,1]}.join

 something = "#{name},#{data[0]},#{data[1][0..4]},#{data[1][5..-1]},#{tel}"


    ScraperWiki.save(['data'], {'data' => something})
end
html = ScraperWiki.scrape("http://www.klicktel.de/branchenbuch/index/search?method=searchSimple&location_id=&trade_id=3302742&_dvform_posted=1&trade=Jugend%C3%A4mter&name=Name&zipCity=m%C3%BCnster&street=Stra%C3%9Fe&streetNumber=Nr.&radial=50%20km")

puts html


require 'nokogiri'

doc = Nokogiri::HTML(html)

doc.search('li.standard').each do |entry|

  name = entry.css(".fn").first.inner_html
  data = entry.css("p.data").first.inner_html.split("<br>").map(&:'strip')
  tel = entry.at_css(".action").inner_text.match(/^([0-9 ()]+) /)[1] + entry.css(".action img").collect{|i|i['src'][-5,1]}.join

 something = "#{name},#{data[0]},#{data[1][0..4]},#{data[1][5..-1]},#{tel}"


    ScraperWiki.save(['data'], {'data' => something})
end
