# Frávega - Scrapper para Productos por categoria
require 'nokogiri'

categories = ["videojuegos/consolas",
              "television-y-video/televisores",
              "informatica/computadoras",
              "informatica/tablets",
              "celulares-telefonos/celulares-libres",
              "climatizacion/aire-acondicionado-split",
              "refrigeracion/heladeras-con-freezer",
              "lavado/lavarropas"
]

#categories = ["television-y-video/televisores",
#              "television-y-video/reproductores",
#              "television-y-video/proyectores",
#              "television-y-video/accesorios",
#              "television-y-video/sintonizadores-tv-digital",
#              "celulares-telefonos/celulares-libres",
#              "celulares-telefonos/celulares-de-operadores",
#              "celulares-telefonos/accesorios",
#              "celulares-telefonos/telefonia-fija",
#              "camaras-video-camaras/camaras-fotograficas"
#]

html = ScraperWiki.scrape "http://www.fravega.com/"
doc = Nokogiri::HTML(html, nil, 'utf-8')
error = nil

doc.search(".categories .subcats p").each do |item|

  lastPage = false
  pageIndex = 0
  pagesCount = 10
  
  categoryUrl = item.css("a")[0]["href"] + "?p="
  categoryName = categoryUrl.split("/")[4].split(".")[0]
  subCategoryName = categoryUrl.split("/")[5].split(".")[0]

  if (categories.include?("#{categoryName}/#{subCategoryName}"))
    p "Procesando #{categoryName}/#{subCategoryName}"
    
    while !lastPage
      pageIndex = pageIndex + 1
      productsDoc = nil
      
      if (pageIndex <= pagesCount)
        begin
          productsHtml = ScraperWiki.scrape categoryUrl + pageIndex.to_s
          productsDoc = Nokogiri::HTML(productsHtml , nil, 'utf-8')
          
          pagesCount = 0
          pages = productsDoc.search(".toolbar-bottom .toolbar .pager .pages li a:not(.next)")
          
          if pages.count > 0
            if pages.last.content != "..."
              pagesCount = Integer(pages.last.content)
            else
              pagesCount = Integer(pages[pages.count - 2].content)
            end
          end

          p "pagesCount: #{pagesCount }"
        rescue Exception => e
          error = e
          p "Error #{error} al ejecutar #{categoryUrl + pageIndex.to_s}"
        end
      else
        lastPage = true
      end
      
      if !productsDoc.nil? 
        productsDoc.search("#category-products .item").each do |product| 
          detailUrl = product.css(".product-name a")[0]["href"]
          
          begin
            detailHtml = ScraperWiki.scrape detailUrl 
            detailDoc = Nokogiri::HTML(detailHtml , nil, 'utf-8')
          rescue Exception => e
            detailHtml = ""
            detailDoc = ""
            error = e
            p "Error #{error} al ejecutar #{detailUrl}"
            #break
          end
          
          if detailHtml != ""
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
                subCategory: subCategoryName,
                status: 0,
              }   
          
              ScraperWiki::save_sqlite(['sku'], productByCategory) 
              
            rescue
              #No hago nada por el momento
            end

          end #end if     
          
        end #end each
      
      end #end if
      
    end #end while
    
    if error == nil
      ScraperWiki::sqliteexecute("delete from swdata where status = 1 and category='#{categoryName}' and subCategory='#{subCategoryName}'")
      ScraperWiki::commit() 
      ScraperWiki::sqliteexecute("update swdata set status = 1 where status = 0 and category='#{categoryName}' and subCategory='#{subCategoryName}'")
      ScraperWiki::commit() 
    else
      error = nil
    end
    
  end #end if
  
end #end each

