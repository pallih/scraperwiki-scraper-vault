# Blank Ruby

require 'nokogiri'
require 'open-uri'

# stock results 
provincias = {}

# get the source
url = 'http://es.wikipedia.org/w/index.php?title=Provincias_de_Argentina&printable=yes'
doc = Nokogiri::HTML(open(url))

# tables positions of the data we want to parse
tables = [2, 3]

tables.each do |table|
  $i = table
  doc.xpath("//table[#$i]/tr").each do |tr| 
    tds = tr.children
    provincia = []
  
    for td in tds
      # we don't care about the headers, really
      if (["text", "th"].include?(td.name))
        td.unlink
      else
        provincia << td.content.to_s.gsub(/\[\d+\]/,'')
      end
    end
    
    name = provincia[0]
    # special case for the Capital Federal
    if ($i == 2 and !provincia[0].nil?)
      name << " (CF)"
    end

    provincias[ provincia[1] ] = {
      id_: provincia[1],
      iso: provincia[1],
      name: name,
      hab: provincia[2],
      area: provincia[3],
    }

  if (!provincia[1].nil?)
    ScraperWiki::save_sqlite(['id_'], provincias[provincia[1]])
  end

  end
end



# Blank Ruby

require 'nokogiri'
require 'open-uri'

# stock results 
provincias = {}

# get the source
url = 'http://es.wikipedia.org/w/index.php?title=Provincias_de_Argentina&printable=yes'
doc = Nokogiri::HTML(open(url))

# tables positions of the data we want to parse
tables = [2, 3]

tables.each do |table|
  $i = table
  doc.xpath("//table[#$i]/tr").each do |tr| 
    tds = tr.children
    provincia = []
  
    for td in tds
      # we don't care about the headers, really
      if (["text", "th"].include?(td.name))
        td.unlink
      else
        provincia << td.content.to_s.gsub(/\[\d+\]/,'')
      end
    end
    
    name = provincia[0]
    # special case for the Capital Federal
    if ($i == 2 and !provincia[0].nil?)
      name << " (CF)"
    end

    provincias[ provincia[1] ] = {
      id_: provincia[1],
      iso: provincia[1],
      name: name,
      hab: provincia[2],
      area: provincia[3],
    }

  if (!provincia[1].nil?)
    ScraperWiki::save_sqlite(['id_'], provincias[provincia[1]])
  end

  end
end



