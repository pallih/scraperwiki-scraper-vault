# encoding utf-8
# Este programa tiene como objetivo  obtener los códigos de las CAAAs
# para posteriormente extraer los presupuestos de 2012

require "mechanize"

#CONSTANTES siempre con mayúsculas
COOKIE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/inicio.aspx" #si agragáramos a la URL más números al azar abría un error que se vería reflejado por el BeginRescue que introducimos más adelante
BASE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/SelconsultaDC.aspx"

#Asi se piden las cookies, para evitar que en las peticiones posteriores el servidor no responda a mis peticiones de información

agent = Mechanize.new

#TODO rescue
#Esto es un control añadido en caso de que se estén escrapeando más páginas y queramos que el programa continúe a pesar de los errores
#Además con este proceso creamos una tabla auxiliar de errores que va guardándolos en la opción Data de Firebug
begin
  agent.get(COOKIE_URL)
rescue Mechanize::ResponseCodeError => the_error
  data = {
    url: COOKIE_URL,
    msg: "Ha habido un error al ir a por la cookie"
  }
  ScraperWiki::save_sqlite(['url'], data, table_name="sw_log")
end

#Repetimos en proceso para BASE_URL
begin
  page = agent.get(BASE_URL)
rescue Mechanize::ResponseCodeError => the_error
  data = {
    url: BASE_URL,
    msg: "Ha habido un error al ir a por los codigos de CCAA"
  }
  ScraperWiki::save_sqlite(['url'], data, table_name="sw_log")
end

if (page)
  puts page.content
  #Access nokogiri parser
     #OJO A partir de este paso, ya podemos generar el documento de donde vamos a extraer el ID de la tabla
  doc = page.parser
  #extraer el select
  select = doc.css("select#ctl00_MainContent_autonomia") #este es el ID
  puts select
  ccaas = select.css("option")
puts ccaas.length
  #recorrer el array de resultados  
  ccaas.each do |ccaa|
  if (ccaa["value"] == "00") #agregamos este fórmula para que no recoja el Total de Comunidades
   next
  puts ccaa.text
  puts ccaa["value"]
  end

  #Creas la variable data para incluirla en la formula ScrapperWiki
  data = {
  id: ccaa["value"],
  nombre: ccaa.text
  }
  ScraperWiki::save_sqlite(unique_keys=["id"], data) #Es un diccionario de datos
  end
end
