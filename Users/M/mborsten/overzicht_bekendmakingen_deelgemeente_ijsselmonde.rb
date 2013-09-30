require 'nokogiri'

base_path = "http://www.rotterdam.nl"

page_range = 1..41

pagedata = Array.new

page_range.each do |page_number|

html = ScraperWiki.scrape("http://www.rotterdam.nl/overzicht_bekendmakingen_deelgemeente_ijsselmonde?sma=1098510&page=#{page_number.to_s}")
doc = Nokogiri::HTML(html)


doc.xpath('//dl[@class="list_options"]/dd').each do |node|

title = node.xpath('a/@title').to_s
link = node.xpath('a/@href').to_s

ablink = base_path + link

itemhtml = ScraperWiki.scrape(ablink)
itemdoc = Nokogiri::HTML(itemhtml)

datum = itemdoc.xpath('//p[@class="date"]').text.rstrip

text = ""

itemdoc.xpath('//div[@id="webeditor"]//p').each do |text_part|
  
  text << text_part

end

data = {
    
    'title' => title,
    'link' => ablink,
    'date' => datum,
    'text' => text,
  }

puts data

if(title != "")

pagedata.push data

end
end
end

ScraperWiki.save_sqlite(unique_keys=['link'], data=pagedata)
require 'nokogiri'

base_path = "http://www.rotterdam.nl"

page_range = 1..41

pagedata = Array.new

page_range.each do |page_number|

html = ScraperWiki.scrape("http://www.rotterdam.nl/overzicht_bekendmakingen_deelgemeente_ijsselmonde?sma=1098510&page=#{page_number.to_s}")
doc = Nokogiri::HTML(html)


doc.xpath('//dl[@class="list_options"]/dd').each do |node|

title = node.xpath('a/@title').to_s
link = node.xpath('a/@href').to_s

ablink = base_path + link

itemhtml = ScraperWiki.scrape(ablink)
itemdoc = Nokogiri::HTML(itemhtml)

datum = itemdoc.xpath('//p[@class="date"]').text.rstrip

text = ""

itemdoc.xpath('//div[@id="webeditor"]//p').each do |text_part|
  
  text << text_part

end

data = {
    
    'title' => title,
    'link' => ablink,
    'date' => datum,
    'text' => text,
  }

puts data

if(title != "")

pagedata.push data

end
end
end

ScraperWiki.save_sqlite(unique_keys=['link'], data=pagedata)
