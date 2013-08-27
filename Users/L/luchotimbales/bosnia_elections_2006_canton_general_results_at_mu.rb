# Programa en Ruby para obtener información de senadores españoles

zona={}
zona [0]="201"
zona [1]="202"
zona [2]="203"
zona [3]="204"
zona [4]="205"
zona [5]="206"
zona [6]="207"
zona [7]="208"
zona [8]="209"
zona [9]="210"

$provincia={},$municipio={}, distrito={},$id_mun={},id_dis={},url_mun={},url_dis={},$counter_mun=0,counter_id=0,counter_url=0

# Primera pantalla

puts "********************Primera Parte************************************************************************************"
for i in 3..9
    url= "http://www.izbori.ba/rezultati/konacni/kantoni/cantonsMainPage.asp?jed="+ zona[i]
    html= ScraperWiki.scrape(url)
    require 'nokogiri'
    
    doc = Nokogiri::HTML(html, nil, 'utf-8')
    doc.search('td> a> span[@class="style7"]').each do |muni|
    #puts "municipio: "+ muni.inner_html
    $municipio[$counter_mun]=muni.inner_html
    $provincia[$counter_mun]=zona[i]
    $counter_mun=$counter_mun+1
    end
    puts "added municipios zona "+ zona[i]
    
    doc.search('table[@class="style7"]> tr> td[@width="50"]').each do |id|
    #puts "id: "+ id.inner_html
    temp=id.inner_html.to_i()
    if temp< 10 
      $id_mun[counter_id]="00"+ temp.to_s() 
    else
      if temp<100
        $id_mun[counter_id]="0"+ temp.to_s() 
      else
        $id_mun[counter_id]= temp.to_s() 
      end
    end
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

counter_part3=0

for j in 0..$counter_mun-1
  url="http://www.izbori.ba/rezultati/konacni/PoOsnovnimJedinicamaUkupno.asp?nivo="+$provincia[j]+"&kod="+ $id_mun[j]
  puts "LA URL de los datos "+ url +".."
  html=ScraperWiki.scrape(url)
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
            ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_partido +"_"+$id_mun[j], "Municipio"=> $municipio[j],"Provincia"=> $provincia[j],"Partido"=> $partido, "resultados"=> $resultados})
          end
        end
      end
    end
  end
end
# Programa en Ruby para obtener información de senadores españoles

zona={}
zona [0]="201"
zona [1]="202"
zona [2]="203"
zona [3]="204"
zona [4]="205"
zona [5]="206"
zona [6]="207"
zona [7]="208"
zona [8]="209"
zona [9]="210"

$provincia={},$municipio={}, distrito={},$id_mun={},id_dis={},url_mun={},url_dis={},$counter_mun=0,counter_id=0,counter_url=0

# Primera pantalla

puts "********************Primera Parte************************************************************************************"
for i in 3..9
    url= "http://www.izbori.ba/rezultati/konacni/kantoni/cantonsMainPage.asp?jed="+ zona[i]
    html= ScraperWiki.scrape(url)
    require 'nokogiri'
    
    doc = Nokogiri::HTML(html, nil, 'utf-8')
    doc.search('td> a> span[@class="style7"]').each do |muni|
    #puts "municipio: "+ muni.inner_html
    $municipio[$counter_mun]=muni.inner_html
    $provincia[$counter_mun]=zona[i]
    $counter_mun=$counter_mun+1
    end
    puts "added municipios zona "+ zona[i]
    
    doc.search('table[@class="style7"]> tr> td[@width="50"]').each do |id|
    #puts "id: "+ id.inner_html
    temp=id.inner_html.to_i()
    if temp< 10 
      $id_mun[counter_id]="00"+ temp.to_s() 
    else
      if temp<100
        $id_mun[counter_id]="0"+ temp.to_s() 
      else
        $id_mun[counter_id]= temp.to_s() 
      end
    end
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

counter_part3=0

for j in 0..$counter_mun-1
  url="http://www.izbori.ba/rezultati/konacni/PoOsnovnimJedinicamaUkupno.asp?nivo="+$provincia[j]+"&kod="+ $id_mun[j]
  puts "LA URL de los datos "+ url +".."
  html=ScraperWiki.scrape(url)
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
            ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_partido +"_"+$id_mun[j], "Municipio"=> $municipio[j],"Provincia"=> $provincia[j],"Partido"=> $partido, "resultados"=> $resultados})
          end
        end
      end
    end
  end
end
# Programa en Ruby para obtener información de senadores españoles

zona={}
zona [0]="201"
zona [1]="202"
zona [2]="203"
zona [3]="204"
zona [4]="205"
zona [5]="206"
zona [6]="207"
zona [7]="208"
zona [8]="209"
zona [9]="210"

$provincia={},$municipio={}, distrito={},$id_mun={},id_dis={},url_mun={},url_dis={},$counter_mun=0,counter_id=0,counter_url=0

# Primera pantalla

puts "********************Primera Parte************************************************************************************"
for i in 3..9
    url= "http://www.izbori.ba/rezultati/konacni/kantoni/cantonsMainPage.asp?jed="+ zona[i]
    html= ScraperWiki.scrape(url)
    require 'nokogiri'
    
    doc = Nokogiri::HTML(html, nil, 'utf-8')
    doc.search('td> a> span[@class="style7"]').each do |muni|
    #puts "municipio: "+ muni.inner_html
    $municipio[$counter_mun]=muni.inner_html
    $provincia[$counter_mun]=zona[i]
    $counter_mun=$counter_mun+1
    end
    puts "added municipios zona "+ zona[i]
    
    doc.search('table[@class="style7"]> tr> td[@width="50"]').each do |id|
    #puts "id: "+ id.inner_html
    temp=id.inner_html.to_i()
    if temp< 10 
      $id_mun[counter_id]="00"+ temp.to_s() 
    else
      if temp<100
        $id_mun[counter_id]="0"+ temp.to_s() 
      else
        $id_mun[counter_id]= temp.to_s() 
      end
    end
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

counter_part3=0

for j in 0..$counter_mun-1
  url="http://www.izbori.ba/rezultati/konacni/PoOsnovnimJedinicamaUkupno.asp?nivo="+$provincia[j]+"&kod="+ $id_mun[j]
  puts "LA URL de los datos "+ url +".."
  html=ScraperWiki.scrape(url)
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
            ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_partido +"_"+$id_mun[j], "Municipio"=> $municipio[j],"Provincia"=> $provincia[j],"Partido"=> $partido, "resultados"=> $resultados})
          end
        end
      end
    end
  end
end
