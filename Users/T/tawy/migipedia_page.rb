# Blank Ruby

require 'nokogiri'
require 'open-uri'

def get_page(url)
  content= nil
  begin
    content= Nokogiri::HTML(open(url))
  rescue
    content=nil
  end
  return content
end


  #START = "http://www.migipedia.ch/fr/products/category"
  START = "http://www.migipedia.ch/fr/denrees-alimentaires"

#  START = "http://www.migipedia.ch/fr/electronique"

def get_info(baseUrl)
  categories = get_page(baseUrl)
  return if categories.nil? 
  categories.xpath("//*[@class='column grid_3 result-node result-node-product']/div/a").each do |object|
    page = get_page("http://www.migipedia.ch" + object.attr('href'))
    return if page.nil? 
    table = "//*[@class='sticky-enabled sticky-table']/tbody"
    page.xpath(table+"/tr[1]/td[2]").search('br').each do |br|
        br.replace("\n")
    end
    page.xpath(table+"/tr[1]/td[2]").text.split("\n").each do |ean|
      entity= {
        :denomination_value => object.attr('label'),
        :barcode =>            ean,
        :size =>               page.xpath(table+"/tr[2]/td[2]").text,
        :image_url =>          page.xpath("//*[@class='product-image grid_8 fixed']/div/img").attr('src').value
      }
      puts entity
      ScraperWiki::save_sqlite(['barcode'], entity)
    end
end
end

  def get_sub_cat(baseUrl)
    cat_page = get_page(baseUrl)
    return if cat_page.nil? 
    cat_page.xpath("//*[@id='content']/div/div/div/div/ul/li/a").each do |node|
        url="http://www.migipedia.ch" + node.attr('href')
        puts url
        get_sub_cat(url)
        get_info(url)
    end
  end

get_sub_cat(START)