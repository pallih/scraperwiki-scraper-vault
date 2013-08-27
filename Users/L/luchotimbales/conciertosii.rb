# Blank Ruby
# Ruby for collection of concerts

$Concierto =""
$Fecha =""
$Lugar =""
$Ciudad=""
$URL=""
$Reviewer=""

obras={},compositor={},interprete={}, instrumento={},  

$obra_compositor={}, $Url_concert={}


puts "*********************STARTING***************"
puts "*********************Getting list of concerts***************"

# Getting list of concerts
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=conciertos&query=select%20*%20from%20%60swdata%60%20limit%20100000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('tr').each do |datos|
  if l==0 then
  else
    #puts datos.css("td")[0].inner_html
    $Url_concert[l-1]=datos.css("td")[0].inner_html
  end
  l=l+1
end

puts "*********************STARTING***************"
puts "*********************Getting list of concerts***************"

for i in 2654..2654
          puts "******************concierto # "+ i.to_s() +"********************"
          num_obras=0
          num_compositores=0
          num_instrumentos=0
          
          $URL=$Url_concert[i]
          puts $URL
          
          html = ScraperWiki.scrape($URL)
          puts html
          counter=1
            
            require 'nokogiri'
            
            # titulo del concierto
            doc = Nokogiri::HTML(html, nil, 'utf-8')
            doc.search('h1').each do |row|
              $Concierto = row.text
            end
            
            # fecha
            doc.search('span[@property="v:dtreviewed"]').each do |row|
              $Fecha = row.text
            end
            
            # lugar
            doc.search('span[@property="v:itemreviewed"]').each do |row|
              $Lugar = row.css("a")[0].text
              if not row.css("a")[1].nil? then
                $Ciudad = row.css("a")[1].text
                puts "$Ciudad"
              else
                $Ciudad =""
              end
            end
            
            # compositores y obras
            doc.search('div[@style="margin-bottom:5px"]').each do |row|
            $obra_compositor[num_obras]=row.text
              if not   obras[num_obras]=row.css("a")[0].nil?  then
                obras[num_obras]=row.css("a")[0].text
              else
                obras[num_obras]=""  
              end
              if not  compositor[num_obras]=row.css("a")[1].nil?  then
                compositor[num_obras]=row.css("a")[1].text
              else
                compositor[num_obras]=""
              end
              num_obras=num_obras+1
            end
            
            #interpretes
            doc.search('td[@rowspan="2"]> div[@class="eventperformers"]> strong').each do |row|
              #puts "interpretes: "+ row
              interprete[num_compositores]=row.text
              num_compositores=num_compositores+1
            end

            #instrumentos
            doc.search('td[@rowspan="2"]> div[@class="eventperformers"]> a').each do |row|
              #puts "instrumento: "+ row
              instrumento[num_instrumentos]=row.text
              num_instrumentos=num_instrumentos+1
            end
            
            if num_compositores > num_instrumentos then
              for k in num_instrumentos..num_compositores
                instrumento[k]=""
              end
            end
            # juntar interpretes e instrumentos 
            interpretes_juntos=""
            iteraciones =num_compositores-1
            puts "iteraciones :"+ iteraciones.to_s()
            for t in 0..iteraciones-1
                interpretes_juntos = interpretes_juntos + interprete[t] +" ("+ instrumento[t] +"); "
            end

            #debugging
            puts "concierto: "+ $Concierto
            puts "fecha: "+ $Fecha
            puts "url: "+ $URL
            puts "lugar: "+ $Lugar
            puts "ciudad: "+ $Ciudad
            puts "# obras: "+ num_obras.to_s()
            puts "obras: "+ obras.to_s()
            puts "compositores: "+ compositor.to_s()
            puts "# interpretes: "+ num_compositores.to_s()
            puts "# instrumentos: "+ num_instrumentos.to_s()
            puts "interpretes e instrumentos: "+ interpretes_juntos

            #guardamos los datos
          
            for j in 0..(num_obras/2)-1
            
                  record={}
                  record ['ID']= $URL +"_"+ j.to_s()
                  record ['Concierto']= $Concierto
                  record ['ConciertoID']= i.to_s()
                  record ['Fecha']= $Fecha
                  record ['URL']= $URL
                  record ['Lugar']=$Lugar
                  record ['Ciudad']=$Ciudad
                  record ['Compositor']= compositor[j]
                  record ['Obra']= obras[j]
                  record ['Obra_Compositor']= $obra_compositor[j]
                  record ['Interpretes']= interpretes_juntos
                  ScraperWiki.save_sqlite(["ID"], record)
          
          
            end
end
# Blank Ruby
# Ruby for collection of concerts

$Concierto =""
$Fecha =""
$Lugar =""
$Ciudad=""
$URL=""
$Reviewer=""

obras={},compositor={},interprete={}, instrumento={},  

$obra_compositor={}, $Url_concert={}


puts "*********************STARTING***************"
puts "*********************Getting list of concerts***************"

# Getting list of concerts
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=conciertos&query=select%20*%20from%20%60swdata%60%20limit%20100000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('tr').each do |datos|
  if l==0 then
  else
    #puts datos.css("td")[0].inner_html
    $Url_concert[l-1]=datos.css("td")[0].inner_html
  end
  l=l+1
end

puts "*********************STARTING***************"
puts "*********************Getting list of concerts***************"

for i in 2654..2654
          puts "******************concierto # "+ i.to_s() +"********************"
          num_obras=0
          num_compositores=0
          num_instrumentos=0
          
          $URL=$Url_concert[i]
          puts $URL
          
          html = ScraperWiki.scrape($URL)
          puts html
          counter=1
            
            require 'nokogiri'
            
            # titulo del concierto
            doc = Nokogiri::HTML(html, nil, 'utf-8')
            doc.search('h1').each do |row|
              $Concierto = row.text
            end
            
            # fecha
            doc.search('span[@property="v:dtreviewed"]').each do |row|
              $Fecha = row.text
            end
            
            # lugar
            doc.search('span[@property="v:itemreviewed"]').each do |row|
              $Lugar = row.css("a")[0].text
              if not row.css("a")[1].nil? then
                $Ciudad = row.css("a")[1].text
                puts "$Ciudad"
              else
                $Ciudad =""
              end
            end
            
            # compositores y obras
            doc.search('div[@style="margin-bottom:5px"]').each do |row|
            $obra_compositor[num_obras]=row.text
              if not   obras[num_obras]=row.css("a")[0].nil?  then
                obras[num_obras]=row.css("a")[0].text
              else
                obras[num_obras]=""  
              end
              if not  compositor[num_obras]=row.css("a")[1].nil?  then
                compositor[num_obras]=row.css("a")[1].text
              else
                compositor[num_obras]=""
              end
              num_obras=num_obras+1
            end
            
            #interpretes
            doc.search('td[@rowspan="2"]> div[@class="eventperformers"]> strong').each do |row|
              #puts "interpretes: "+ row
              interprete[num_compositores]=row.text
              num_compositores=num_compositores+1
            end

            #instrumentos
            doc.search('td[@rowspan="2"]> div[@class="eventperformers"]> a').each do |row|
              #puts "instrumento: "+ row
              instrumento[num_instrumentos]=row.text
              num_instrumentos=num_instrumentos+1
            end
            
            if num_compositores > num_instrumentos then
              for k in num_instrumentos..num_compositores
                instrumento[k]=""
              end
            end
            # juntar interpretes e instrumentos 
            interpretes_juntos=""
            iteraciones =num_compositores-1
            puts "iteraciones :"+ iteraciones.to_s()
            for t in 0..iteraciones-1
                interpretes_juntos = interpretes_juntos + interprete[t] +" ("+ instrumento[t] +"); "
            end

            #debugging
            puts "concierto: "+ $Concierto
            puts "fecha: "+ $Fecha
            puts "url: "+ $URL
            puts "lugar: "+ $Lugar
            puts "ciudad: "+ $Ciudad
            puts "# obras: "+ num_obras.to_s()
            puts "obras: "+ obras.to_s()
            puts "compositores: "+ compositor.to_s()
            puts "# interpretes: "+ num_compositores.to_s()
            puts "# instrumentos: "+ num_instrumentos.to_s()
            puts "interpretes e instrumentos: "+ interpretes_juntos

            #guardamos los datos
          
            for j in 0..(num_obras/2)-1
            
                  record={}
                  record ['ID']= $URL +"_"+ j.to_s()
                  record ['Concierto']= $Concierto
                  record ['ConciertoID']= i.to_s()
                  record ['Fecha']= $Fecha
                  record ['URL']= $URL
                  record ['Lugar']=$Lugar
                  record ['Ciudad']=$Ciudad
                  record ['Compositor']= compositor[j]
                  record ['Obra']= obras[j]
                  record ['Obra_Compositor']= $obra_compositor[j]
                  record ['Interpretes']= interpretes_juntos
                  ScraperWiki.save_sqlite(["ID"], record)
          
          
            end
end
# Blank Ruby
# Ruby for collection of concerts

$Concierto =""
$Fecha =""
$Lugar =""
$Ciudad=""
$URL=""
$Reviewer=""

obras={},compositor={},interprete={}, instrumento={},  

$obra_compositor={}, $Url_concert={}


puts "*********************STARTING***************"
puts "*********************Getting list of concerts***************"

# Getting list of concerts
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=conciertos&query=select%20*%20from%20%60swdata%60%20limit%20100000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('tr').each do |datos|
  if l==0 then
  else
    #puts datos.css("td")[0].inner_html
    $Url_concert[l-1]=datos.css("td")[0].inner_html
  end
  l=l+1
end

puts "*********************STARTING***************"
puts "*********************Getting list of concerts***************"

for i in 2654..2654
          puts "******************concierto # "+ i.to_s() +"********************"
          num_obras=0
          num_compositores=0
          num_instrumentos=0
          
          $URL=$Url_concert[i]
          puts $URL
          
          html = ScraperWiki.scrape($URL)
          puts html
          counter=1
            
            require 'nokogiri'
            
            # titulo del concierto
            doc = Nokogiri::HTML(html, nil, 'utf-8')
            doc.search('h1').each do |row|
              $Concierto = row.text
            end
            
            # fecha
            doc.search('span[@property="v:dtreviewed"]').each do |row|
              $Fecha = row.text
            end
            
            # lugar
            doc.search('span[@property="v:itemreviewed"]').each do |row|
              $Lugar = row.css("a")[0].text
              if not row.css("a")[1].nil? then
                $Ciudad = row.css("a")[1].text
                puts "$Ciudad"
              else
                $Ciudad =""
              end
            end
            
            # compositores y obras
            doc.search('div[@style="margin-bottom:5px"]').each do |row|
            $obra_compositor[num_obras]=row.text
              if not   obras[num_obras]=row.css("a")[0].nil?  then
                obras[num_obras]=row.css("a")[0].text
              else
                obras[num_obras]=""  
              end
              if not  compositor[num_obras]=row.css("a")[1].nil?  then
                compositor[num_obras]=row.css("a")[1].text
              else
                compositor[num_obras]=""
              end
              num_obras=num_obras+1
            end
            
            #interpretes
            doc.search('td[@rowspan="2"]> div[@class="eventperformers"]> strong').each do |row|
              #puts "interpretes: "+ row
              interprete[num_compositores]=row.text
              num_compositores=num_compositores+1
            end

            #instrumentos
            doc.search('td[@rowspan="2"]> div[@class="eventperformers"]> a').each do |row|
              #puts "instrumento: "+ row
              instrumento[num_instrumentos]=row.text
              num_instrumentos=num_instrumentos+1
            end
            
            if num_compositores > num_instrumentos then
              for k in num_instrumentos..num_compositores
                instrumento[k]=""
              end
            end
            # juntar interpretes e instrumentos 
            interpretes_juntos=""
            iteraciones =num_compositores-1
            puts "iteraciones :"+ iteraciones.to_s()
            for t in 0..iteraciones-1
                interpretes_juntos = interpretes_juntos + interprete[t] +" ("+ instrumento[t] +"); "
            end

            #debugging
            puts "concierto: "+ $Concierto
            puts "fecha: "+ $Fecha
            puts "url: "+ $URL
            puts "lugar: "+ $Lugar
            puts "ciudad: "+ $Ciudad
            puts "# obras: "+ num_obras.to_s()
            puts "obras: "+ obras.to_s()
            puts "compositores: "+ compositor.to_s()
            puts "# interpretes: "+ num_compositores.to_s()
            puts "# instrumentos: "+ num_instrumentos.to_s()
            puts "interpretes e instrumentos: "+ interpretes_juntos

            #guardamos los datos
          
            for j in 0..(num_obras/2)-1
            
                  record={}
                  record ['ID']= $URL +"_"+ j.to_s()
                  record ['Concierto']= $Concierto
                  record ['ConciertoID']= i.to_s()
                  record ['Fecha']= $Fecha
                  record ['URL']= $URL
                  record ['Lugar']=$Lugar
                  record ['Ciudad']=$Ciudad
                  record ['Compositor']= compositor[j]
                  record ['Obra']= obras[j]
                  record ['Obra_Compositor']= $obra_compositor[j]
                  record ['Interpretes']= interpretes_juntos
                  ScraperWiki.save_sqlite(["ID"], record)
          
          
            end
end
