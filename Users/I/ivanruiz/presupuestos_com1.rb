# encoding: utf-8
# Este programa tiene por objetivo obtener los códigos de las CCAAs 
# para posteriormente extraer los presupuestos de 2012
#LIBRERIAS

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
    data = {
      id: ccaa["value"],
      nombre: ccaa.text
    }
    Scraperwiki::save_sqlite(unique_keys=["id"], data)
  end
end
