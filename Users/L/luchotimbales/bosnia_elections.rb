# Programa en Ruby para obtener información de senadores españoles

zona={}
zona [0]="512"
zona [1]="511"
zona [2]="513"
zona [3]="514"
zona [4]="515"
zona [5]="521"
zona [6]="522"
zona [7]="523"

$municipio={}, distrito={},$id_mun={},id_dis={},url_mun={},url_dis={},$counter_mun=0,counter_id=0,counter_url=0

# Primera pantalla

puts "********************Primera Parte************************************************************************************" 
for i in 0..7
    url= "http://www.izbori.ba/rezultati/konacni/parlament_bih/bihMainPage.asp?jed="+ zona[i]
    html= ScraperWiki.scrape(url) 
    require 'nokogiri'
    
    doc = Nokogiri::HTML(html, nil, 'utf-8')
    doc.search('td> a> span[@class="style7"]').each do |muni|
    #puts "municipio: "+ muni.inner_html
    $municipio[$counter_mun]=muni.inner_html
    $counter_mun=$counter_mun+1
    end
    puts "added municipios zona "+ zona[i]
    
    doc.search('table[@class="style7"]> tr> td[@width="50"]').each do |id| 
    #puts "id: "+ id.inner_html
    $id_mun[counter_id]=id.inner_html.gsub(" ","")
    counter_id=counter_id+1
    end
    puts "added ids zona "+ zona[i]
      
    counter=0  
    doc.search('table[@class="style7"]> tr> td> a').each do |url|
    #puts url['href']
    url_mun[counter_url]=url['href'].gsub("..", "http://www.izbori.ba/rezultati/konacni")
    url_mun[counter_url]=url_mun[counter_url].gsub(" ", "")    
    #puts "url :"+ url_mun[counter_url]
    counter_url=counter_url+1
    end
    puts "added urls zona "+ zona[i]
    
    #for j in 0..counter_url-1
    #  ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> id_mun[j], "Municipio"=> municipio[j], "URL"=> url_mun[j]})
    #end
    #puts "added data to table zona "+ zona[i]

end

#segunda pantalla
puts "********************Segunda Parte************************************************************************************"

$url_resultados_globales_municipio={}
counter_part2=0

for j in 0..$counter_mun-1
  puts url_mun[j]
  url= url_mun[j]  
  html= ScraperWiki.scrape(url)
  puts html
  doc = Nokogiri::HTML(html, nil, 'utf-8') 
  doc.search('td> a').each do |linea|
    #puts "linea: "+ linea.inner_html
    if counter_part2==0 then
       $url_resultados_globales_municipio[j]="http://www.izbori.ba/rezultati/konacni/"+ linea['href']
       puts "url resultados globales:"+ $url_resultados_globales_municipio[j]
       puts "municipio: "+ $municipio[j]
       counter_part2= counter_part2+1
    else    
        nombre2= linea.inner_html.gsub(/<\/?[^>]*>/,"")
        #puts "nombre 2: "+ nombre2
    end
  end
  
  doc.search('div> a> span[@class="style14"]').each do |linea|
    if counter_part2==1
      #puts "id distrito: "+ linea.inner_html
      #puts "url"+ linea.parent['href']
      url_distrito="http://www.izbori.ba/rezultati/konacni/"+ linea.parent['href']
      id_distrito=linea.inner_html
      counter_part2= counter_part2+1
    else
      if counter_part2==2
        #puts "nombre 1: "+ linea.inner_html
        nombre1=linea.inner_html
        counter_part2= 1
      end
    end
    counter_part2=0
  end
end

#tercera pantalla - empezamos con los resultados globales por municipio
puts "********************Tercera Parte************************************************************************************"

counter_part3=0

for j in 0..$counter_mun-1
  puts "tercera url"+ $url_resultados_globales_municipio[j]
  
  html=ScraperWiki.scrape($url_resultados_globales_municipio[j])
  puts html
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('table[@class="style7"]> tr> td').each do |linea|
    #puts "linea resultados: "+ linea.inner_html
    if counter_part3==00
      counter_part3=1
    else
      if counter_part3==1
        $id_partido=linea.inner_html
        puts "id partido: "+ $id_partido
        counter_part3=2
      else
        if counter_part3==2
          $partido=linea.inner_html.gsub(/<\/?[^>]*>/,"")
          puts "partido: "+ $partido
          counter_part3=3
        else
          if counter_part3==3
            $resultados=linea.inner_html.gsub(/<\/?[^>]*>/,"")
            puts "resultados: "+ $resultados
            counter_part3=0
            ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_partido+"_"+$id_mun[j], "Municipio"=> $municipio[j], "Partido"=> $partido, "resultados"=> $resultados})
          end
        end
      end
    end
  end
end
