require 'nokogiri'

url = "http://www.leipzig.de/de/buerger/politik/wahlen/stadtrat/2009/wahlkreise/15924.aspx"
html = ScraperWiki.scrape(url)

doc = Nokogiri::HTML(html)

basepath = "/html/body/div[6]/table/tr/td[3]/table[4]/tr[5]/td/table/tr/td[2]/table/tr[%i]"


for i in 10..18

  xpath = basepath % i.to_s
  row = doc.xpath(xpath)

  name    = row.xpath('./td[1]').text.strip
  votes   = row.xpath('./td[2]').text
  percent = row.xpath('./td[3]').text

  result = {
    'name'    => name,
    'votes'   => votes,
    'percent' => percent
  }

  unique_keys = ['name']

  ScraperWiki.save_sqlite(unique_keys, result)

end

require 'nokogiri'

url = "http://www.leipzig.de/de/buerger/politik/wahlen/stadtrat/2009/wahlkreise/15924.aspx"
html = ScraperWiki.scrape(url)

doc = Nokogiri::HTML(html)

basepath = "/html/body/div[6]/table/tr/td[3]/table[4]/tr[5]/td/table/tr/td[2]/table/tr[%i]"


for i in 10..18

  xpath = basepath % i.to_s
  row = doc.xpath(xpath)

  name    = row.xpath('./td[1]').text.strip
  votes   = row.xpath('./td[2]').text
  percent = row.xpath('./td[3]').text

  result = {
    'name'    => name,
    'votes'   => votes,
    'percent' => percent
  }

  unique_keys = ['name']

  ScraperWiki.save_sqlite(unique_keys, result)

end

