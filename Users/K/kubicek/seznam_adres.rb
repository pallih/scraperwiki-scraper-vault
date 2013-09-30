# Blank Ruby
sourcescraper = 'adresy_v_praze_7'

ScraperWiki::attach(sourcescraper)           

data = ScraperWiki::select(           
    "* from adresy_v_praze_7.swdata order by district, numbers"
)

puts "<table>"           
puts "<tr><th>k.u. a c.p.</th><th>Ulice a c.o.</th>"
for d in data
  popisne, orientacni = d["numbers"].split("/",2)
  puts "<tr>"
  puts "<td>", d["district"], popisne, "</td>"
  puts "<td>", d["street"], orientacni, "</td>"
  puts "</tr>"
end
puts "</table>"

# Blank Ruby
sourcescraper = 'adresy_v_praze_7'

ScraperWiki::attach(sourcescraper)           

data = ScraperWiki::select(           
    "* from adresy_v_praze_7.swdata order by district, numbers"
)

puts "<table>"           
puts "<tr><th>k.u. a c.p.</th><th>Ulice a c.o.</th>"
for d in data
  popisne, orientacni = d["numbers"].split("/",2)
  puts "<tr>"
  puts "<td>", d["district"], popisne, "</td>"
  puts "<td>", d["street"], orientacni, "</td>"
  puts "</tr>"
end
puts "</table>"

