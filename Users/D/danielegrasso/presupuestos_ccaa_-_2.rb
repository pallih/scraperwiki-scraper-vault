# Blank Ruby
#Obtener los presupuestos de las CCAAS de 2012. 
#Se basa en el paso anterior, guardado como Presupuestos CCAA.
#encoding:utf-8
#LIBRERIAS
require 'mechanize'

#CONSTANTES
COOKIE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/inicio.aspx"
BASE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/Consulta_FuncionalDC.aspx?ano=2012&cente="
YEAR = "2012"

#Conecte con la tabla anterior

ScraperWiki::attach("presupuestosccaa1")

agent = Mechanize.new

begin
  agent.get(COOKIE_URL)
rescue Mechanize::ResponseCodeError => the_error
  data = {
    url: COOKIE_URL,
    msg: "Ha habido un error al ir a por la cookie"
  }
  ScraperWiki::save_sqlite(['url'], data, table_name="sw_log")
end

#Selecciono todos los registros y por cada uno cojo la base url y le pego el ID de cada una de las filas(de la otra tabla)

ccaas = ScraperWiki::select("* from presupuestosccaa1.swdata")
ccaas.each do |ccaa|
  sleep(1)
  url = "#{BASE_URL}#{ccaa['id']}"
  puts url
  begin
    page = agent.get(url)
  rescue Mechanize::ResponseCodeError => the_error
    data = {
      url: url,
      msg: "Ha habido un error al ir a por los presupuestos de la CCAA"
    }
    ScraperWiki::save_sqlite(['url'], data, table_name="sw_log")
  end #Final Rescue
  if (page)
    page.encoding = "UTF-8"
    puts page.content
   #Access nokogiri parser
  doc = page.parser
  table = doc.css "table.tabla_consulta"

  #puts table[0]

rows = table[0].css("tbody tr")
rows.each do |row|
  celdas = row.css("td") #Para que se quede con esas celdas
  data = {               #Para que cree una tabla     
      idCCAA: ccaa['id'],
      nombreCCAA: ccaa['nombre'],
      anio: YEAR,
      codigo: celdas[0].text,
      cuenta: celdas[1].text,
      importe: celdas[2].text.gsub(".","").gsub(",", "."), #sirve para quitar puntos de miles y cambiar comas de decimales por puntos-y currar en refine.
      imported: celdas[3].text.gsub(".","").gsub(",", ".") 
          }
#Guarda los datos en una base de datos
 ScraperWiki::save_sqlite(unique_keys=['idCCAA','anio','codigo'], data, table_name="presupuestosCCAA2012")

    end #Final do - rows.each
  end #Final IF
end #Final Bucle, que empieza en do

=begin
agent = Mechanize.new
begin
  agent.get(COOKIE_URL)
rescue Mechanize::ResponseCodeError => the_error
  data = {
    url: COOKIE_URL,
    msg: "Ha habido un error al ir a por la cookie"
  }
  ScraperWiki::save_sqlite(['url'], data, table_name="sw_log")
end

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
  doc = page.parser
  #extraer el select
  select = doc.css("select#ctl00_MainContent_autonomia")
  puts select
  ccaas = select.css("option")
  puts ccaas.length
  #Recorrer el array de resultados
  ccaas.each do |ccaa|
    if (ccaa["value"] == "00")
      next
    end
    data = {
      id: ccaa["value"],
      nombre: ccaa.text.strip
    }
    ScraperWiki::save_sqlite(unique_keys=["id"], data)
  end
end
=end