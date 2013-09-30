require 'open-uri'
require 'nokogiri'
require 'pp'
require 'iconv'

html = open('http://www.hzs.sk/index.php?lang=sk&site=statistika&p=oblast:SL')
html = doc = Nokogiri::HTML(html)
table = doc.xpath('//html/body/table/tr/td/table/tr/td/table/td/table/tr')
table.shift
hedre0 = table.shift
hedre1 = table.shift
hedre = hedre0.xpath('.//td') + hedre1.xpath('.//td')
table.xpath('.//td').each_slice(9) do |row|
  data = {
    "date" => row[0].text.to_s,
    "place" => row[1].text.to_s,
    "orientation" => row[2].text.to_s,
    "landing" => row[3].text.to_s,
    "hardness" => row[4].text.to_s,
    "head" => row[5].text.to_s,
    "postihnuti" => row[6].text.to_s,
    "snow" => row[7].text.to_s,
    "odtrh" => row[8].text.to_s
  }

#  dt = {}
#  data.each_pair do |x,y| 
#    dt.merge!({
#      x.to_s =>
#      Iconv.iconv('utf8', 'cp1250', y).to_s
#    })
#  end

  ScraperWiki.save_sqlite(unique_keys = [], data = data)
end
require 'open-uri'
require 'nokogiri'
require 'pp'
require 'iconv'

html = open('http://www.hzs.sk/index.php?lang=sk&site=statistika&p=oblast:SL')
html = doc = Nokogiri::HTML(html)
table = doc.xpath('//html/body/table/tr/td/table/tr/td/table/td/table/tr')
table.shift
hedre0 = table.shift
hedre1 = table.shift
hedre = hedre0.xpath('.//td') + hedre1.xpath('.//td')
table.xpath('.//td').each_slice(9) do |row|
  data = {
    "date" => row[0].text.to_s,
    "place" => row[1].text.to_s,
    "orientation" => row[2].text.to_s,
    "landing" => row[3].text.to_s,
    "hardness" => row[4].text.to_s,
    "head" => row[5].text.to_s,
    "postihnuti" => row[6].text.to_s,
    "snow" => row[7].text.to_s,
    "odtrh" => row[8].text.to_s
  }

#  dt = {}
#  data.each_pair do |x,y| 
#    dt.merge!({
#      x.to_s =>
#      Iconv.iconv('utf8', 'cp1250', y).to_s
#    })
#  end

  ScraperWiki.save_sqlite(unique_keys = [], data = data)
end
