# coding: utf-8
require 'nokogiri'

base_url = "http://www.abe-natsumi.com/blog/"

html = ScraperWiki.scrape(base_url).force_encoding('utf-8')
doc = Nokogiri::HTML(html)
for link in doc.search("div[@class='sideMiddle']")[1]/:a #/
  id = $1 if link[:href]=~/\?id=(\d+)/
  href = base_url+URI.encode(link[:href])
  doc2 = Nokogiri::HTML(ScraperWiki.scrape(href).force_encoding('utf-8'))
  data ={
    :id => id,
    :link => href,
    :title => doc2.search("h2[@class='blogTitle']").inner_html,
    :date => Time.parse(doc2.search("div[@class='blogDate']").inner_html),
    :content => doc2.search("p[@class='blogText']").inner_html
  }
  ScraperWiki.save(['id'], [data])
end
# coding: utf-8
require 'nokogiri'

base_url = "http://www.abe-natsumi.com/blog/"

html = ScraperWiki.scrape(base_url).force_encoding('utf-8')
doc = Nokogiri::HTML(html)
for link in doc.search("div[@class='sideMiddle']")[1]/:a #/
  id = $1 if link[:href]=~/\?id=(\d+)/
  href = base_url+URI.encode(link[:href])
  doc2 = Nokogiri::HTML(ScraperWiki.scrape(href).force_encoding('utf-8'))
  data ={
    :id => id,
    :link => href,
    :title => doc2.search("h2[@class='blogTitle']").inner_html,
    :date => Time.parse(doc2.search("div[@class='blogDate']").inner_html),
    :content => doc2.search("p[@class='blogText']").inner_html
  }
  ScraperWiki.save(['id'], [data])
end
