#encoding:utf-8
#Este programa tiene por objetivo obtener las subvenciones a partidos políticos
#Se basa en un paso anterior boe_subvenciones
#LIBRERIAS
require 'mechanize'

#CONSTANTES

ScraperWiki::attach("boe")

agent = Mechanize.new

disposiciones = ScraperWiki::select("* from boe.swdata")
disposiciones.each do |disposicion|
  #no machacar al ministerio
  sleep(1)
  url = disposicion['urlBOE']
  puts url
  begin
    page = agent.get(url)
  rescue Mechanize::ResponseCodeError => the_error
    data = {
      url: url,
      msg: "Ha habido un error al ir a por la disposicion del BOE"
    }
    ScraperWiki::save_sqlite(['url'], data, table_name="sw_log")
  end #Final rescue
  if (page)
    puts page.content
    #Access nokogiri parser
    doc = page.parser
    table = doc.css("table.tabla")
    rows = table.css("tr")
    rows.each do |row|
      celdas = row.css("td")
      data = {
        partido: celdas[0].text.strip,
        importe: celdas[1].text.strip
      }
      puts data
      ScraperWiki::save_sqlite(unique_keys=["partido"], data)
    end #Fin de bucle filas
  end #Final if página
end #Final bucle disposiciones
