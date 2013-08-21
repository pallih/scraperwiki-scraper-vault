# encoding: utf-8
# Este programa tiene por objetivo obtener los códigos de las CCAAs
# para posteriormente extraer los presupuestos de 2012
# librerias
require 'mechanize'
require 'nokogiri'

#CONSTANTES
COOKIE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/inicio.aspx"
BASE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/SelconsultaDC.aspx"

ScraperWiki::attach("

agent = Mechanize.new
#TODO rescue
begin
  agent.get(COOKIE_URL)
rescue Mechanize::ResponseCodeError => the_error
  data = {
   url: COOKIE_URL,
   msg: "Ha habido un error al ir por la cookie"
  }
  Scraperwiki::save_sqlite(['url'], data, table_name="sw_log")
  puts "Ha habido un error al ir por la cookie"
end

begin
  page = agent.get(BASE_URL)
rescue Mechanize::ResponseCodeError => the_error
  data = {
   url: BASE_URL,
   msg: "Ha habido un error al ir por la cookie"
  }
  Scraperwiki::save_sqlite(['url'], data, table_name="sw_log")
  puts "Ha habido un error al ir por los códigos de CCAA"
end

if (page)
  puts page.content
  #Access nokogiri parser
  doc = page.parser
  #Extraer el select
  select = doc.css("select#ctl00_MainContent_autonomia")
  puts select
  ccaas = select.css("option")
  puts ccaas.length
  #Recorrer el array de resultados
  ccaas.each do |ccaa|
    if (ccaa["value"] == "00")
      next
    end 
#Este bucle vale para ignorar valores, como el total de las comunidades
    data = {
      id: ccaa["value"],
      nombre: ccaa.text.strip
#.strip vale para limpiar espacios anteriores y posteriores al texto
    }
#PARA GUARDAR EN SQLITE
    ScraperWiki::save_sqlite(unique_keys=["id"], data)
#PARA MOSTRAR EN PANTALLA
    #puts ccaa
    #puts ccaa.text
    #puts ccaa["value"]
  end
end