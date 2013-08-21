# Frávega - Scrapper para Productos por categoria

require 'nokogiri'

begin
  html = ScraperWiki.scrape "http://www.fravega.com/"
rescue
  html = ""
end

error = nil

doc = Nokogiri::HTML(html, nil, 'utf-8')

doc.search("#tab-categorias .item").each do |item|

  if error != nil
    break
  end

  finishedCategoryLastPage = false

  firstProductInPage = ""
  
  pageIndex = 0

  categoryName = item.css(".category-name a")[0]["href"].split("/")[4].split(".")[0]

  while !finishedCategoryLastPage do
  
    if error != nil
      break
    end

    pageIndex = pageIndex + 1

    categoryUrl = item.css(".category-name a")[0]["href"] + "?p=" + pageIndex.to_s

    if (pageIndex <= 10)
      begin
        productsHtml = ScraperWiki.scrape categoryUrl
      rescue Exception => e
        finishedCategoryLastPage = true
        error = e
        break
      end
    else
      finishedCategoryLastPage = true
    end

    if !finishedCategoryLastPage && error == nil

      productsDoc = Nokogiri::HTML(productsHtml , nil, 'utf-8')
  
      productsDoc.search("#category-products .item").each do |product| 
   
        detailUrl = product.css(".product-name a")[0]["href"]
      
        begin
          detailHtml =  ScraperWiki.scrape detailUrl 
          detailDoc = Nokogiri::HTML(detailHtml , nil, 'utf-8')
        rescue Exception => e
          detailHtml = ""
          detailDoc = ""
          error = e
          break
        end
    
        if detailDoc != ""

          begin
            productByCategory = {
              sku: product.css(".product-sku")[0].content.split(" ")[1],
              productUrl: product.css(".product-name a")[0]["href"],
              name: product.css(".product-name")[0].content,
              brand: product.css(".marca")[0].content,
              pfonline: ((product.css(".pf-online .price")[0] == nil) ? "": product.css(".pf-online .price")[0].content ),
              pfregular: ((product.css(".pf-regular .price")[0] == nil) ? "": product.css(".pf-regular .price")[0].content ),
              imageUrl: product.css(".product-image a img")[0]["src"],
              description: detailDoc.css(".descn")[0].content,
              specificationTable: detailDoc.search("#tab-detalles table")[0],
              costsTable: detailDoc.search("#tab-tiempoycosto table")[0],
              category: categoryName,
              status: 0,
            }   
        
            ScraperWiki::save_sqlite(['sku'], productByCategory) 
            
          rescue
            #No hago nada por el momento
          end

        end #end if     

      end #end each
    
    else
      break
    end #end if

  end #end while

end #end each

if error == nil
  ScraperWiki::sqliteexecute("delete from swdata where status = 1")
  ScraperWiki::commit() 
  ScraperWiki::sqliteexecute("update swdata set status = 1 where status = 0")
  ScraperWiki::commit() 
else
 ScraperWiki::sqliteexecute("delete from swdata where status = 0")  
  ScraperWiki::commit() 
end