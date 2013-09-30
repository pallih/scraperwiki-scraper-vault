# Script Ruby para enseñar como sacar datos de la página http://www.belgenet.net



################################################################################
# LECCIÓN 1: OBTENER DATOS DE UNA TABLA
# 1. Buscar tabla dentro del html
# 2. Extraer elementos que necesitamos
# 3. Guardarlo en la base de datos
# 4. Ver los datos
################################################################################


url= "http://www.belgenet.net/ayrinti.php?yil_id=15"  # una URL cualquiera
html= ScraperWiki.scrape(url) # la scrapeamos
puts html

# 1. Buscar tabla dentro del html
i=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'iso-8859-9')
doc.search('table[@cellpadding="3"]> tr').each do |row| # aquí nos quedamos con las filas de la tabla que tiene el cellpadding="3" que es la tabla de resultados

# 2. Extraer elementos que necesitamos
  if i==0 then # con este contador pasamos de la primera fila que es donde estan las cabeceras
    i=i+1
  else

    puts row.css('td')[2].inner_text # dentro de la fila nos quedamos con la columnas 2, 3 y 4. Fijate que la numeración de las columnas empiezan en 0
    puts row.css('td')[3].inner_text
    puts row.css('td')[4].inner_text

# 3. Guardarlo en la base de datos    
    # Ahora vamos a guardar la información en una tabla
    record={} # declaramos un array para guardar los valores
    record["Partido"]=row.css('td')[2].inner_text #guardamos en el array los elementos que queremos 
    record["Porcentaje votos"]=row.css('td')[3].inner_text
    record["Total votos"]=row.css('td')[4].inner_text
    ScraperWiki.save_sqlite(["Partido"], record) #con esta linea guardamos el array poniendo como ID unico "Partido"
    i=i+1
  end
end

# 4. Ver los datos
# Los datos los puedes ver en: https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=curso_web_scraping&query=select%20*%20from%20swdata%20limit%2010000
# Script Ruby para enseñar como sacar datos de la página http://www.belgenet.net



################################################################################
# LECCIÓN 1: OBTENER DATOS DE UNA TABLA
# 1. Buscar tabla dentro del html
# 2. Extraer elementos que necesitamos
# 3. Guardarlo en la base de datos
# 4. Ver los datos
################################################################################


url= "http://www.belgenet.net/ayrinti.php?yil_id=15"  # una URL cualquiera
html= ScraperWiki.scrape(url) # la scrapeamos
puts html

# 1. Buscar tabla dentro del html
i=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'iso-8859-9')
doc.search('table[@cellpadding="3"]> tr').each do |row| # aquí nos quedamos con las filas de la tabla que tiene el cellpadding="3" que es la tabla de resultados

# 2. Extraer elementos que necesitamos
  if i==0 then # con este contador pasamos de la primera fila que es donde estan las cabeceras
    i=i+1
  else

    puts row.css('td')[2].inner_text # dentro de la fila nos quedamos con la columnas 2, 3 y 4. Fijate que la numeración de las columnas empiezan en 0
    puts row.css('td')[3].inner_text
    puts row.css('td')[4].inner_text

# 3. Guardarlo en la base de datos    
    # Ahora vamos a guardar la información en una tabla
    record={} # declaramos un array para guardar los valores
    record["Partido"]=row.css('td')[2].inner_text #guardamos en el array los elementos que queremos 
    record["Porcentaje votos"]=row.css('td')[3].inner_text
    record["Total votos"]=row.css('td')[4].inner_text
    ScraperWiki.save_sqlite(["Partido"], record) #con esta linea guardamos el array poniendo como ID unico "Partido"
    i=i+1
  end
end

# 4. Ver los datos
# Los datos los puedes ver en: https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=curso_web_scraping&query=select%20*%20from%20swdata%20limit%2010000
