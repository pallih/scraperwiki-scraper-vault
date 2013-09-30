#encoding: utf-8
#Programa tiene por objetivo obtener los códigos de las CCAA para
# después extraer los presupuestos de 2012.

#Llamo las librearías
require 'mechanize'


#Me guardo la cookie, que está en la página inicial, por la que pasaría navegando normalmente.
#CONSTANTES
COOKIE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/inicio.aspx"
BASE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/SelconsultaDC.aspx"


#Ponemos un "rescue" por cada URL, haciendo que alamacene los errores en una tabla de datos.

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

if(page)
  puts page.content
  #Access nokogiri parser. Porque nokogiri está incluida en Mechanize
  doc = page.parser
  #extraer el select. En la página me quedo con el select que tenga ese "id".
  select = doc.css("select#ctl00_MainContent_autonomia")
  #poner el select en pantalla
puts select
  #Una vez obtenida la variable Select, quédate solo con los "option"
ccaas = select.css("option")
  #Ahora me dice cuantos tenemos (19 ccaa + total)
puts ccaas.length
  #Recorremos el array de resultado y damos un nombre a la variable, que los asigne a cada una. Con el puts los pone en pantalla.
  #(Tras el próximo paso, comento el puts ccaa porque ya no me interesa que me lo sque en pantalla).
ccaas.each do |ccaa|
#puts ccaa
#Para que me saque el texto del elemento
puts ccaa.text
puts ccaa["value"]
#Para guardar: ScraperWiki::save_sqlite(unique_keys=["a"], data={"a"=>1, "bbb"=>"Hi there"})
#Antes, le decimos que no coja el valor "OO", que es el del total de las CCAA. Con next lo salta.
    if ccaa["value"]=="00"
      next
  end
    data = {
      id: ccaa["value"],
      nombre: ccaa.text.strip
    }
    ScraperWiki::save_sqlite(unique_keys=["id"], data)

 

  end
end#encoding: utf-8
#Programa tiene por objetivo obtener los códigos de las CCAA para
# después extraer los presupuestos de 2012.

#Llamo las librearías
require 'mechanize'


#Me guardo la cookie, que está en la página inicial, por la que pasaría navegando normalmente.
#CONSTANTES
COOKIE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/inicio.aspx"
BASE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/SelconsultaDC.aspx"


#Ponemos un "rescue" por cada URL, haciendo que alamacene los errores en una tabla de datos.

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

if(page)
  puts page.content
  #Access nokogiri parser. Porque nokogiri está incluida en Mechanize
  doc = page.parser
  #extraer el select. En la página me quedo con el select que tenga ese "id".
  select = doc.css("select#ctl00_MainContent_autonomia")
  #poner el select en pantalla
puts select
  #Una vez obtenida la variable Select, quédate solo con los "option"
ccaas = select.css("option")
  #Ahora me dice cuantos tenemos (19 ccaa + total)
puts ccaas.length
  #Recorremos el array de resultado y damos un nombre a la variable, que los asigne a cada una. Con el puts los pone en pantalla.
  #(Tras el próximo paso, comento el puts ccaa porque ya no me interesa que me lo sque en pantalla).
ccaas.each do |ccaa|
#puts ccaa
#Para que me saque el texto del elemento
puts ccaa.text
puts ccaa["value"]
#Para guardar: ScraperWiki::save_sqlite(unique_keys=["a"], data={"a"=>1, "bbb"=>"Hi there"})
#Antes, le decimos que no coja el valor "OO", que es el del total de las CCAA. Con next lo salta.
    if ccaa["value"]=="00"
      next
  end
    data = {
      id: ccaa["value"],
      nombre: ccaa.text.strip
    }
    ScraperWiki::save_sqlite(unique_keys=["id"], data)

 

  end
end