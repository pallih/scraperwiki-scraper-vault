#encoding:utf-8
#Este programa tiene por objetivo obtener los presupuestos de las CCAAs de 2012
#se basa en un paso anterior PresupuestosCCAA
#LIBRERIAS
require 'mechanize'

#CONSTANTES
COOKIE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/inicio.aspx"
BASE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/Consulta_FuncionalDC.aspx?ano=2012&cente="

ScraperWiki::attach("presupuestoccaa") 

agent = Mechanize.new
#TODO rescue
begin
  agent.get(COOKIE_URL)
rescue Mechanize::ResponseCodeError => the_error
  data = {
  url: COOKIE_URL,
  msg: "Ha habido un error al ir a por la cookie"
}
  ScraperWiki::save_sqlite(['url'], data, table_name="sw_log")
end

ccaas = ScraperWiki::select("* from presupuestoccaa.swdata")
ccaas.each do |ccaa| #bucle, interacción
  #no machacar al ministerio
  sleep(1)
  #puts ccaa["id"]
  url = "#{BASE_URL}#{ccaa['id']}"
  #dentro de corchetes, mejor utilizar comillas para que no piense que es un error y sepa que es una variable
  puts url
  begin
    page = agent.get(BASE_URL)
  rescue Mechanize::ResponseCodeError => the_error
    data = {
      url: BASE_URL,
      msg: "Ha habido un error al ir a por los códigos de CCAA"
     }
     ScraperWiki::save_sqlite(['url'], data, table_name="sw_log")
  end #final rescue

  if (page)
    puts page.content
    #Access nokogiri parser
    doc = page.parser

  end #final de if

end #final de bucle




=begin
if (page)
  puts page.content
  #Access nokogiri parser
  doc = page.parser
  #extraer el select
  select = doc.css("select#ctl00_MainContent_autonomia")
  puts select
  ccaas = select.css("option")
  #para saber cuántas opciones hay
  puts ccaas.length
#recorrer el array de resultados
  ccaas.each do |ccaa|
    #creamos variables donde registramos los datos que seleccionamos
    #esto es un diccionario de datos, con elementos separados por comas y cada uno con un nombre
    if (ccaa["value"] == "00")
      next
    end
    data = {
      id: ccaa["value"],
      nombre: ccaa.text.strip
}
  #La clave única es el id, de modo que no se va a repetir
  #Los datos de id y nombre están en data porque los hemos puesto antes  
  ScraperWiki::save_sqlite(unique_keys=["id"], data)

    #puts ccaa
    #puts ccaa.text
    #puts ccaa["value"]
#estos puts sirven para ver en pantalla lo que quiero seleccionar
#una vez lo he aislado, no me hacen falta y lo que hago es sacar los datos
    
  end
end
=end
