# Blank Ruby

require 'nokogiri'
require 'open-uri'

# stock results 
estaciones = {}

# get the source
url = 'http://www.insivumeh.gob.gt/meteorologia/boletintiempo.htm'
doc = Nokogiri::HTML(open(url))

# tables positions of the data we want to parse
tables = [0]

tables.each do |table|
  $i = table
  doc.xpath("//table[#$i]/tr").each do |tr| 
    tds = tr.children
    estacion = []
  
    for td in tds
      # we don't care about the headers, really
      if (["text", "th"].include?(td.name))
        td.unlink
      else
        estacion << td.content.to_s.gsub(/\[\d+\]/,'')
      end
    end
    
    name = estacion[0]
    # special case for the Capital Federal
    #if ($i == 2 and !estacion[0].nil?)
    #  name << " (CF)"
    #end

    estaciones[ estacion[1] ] = {
      direccion_viento: estacion[1],
      iso: estacion[1],
      velocidad: name,
      visibilidad: estacion[2],
      tiempo: estacion[3],
    }

  if (!estacion[1].nil?)
    ScraperWiki::save_sqlite(['id_'], estaciones[estacion[1]])
  end

  end
end



