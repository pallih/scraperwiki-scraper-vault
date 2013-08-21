#encoding:utf-8
#Este programa tiene por objetivo obtener los enlaces a
#las disposiciones del BOE que tratan de subvenciones a partidos políticos
#LIBRERIAS
require 'mechanize'

#CONSTANTES
BASE_URL = "http://www.boe.es/buscar/boe.php?campo%5B1%5D=DOC&dato%5B1%5D=Ley+Org%E1nica+8%2F2007"\
"&operador%5B1%5D=and&campo%5B3%5D=DEM&dato%5B3%5D=Ministerio+del+interior&operador%5B3%5D=and"\
"&page_hits=100&sort_field%5B0%5D=fpu&sort_order%5B0%5D=asc&sort_field%5B1%5D=ref"\
"&sort_order%5B1%5D=asc&accion=Buscar"

agent = Mechanize.new

begin
  page = agent.get(BASE_URL)
rescue Mechanize::ResponseCodeError => the_error
  data = {
    url: BASE_URL,
    msg: "Ha habido un error al ir a por las disposiciones del boe"
  }
  ScraperWiki::save_sqlite(['url'], data, table_name="sw_log")
end

if (page)
  puts page.content
  #Access nokogiri parser
  doc = page.parser
  #extraer lista de enlaces
  enlacesMas = doc.css("div.enlacesMas")
  #quedarnos con el primer enlace
  links = enlacesMas.css("a.resultado-busqueda-link-defecto")
  #Bucle para recorrer enlaces
  links.each do |link|
    data = {
      id: link["href"].gsub(/.*id=/,""),
      urlBOE: link["href"].gsub(/\.\./,"http://www.boe.es")
    }
    ScraperWiki::save_sqlite(unique_keys=["id"], data)
  end #FINAL DEL BUCLE DE LINKS
end #FINAL DEL IF
