# Blank Ruby
sourcescraper = 'spb_bru_comp_parallel'

ScraperWiki::attach(sourcescraper)
data = ScraperWiki::select(           
    "* from "+sourcescraper+".swdata order by price asc limit 30"
)
puts "<table border = 1>"
puts "<tr><th>Price</th><th colspan=1>Go</th><th colspan=1>Return</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["price"].to_s, "</td>"
  puts "<td>", (d["wday1"] + " <b>" + d["departure_date"][0..-9] + "</b>  " + d["departure_time1"] + "->" + d["arrival_time1"] + " (" + d["duration1"].round(1).to_s + " hours)"), "</td>"
  puts "<td>", (d["wday2"] + " <b>" + d["arrival_date"][0..-9] + "</b>  " + d["departure_time2"] + "->" + d["arrival_time2"] + " (" + d["duration2"].round(1).to_s + " hours)"), "</td>"
  puts "</tr>"
end
puts "</table>"
# Blank Ruby
sourcescraper = 'spb_bru_comp_parallel'

ScraperWiki::attach(sourcescraper)
data = ScraperWiki::select(           
    "* from "+sourcescraper+".swdata order by price asc limit 30"
)
puts "<table border = 1>"
puts "<tr><th>Price</th><th colspan=1>Go</th><th colspan=1>Return</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["price"].to_s, "</td>"
  puts "<td>", (d["wday1"] + " <b>" + d["departure_date"][0..-9] + "</b>  " + d["departure_time1"] + "->" + d["arrival_time1"] + " (" + d["duration1"].round(1).to_s + " hours)"), "</td>"
  puts "<td>", (d["wday2"] + " <b>" + d["arrival_date"][0..-9] + "</b>  " + d["departure_time2"] + "->" + d["arrival_time2"] + " (" + d["duration2"].round(1).to_s + " hours)"), "</td>"
  puts "</tr>"
end
puts "</table>"
# Blank Ruby
sourcescraper = 'spb_bru_comp_parallel'

ScraperWiki::attach(sourcescraper)
data = ScraperWiki::select(           
    "* from "+sourcescraper+".swdata order by price asc limit 30"
)
puts "<table border = 1>"
puts "<tr><th>Price</th><th colspan=1>Go</th><th colspan=1>Return</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["price"].to_s, "</td>"
  puts "<td>", (d["wday1"] + " <b>" + d["departure_date"][0..-9] + "</b>  " + d["departure_time1"] + "->" + d["arrival_time1"] + " (" + d["duration1"].round(1).to_s + " hours)"), "</td>"
  puts "<td>", (d["wday2"] + " <b>" + d["arrival_date"][0..-9] + "</b>  " + d["departure_time2"] + "->" + d["arrival_time2"] + " (" + d["duration2"].round(1).to_s + " hours)"), "</td>"
  puts "</tr>"
end
puts "</table>"
