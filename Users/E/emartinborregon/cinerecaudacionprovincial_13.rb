# encoding: utf-8
# LIBRERIAS
require 'open-uri'
require 'nokogiri'

#CONSTANTES
BASE_URL = "http://www.mcu.es/cine/MC/CDC/Anio"
SUFFIX = "/CineProvincias.html"


# Ejercicio 4: leer la página web y sacarla por pantalla
#LEER ENTRADAS
=begin
for year in 2002..2011 do
  #PARA CADA ENTRADA
  url = "#{BASE_URL}#{year}#{SUFFIX}"
  puts url
  #page = open(url)
  #RECUPERAR INFORMACION
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

# Ejercicio 6a: Parsear la página HTML para quedarse con la tabla de datos limpios
=begin
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




# encoding: utf-8
# LIBRERIAS
require 'open-uri'
require 'nokogiri'

#CONSTANTES
BASE_URL = "http://www.mcu.es/cine/MC/CDC/Anio"
SUFFIX = "/CineProvincias.html"


# Ejercicio 4: leer la página web y sacarla por pantalla
#LEER ENTRADAS
=begin
for year in 2002..2011 do
  #PARA CADA ENTRADA
  url = "#{BASE_URL}#{year}#{SUFFIX}"
  puts url
  #page = open(url)
  #RECUPERAR INFORMACION
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

# Ejercicio 6a: Parsear la página HTML para quedarse con la tabla de datos limpios
=begin
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




