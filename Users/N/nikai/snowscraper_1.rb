snowscraper = 'snowscraper'
limit = 20
offset = 0

hd = {
  tst:  "timestamp",
  pshb: "snow height at mountain ski runs",
  psqb: "snow quality at mountain ski runs",
  psht: "snow height at ski runs in valley",
  sho:  "snow height in town",
  tabc: "temperature at the mountain in &deg;C",
  tatc: "temperature in valley in &deg;C",
  lns:  "day of last snowfall",
  ait:  "downhill into valley",
  bpkm: "snowy ski runs in km",
  alws: "avalanche warning status"
}

ScraperWiki.attach(snowscraper, "src")

sdata = ScraperWiki.sqliteexecute("select * from src.swdata limit ? offset ?", [limit, offset])
keys = sdata["keys"]
rows = sdata["data"]

print '<h2>The latest snow reports for Kitzb&uuml;hel:</h2>' #   '(' + keys.size.to_s + ' columns)'
print '<table border="1" style="border-collapse:collapse;">'

print "<tr>"
keys.each { |desc| puts "<th>#{hd[desc.intern]}</th>" }

puts "</tr>"

rows.each do |row|
  puts "<tr>"
  row.each { |value| puts "<td>#{value.to_s}</td>" }
  puts "</tr>"
end
    
puts "</table>"