#encoding:utf-8
#Este programa tiene por objetivo obtener los presupuestos de las CCAAs de 2012
#Se basa en un paso anterior PresupuestosCCAA1
#LIBRERIAS
require 'mechanize'

#CONSTANTES
COOKIE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/inicio.aspx"
BASE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/Consulta_FuncionalDC.aspx?ano=2012&cente="

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


ccaas = ScraperWiki::select("* from presupuestosccaa1.swdata")
ccaas.each do |ccaa|
  #no machacar al ministerio
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
  end #Final rescue
  if (page)
    puts page.content
    #Access nokogiri parser
  end #Final if
end #Final bucle

#encoding:utf-8
#Este programa tiene por objetivo obtener los presupuestos de las CCAAs de 2012
#Se basa en un paso anterior PresupuestosCCAA1
#LIBRERIAS
require 'mechanize'

#CONSTANTES
COOKIE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/inicio.aspx"
BASE_URL = "http://serviciosweb.meh.es/apps/publicacionpresupuestos/aspx/Consulta_FuncionalDC.aspx?ano=2012&cente="

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


ccaas = ScraperWiki::select("* from presupuestosccaa1.swdata")
ccaas.each do |ccaa|
  #no machacar al ministerio
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
  end #Final rescue
  if (page)
    puts page.content
    #Access nokogiri parser
  end #Final if
end #Final bucle

