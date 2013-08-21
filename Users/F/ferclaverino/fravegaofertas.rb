# Blank Ruby

html = ScraperWiki.scrape "http://www.fravega.com/"
p html

require 'nokogiri'

doc = Nokogiri::HTML(html, nil, 'utf-8')

doc.search('title').each do |title|
  p title.inner_html
end

doc.search("#tab-productos .item").each do |item|
  product = {
    name: item.css(".product-name")[0].content,
    brand: item.css(".marca")[0].content,
    sku: item.css(".product-sku")[0].content,
    pfonline: item.css(".pf-online .price")[0].content,
    #pfregular: item.css(".pf-regular .price").content
  }    
  ScraperWiki::save_sqlite(['sku'], product) 
end