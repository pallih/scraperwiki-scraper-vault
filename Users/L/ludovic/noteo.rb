require 'nokogiri'
require 'open-uri'

def extract_product(url)
  product_page = Nokogiri::HTML open(url)

  barcode_node= product_page.at_xpath("//*[@id='product_detail']/div[2]/div[4]/a")
  description_node= product_page.at_xpath("//*[@id='main']/article/div/div[2]/h1/span[1]")
  brand_node= product_page.at_xpath("//*[@id='main']/article/div/div[2]/h1/span[3]")
  image_node= product_page.at_xpath("//*[@id='product_img']")
  barcode= barcode_node.attr('href').split('/').last rescue nil
  if barcode.nil? == false
    entity= {
      :barcode => barcode,
      :description => description_node.text(),
      :brand =>  brand_node.text().split(':').last,
      :image_url => image_node.attr('src')
    }
    ScraperWiki::save_sqlite(['barcode'], entity)
  end
end

items=1
categories = Nokogiri::HTML open("http://www.noteo.info/resultats/")
categories.xpath("//*[@id='resultat-recherche']/tbody/tr/th/a").each do |category|
  url= "http://www.noteo.info"+category.attr('href')
  extract_product(url)
end


1980.times do 
  items+=15
  categories = Nokogiri::HTML open("http://www.noteo.info/resultats/?type=2&start=#{items}&order%5Bid%5D=0&order%5Btype%5D=1")
  categories.xpath("//*[@id='resultat-recherche']/tbody/tr/th/a").each do |category|
    url= "http://www.noteo.info"+category.attr('href')
    extract_product(url)    
  end
end


