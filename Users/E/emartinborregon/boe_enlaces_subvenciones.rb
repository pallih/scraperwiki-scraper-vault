# encoding: utf-8
# Este programa tiene por objetivo obtener los enlances de una busqueda del BOE
# para posteriormente scrapear las distintas paginas
# librerias
require 'mechanize'

#CONSTANTES
BASE_URL = "http://www.boe.es/buscar/boe.php?campo%5B0%5D=ORI&dato%5B0%5D=&operador%5B0%5D=and&campo%5B1%5D=DOC&dato%5B1%5D=Ley+Org%E1nica+8%2F2007&operador%5B1%5D=and&campo%5B2%5D=TIT&dato%5B2%5D=&operador%5B2%5D=and&campo%5B3%5D=DEM&dato%5B3%5D=Ministerio+del+Interior&operador%5B3%5D=and&campo%5B4%5D=NBO&dato%5B4%5D=&operador%5B4%5D=and&campo%5B5%5D=NOF&dato%5B5%5D=&operador%5B5%5D=and&operador%5B6%5D=and&campo%5B6%5D=FPU&dato%5B6%5D%5B0%5D=&dato%5B6%5D%5B1%5D=&page_hits=100&sort_field%5B0%5D=fpu&sort_order%5B0%5D=asc&sort_field%5B1%5D=ref&sort_order%5B1%5D=asc&accion=Buscar"

agent = Mechanize.new

page = agent.get(BASE_URL)

if (page)
  puts page.content
  #Access nokogiri parser
  doc = page.parser
  #Extraer el link
  enlacesMas = doc.css("div.enlacesMas")
  links = enlacesMas.css("a.resultado-busqueda-link-defecto")
#Este bucle sirve para buscar todos los links
  links.each do |link|
    data = {
      id: link["href"].gsub(/.*id=/,""),
      urlBOE: link["href"].gsub(/\.\./,"http://www.boe.es")
    }
  ScraperWiki::save_sqlite(unique_keys=["id"], data)  
  end
end

