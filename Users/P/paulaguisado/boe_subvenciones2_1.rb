#encoding:utf-8
#Este programa tiene por objetivo obtener los enlaces a
#las disposiciones del BOE que tratan de subvenciones a partidos políticos
#LIBRERIAS
require 'mechanize'

 
#CONSTANTES

ScraperWiki::attach("boe_subvenciones1")

agent = Mechanize.new

disposiciones = ScraperWiki::select("* from boe_subvenciones1.swdata")
disposiciones.each do |disposicion|
  #no machacar al ministerio
  sleep(1)
  url = disposicion["urlBOE"]
  puts url

  begin
    page = agent.get(url)
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
    table = doc.css ("table.tabla")
    rows = table.css("tr")
    rows.each do |row|
      celdas = row.css("td")
      data = {
         partido: celdas[0].text.strip, 
         importe: celdas[1].text.strip
      }
      puts data
      ScraperWiki::save_sqlite(unique_keys=["partido"], data)
    end #final de do

  end #final de if

end #final de bucle

