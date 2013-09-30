# Frávega - Scrapper para Productos en Oferta

require 'nokogiri'

html = ScraperWiki.scrape "http://www.fravega.com/"
error = nil

doc = Nokogiri::HTML(html, nil, 'utf-8')

doc.search("#tab-fravega .item").each do |item|

     begin
      deteailHtml =  ScraperWiki.scrape item.css(".product-name a")[0]["href"]
      detailDoc = Nokogiri::HTML(deteailHtml, nil, 'utf-8')
    rescue Exception => e
      error = e
  
      break
    end
  
    product = {
      sku: item.css(".product-sku")[0].content.split(" ")[1],
      productUrl: item.css(".product-name a")[0]["href"],
      name: item.css(".product-name")[0].content,
      brand: item.css(".marca")[0].content,
      pfonline: ((item.css(".pf-online .price")[0] == nil) ? "": item.css(".pf-online .price")[0].content ),
      pfregular: ((item.css(".pf-regular .price")[0] == nil) ? "": item.css(".pf-regular .price")[0].content ),
      imageUrl: item.css(".product-image a img")[0]["src"],
      description: detailDoc.css(".descn")[0].content,
      specificationTable: detailDoc.search("#tab-detalles table")[0],
      costsTable: detailDoc.search("#tab-tiempoycosto table")[0],
      status: 0,
    }   

  ScraperWiki::save_sqlite(['sku'], product) 
end

if error == nil
  ScraperWiki::sqliteexecute("delete from swdata where status = 1")
  ScraperWiki::commit() 
  ScraperWiki::sqliteexecute("update swdata set status = 1 where status = 0")
  ScraperWiki::commit() 
else 
    ScraperWiki::sqliteexecute("delete from swdata where status = 0")  
    ScraperWiki::commit() 
end# Frávega - Scrapper para Productos en Oferta

require 'nokogiri'

html = ScraperWiki.scrape "http://www.fravega.com/"
error = nil

doc = Nokogiri::HTML(html, nil, 'utf-8')

doc.search("#tab-fravega .item").each do |item|

     begin
      deteailHtml =  ScraperWiki.scrape item.css(".product-name a")[0]["href"]
      detailDoc = Nokogiri::HTML(deteailHtml, nil, 'utf-8')
    rescue Exception => e
      error = e
  
      break
    end
  
    product = {
      sku: item.css(".product-sku")[0].content.split(" ")[1],
      productUrl: item.css(".product-name a")[0]["href"],
      name: item.css(".product-name")[0].content,
      brand: item.css(".marca")[0].content,
      pfonline: ((item.css(".pf-online .price")[0] == nil) ? "": item.css(".pf-online .price")[0].content ),
      pfregular: ((item.css(".pf-regular .price")[0] == nil) ? "": item.css(".pf-regular .price")[0].content ),
      imageUrl: item.css(".product-image a img")[0]["src"],
      description: detailDoc.css(".descn")[0].content,
      specificationTable: detailDoc.search("#tab-detalles table")[0],
      costsTable: detailDoc.search("#tab-tiempoycosto table")[0],
      status: 0,
    }   

  ScraperWiki::save_sqlite(['sku'], product) 
end

if error == nil
  ScraperWiki::sqliteexecute("delete from swdata where status = 1")
  ScraperWiki::commit() 
  ScraperWiki::sqliteexecute("update swdata set status = 1 where status = 0")
  ScraperWiki::commit() 
else 
    ScraperWiki::sqliteexecute("delete from swdata where status = 0")  
    ScraperWiki::commit() 
end