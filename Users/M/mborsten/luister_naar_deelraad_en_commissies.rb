require 'nokogiri'

link = "http://www.deelraadinfo.nl/IJsselmonde/Deelraad/Luister_naar_deelraad_en_commissies/Luister_naar_Deelraad_en_Commissies"
html = ScraperWiki.scrape(link)
doc = Nokogiri::HTML(html)

full_list = Array.new

doc.xpath('//div[@id="content"]//a').each do |link|

 mp3_link = link.xpath('@href').text
 title = link.xpath('@title').text
  
 data = {"title" => title, "link" => mp3_link}
 full_list.push data
end

puts full_list

ScraperWiki.save_sqlite(unique_keys=['link'], data=full_list)
require 'nokogiri'

link = "http://www.deelraadinfo.nl/IJsselmonde/Deelraad/Luister_naar_deelraad_en_commissies/Luister_naar_Deelraad_en_Commissies"
html = ScraperWiki.scrape(link)
doc = Nokogiri::HTML(html)

full_list = Array.new

doc.xpath('//div[@id="content"]//a').each do |link|

 mp3_link = link.xpath('@href').text
 title = link.xpath('@title').text
  
 data = {"title" => title, "link" => mp3_link}
 full_list.push data
end

puts full_list

ScraperWiki.save_sqlite(unique_keys=['link'], data=full_list)
