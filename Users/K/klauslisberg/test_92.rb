require 'nokogiri'

html = ScraperWiki.scrape('http://www.onlinenewspapers.com')


html = ScraperWiki.scrape('http://www.kokuna.dk/dyner/medium-1.html')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='category-products']")

for v in parent.search("li")
data = {
    'src' => "koa",
    'navn' => v.css(".product-name").text,  
    'size' => v.css(".product-size").text,
    'type' => v.css(".product-season").text,
    'oldprice' => v.css(".old-price").text,
    'specialprice' => v.css(".special-price").text,
    'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['time', 'navn','size','type', 'specialprice'], data=data)
end

html = ScraperWiki.scrape('http://www.kokuna.dk/dyner/varm.html')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='category-products']")

for v in parent.search("li")
data = {
    'src' => "koa",
    'navn' => v.css(".product-name").text,  
    'size' => v.css(".product-size").text,
    'type' => v.css(".product-season").text,
    'oldprice' => v.css(".old-price").text,
    'specialprice' => v.css(".special-price").text,
    'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['time', 'navn','size','type', 'specialprice'], data=data)
end

html = ScraperWiki.scrape('http://www.kokuna.dk/puder/alle-storrelser.html')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='category-products']")

for v in parent.search("li")
data = {
    'src' => "koa",
    'navn' => v.css(".product-name").text,  
    'size' => v.css(".product-size").text,
    'type' => v.css(".product-season").text,
    'oldprice' => v.css(".old-price").text,
    'specialprice' => v.css(".special-price").text,
    'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['time', 'navn','size','type', 'specialprice'], data=data)
end



html = ScraperWiki.scrape('http://www.tinga.dk/silkedyner_og_puder-c-89.html')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//form[@name='product_list']")

for v in parent
data = {
      'src' => "tia",
      'navn' => v.xpath(".//td[@align='left']").first.xpath(".//a").text,               
      'size' => v.xpath(".//td[@align='left']").first.xpath(".//p").text,   
      'oldprice' => v.xpath(".//td[@align='left']").last.xpath(".//s").text,            
      'specialprice' => v.xpath(".//td[@align='left']").last.xpath(".//span").text,

      'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['src', 'time', 'navn', 'size', 'oldprice', 'specialprice'], data=data)
end



require 'nokogiri'

html = ScraperWiki.scrape('http://www.dynehuset.dk/alt-i-silkedyner-og-hovedpuder/sommerdyner')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='product']")

for v in parent
specialprice = v.xpath(".//div[@class='product_price']").xpath(".//font[@color='red']").text
if(specialprice.empty?)   
   specialprice = v.xpath(".//div[@class='product_price']").text
end

data = {
      'src' => "dyt",
      'navn' => v.xpath(".//h2").text,               
      'size' => v.xpath(".//div[@class='product_description']").text,   
      'oldprice' => v.xpath(".//div[@class='product_price']").xpath(".//font[@style='text-decoration: line-through;']").text,                  
      'specialprice' => specialprice,            
      'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['src', 'time', 'navn', 'size', 'specialprice', 'oldprice'], data=data)
end

html = ScraperWiki.scrape('http://www.dynehuset.dk/alt-i-silkedyner-og-hovedpuder/helarsdyner')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='product']")

for v in parent
specialprice = v.xpath(".//div[@class='product_price']").xpath(".//font[@color='red']").text
if(specialprice.empty?)   
   specialprice = v.xpath(".//div[@class='product_price']").text
end

data = {
      'src' => "dyt",
      'navn' => v.xpath(".//h2").text,               
      'size' => v.xpath(".//div[@class='product_description']").text,   
      'oldprice' => v.xpath(".//div[@class='product_price']").xpath(".//font[@style='text-decoration: line-through;']").text,                  
      'specialprice' => specialprice,            
      'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['src', 'time', 'navn', 'size', 'oldprice', 'specialprice'], data=data)
end

html = ScraperWiki.scrape('http://www.dynehuset.dk/alt-i-silkedyner-og-hovedpuder/helarsdyner-lune')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='product']")

for v in parent
specialprice = v.xpath(".//div[@class='product_price']").xpath(".//font[@color='red']").text
  if(specialprice.empty?)   
   specialprice = v.xpath(".//div[@class='product_price']").text
end


data = {
      'src' => "dyt",
      'navn' => v.xpath(".//h2").text,               
      'size' => v.xpath(".//div[@class='product_description']").text,   
      'oldprice' => v.xpath(".//div[@class='product_price']").xpath(".//font[@style='text-decoration: line-through;']").text,                  
      'specialprice' => specialprice,            
      'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['src', 'time', 'navn', 'size', 'oldprice', 'specialprice'],data=data)
end

html = ScraperWiki.scrape('http://www.dynehuset.dk/alt-i-silkedyner-og-hovedpuder/hovedpuder')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='product']")

for v in parent
specialprice = v.xpath(".//div[@class='product_price']").xpath(".//font[@color='red']").text
  if(specialprice.empty?)   
   specialprice = v.xpath(".//div[@class='product_price']").text
end

data = {
      'src' => "dyt",
      'navn' => v.xpath(".//h2").text,               
      'size' => v.xpath(".//div[@class='product_description']").text,   
      'oldprice' => v.xpath(".//div[@class='product_price']").xpath(".//font[@style='text-decoration: line-through;']").text,                  
      'specialprice' => specialprice,            
      'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['src', 'time', 'navn', 'size', 'oldprice', 'specialprice'], data=data)
end




require 'nokogiri'

html = ScraperWiki.scrape('http://www.onlinenewspapers.com')


html = ScraperWiki.scrape('http://www.kokuna.dk/dyner/medium-1.html')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='category-products']")

for v in parent.search("li")
data = {
    'src' => "koa",
    'navn' => v.css(".product-name").text,  
    'size' => v.css(".product-size").text,
    'type' => v.css(".product-season").text,
    'oldprice' => v.css(".old-price").text,
    'specialprice' => v.css(".special-price").text,
    'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['time', 'navn','size','type', 'specialprice'], data=data)
end

html = ScraperWiki.scrape('http://www.kokuna.dk/dyner/varm.html')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='category-products']")

for v in parent.search("li")
data = {
    'src' => "koa",
    'navn' => v.css(".product-name").text,  
    'size' => v.css(".product-size").text,
    'type' => v.css(".product-season").text,
    'oldprice' => v.css(".old-price").text,
    'specialprice' => v.css(".special-price").text,
    'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['time', 'navn','size','type', 'specialprice'], data=data)
end

html = ScraperWiki.scrape('http://www.kokuna.dk/puder/alle-storrelser.html')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='category-products']")

for v in parent.search("li")
data = {
    'src' => "koa",
    'navn' => v.css(".product-name").text,  
    'size' => v.css(".product-size").text,
    'type' => v.css(".product-season").text,
    'oldprice' => v.css(".old-price").text,
    'specialprice' => v.css(".special-price").text,
    'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['time', 'navn','size','type', 'specialprice'], data=data)
end



html = ScraperWiki.scrape('http://www.tinga.dk/silkedyner_og_puder-c-89.html')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//form[@name='product_list']")

for v in parent
data = {
      'src' => "tia",
      'navn' => v.xpath(".//td[@align='left']").first.xpath(".//a").text,               
      'size' => v.xpath(".//td[@align='left']").first.xpath(".//p").text,   
      'oldprice' => v.xpath(".//td[@align='left']").last.xpath(".//s").text,            
      'specialprice' => v.xpath(".//td[@align='left']").last.xpath(".//span").text,

      'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['src', 'time', 'navn', 'size', 'oldprice', 'specialprice'], data=data)
end



require 'nokogiri'

html = ScraperWiki.scrape('http://www.dynehuset.dk/alt-i-silkedyner-og-hovedpuder/sommerdyner')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='product']")

for v in parent
specialprice = v.xpath(".//div[@class='product_price']").xpath(".//font[@color='red']").text
if(specialprice.empty?)   
   specialprice = v.xpath(".//div[@class='product_price']").text
end

data = {
      'src' => "dyt",
      'navn' => v.xpath(".//h2").text,               
      'size' => v.xpath(".//div[@class='product_description']").text,   
      'oldprice' => v.xpath(".//div[@class='product_price']").xpath(".//font[@style='text-decoration: line-through;']").text,                  
      'specialprice' => specialprice,            
      'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['src', 'time', 'navn', 'size', 'specialprice', 'oldprice'], data=data)
end

html = ScraperWiki.scrape('http://www.dynehuset.dk/alt-i-silkedyner-og-hovedpuder/helarsdyner')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='product']")

for v in parent
specialprice = v.xpath(".//div[@class='product_price']").xpath(".//font[@color='red']").text
if(specialprice.empty?)   
   specialprice = v.xpath(".//div[@class='product_price']").text
end

data = {
      'src' => "dyt",
      'navn' => v.xpath(".//h2").text,               
      'size' => v.xpath(".//div[@class='product_description']").text,   
      'oldprice' => v.xpath(".//div[@class='product_price']").xpath(".//font[@style='text-decoration: line-through;']").text,                  
      'specialprice' => specialprice,            
      'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['src', 'time', 'navn', 'size', 'oldprice', 'specialprice'], data=data)
end

html = ScraperWiki.scrape('http://www.dynehuset.dk/alt-i-silkedyner-og-hovedpuder/helarsdyner-lune')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='product']")

for v in parent
specialprice = v.xpath(".//div[@class='product_price']").xpath(".//font[@color='red']").text
  if(specialprice.empty?)   
   specialprice = v.xpath(".//div[@class='product_price']").text
end


data = {
      'src' => "dyt",
      'navn' => v.xpath(".//h2").text,               
      'size' => v.xpath(".//div[@class='product_description']").text,   
      'oldprice' => v.xpath(".//div[@class='product_price']").xpath(".//font[@style='text-decoration: line-through;']").text,                  
      'specialprice' => specialprice,            
      'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['src', 'time', 'navn', 'size', 'oldprice', 'specialprice'],data=data)
end

html = ScraperWiki.scrape('http://www.dynehuset.dk/alt-i-silkedyner-og-hovedpuder/hovedpuder')

doc = Nokogiri::HTML(html)

parent = doc.xpath("//div[@class='product']")

for v in parent
specialprice = v.xpath(".//div[@class='product_price']").xpath(".//font[@color='red']").text
  if(specialprice.empty?)   
   specialprice = v.xpath(".//div[@class='product_price']").text
end

data = {
      'src' => "dyt",
      'navn' => v.xpath(".//h2").text,               
      'size' => v.xpath(".//div[@class='product_description']").text,   
      'oldprice' => v.xpath(".//div[@class='product_price']").xpath(".//font[@style='text-decoration: line-through;']").text,                  
      'specialprice' => specialprice,            
      'time' => Time.now.strftime("%Y-%m-%d")
    }     
    ScraperWiki.save_sqlite(unique_keys=['src', 'time', 'navn', 'size', 'oldprice', 'specialprice'], data=data)
end




