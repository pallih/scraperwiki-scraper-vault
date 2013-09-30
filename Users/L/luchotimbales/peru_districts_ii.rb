# Ruby script to obtains electoral results from Peru @ http://www.infogob.com.pe


$id_distrito={},$region={}, $provincia={}, $distrito={}, $total_electores={}, $poblacion={}, $electores_varones={}, $superficie={}, $electores_mujeres={}, $ultimo_censo={}, $indicador_pobreza={}


puts "*********************STARTING***************"
puts "*********************Getting list of distritos***************"

# Getting list of distritos
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=peru_districts&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('td').each do |datos|
  if l==0 then
  else
    #puts datos.inner_html
    $id_distrito[l-1]=datos.inner_html
  end
  l=l+1
end

puts "*********************Getting DATOS GENERALES***************"
# Getting DATOS GENERALES

for p in -1..l-1

  url= "http://www.infogob.com.pe/Localidad/ubigeo.aspx?IdUbigeo="+ $id_distrito[p].to_s() +"&IdTab=0"
  puts url
  html= ScraperWiki.scrape(url)
  puts html
  
  i=0
  k=0
  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('table[@class="mylista"] > tr > td').each do |datos|
    #puts datos.inner_html  
    if i==1 then #region
      puts datos.inner_html
      $region[k]=datos.inner_html
    else
      if i==5 then #provincia
        puts datos.inner_html
        $provincia[k]=datos.inner_html
      else
        if i==9 then #Distrito
          puts datos.inner_html
          $distrito[k]=datos.inner_html
        else
          if i==11 then #total electores
             puts datos.inner_html
             $total_electores[k]=datos.inner_html 
          else
            if i==13 then #Poblacion
              puts "poblacion: "+ datos.inner_html
              $poblacion[k]=datos.inner_html
            else
              if i==15 then# electores varones
                puts datos.inner_html
                $electores_varones[k]=datos.inner_html
              else
                if i==17 then# superficie
                  puts datos.inner_html
                  $superficie[k]=datos.inner_html
                else
                  if i==19 then #electores mujeres
                    puts datos.inner_html
                    $electores_mujeres[k]=datos.inner_html
                  else
                    if i==21 then #ultimo censo
                      puts datos.inner_html
                      $ultimo_censo[k]=datos.inner_html
                    else
                      if i==23 then # indicador pobreza
                        puts datos.inner_html
                        $indicador_pobreza[k]=datos.inner_html
                        ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_distrito[p], "region"=> $region[k], "provincia"=> $provincia[k], "distrito"=> $distrito[k], "total_electores"=> $total_electores[k], "Poblacion"=> $poblacion[k], "electores_varones"=> $electores_varones[k], "superficie"=> $superficie[k], "electores_mujeres"=> $electores_mujeres[k], "ultimo_censo"=> $ultimo_censo[k], "indicador_pobreza"=> $indicador_pobreza[k]})
                        k=k+1
                      end
                    end
                  end
                end
              end
            end
          end
        end
      end
    end
  i=i+1
  end

end

# Ruby script to obtains electoral results from Peru @ http://www.infogob.com.pe


$id_distrito={},$region={}, $provincia={}, $distrito={}, $total_electores={}, $poblacion={}, $electores_varones={}, $superficie={}, $electores_mujeres={}, $ultimo_censo={}, $indicador_pobreza={}


puts "*********************STARTING***************"
puts "*********************Getting list of distritos***************"

# Getting list of distritos
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=peru_districts&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('td').each do |datos|
  if l==0 then
  else
    #puts datos.inner_html
    $id_distrito[l-1]=datos.inner_html
  end
  l=l+1
end

puts "*********************Getting DATOS GENERALES***************"
# Getting DATOS GENERALES

for p in -1..l-1

  url= "http://www.infogob.com.pe/Localidad/ubigeo.aspx?IdUbigeo="+ $id_distrito[p].to_s() +"&IdTab=0"
  puts url
  html= ScraperWiki.scrape(url)
  puts html
  
  i=0
  k=0
  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('table[@class="mylista"] > tr > td').each do |datos|
    #puts datos.inner_html  
    if i==1 then #region
      puts datos.inner_html
      $region[k]=datos.inner_html
    else
      if i==5 then #provincia
        puts datos.inner_html
        $provincia[k]=datos.inner_html
      else
        if i==9 then #Distrito
          puts datos.inner_html
          $distrito[k]=datos.inner_html
        else
          if i==11 then #total electores
             puts datos.inner_html
             $total_electores[k]=datos.inner_html 
          else
            if i==13 then #Poblacion
              puts "poblacion: "+ datos.inner_html
              $poblacion[k]=datos.inner_html
            else
              if i==15 then# electores varones
                puts datos.inner_html
                $electores_varones[k]=datos.inner_html
              else
                if i==17 then# superficie
                  puts datos.inner_html
                  $superficie[k]=datos.inner_html
                else
                  if i==19 then #electores mujeres
                    puts datos.inner_html
                    $electores_mujeres[k]=datos.inner_html
                  else
                    if i==21 then #ultimo censo
                      puts datos.inner_html
                      $ultimo_censo[k]=datos.inner_html
                    else
                      if i==23 then # indicador pobreza
                        puts datos.inner_html
                        $indicador_pobreza[k]=datos.inner_html
                        ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_distrito[p], "region"=> $region[k], "provincia"=> $provincia[k], "distrito"=> $distrito[k], "total_electores"=> $total_electores[k], "Poblacion"=> $poblacion[k], "electores_varones"=> $electores_varones[k], "superficie"=> $superficie[k], "electores_mujeres"=> $electores_mujeres[k], "ultimo_censo"=> $ultimo_censo[k], "indicador_pobreza"=> $indicador_pobreza[k]})
                        k=k+1
                      end
                    end
                  end
                end
              end
            end
          end
        end
      end
    end
  i=i+1
  end

end

# Ruby script to obtains electoral results from Peru @ http://www.infogob.com.pe


$id_distrito={},$region={}, $provincia={}, $distrito={}, $total_electores={}, $poblacion={}, $electores_varones={}, $superficie={}, $electores_mujeres={}, $ultimo_censo={}, $indicador_pobreza={}


puts "*********************STARTING***************"
puts "*********************Getting list of distritos***************"

# Getting list of distritos
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=peru_districts&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('td').each do |datos|
  if l==0 then
  else
    #puts datos.inner_html
    $id_distrito[l-1]=datos.inner_html
  end
  l=l+1
end

puts "*********************Getting DATOS GENERALES***************"
# Getting DATOS GENERALES

for p in -1..l-1

  url= "http://www.infogob.com.pe/Localidad/ubigeo.aspx?IdUbigeo="+ $id_distrito[p].to_s() +"&IdTab=0"
  puts url
  html= ScraperWiki.scrape(url)
  puts html
  
  i=0
  k=0
  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('table[@class="mylista"] > tr > td').each do |datos|
    #puts datos.inner_html  
    if i==1 then #region
      puts datos.inner_html
      $region[k]=datos.inner_html
    else
      if i==5 then #provincia
        puts datos.inner_html
        $provincia[k]=datos.inner_html
      else
        if i==9 then #Distrito
          puts datos.inner_html
          $distrito[k]=datos.inner_html
        else
          if i==11 then #total electores
             puts datos.inner_html
             $total_electores[k]=datos.inner_html 
          else
            if i==13 then #Poblacion
              puts "poblacion: "+ datos.inner_html
              $poblacion[k]=datos.inner_html
            else
              if i==15 then# electores varones
                puts datos.inner_html
                $electores_varones[k]=datos.inner_html
              else
                if i==17 then# superficie
                  puts datos.inner_html
                  $superficie[k]=datos.inner_html
                else
                  if i==19 then #electores mujeres
                    puts datos.inner_html
                    $electores_mujeres[k]=datos.inner_html
                  else
                    if i==21 then #ultimo censo
                      puts datos.inner_html
                      $ultimo_censo[k]=datos.inner_html
                    else
                      if i==23 then # indicador pobreza
                        puts datos.inner_html
                        $indicador_pobreza[k]=datos.inner_html
                        ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_distrito[p], "region"=> $region[k], "provincia"=> $provincia[k], "distrito"=> $distrito[k], "total_electores"=> $total_electores[k], "Poblacion"=> $poblacion[k], "electores_varones"=> $electores_varones[k], "superficie"=> $superficie[k], "electores_mujeres"=> $electores_mujeres[k], "ultimo_censo"=> $ultimo_censo[k], "indicador_pobreza"=> $indicador_pobreza[k]})
                        k=k+1
                      end
                    end
                  end
                end
              end
            end
          end
        end
      end
    end
  i=i+1
  end

end

# Ruby script to obtains electoral results from Peru @ http://www.infogob.com.pe


$id_distrito={},$region={}, $provincia={}, $distrito={}, $total_electores={}, $poblacion={}, $electores_varones={}, $superficie={}, $electores_mujeres={}, $ultimo_censo={}, $indicador_pobreza={}


puts "*********************STARTING***************"
puts "*********************Getting list of distritos***************"

# Getting list of distritos
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=peru_districts&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('td').each do |datos|
  if l==0 then
  else
    #puts datos.inner_html
    $id_distrito[l-1]=datos.inner_html
  end
  l=l+1
end

puts "*********************Getting DATOS GENERALES***************"
# Getting DATOS GENERALES

for p in -1..l-1

  url= "http://www.infogob.com.pe/Localidad/ubigeo.aspx?IdUbigeo="+ $id_distrito[p].to_s() +"&IdTab=0"
  puts url
  html= ScraperWiki.scrape(url)
  puts html
  
  i=0
  k=0
  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('table[@class="mylista"] > tr > td').each do |datos|
    #puts datos.inner_html  
    if i==1 then #region
      puts datos.inner_html
      $region[k]=datos.inner_html
    else
      if i==5 then #provincia
        puts datos.inner_html
        $provincia[k]=datos.inner_html
      else
        if i==9 then #Distrito
          puts datos.inner_html
          $distrito[k]=datos.inner_html
        else
          if i==11 then #total electores
             puts datos.inner_html
             $total_electores[k]=datos.inner_html 
          else
            if i==13 then #Poblacion
              puts "poblacion: "+ datos.inner_html
              $poblacion[k]=datos.inner_html
            else
              if i==15 then# electores varones
                puts datos.inner_html
                $electores_varones[k]=datos.inner_html
              else
                if i==17 then# superficie
                  puts datos.inner_html
                  $superficie[k]=datos.inner_html
                else
                  if i==19 then #electores mujeres
                    puts datos.inner_html
                    $electores_mujeres[k]=datos.inner_html
                  else
                    if i==21 then #ultimo censo
                      puts datos.inner_html
                      $ultimo_censo[k]=datos.inner_html
                    else
                      if i==23 then # indicador pobreza
                        puts datos.inner_html
                        $indicador_pobreza[k]=datos.inner_html
                        ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_distrito[p], "region"=> $region[k], "provincia"=> $provincia[k], "distrito"=> $distrito[k], "total_electores"=> $total_electores[k], "Poblacion"=> $poblacion[k], "electores_varones"=> $electores_varones[k], "superficie"=> $superficie[k], "electores_mujeres"=> $electores_mujeres[k], "ultimo_censo"=> $ultimo_censo[k], "indicador_pobreza"=> $indicador_pobreza[k]})
                        k=k+1
                      end
                    end
                  end
                end
              end
            end
          end
        end
      end
    end
  i=i+1
  end

end

