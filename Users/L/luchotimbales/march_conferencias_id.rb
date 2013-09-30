titulo=String.new
url_resultado=String.new
record={}

for i in 1..236
    url= "http://www.march.es/conferencias/anteriores/?p0="+ i.to_s()+"&l=1"
    html= ScraperWiki.scrape(url,encoding="utf-8")     
    puts html
          
    html2 = html.slice (html.index("RESULTADOS")+14..html.index("FIN PRESENTACI")-30)
    puts html2
    
    require 'nokogiri'
    doc = Nokogiri::HTML(html2 , nil, 'utf-8')
    puts doc
    counter=0
    doc.search('div[@class="fototitulo"]').each do |row|
      puts "http://www.march.es"+ row.css('a').attr('href')
      puts row.css('a[@class="nombreciclo"]').text
      url_resultado="http://www.march.es"+ row.css('a').attr('href')
      titulo= row.css('a[@class="nombreciclo"]').text

      if url_resultado.include?"/conferencias/detalle" then      
        record ['ID']= "Page: " + i.to_s() +" Conferencia: "+ counter.to_s()
        record ['URL conferencia']= url_resultado
        record ['Titulo']= titulo
        ScraperWiki.save_sqlite(["ID"], record)
        counter=counter+1
      end

    end
counter=0
end    titulo=String.new
url_resultado=String.new
record={}

for i in 1..236
    url= "http://www.march.es/conferencias/anteriores/?p0="+ i.to_s()+"&l=1"
    html= ScraperWiki.scrape(url,encoding="utf-8")     
    puts html
          
    html2 = html.slice (html.index("RESULTADOS")+14..html.index("FIN PRESENTACI")-30)
    puts html2
    
    require 'nokogiri'
    doc = Nokogiri::HTML(html2 , nil, 'utf-8')
    puts doc
    counter=0
    doc.search('div[@class="fototitulo"]').each do |row|
      puts "http://www.march.es"+ row.css('a').attr('href')
      puts row.css('a[@class="nombreciclo"]').text
      url_resultado="http://www.march.es"+ row.css('a').attr('href')
      titulo= row.css('a[@class="nombreciclo"]').text

      if url_resultado.include?"/conferencias/detalle" then      
        record ['ID']= "Page: " + i.to_s() +" Conferencia: "+ counter.to_s()
        record ['URL conferencia']= url_resultado
        record ['Titulo']= titulo
        ScraperWiki.save_sqlite(["ID"], record)
        counter=counter+1
      end

    end
counter=0
end    titulo=String.new
url_resultado=String.new
record={}

for i in 1..236
    url= "http://www.march.es/conferencias/anteriores/?p0="+ i.to_s()+"&l=1"
    html= ScraperWiki.scrape(url,encoding="utf-8")     
    puts html
          
    html2 = html.slice (html.index("RESULTADOS")+14..html.index("FIN PRESENTACI")-30)
    puts html2
    
    require 'nokogiri'
    doc = Nokogiri::HTML(html2 , nil, 'utf-8')
    puts doc
    counter=0
    doc.search('div[@class="fototitulo"]').each do |row|
      puts "http://www.march.es"+ row.css('a').attr('href')
      puts row.css('a[@class="nombreciclo"]').text
      url_resultado="http://www.march.es"+ row.css('a').attr('href')
      titulo= row.css('a[@class="nombreciclo"]').text

      if url_resultado.include?"/conferencias/detalle" then      
        record ['ID']= "Page: " + i.to_s() +" Conferencia: "+ counter.to_s()
        record ['URL conferencia']= url_resultado
        record ['Titulo']= titulo
        ScraperWiki.save_sqlite(["ID"], record)
        counter=counter+1
      end

    end
counter=0
end    titulo=String.new
url_resultado=String.new
record={}

for i in 1..236
    url= "http://www.march.es/conferencias/anteriores/?p0="+ i.to_s()+"&l=1"
    html= ScraperWiki.scrape(url,encoding="utf-8")     
    puts html
          
    html2 = html.slice (html.index("RESULTADOS")+14..html.index("FIN PRESENTACI")-30)
    puts html2
    
    require 'nokogiri'
    doc = Nokogiri::HTML(html2 , nil, 'utf-8')
    puts doc
    counter=0
    doc.search('div[@class="fototitulo"]').each do |row|
      puts "http://www.march.es"+ row.css('a').attr('href')
      puts row.css('a[@class="nombreciclo"]').text
      url_resultado="http://www.march.es"+ row.css('a').attr('href')
      titulo= row.css('a[@class="nombreciclo"]').text

      if url_resultado.include?"/conferencias/detalle" then      
        record ['ID']= "Page: " + i.to_s() +" Conferencia: "+ counter.to_s()
        record ['URL conferencia']= url_resultado
        record ['Titulo']= titulo
        ScraperWiki.save_sqlite(["ID"], record)
        counter=counter+1
      end

    end
counter=0
end    