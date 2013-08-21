# Ruby para scrapear los datos de las municipales en bosnia del 2008

$id_municipio={}, $municipio={}, $partido={},$id_partido={}, $resultado={}, $resultado_porcentaje={}, $redov={}, $post={}, $Odsus={}, $Pot={}

# rellenamos la variable de municipios

puts "*********************EMPEZAMOS :)***************"
url= "http://www.izbori.ba/Mandati27102008/index.asp"
html= ScraperWiki.scrape(url)
puts html

i=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('option').each do |linea|
#puts linea.inner_html
#puts linea['value']
ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
temp = ic.iconv(linea.inner_html)
$municipio[i]=temp
$id_municipio[i]=linea['value']
i=i+1
end

puts "*********************TENEMOS LOS MUNICIPIOS***************"
for count in 0..i-1
    puts "*********************MUNICIPIO"+  $id_municipio[count] +": "+ $municipio[count] +"***************"
    url= "http://www.izbori.ba/Mandati27102008/ShowMunicipality.asp?MunicipalityCode="+ $id_municipio[count]
    html= ScraperWiki.scrape(url)
    #puts html
    
    require 'nokogiri'
    
    i=0 #contador
    
    #Nombre de partidos
    doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@width="604"]> table[@class="style7"]> tr> td> a> b> span').each do |linea|
        #puts linea.inner_html
        ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
        temp = ic.iconv(linea.inner_html)
        $partido[i]=temp
      i=i+1
    end
    
    doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@width="604"]> table[@class="style7"]> tr> td> a> span').each do |linea|
        #puts linea.inner_html
        ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
        temp = ic.iconv(linea.inner_html)
        $partido[i]=temp
      i=i+1
    end
    
    i=0 #contador
    #IDs de partidos
    doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@width="604"]> table[@class="style7"]> tr> td[@width="6%"]> div [@align="center"]').each do |linea|
    #  puts linea.inner_html
      $id_partido[i]=linea.inner_html
      i=i+1
    end
    
    i=0
    #resultados %
    doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@width="604"]> table[@class="style7"]> tr> td > div> span').each do |linea|
    #    puts linea.inner_html
      $resultado_porcentaje[i]=linea.inner_html
      i=i+1
    end
    
    i=0
    #resultados totales
    doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@width="604"]> table[@class="style7"]> tr> td > div[@align="right"]> b').each do |linea|
    #    puts linea.inner_html
      $resultado[i]=linea.inner_html
      i=i+1
    end
    
    i=1
    j=0
    #resultados desagregados
    # el primero no es bueno, nos quedamos con 3,6,9,etc...
    doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@width="604"]> table[@class="style7"]> tr> td > div[@align="right"]> table> tr> td> div').each do |linea|
    #    puts linea.inner_html
        if i==3 then
          $redov[j]=linea.inner_html
        else 
            if i==6 then
              $post[j]=linea.inner_html
            else
                if i==9 then
                  $Odsus[j]=linea.inner_html
                else
                    if i==12 then
                      $Pot[j]=linea.inner_html
                      j=j+1
                      i=0
                    end
                end
            end
        end
        i=i+1
    end
    
    for i in 0..j-1
    
#    puts $municipio[count]
#    puts $partido[i]
#    puts $id_partido[i]
#    puts $resultado_porcentaje[i]
#    puts $resultado[i]
#    puts $redov[i]
#    puts $post[i]
#    puts $Odsus[i]
#    puts $Pot[i]
    
    ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_municipio[count] +"_"+ $id_partido[i], "ID Municipio"=> $id_municipio[count], "Municipio"=> $municipio[count], "Partido"=> $partido[i], "ID_Partido"=> $id_partido[i], "Resultado"=> $resultado_porcentaje[i], "Resultado Total"=> $resultado[i], "Redovni"=> $redov[i], "Postom"=> $post[i], "Odsustvo"=> $Odsus[i], "Potvrdeni"=> $Pot[i]})
    
    end
end
# Ruby para scrapear los datos de las municipales en bosnia del 2008

$id_municipio={}, $municipio={}, $partido={},$id_partido={}, $resultado={}, $resultado_porcentaje={}, $redov={}, $post={}, $Odsus={}, $Pot={}

# rellenamos la variable de municipios

puts "*********************EMPEZAMOS :)***************"
url= "http://www.izbori.ba/Mandati27102008/index.asp"
html= ScraperWiki.scrape(url)
puts html

i=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('option').each do |linea|
#puts linea.inner_html
#puts linea['value']
ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
temp = ic.iconv(linea.inner_html)
$municipio[i]=temp
$id_municipio[i]=linea['value']
i=i+1
end

puts "*********************TENEMOS LOS MUNICIPIOS***************"
for count in 0..i-1
    puts "*********************MUNICIPIO"+  $id_municipio[count] +": "+ $municipio[count] +"***************"
    url= "http://www.izbori.ba/Mandati27102008/ShowMunicipality.asp?MunicipalityCode="+ $id_municipio[count]
    html= ScraperWiki.scrape(url)
    #puts html
    
    require 'nokogiri'
    
    i=0 #contador
    
    #Nombre de partidos
    doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@width="604"]> table[@class="style7"]> tr> td> a> b> span').each do |linea|
        #puts linea.inner_html
        ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
        temp = ic.iconv(linea.inner_html)
        $partido[i]=temp
      i=i+1
    end
    
    doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@width="604"]> table[@class="style7"]> tr> td> a> span').each do |linea|
        #puts linea.inner_html
        ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
        temp = ic.iconv(linea.inner_html)
        $partido[i]=temp
      i=i+1
    end
    
    i=0 #contador
    #IDs de partidos
    doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@width="604"]> table[@class="style7"]> tr> td[@width="6%"]> div [@align="center"]').each do |linea|
    #  puts linea.inner_html
      $id_partido[i]=linea.inner_html
      i=i+1
    end
    
    i=0
    #resultados %
    doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@width="604"]> table[@class="style7"]> tr> td > div> span').each do |linea|
    #    puts linea.inner_html
      $resultado_porcentaje[i]=linea.inner_html
      i=i+1
    end
    
    i=0
    #resultados totales
    doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@width="604"]> table[@class="style7"]> tr> td > div[@align="right"]> b').each do |linea|
    #    puts linea.inner_html
      $resultado[i]=linea.inner_html
      i=i+1
    end
    
    i=1
    j=0
    #resultados desagregados
    # el primero no es bueno, nos quedamos con 3,6,9,etc...
    doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@width="604"]> table[@class="style7"]> tr> td > div[@align="right"]> table> tr> td> div').each do |linea|
    #    puts linea.inner_html
        if i==3 then
          $redov[j]=linea.inner_html
        else 
            if i==6 then
              $post[j]=linea.inner_html
            else
                if i==9 then
                  $Odsus[j]=linea.inner_html
                else
                    if i==12 then
                      $Pot[j]=linea.inner_html
                      j=j+1
                      i=0
                    end
                end
            end
        end
        i=i+1
    end
    
    for i in 0..j-1
    
#    puts $municipio[count]
#    puts $partido[i]
#    puts $id_partido[i]
#    puts $resultado_porcentaje[i]
#    puts $resultado[i]
#    puts $redov[i]
#    puts $post[i]
#    puts $Odsus[i]
#    puts $Pot[i]
    
    ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_municipio[count] +"_"+ $id_partido[i], "ID Municipio"=> $id_municipio[count], "Municipio"=> $municipio[count], "Partido"=> $partido[i], "ID_Partido"=> $id_partido[i], "Resultado"=> $resultado_porcentaje[i], "Resultado Total"=> $resultado[i], "Redovni"=> $redov[i], "Postom"=> $post[i], "Odsustvo"=> $Odsus[i], "Potvrdeni"=> $Pot[i]})
    
    end
end
