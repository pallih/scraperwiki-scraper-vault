# Frávega - Scrapper para Productos más vendidos

html = ScraperWiki.scrape "http://www.fravega.com/"

require 'nokogiri'

ScraperWiki::sqliteexecute("CREATE TABLE if not exists temporaryProducts (`sku` string,`productUrl` string,`name` string,`brand` string,`pfonline` string,`pfregular` string,`imageUrl` string)")

ScraperWiki::sqliteexecute("CREATE TABLE if not exists products(`sku` string,`productUrl` string,`name` string,`brand` string,`pfonline` string,`pfregular` string,`imageUrl` string)")

ScraperWiki::sqliteexecute("delete from temporaryProducts ")

error = nil

doc = Nokogiri::HTML(html, nil, 'utf-8')

doc.search("#tab-productos .item").each do |item|

    begin
      deteailHtml =  ScraperWiki.scrape item.css(".product-name a")[0]["href"]
      #detailDoc = Nokogiri::HTML(deteailHtml, nil, 'utf-8')
    rescue Exception=>e
        error=e
        break
    end 

  ScraperWiki::sqliteexecute(
            "insert into temporaryProducts (sku,productUrl,name,brand,pfonline,pfregular,imageUrl) 
            values (?,?,?,?,?,?,?)",
            [item.css(".product-sku")[0].content.split(" ")[1],
            item.css(".product-name a")[0]["href"],
            item.css(".product-name")[0].content,
            item.css(".marca")[0].content,item.css(".pf-online .price")[0].content,
            ((item.css(".pf-regular .price")[0] == nil) ? "": item.css(".pf-regular .price")[0].content ),
            item.css(".product-image a img")[0]["src"] ])
 
end

if error==nil
  ScraperWiki::sqliteexecute("delete from products")
  ScraperWiki::sqliteexecute("insert into products (sku,productUrl,name,brand,pfonline,pfregular,imageUrl) select sku,productUrl,name,brand,pfonline,pfregular,imageUrl from temporaryProducts")
  ScraperWiki::commit() 
end
ScraperWiki::sqliteexecute("select * from products")
ScraperWiki::sqliteexecute("select * from temporaryProducts")# Frávega - Scrapper para Productos más vendidos

html = ScraperWiki.scrape "http://www.fravega.com/"

require 'nokogiri'

ScraperWiki::sqliteexecute("CREATE TABLE if not exists temporaryProducts (`sku` string,`productUrl` string,`name` string,`brand` string,`pfonline` string,`pfregular` string,`imageUrl` string)")

ScraperWiki::sqliteexecute("CREATE TABLE if not exists products(`sku` string,`productUrl` string,`name` string,`brand` string,`pfonline` string,`pfregular` string,`imageUrl` string)")

ScraperWiki::sqliteexecute("delete from temporaryProducts ")

error = nil

doc = Nokogiri::HTML(html, nil, 'utf-8')

doc.search("#tab-productos .item").each do |item|

    begin
      deteailHtml =  ScraperWiki.scrape item.css(".product-name a")[0]["href"]
      #detailDoc = Nokogiri::HTML(deteailHtml, nil, 'utf-8')
    rescue Exception=>e
        error=e
        break
    end 

  ScraperWiki::sqliteexecute(
            "insert into temporaryProducts (sku,productUrl,name,brand,pfonline,pfregular,imageUrl) 
            values (?,?,?,?,?,?,?)",
            [item.css(".product-sku")[0].content.split(" ")[1],
            item.css(".product-name a")[0]["href"],
            item.css(".product-name")[0].content,
            item.css(".marca")[0].content,item.css(".pf-online .price")[0].content,
            ((item.css(".pf-regular .price")[0] == nil) ? "": item.css(".pf-regular .price")[0].content ),
            item.css(".product-image a img")[0]["src"] ])
 
end

if error==nil
  ScraperWiki::sqliteexecute("delete from products")
  ScraperWiki::sqliteexecute("insert into products (sku,productUrl,name,brand,pfonline,pfregular,imageUrl) select sku,productUrl,name,brand,pfonline,pfregular,imageUrl from temporaryProducts")
  ScraperWiki::commit() 
end
ScraperWiki::sqliteexecute("select * from products")
ScraperWiki::sqliteexecute("select * from temporaryProducts")