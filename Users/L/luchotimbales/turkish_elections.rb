# Extraer datos electorales de la página www.belge.net

year={}
year[1954]=2
year[1957]=3
year[1961]=4
year[1965]=5
year[1969]=6
year[1973]=7
year[1977]=8
year[1983]=9
year[1987]=10
year[1991]=11
year[1995]=12
year[1999]=13
year[2003]=14
year[2007]=15

# declarar array
$id_province={}
$year_eleccion={}

# Crear variable con identificador de provincia de la página html
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=provincias&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('tr').each do |datos|
  #puts datos
  if l==0 then
  else
    #puts datos.css('td')[1].inner_text
    $id_province[l]=datos.css('td')[2].inner_text
    $year_eleccion[l]=datos.css('td')[3].inner_text
  end
  l=l+1
end

puts "Numero de provincias: "+ l.to_s()


for p in 992..l-1
  puts p
  puts "Year: "+$year_eleccion[p]
  puts "Provincia: "+ $id_province[p].to_s()
  url= "http://www.belgenet.net/ayrinti.php?yil_id="+year[$year_eleccion[p].to_i()].to_s()+"&il_id="+ $id_province[p].to_s()
  puts "fuente: "+ url
  html= ScraperWiki.scrape(url)
  puts html
  i=0
  doc = Nokogiri::HTML(html, nil, 'iso-8859-9')
  doc.search('table[@cellpadding="3"]> tr').each do |row| # aquí nos quedamos con las filas de la tabla que tiene el cellpadding="3" que es la tabla de resultados
  puts i
  # 2. Extraer elementos que necesitamos
    if i==0 then # con este contador pasamos de la primera fila que es donde estan las cabeceras
      i=i+1
    else  
      #puts row.css('td')[2].inner_text # dentro de la fila nos quedamos con la columnas 2, 3 y 4. Fijate que la numeración de las columnas empiezan en 0
      #puts row.css('td')[3].inner_text
      #puts row.css('td')[4].inner_text
  
  # 3. Guardarlo en la base de datos    
      # Ahora vamos a guardar la información en una tabla
      record={} # declaramos un array para guardar los valores
      record["ID"]=$year_eleccion[p].to_s()+"_"+$id_province[p].to_s() +"_"+row.css('td')[2].inner_text
      record["Year"]= $year_eleccion[p].to_s()
      record["ID_Provincia"]=$id_province[p].to_s()
      record["Partido"]=row.css('td')[2].inner_text #guardamos en el array los elementos que queremos
      record["Porcentaje votos"]=row.css('td')[3].inner_text
      record["Total votos"]=row.css('td')[4].inner_text
      ScraperWiki.save_sqlite(["ID"], record) #con esta linea guardamos el array poniendo como ID unico "Partido"
      puts "saved in database"
      i=i+1
    end
  end
end

# Extraer datos electorales de la página www.belge.net

year={}
year[1954]=2
year[1957]=3
year[1961]=4
year[1965]=5
year[1969]=6
year[1973]=7
year[1977]=8
year[1983]=9
year[1987]=10
year[1991]=11
year[1995]=12
year[1999]=13
year[2003]=14
year[2007]=15

# declarar array
$id_province={}
$year_eleccion={}

# Crear variable con identificador de provincia de la página html
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=provincias&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('tr').each do |datos|
  #puts datos
  if l==0 then
  else
    #puts datos.css('td')[1].inner_text
    $id_province[l]=datos.css('td')[2].inner_text
    $year_eleccion[l]=datos.css('td')[3].inner_text
  end
  l=l+1
end

puts "Numero de provincias: "+ l.to_s()


for p in 992..l-1
  puts p
  puts "Year: "+$year_eleccion[p]
  puts "Provincia: "+ $id_province[p].to_s()
  url= "http://www.belgenet.net/ayrinti.php?yil_id="+year[$year_eleccion[p].to_i()].to_s()+"&il_id="+ $id_province[p].to_s()
  puts "fuente: "+ url
  html= ScraperWiki.scrape(url)
  puts html
  i=0
  doc = Nokogiri::HTML(html, nil, 'iso-8859-9')
  doc.search('table[@cellpadding="3"]> tr').each do |row| # aquí nos quedamos con las filas de la tabla que tiene el cellpadding="3" que es la tabla de resultados
  puts i
  # 2. Extraer elementos que necesitamos
    if i==0 then # con este contador pasamos de la primera fila que es donde estan las cabeceras
      i=i+1
    else  
      #puts row.css('td')[2].inner_text # dentro de la fila nos quedamos con la columnas 2, 3 y 4. Fijate que la numeración de las columnas empiezan en 0
      #puts row.css('td')[3].inner_text
      #puts row.css('td')[4].inner_text
  
  # 3. Guardarlo en la base de datos    
      # Ahora vamos a guardar la información en una tabla
      record={} # declaramos un array para guardar los valores
      record["ID"]=$year_eleccion[p].to_s()+"_"+$id_province[p].to_s() +"_"+row.css('td')[2].inner_text
      record["Year"]= $year_eleccion[p].to_s()
      record["ID_Provincia"]=$id_province[p].to_s()
      record["Partido"]=row.css('td')[2].inner_text #guardamos en el array los elementos que queremos
      record["Porcentaje votos"]=row.css('td')[3].inner_text
      record["Total votos"]=row.css('td')[4].inner_text
      ScraperWiki.save_sqlite(["ID"], record) #con esta linea guardamos el array poniendo como ID unico "Partido"
      puts "saved in database"
      i=i+1
    end
  end
end

# Extraer datos electorales de la página www.belge.net

year={}
year[1954]=2
year[1957]=3
year[1961]=4
year[1965]=5
year[1969]=6
year[1973]=7
year[1977]=8
year[1983]=9
year[1987]=10
year[1991]=11
year[1995]=12
year[1999]=13
year[2003]=14
year[2007]=15

# declarar array
$id_province={}
$year_eleccion={}

# Crear variable con identificador de provincia de la página html
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=provincias&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('tr').each do |datos|
  #puts datos
  if l==0 then
  else
    #puts datos.css('td')[1].inner_text
    $id_province[l]=datos.css('td')[2].inner_text
    $year_eleccion[l]=datos.css('td')[3].inner_text
  end
  l=l+1
end

puts "Numero de provincias: "+ l.to_s()


for p in 992..l-1
  puts p
  puts "Year: "+$year_eleccion[p]
  puts "Provincia: "+ $id_province[p].to_s()
  url= "http://www.belgenet.net/ayrinti.php?yil_id="+year[$year_eleccion[p].to_i()].to_s()+"&il_id="+ $id_province[p].to_s()
  puts "fuente: "+ url
  html= ScraperWiki.scrape(url)
  puts html
  i=0
  doc = Nokogiri::HTML(html, nil, 'iso-8859-9')
  doc.search('table[@cellpadding="3"]> tr').each do |row| # aquí nos quedamos con las filas de la tabla que tiene el cellpadding="3" que es la tabla de resultados
  puts i
  # 2. Extraer elementos que necesitamos
    if i==0 then # con este contador pasamos de la primera fila que es donde estan las cabeceras
      i=i+1
    else  
      #puts row.css('td')[2].inner_text # dentro de la fila nos quedamos con la columnas 2, 3 y 4. Fijate que la numeración de las columnas empiezan en 0
      #puts row.css('td')[3].inner_text
      #puts row.css('td')[4].inner_text
  
  # 3. Guardarlo en la base de datos    
      # Ahora vamos a guardar la información en una tabla
      record={} # declaramos un array para guardar los valores
      record["ID"]=$year_eleccion[p].to_s()+"_"+$id_province[p].to_s() +"_"+row.css('td')[2].inner_text
      record["Year"]= $year_eleccion[p].to_s()
      record["ID_Provincia"]=$id_province[p].to_s()
      record["Partido"]=row.css('td')[2].inner_text #guardamos en el array los elementos que queremos
      record["Porcentaje votos"]=row.css('td')[3].inner_text
      record["Total votos"]=row.css('td')[4].inner_text
      ScraperWiki.save_sqlite(["ID"], record) #con esta linea guardamos el array poniendo como ID unico "Partido"
      puts "saved in database"
      i=i+1
    end
  end
end

