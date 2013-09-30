expo=String.new
url_expo=String.new
record={}

count_records=1

for i in 19..19
    url= "http://www.march.es/arte/exposiciones/?p0="+ i.to_s() +"&p1=21&p6=1&l=1"
    html= ScraperWiki.scrape(url,encoding="utf-8")     
    puts html
          
    html2 = html.slice (html.index("RESULTADOS")+14..html.index("FIN PRESENTACI")-30)
    puts html2
    
    require 'nokogiri'
    doc = Nokogiri::HTML(html2 , nil, 'utf-8')
    puts doc
    counter=0
    doc.search('ul[@class="exposicionmostrada"]').each do |row|

      puts row
      
      if not row.css('a').nil? then
        puts "http://www.march.es"+ row.css('a').attr('href')
        url_expo="http://www.march.es"+ row.css('a').attr('href')
      else
        puts "no url"
        url_expo="NA"
      end

      puts row.css('ul[@class="fichatecnica"]>li>strong').text
      puts row.css('ul[@class="fichatecnica"]>li>p').text
      puts row.css('a[@class="enlace"]').text
      expo= row.css('ul[@class="fichatecnica"]>li>strong').text
      expo_desc= row.css('ul[@class="fichatecnica"]>li>p').text
      expo_lugar_fechas=row.css('a[@class="enlace"]').text
      
      
      record ['ID']= "Page: "+ i.to_s() +" Exposicion: "+ counter.to_s() 
      record ['URL ciclo']= url_expo
      record ['Titulo Ciclo']= expo
      record ['Descripcion']= expo_desc
      record ['Lugar y fechas']= expo_lugar_fechas
      ScraperWiki.save_sqlite(["ID"], record)
      counter=counter+1
                   
    end

counter=0
end

record ['ID']= "Page: 16 Exposicion: 8"
record ['URL ciclo']= "NA"
record ['Titulo Ciclo']= "Fernando Pessoa: el eterno viajero"
record ['Descripcion']= " "
record ['Lugar y fechas']= "Madrid, Fundacion Juan March (03/06/1981 - 26/06/1981)"
ScraperWiki.save_sqlite(["ID"], record)

record ['ID']= "Page: 16 Exposicion: 9"
record ['URL ciclo']= "http://www.march.es/arte/exposiciones/exposicion.asp?clave_expo=190"
record ['Titulo Ciclo']= "Mirrors and Windows ('Espejos y ventanas') - Fotografia americana desde 1960"
record ['Descripcion']= "185 fotografias de 101 artistas norteamericanos, muestra del arte de la fotografia en los Estados Unidos desde 1960."
record ['Lugar y fechas']= "Madrid, Fundacion Juan March (22/05/1981 - 28/06/1981)"
ScraperWiki.save_sqlite(["ID"], record)     
