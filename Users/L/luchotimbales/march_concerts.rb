ciclo=String.new
url_ciclo=String.new
interpretes=String.new
record={}
$compositores={}

count_records=1

for i in 201..310
    url= "http://www.march.es/musica/publicaciones/buscadormusica/?p0="+ i.to_s() +"&l=1"
    html= ScraperWiki.scrape(url,encoding="utf-8")     
    puts html
          
    html2 = html.slice (html.index("RESULTADOS")+14..html.index("FIN PRESENTACI")-30)
    puts html2
    
    require 'nokogiri'
    doc = Nokogiri::HTML(html2 , nil, 'utf-8')
    puts doc
    counter=0
    doc.search('div[@class="fototitulo"]').each do |row|

      puts row
      puts "http://www.march.es"+ row.css('a').attr('href')
      puts row.css('a[@class="nombreciclo"]').text
      url_ciclo="http://www.march.es"+ row.css('a').attr('href')
      ciclo= row.css('a[@class="nombreciclo"]').text

      for j in 0..row.css('li[@class="tituloConferencia"]').length-1
        puts row.css('li[@class="tituloConferencia"]')[j].text
        concierto =row.css('li[@class="tituloConferencia"]')[j].text
        puts row.css('li[@class="fechaConferencia"]')[j].text
        fecha=row.css('li[@class="fechaConferencia"]')[j].text

         puts "conciertos: "+ row.css('li[@class="tituloConferencia"]').length.to_s() +" interpretes o compositores:" + row.css('li[@class="tituloConferenciantes"]').length.to_s()
        
        if (row.css('li[@class="tituloConferencia"]').length*2) == row.css('li[@class="tituloConferenciantes"]').length then        
            puts row.css('li[@class="tituloConferenciantes"]')[((j+1)*2)-2].text
            interpretes=row.css('li[@class="tituloConferenciantes"]')[((j+1)*2)-2].text
            
            puts row.css('li[@class="tituloConferenciantes"]')[((j+1)*2)-1].text.split(",")
            $compositores=row.css('li[@class="tituloConferenciantes"]')[((j+1)*2)-1].text.split(",")
            
            for k in 0..$compositores.length-1        
                # añadimos fila a los datos
                record ['ID']= "Page: "+ i.to_s() +" Concierto: "+ counter.to_s() + " Compositor: "+ k.to_s() 
                record ['URL ciclo']= url_ciclo
                record ['Titulo Ciclo']= ciclo
                record ['Concierto']= concierto
                record ['Fecha']= fecha
                record ['Interpretes']= interpretes
                record ['Compositores']= $compositores[k]
                record ['Record No']= count_records.to_s()
                ScraperWiki.save_sqlite(["ID"], record)
                counter=counter+1
                count_records=count_records+1
            end
        else
           puts "faltan interpretes o compositores"
           puts row.css('li[@class="tituloConferenciantes"]')[j].text
           interpretes=row.css('li[@class="tituloConferenciantes"]')[j].text
           record ['ID']= "Page: "+ i.to_s() +" Concierto: "+ counter.to_s() + " Compositor: 0"
           record ['URL ciclo']= url_ciclo
           record ['Titulo Ciclo']= ciclo
           record ['Concierto']= concierto
           record ['Fecha']= fecha
           record ['Interpretes']= interpretes
           record ['Compositores']="NA"
           record ['Record No']= count_records.to_s()
           ScraperWiki.save_sqlite(["ID"], record)
           counter=counter+1
           count_records=count_records+1 
        end
      end
      
      for j in 0..row.css('span[@class="tituloConferencia"]').length-1
        puts "paso por span"
        puts row.css('span[@class="tituloConferencia"]')[j].text
        concierto =row.css('span[@class="tituloConferencia"]')[j].text
        puts row.css('span[@class="fechaConferencia"]')[j].text
        fecha=row.css('span[@class="fechaConferencia"]')[j].text
        
        puts "conciertos: "+ row.css('span[@class="tituloConferencia"]').length.to_s() +" interpretes o compositores:" + row.css('li[@class="tituloConferenciantes"]').length.to_s()

        if (row.css('span[@class="tituloConferencia"]').length*2) == row.css('li[@class="tituloConferenciantes"]').length then
            puts row.css('li[@class="tituloConferenciantes"]')[((j+1)*2)-2].text
            interpretes=row.css('li[@class="tituloConferenciantes"]')[((j+1)*2)-2].text
            
            puts row.css('li[@class="tituloConferenciantes"]')[((j+1)*2)-1].text.split(",")
            $compositores=row.css('li[@class="tituloConferenciantes"]')[((j+1)*2)-1].text.split(",")       
            
            for k in 0..$compositores.length-1        
                # añadimos fila a los datos
                record ['ID']= "Page: "+ i.to_s() +" Concierto: "+ counter.to_s() + " Compositor: "+ k.to_s()
                record ['URL ciclo']= url_ciclo
                record ['Titulo Ciclo']= ciclo
                record ['Concierto']= concierto
                record ['Fecha']= fecha
                record ['Interpretes']= interpretes
                record ['Compositores']= $compositores[k]
                record ['Record No']= count_records.to_s()
                ScraperWiki.save_sqlite(["ID"], record)
                counter=counter+1
                count_records=count_records+1
            end
        else
            puts "faltan interpretes o compositores"
            puts row.css('li[@class="tituloConferenciantes"]')[j].text
            interpretes=row.css('li[@class="tituloConferenciantes"]')[j].text
            record ['ID']= "Page: "+ i.to_s() +" Concierto: "+ counter.to_s() + " Compositor: 0"
            record ['URL ciclo']= url_ciclo
            record ['Titulo Ciclo']= ciclo
            record ['Concierto']= concierto
            record ['Fecha']= fecha
            record ['Interpretes']= interpretes
            record ['Compositores']="NA"
            record ['Record No']= count_records.to_s()
            ScraperWiki.save_sqlite(["ID"], record)
            counter=counter+1
            count_records=count_records+1 

        end
      end           
    end

counter=0
end    