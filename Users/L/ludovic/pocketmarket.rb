require 'nokogiri'
require 'open-uri'

categories_content= ScraperWiki::scrape("http://pocketmarket.fr/245-2034-fruits-frais")
categories = Nokogiri::HTML categories_content
categories.xpath("//a").each do |category|
  url= category['href']
  if url.split("?").count == 2
    url+= '&n=500' 
  else
    url+= '?n=200'
  end
  products_page= Nokogiri::HTML(open(url))
  products_page.xpath("//*[@id='product_list']/li/div").each do |node|
    link_node= node.at_xpath("./div[1]/a")
    img_node= node.at_xpath("./a/img")
    entity= {
      :denomination_value => link_node.text(),
      :barcode => link_node.attr('href').split('-').last.split('.html').first,
      :image_url => img_node.attr('src')
    }
    ScraperWiki::save_sqlite(['barcode'], entity)
  end
end



require 'nokogiri'
require 'open-uri'

categories_content= ScraperWiki::scrape("http://pocketmarket.fr/245-2034-fruits-frais")
categories = Nokogiri::HTML categories_content
categories.xpath("//a").each do |category|
  url= category['href']
  if url.split("?").count == 2
    url+= '&n=500' 
  else
    url+= '?n=200'
  end
  products_page= Nokogiri::HTML(open(url))
  products_page.xpath("//*[@id='product_list']/li/div").each do |node|
    link_node= node.at_xpath("./div[1]/a")
    img_node= node.at_xpath("./a/img")
    entity= {
      :denomination_value => link_node.text(),
      :barcode => link_node.attr('href').split('-').last.split('.html').first,
      :image_url => img_node.attr('src')
    }
    ScraperWiki::save_sqlite(['barcode'], entity)
  end
end



