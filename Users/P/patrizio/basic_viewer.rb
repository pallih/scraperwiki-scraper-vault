sourcescraper = 'bookingcom'

ScraperWiki.attach( sourcescraper )

data = ScraperWiki.select("* from swdata" ) 

puts "<table>" 
puts "<tr><th>Date</th><th>Property</th><th>Nr. reviews</th>" 
for d in data 
  puts "<tr>" 
  puts "<td>", d["Date"], "</td>" 
  puts "<td>", d["Property"], "</td>"
  puts "<td>", d["Nr.of Reviews"], "</td>" 
  puts "</tr>" 
end 
puts "</table>"
