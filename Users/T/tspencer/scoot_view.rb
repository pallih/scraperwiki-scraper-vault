#########################################
# Simple table of values from one scraper
#########################################

sourcescraper = "scoot"
limit = 50
offset = 0

# connect to the source database giving it the name src
ScraperWiki.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = ScraperWiki.sqliteexecute("select 
a.flightdate Depart, 
b.flightdate Return,
CAST(julianday(b.flightdate) - julianday(a.flightdate) as Integer) TripLength,
a.flightprice + b.flightprice  TotalCost,
CAST((a.flightprice + b.flightprice) / (julianday(b.flightdate) - julianday(a.flightdate)) as Integer) CostPerDay,
a.flightprice Outbound,
b.flightprice Inbound,
datetime(a.scrapedate,'+10 hours') Scraped
from src.swdata a
inner join src.swdata b
on a.scrapedate = b.scrapedate
and strftime('%m',a.flightdate) != strftime('%m',b.flightdate)
and a.flightdate < b.flightdate
where CAST(julianday(b.flightdate) - julianday(a.flightdate) as Integer) > 12
order by a.scrapedate desc, totalcost asc, triplength desc
limit 50")
keys = sdata["keys"]
rows = sdata["data"]

print '<h2>Scoot Flight Prices: Sydney to Singapore Return</h2>'
print '<h3>Depart 22/12 - 25/12, Return 3/1 - 6/1 </h3>'
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>"
keys.each do |key|
  puts "<th>#{key}</th>"
end

puts "</tr>"

# rows
rows.each do |row|
  puts "<tr>"
  row.each do |value|

    puts "<td>#{value.to_s}</td>"
  end
  puts "</tr>"
end
    
puts "</table>"
