#encoding: utf-8
#Programa tiene por objetivo sacar los enlaces a las subvenciones a partidos en el BOE, entre 2007 y  2012


#Llamo las librearías
require 'mechanize'


#No hay cokies
#CONSTANTES
BASE_URL = "http://www.boe.es/buscar/boe.php?campo%5B1%5D=DOC&dato%5B1%5D=Ley+Org%E1nica+8%2F2007&operador%5B1%5D=and&campo%5B3%5D=DEM&dato%5B3%5D=Ministerio+del+interior&operador%5B3%5D=and&page_hits=100&sort_field%5B0%5D=fpu&sort_order%5B0%5D=asc&sort_field%5B1%5D=ref&sort_order%5B1%5D=asc&accion=Buscar
"

#Ponemos un "rescue" por cada URL, haciendo que alamacene los errores en una tabla de datos.

agent = Mechanize.new

begin
  page = agent.get(BASE_URL)
rescue Mechanize::ResponseCodeError => the_error
  data = {
    url: BASE_URL,
    msg: "Ha habido un error al ir a por los codigos de CCAA"
  }
  ScraperWiki::save_sqlite(['url'], data, table_name="sw_log")
end

if(page)
puts page.content


  #Access nokogiri parser. Porque nokogiri está incluida en Mechanize
  doc = page.parser
  #extraemos la variable. En la página me quedo con el "enlacesMas" que es donde está el enlace que quiero
  enlacesMas = doc.css("div.enlacesMas") #aquí estoy creando la variable

links = enlacesMas.css("a.resultado-busqueda-link-defecto") #Aquí le digo que dentro de "EnlacesMas" quier crearme con "a...." como #enlace. Por eso lo llamno "link"
links.each do |link|
  puts link["href"]
  id = link["href"].gsub(/.*id=/,"") #expresion regular con la que me cargo lo que hay delante del ID en la URL
  
  #puts id
  urlBOE = link["href"].gsub(/\.\./,"http://www.boe.es")
#puts urlBOE
  data = {
      id: link["href"].gsub(/.*id=/,""),
      urlBOE: link["href"].gsub(/\.\./,"http://www.boe.es")
    }
    ScraperWiki::save_sqlite(unique_keys=["id"], data)

  end
end
#encoding: utf-8
#Programa tiene por objetivo sacar los enlaces a las subvenciones a partidos en el BOE, entre 2007 y  2012


#Llamo las librearías
require 'mechanize'


#No hay cokies
#CONSTANTES
BASE_URL = "http://www.boe.es/buscar/boe.php?campo%5B1%5D=DOC&dato%5B1%5D=Ley+Org%E1nica+8%2F2007&operador%5B1%5D=and&campo%5B3%5D=DEM&dato%5B3%5D=Ministerio+del+interior&operador%5B3%5D=and&page_hits=100&sort_field%5B0%5D=fpu&sort_order%5B0%5D=asc&sort_field%5B1%5D=ref&sort_order%5B1%5D=asc&accion=Buscar
"

#Ponemos un "rescue" por cada URL, haciendo que alamacene los errores en una tabla de datos.

agent = Mechanize.new

begin
  page = agent.get(BASE_URL)
rescue Mechanize::ResponseCodeError => the_error
  data = {
    url: BASE_URL,
    msg: "Ha habido un error al ir a por los codigos de CCAA"
  }
  ScraperWiki::save_sqlite(['url'], data, table_name="sw_log")
end

if(page)
puts page.content


  #Access nokogiri parser. Porque nokogiri está incluida en Mechanize
  doc = page.parser
  #extraemos la variable. En la página me quedo con el "enlacesMas" que es donde está el enlace que quiero
  enlacesMas = doc.css("div.enlacesMas") #aquí estoy creando la variable

links = enlacesMas.css("a.resultado-busqueda-link-defecto") #Aquí le digo que dentro de "EnlacesMas" quier crearme con "a...." como #enlace. Por eso lo llamno "link"
links.each do |link|
  puts link["href"]
  id = link["href"].gsub(/.*id=/,"") #expresion regular con la que me cargo lo que hay delante del ID en la URL
  
  #puts id
  urlBOE = link["href"].gsub(/\.\./,"http://www.boe.es")
#puts urlBOE
  data = {
      id: link["href"].gsub(/.*id=/,""),
      urlBOE: link["href"].gsub(/\.\./,"http://www.boe.es")
    }
    ScraperWiki::save_sqlite(unique_keys=["id"], data)

  end
end
