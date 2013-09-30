#Objetivo: sacar recaudación cine por provincia desde 2002 hasta 2011

# encoding: utf-8
# LIBRERIAS:open-uri para el 4; nokogiri para el 5
require 'open-uri'
require 'nokogiri'

#CONSTANTES
BASE_URL = "http://www.mcu.es/cine/MC/CDC/Anio"
SUFFIX = "/CineProvincias.html"
=begin
# Ejercicio 4: leer la página web y sacarla por pantalla
#LEER ENTRADAS
for year in 2002..2011 do
  #PARA CADA ENTRADA
  url = "#{BASE_URL}#{year}#{SUFFIX}"
  puts url
  #page = open(url)
#RECUPERAR INFORMACION. Lo de aquí abajo sirve para decirle a la página que eres Mozilla. Algunas no aceptan que entres como #'anónimo'. Para cada línea, sácamela en pantalla

  page = open(url,'User-Agent' => 'Mozilla/5.0')

  #PROCESAR INFORMACION
  page.each_line do |line|
    #GUARDAR INFORMACION
    puts line
  end
end
=end


# Ejercicio 5: Parsear la página HTML para quedarse con la tabla de datos
=begin
for year in 2002..2011 do
  #PARA CADA ENTRADA
  url = "#{BASE_URL}#{year}#{SUFFIX}"
  puts url
  #RECUPERAR INFORMACION
  page = open(url,'User-Agent' => 'Mozilla/5.0')
  #PROCESAR INFORMACION: se la haces buscar en los CSS. Allí está tbRestultados (tb es tabla, tr es table row, td es table data)
  doc = Nokogiri::HTML(page)
  resultados = doc.css("div.tbResultados")
  #puts resultados.class
  filas = resultados.css("tr")
  filas.each_with_index do |fila,i|
    next if i == 0
    celdas = fila.css("td")
    data = {
      year: year,
      ranking: celdas[0].text,
      provincia: celdas[1].text,
      espectadores: celdas[2].text,
      salas: celdas[3].text,
      recaudacion: celdas[4].text
    }
    puts data
  end
  #Vamos a darle un respiro a la web del ministerio de cultura
  # una petición cada segundo
  sleep(1)
end
=end

=begin
# Ejercicio 6a: Parsear la página HTML para quedarse con la tabla de datos limpios
#Con el .strip se carga los espacios blancos en las celdas de datos .
for year in 2002..2011 do
  #PARA CADA ENTRADA
  url = "#{BASE_URL}#{year}#{SUFFIX}"
  puts url
  #RECUPERAR INFORMACION
  page = open(url,'User-Agent' => 'Mozilla/5.0')
  #PROCESAR INFORMACION
  doc = Nokogiri::HTML(page)
  resultados = doc.css("div.tbResultados")
  #puts resultados.class
  filas = resultados.css("tr")
  filas.each_with_index do |fila,i|
    next if i == 0
    celdas = fila.css("td")
    data = {
      year: year,
      ranking: celdas[0].text.strip,
      provincia: celdas[1].text.strip,
      espectadores: celdas[2].text.strip,
      salas: celdas[3].text.strip,
      recaudacion: celdas[4].text.strip
    }
    puts data 
  end
  #Vamos a darle un respiro a la web del ministerio de cultura
  # una petición cada segundo
  sleep(1)
end
=end

# Ejercicio 6b: Parsear la página HTML para quedarse con la tabla de datos limpios y guardar en tabla de scraperWiki

for year in 2002..2011 do
  #PARA CADA ENTRADA
  url = "#{BASE_URL}#{year}#{SUFFIX}"
  puts url
  #RECUPERAR INFORMACION
  page = open(url,'User-Agent' => 'Mozilla/5.0')
  #PROCESAR INFORMACION
  doc = Nokogiri::HTML(page)
  resultados = doc.css("div.tbResultados")
  #puts resultados.class
  filas = resultados.css("tr")
  filas.each_with_index do |fila,i|
    next if i == 0
    celdas = fila.css("td")
    data = {
      year: year,
      ranking: celdas[0].text.strip,
      provincia: celdas[1].text.strip,
      espectadores: celdas[2].text.strip,
      salas: celdas[3].text.strip,
      recaudacion: celdas[4].text.strip
    }
    ScraperWiki::save_sqlite(['year','provincia'], data)
  end
  #Vamos a darle un respiro a la web del ministerio de cultura
  # una petición cada segundo
  sleep(1)
end




#Objetivo: sacar recaudación cine por provincia desde 2002 hasta 2011

# encoding: utf-8
# LIBRERIAS:open-uri para el 4; nokogiri para el 5
require 'open-uri'
require 'nokogiri'

#CONSTANTES
BASE_URL = "http://www.mcu.es/cine/MC/CDC/Anio"
SUFFIX = "/CineProvincias.html"
=begin
# Ejercicio 4: leer la página web y sacarla por pantalla
#LEER ENTRADAS
for year in 2002..2011 do
  #PARA CADA ENTRADA
  url = "#{BASE_URL}#{year}#{SUFFIX}"
  puts url
  #page = open(url)
#RECUPERAR INFORMACION. Lo de aquí abajo sirve para decirle a la página que eres Mozilla. Algunas no aceptan que entres como #'anónimo'. Para cada línea, sácamela en pantalla

  page = open(url,'User-Agent' => 'Mozilla/5.0')

  #PROCESAR INFORMACION
  page.each_line do |line|
    #GUARDAR INFORMACION
    puts line
  end
end
=end


# Ejercicio 5: Parsear la página HTML para quedarse con la tabla de datos
=begin
for year in 2002..2011 do
  #PARA CADA ENTRADA
  url = "#{BASE_URL}#{year}#{SUFFIX}"
  puts url
  #RECUPERAR INFORMACION
  page = open(url,'User-Agent' => 'Mozilla/5.0')
  #PROCESAR INFORMACION: se la haces buscar en los CSS. Allí está tbRestultados (tb es tabla, tr es table row, td es table data)
  doc = Nokogiri::HTML(page)
  resultados = doc.css("div.tbResultados")
  #puts resultados.class
  filas = resultados.css("tr")
  filas.each_with_index do |fila,i|
    next if i == 0
    celdas = fila.css("td")
    data = {
      year: year,
      ranking: celdas[0].text,
      provincia: celdas[1].text,
      espectadores: celdas[2].text,
      salas: celdas[3].text,
      recaudacion: celdas[4].text
    }
    puts data
  end
  #Vamos a darle un respiro a la web del ministerio de cultura
  # una petición cada segundo
  sleep(1)
end
=end

=begin
# Ejercicio 6a: Parsear la página HTML para quedarse con la tabla de datos limpios
#Con el .strip se carga los espacios blancos en las celdas de datos .
for year in 2002..2011 do
  #PARA CADA ENTRADA
  url = "#{BASE_URL}#{year}#{SUFFIX}"
  puts url
  #RECUPERAR INFORMACION
  page = open(url,'User-Agent' => 'Mozilla/5.0')
  #PROCESAR INFORMACION
  doc = Nokogiri::HTML(page)
  resultados = doc.css("div.tbResultados")
  #puts resultados.class
  filas = resultados.css("tr")
  filas.each_with_index do |fila,i|
    next if i == 0
    celdas = fila.css("td")
    data = {
      year: year,
      ranking: celdas[0].text.strip,
      provincia: celdas[1].text.strip,
      espectadores: celdas[2].text.strip,
      salas: celdas[3].text.strip,
      recaudacion: celdas[4].text.strip
    }
    puts data 
  end
  #Vamos a darle un respiro a la web del ministerio de cultura
  # una petición cada segundo
  sleep(1)
end
=end

# Ejercicio 6b: Parsear la página HTML para quedarse con la tabla de datos limpios y guardar en tabla de scraperWiki

for year in 2002..2011 do
  #PARA CADA ENTRADA
  url = "#{BASE_URL}#{year}#{SUFFIX}"
  puts url
  #RECUPERAR INFORMACION
  page = open(url,'User-Agent' => 'Mozilla/5.0')
  #PROCESAR INFORMACION
  doc = Nokogiri::HTML(page)
  resultados = doc.css("div.tbResultados")
  #puts resultados.class
  filas = resultados.css("tr")
  filas.each_with_index do |fila,i|
    next if i == 0
    celdas = fila.css("td")
    data = {
      year: year,
      ranking: celdas[0].text.strip,
      provincia: celdas[1].text.strip,
      espectadores: celdas[2].text.strip,
      salas: celdas[3].text.strip,
      recaudacion: celdas[4].text.strip
    }
    ScraperWiki::save_sqlite(['year','provincia'], data)
  end
  #Vamos a darle un respiro a la web del ministerio de cultura
  # una petición cada segundo
  sleep(1)
end




