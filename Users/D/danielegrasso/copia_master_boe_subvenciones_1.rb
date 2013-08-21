# encoding: utf-8
# El objetivo de este scraper es obtener el listado de las disposiciones
# del BOE que contienen información de subvenciones a partidos políticos
require 'open-uri'
require 'mechanize'

BASE_URL = 'http://www.boe.es/buscar/boe.php?campo%5B1%5D=DOC&dato%5B1%5D=Ley+Org%E1nica+8%2F2007+sobre+financiaci%F3n+de+los+partidos+pol%EDticos'\
   '&operador%5B1%5D=and&campo%5B3%5D=DEM&dato%5B3%5D=Ministerio+del+Interior&operador%5B3%5D=and&page_hits=100'\
   '&sort_field%5B0%5D=fpu&sort_order%5B0%5D=desc&sort_field%5B1%5D=ref&sort_order%5B1%5D=asc&accion=Buscar'
PREFFIX_URL = 'http://www.boe.es'

agent = Mechanize.new
begin
  page = agent.get(BASE_URL)
rescue Mechanize::ResponseCodeError => the_error
  puts the_error.response_code
end
if (page)
  #Get nokogiri parser
  doc = page.parser
  links = doc.css("div.enlacesMas a.resultado-busqueda-link-defecto")
  puts links.length
  links.each do |link|
    #We have to get rid of the parent redirection
    suffix_url = link["href"].gsub(/\.{2}/,"")
    puts suffix_url
    suffix_url =~ /\?id=(.*)$/
    id = $1 unless $1.nil? 
    puts id
    data = {
      id: id,
      url: "#{PREFFIX_URL}#{suffix_url}"
    }
    ScraperWiki::save_sqlite(unique_keys=['id'], data)
  end
end
