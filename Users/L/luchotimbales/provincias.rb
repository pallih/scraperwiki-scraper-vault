# Script Ruby para enseñar como sacar datos de la página http://www.belgenet.net

year={}
year[2]=1954
year[3]=1957
year[4]=1961
year[5]=1965
year[6]=1969
year[7]=1973
year[8]=1977
year[9]=1983
year[10]=1987
year[11]=1991
year[12]=1995
year[13]=1999
year[14]=2003
year[15]=2007

counter=0
for j in 2..15
  url= "http://www.belgenet.net/ayrinti.php?yil_id="+j.to_s()  # una URL cualquiera
  html= ScraperWiki.scrape(url) # la scrapeamos
  puts html # puts sirve para mostrar la información en la hoja de resultados
  
  # 1. Buscar tabla dentro del html
  
  i=0
  require 'nokogiri' # nokogiri es el programa que hace búsquedas dentro de la página
  doc = Nokogiri::HTML(html, nil, 'windows-1254') # "doc" es el nombre del documento e "iso-8859-9" el formato que se puede ver al principio de la página html
  doc.search('select[@class="select"] > option').each do |row| # aquí nos quedamos con las "option" de la tabla "select" del tipo "class=select"
  
    if i==0 or i==1 then
      i=i+1
    else
      puts "Row: "+ row
      puts "Value: "+ row.attr('value') # mostramos los "values"
      puts "Code Prov: " +row.inner_html.split('-').first # mostramos dentro del html solo la primera parte
      puts "Name Prov: "+ row.inner_html.split('-').last.encode('UTF-8') # mostramos dentro del html solo la ultima parte
  
      province={} # declaramos un array para guardar los valores
      province["Value"]=row.attr('value') # guardamos por partes
      province["Code Province"]=row.inner_html.split('-').first
      province["Year"]=year[j]
      province["ID"]=counter.to_s()
      province["Name Province"]=row.inner_html.split('-').last.encode('UTF-8')
      ScraperWiki.save_sqlite(["Value"], province) #con esta linea guardamos el array poniendo como ID unico "Value"
      puts "saved on database"
      i=i+1
      counter=counter+1
    end
  end
end
# Script Ruby para enseñar como sacar datos de la página http://www.belgenet.net

year={}
year[2]=1954
year[3]=1957
year[4]=1961
year[5]=1965
year[6]=1969
year[7]=1973
year[8]=1977
year[9]=1983
year[10]=1987
year[11]=1991
year[12]=1995
year[13]=1999
year[14]=2003
year[15]=2007

counter=0
for j in 2..15
  url= "http://www.belgenet.net/ayrinti.php?yil_id="+j.to_s()  # una URL cualquiera
  html= ScraperWiki.scrape(url) # la scrapeamos
  puts html # puts sirve para mostrar la información en la hoja de resultados
  
  # 1. Buscar tabla dentro del html
  
  i=0
  require 'nokogiri' # nokogiri es el programa que hace búsquedas dentro de la página
  doc = Nokogiri::HTML(html, nil, 'windows-1254') # "doc" es el nombre del documento e "iso-8859-9" el formato que se puede ver al principio de la página html
  doc.search('select[@class="select"] > option').each do |row| # aquí nos quedamos con las "option" de la tabla "select" del tipo "class=select"
  
    if i==0 or i==1 then
      i=i+1
    else
      puts "Row: "+ row
      puts "Value: "+ row.attr('value') # mostramos los "values"
      puts "Code Prov: " +row.inner_html.split('-').first # mostramos dentro del html solo la primera parte
      puts "Name Prov: "+ row.inner_html.split('-').last.encode('UTF-8') # mostramos dentro del html solo la ultima parte
  
      province={} # declaramos un array para guardar los valores
      province["Value"]=row.attr('value') # guardamos por partes
      province["Code Province"]=row.inner_html.split('-').first
      province["Year"]=year[j]
      province["ID"]=counter.to_s()
      province["Name Province"]=row.inner_html.split('-').last.encode('UTF-8')
      ScraperWiki.save_sqlite(["Value"], province) #con esta linea guardamos el array poniendo como ID unico "Value"
      puts "saved on database"
      i=i+1
      counter=counter+1
    end
  end
end
# Script Ruby para enseñar como sacar datos de la página http://www.belgenet.net

year={}
year[2]=1954
year[3]=1957
year[4]=1961
year[5]=1965
year[6]=1969
year[7]=1973
year[8]=1977
year[9]=1983
year[10]=1987
year[11]=1991
year[12]=1995
year[13]=1999
year[14]=2003
year[15]=2007

counter=0
for j in 2..15
  url= "http://www.belgenet.net/ayrinti.php?yil_id="+j.to_s()  # una URL cualquiera
  html= ScraperWiki.scrape(url) # la scrapeamos
  puts html # puts sirve para mostrar la información en la hoja de resultados
  
  # 1. Buscar tabla dentro del html
  
  i=0
  require 'nokogiri' # nokogiri es el programa que hace búsquedas dentro de la página
  doc = Nokogiri::HTML(html, nil, 'windows-1254') # "doc" es el nombre del documento e "iso-8859-9" el formato que se puede ver al principio de la página html
  doc.search('select[@class="select"] > option').each do |row| # aquí nos quedamos con las "option" de la tabla "select" del tipo "class=select"
  
    if i==0 or i==1 then
      i=i+1
    else
      puts "Row: "+ row
      puts "Value: "+ row.attr('value') # mostramos los "values"
      puts "Code Prov: " +row.inner_html.split('-').first # mostramos dentro del html solo la primera parte
      puts "Name Prov: "+ row.inner_html.split('-').last.encode('UTF-8') # mostramos dentro del html solo la ultima parte
  
      province={} # declaramos un array para guardar los valores
      province["Value"]=row.attr('value') # guardamos por partes
      province["Code Province"]=row.inner_html.split('-').first
      province["Year"]=year[j]
      province["ID"]=counter.to_s()
      province["Name Province"]=row.inner_html.split('-').last.encode('UTF-8')
      ScraperWiki.save_sqlite(["Value"], province) #con esta linea guardamos el array poniendo como ID unico "Value"
      puts "saved on database"
      i=i+1
      counter=counter+1
    end
  end
end
# Script Ruby para enseñar como sacar datos de la página http://www.belgenet.net

year={}
year[2]=1954
year[3]=1957
year[4]=1961
year[5]=1965
year[6]=1969
year[7]=1973
year[8]=1977
year[9]=1983
year[10]=1987
year[11]=1991
year[12]=1995
year[13]=1999
year[14]=2003
year[15]=2007

counter=0
for j in 2..15
  url= "http://www.belgenet.net/ayrinti.php?yil_id="+j.to_s()  # una URL cualquiera
  html= ScraperWiki.scrape(url) # la scrapeamos
  puts html # puts sirve para mostrar la información en la hoja de resultados
  
  # 1. Buscar tabla dentro del html
  
  i=0
  require 'nokogiri' # nokogiri es el programa que hace búsquedas dentro de la página
  doc = Nokogiri::HTML(html, nil, 'windows-1254') # "doc" es el nombre del documento e "iso-8859-9" el formato que se puede ver al principio de la página html
  doc.search('select[@class="select"] > option').each do |row| # aquí nos quedamos con las "option" de la tabla "select" del tipo "class=select"
  
    if i==0 or i==1 then
      i=i+1
    else
      puts "Row: "+ row
      puts "Value: "+ row.attr('value') # mostramos los "values"
      puts "Code Prov: " +row.inner_html.split('-').first # mostramos dentro del html solo la primera parte
      puts "Name Prov: "+ row.inner_html.split('-').last.encode('UTF-8') # mostramos dentro del html solo la ultima parte
  
      province={} # declaramos un array para guardar los valores
      province["Value"]=row.attr('value') # guardamos por partes
      province["Code Province"]=row.inner_html.split('-').first
      province["Year"]=year[j]
      province["ID"]=counter.to_s()
      province["Name Province"]=row.inner_html.split('-').last.encode('UTF-8')
      ScraperWiki.save_sqlite(["Value"], province) #con esta linea guardamos el array poniendo como ID unico "Value"
      puts "saved on database"
      i=i+1
      counter=counter+1
    end
  end
end
