# Programa en Ruby 

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

$provincia={},$municipio={}, $distrito={},$id_mun={},$id_dis={},$id_prov_dis={},url_mun={},url_dis={},$counter_mun=0,counter_id=0,counter_url=0

# Primera pantalla

puts "********************Primera Parte: Municipios************************************************************************************"
for i in 0..0
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
    if temp<10
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
end


#segunda pantalla
puts "********************Segunda Parte: Distritos************************************************************************************"
puts "******Numero de municipios: "+ $counter_mun.to_s()
$counter_dis=0
$counter_dis_names=0

for j in 0..$counter_mun-1
  url="http://www.izbori.ba/rezultati/konacni/PoOsnovnimJedinicamaUkupno.asp?nivo="+$provincia[j].to_s()+"&kod="+ $id_mun[j]
  puts "LA URL "+ url
  html=ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('table[@class="style7"]> tr> td[@width="6%"]').each do |id_dis|
    puts "id_dis"+ id_dis.inner_html
    $id_dis [$counter_dis]=id_dis.inner_html.gsub(/\s+/, "")
    $id_prov_dis[$counter_dis]=$provincia[j]
    $counter_dis=$counter_dis+1
  end
  puts "added id distritos"+ $id_mun[j]


  doc.search('table[@class="style7"]> tr> td > a> span[@class="style7"]').each do |nombres|
    puts "nombre_dis "+ nombres.inner_html
    $distrito[$counter_dis_names]=nombres.inner_html
    $counter_dis_names=$counter_dis_names+1
  end
  puts "added nombres distritos"+ $id_mun[j]

end

puts "********************Tercera Parte: Datos resultados************************************************************************************"
puts "******Numero de distritos: "+ $counter_dis_names.to_s()

counter_part3=0

for j in 0..$counter_dis-1
    url="http://www.izbori.ba/rezultati/konacni/PoOsnovnimJedinicama2.asp?nivo="+ $id_prov_dis[j] +"&Polling="+ $id_dis [j]
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
          #puts "id partido: "+ $id_partido
          counter_part3=2
        else
          if counter_part3==2
            $partido=linea.inner_html.gsub(/<\/?[^>]*>/,"")
            #puts "partido: "+ $partido
            counter_part3=3
          else
            if counter_part3==3
              $resultados=linea.inner_html.gsub(/<\/?[^>]*>/,"")
              #puts "resultados: "+ $resultados
              counter_part3=0
              ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_partido +"_"+$id_dis[j].to_s(), "ID Municipio"=> $id_mun[j], "Municipio"=> $municipio[j], "Distrito"=>$distrito[j],"ID Distrito"=>$id_dis[j],"ID Partido"=> $id_partido,"Partido"=> $partido, "resultados"=> $resultados})
              
            end
          end
        end
      end
    end
    puts "Provincia: "+$provincia[j] +" y distrito: "+ $id_dis [j]
end



# Programa en Ruby 

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

$provincia={},$municipio={}, $distrito={},$id_mun={},$id_dis={},$id_prov_dis={},url_mun={},url_dis={},$counter_mun=0,counter_id=0,counter_url=0

# Primera pantalla

puts "********************Primera Parte: Municipios************************************************************************************"
for i in 0..0
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
    if temp<10
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
end


#segunda pantalla
puts "********************Segunda Parte: Distritos************************************************************************************"
puts "******Numero de municipios: "+ $counter_mun.to_s()
$counter_dis=0
$counter_dis_names=0

for j in 0..$counter_mun-1
  url="http://www.izbori.ba/rezultati/konacni/PoOsnovnimJedinicamaUkupno.asp?nivo="+$provincia[j].to_s()+"&kod="+ $id_mun[j]
  puts "LA URL "+ url
  html=ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('table[@class="style7"]> tr> td[@width="6%"]').each do |id_dis|
    puts "id_dis"+ id_dis.inner_html
    $id_dis [$counter_dis]=id_dis.inner_html.gsub(/\s+/, "")
    $id_prov_dis[$counter_dis]=$provincia[j]
    $counter_dis=$counter_dis+1
  end
  puts "added id distritos"+ $id_mun[j]


  doc.search('table[@class="style7"]> tr> td > a> span[@class="style7"]').each do |nombres|
    puts "nombre_dis "+ nombres.inner_html
    $distrito[$counter_dis_names]=nombres.inner_html
    $counter_dis_names=$counter_dis_names+1
  end
  puts "added nombres distritos"+ $id_mun[j]

end

puts "********************Tercera Parte: Datos resultados************************************************************************************"
puts "******Numero de distritos: "+ $counter_dis_names.to_s()

counter_part3=0

for j in 0..$counter_dis-1
    url="http://www.izbori.ba/rezultati/konacni/PoOsnovnimJedinicama2.asp?nivo="+ $id_prov_dis[j] +"&Polling="+ $id_dis [j]
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
          #puts "id partido: "+ $id_partido
          counter_part3=2
        else
          if counter_part3==2
            $partido=linea.inner_html.gsub(/<\/?[^>]*>/,"")
            #puts "partido: "+ $partido
            counter_part3=3
          else
            if counter_part3==3
              $resultados=linea.inner_html.gsub(/<\/?[^>]*>/,"")
              #puts "resultados: "+ $resultados
              counter_part3=0
              ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_partido +"_"+$id_dis[j].to_s(), "ID Municipio"=> $id_mun[j], "Municipio"=> $municipio[j], "Distrito"=>$distrito[j],"ID Distrito"=>$id_dis[j],"ID Partido"=> $id_partido,"Partido"=> $partido, "resultados"=> $resultados})
              
            end
          end
        end
      end
    end
    puts "Provincia: "+$provincia[j] +" y distrito: "+ $id_dis [j]
end



# Programa en Ruby 

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

$provincia={},$municipio={}, $distrito={},$id_mun={},$id_dis={},$id_prov_dis={},url_mun={},url_dis={},$counter_mun=0,counter_id=0,counter_url=0

# Primera pantalla

puts "********************Primera Parte: Municipios************************************************************************************"
for i in 0..0
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
    if temp<10
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
end


#segunda pantalla
puts "********************Segunda Parte: Distritos************************************************************************************"
puts "******Numero de municipios: "+ $counter_mun.to_s()
$counter_dis=0
$counter_dis_names=0

for j in 0..$counter_mun-1
  url="http://www.izbori.ba/rezultati/konacni/PoOsnovnimJedinicamaUkupno.asp?nivo="+$provincia[j].to_s()+"&kod="+ $id_mun[j]
  puts "LA URL "+ url
  html=ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('table[@class="style7"]> tr> td[@width="6%"]').each do |id_dis|
    puts "id_dis"+ id_dis.inner_html
    $id_dis [$counter_dis]=id_dis.inner_html.gsub(/\s+/, "")
    $id_prov_dis[$counter_dis]=$provincia[j]
    $counter_dis=$counter_dis+1
  end
  puts "added id distritos"+ $id_mun[j]


  doc.search('table[@class="style7"]> tr> td > a> span[@class="style7"]').each do |nombres|
    puts "nombre_dis "+ nombres.inner_html
    $distrito[$counter_dis_names]=nombres.inner_html
    $counter_dis_names=$counter_dis_names+1
  end
  puts "added nombres distritos"+ $id_mun[j]

end

puts "********************Tercera Parte: Datos resultados************************************************************************************"
puts "******Numero de distritos: "+ $counter_dis_names.to_s()

counter_part3=0

for j in 0..$counter_dis-1
    url="http://www.izbori.ba/rezultati/konacni/PoOsnovnimJedinicama2.asp?nivo="+ $id_prov_dis[j] +"&Polling="+ $id_dis [j]
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
          #puts "id partido: "+ $id_partido
          counter_part3=2
        else
          if counter_part3==2
            $partido=linea.inner_html.gsub(/<\/?[^>]*>/,"")
            #puts "partido: "+ $partido
            counter_part3=3
          else
            if counter_part3==3
              $resultados=linea.inner_html.gsub(/<\/?[^>]*>/,"")
              #puts "resultados: "+ $resultados
              counter_part3=0
              ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_partido +"_"+$id_dis[j].to_s(), "ID Municipio"=> $id_mun[j], "Municipio"=> $municipio[j], "Distrito"=>$distrito[j],"ID Distrito"=>$id_dis[j],"ID Partido"=> $id_partido,"Partido"=> $partido, "resultados"=> $resultados})
              
            end
          end
        end
      end
    end
    puts "Provincia: "+$provincia[j] +" y distrito: "+ $id_dis [j]
end



# Programa en Ruby 

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

$provincia={},$municipio={}, $distrito={},$id_mun={},$id_dis={},$id_prov_dis={},url_mun={},url_dis={},$counter_mun=0,counter_id=0,counter_url=0

# Primera pantalla

puts "********************Primera Parte: Municipios************************************************************************************"
for i in 0..0
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
    if temp<10
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
end


#segunda pantalla
puts "********************Segunda Parte: Distritos************************************************************************************"
puts "******Numero de municipios: "+ $counter_mun.to_s()
$counter_dis=0
$counter_dis_names=0

for j in 0..$counter_mun-1
  url="http://www.izbori.ba/rezultati/konacni/PoOsnovnimJedinicamaUkupno.asp?nivo="+$provincia[j].to_s()+"&kod="+ $id_mun[j]
  puts "LA URL "+ url
  html=ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('table[@class="style7"]> tr> td[@width="6%"]').each do |id_dis|
    puts "id_dis"+ id_dis.inner_html
    $id_dis [$counter_dis]=id_dis.inner_html.gsub(/\s+/, "")
    $id_prov_dis[$counter_dis]=$provincia[j]
    $counter_dis=$counter_dis+1
  end
  puts "added id distritos"+ $id_mun[j]


  doc.search('table[@class="style7"]> tr> td > a> span[@class="style7"]').each do |nombres|
    puts "nombre_dis "+ nombres.inner_html
    $distrito[$counter_dis_names]=nombres.inner_html
    $counter_dis_names=$counter_dis_names+1
  end
  puts "added nombres distritos"+ $id_mun[j]

end

puts "********************Tercera Parte: Datos resultados************************************************************************************"
puts "******Numero de distritos: "+ $counter_dis_names.to_s()

counter_part3=0

for j in 0..$counter_dis-1
    url="http://www.izbori.ba/rezultati/konacni/PoOsnovnimJedinicama2.asp?nivo="+ $id_prov_dis[j] +"&Polling="+ $id_dis [j]
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
          #puts "id partido: "+ $id_partido
          counter_part3=2
        else
          if counter_part3==2
            $partido=linea.inner_html.gsub(/<\/?[^>]*>/,"")
            #puts "partido: "+ $partido
            counter_part3=3
          else
            if counter_part3==3
              $resultados=linea.inner_html.gsub(/<\/?[^>]*>/,"")
              #puts "resultados: "+ $resultados
              counter_part3=0
              ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_partido +"_"+$id_dis[j].to_s(), "ID Municipio"=> $id_mun[j], "Municipio"=> $municipio[j], "Distrito"=>$distrito[j],"ID Distrito"=>$id_dis[j],"ID Partido"=> $id_partido,"Partido"=> $partido, "resultados"=> $resultados})
              
            end
          end
        end
      end
    end
    puts "Provincia: "+$provincia[j] +" y distrito: "+ $id_dis [j]
end



