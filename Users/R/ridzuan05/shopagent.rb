# scrape amazon.com for a keyword
require 'nokogiri'
keywords = "near-death experiences"

def scrape div
  a = div.at('.//a/span/..')
  data = {}
  data[:price] = div.at('.//span[@class="saleprice"]|.//span[@class="listprice"]|.//span[@class="sr_price"]|.//span[@class="otherprice"]').text rescue nil
  data['isbn'] = $1 if a['href'] =~ /dp\/([^\/]*)/ rescue nil
  data['name'] = a.text   rescue nil
  ScraperWiki.save_sqlite(unique_keys=['isbn'], data = data)
end

doc = Nokogiri::HTML(ScraperWiki.scrape("http://www.amazon.com/"))
form = doc.at '//form'
url = 'http://www.amazon.com' + form['action']
#puts url

doc = Nokogiri::HTML(ScraperWiki.scrape(url,{"field-keywords" => keywords}))
#puts doc
puts doc.xpath('//div[@class="result"]|//td[@class="searchitem"]').length
doc.css('td.searchitem').each {|div| scrape div}

while next_page = doc.at('a#pagnNextLink')
  doc = Nokogiri::HTML(ScraperWiki.scrape(next_page['href']))
  doc.css('td.searchitem').each {|div| scrape div}
end

# scrape amazon.com for a keyword
require 'nokogiri'
keywords = "near-death experiences"

def scrape div
  a = div.at('.//a/span/..')
  data = {}
  data[:price] = div.at('.//span[@class="saleprice"]|.//span[@class="listprice"]|.//span[@class="sr_price"]|.//span[@class="otherprice"]').text rescue nil
  data['isbn'] = $1 if a['href'] =~ /dp\/([^\/]*)/ rescue nil
  data['name'] = a.text   rescue nil
  ScraperWiki.save_sqlite(unique_keys=['isbn'], data = data)
end

doc = Nokogiri::HTML(ScraperWiki.scrape("http://www.amazon.com/"))
form = doc.at '//form'
url = 'http://www.amazon.com' + form['action']
#puts url

doc = Nokogiri::HTML(ScraperWiki.scrape(url,{"field-keywords" => keywords}))
#puts doc
puts doc.xpath('//div[@class="result"]|//td[@class="searchitem"]').length
doc.css('td.searchitem').each {|div| scrape div}

while next_page = doc.at('a#pagnNextLink')
  doc = Nokogiri::HTML(ScraperWiki.scrape(next_page['href']))
  doc.css('td.searchitem').each {|div| scrape div}
end

