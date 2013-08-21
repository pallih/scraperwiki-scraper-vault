#encoding:utf-8
#Este programa tiene por objetivo tener las subvenciones a partidos politicos
#Se basa en un paso anterior que es SubvencionesBoe1

require 'mechanize'
#CONSTANTES

ScraperWiki::attach("subvencionesboe1")
agent = Mechanize.new

disposiciones = ScraperWiki::select("* from subvencionesboe1.swdata")
disposiciones.each do |disposicion|

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
    #comento este puts para que cuando ejecute el puts table, salga directamente la tabla sin información adicional
    #puts page.content
    
    #Access nokogiri parser
    doc = page.parser
    table = doc.css("table.tabla")
    #puts table
    rows = table.css("tr")
    rows.each do |row|
      celda = row.css("td")

        data = {
          partido: celda[0].text.strip, 
          importe: celda[1].text.strip
        }
        puts data
      ScraperWiki::save_sqlite(unique_keys=["partido"], data)

    end #Fin de bucle de las celdas
  end #Final del bucle if
end #Final bucle disposiciones

