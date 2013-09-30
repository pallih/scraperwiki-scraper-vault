# Blank Ruby

ScraperWiki.attach("test_92")

data = ScraperWiki.select(
    "* from test_92.swdata where src='koa'"
)

puts "<h1>KOA</h1>"
puts "<table style='border:#000 1px solid;' cellspacing='20px'>"
puts "<tr><th>Navn</th><th>Type</th><th>Size</th><th>Specialprice</th><th>Oldprice</th></tr>"
for d in data
  puts "<tr>"
  puts "<td>", d["navn"], "</td>"
  puts "<td>", d["type"], "</td>"
  puts "<td>", d["size"], "</td>"
  puts "<td>", d["specialprice"].to_s, "</td>"
  puts "<td>", d["oldprice"].to_s, "</td>"
  puts "</tr>"
end

puts "</table>"

data = ScraperWiki.select(
    "* from test_92.swdata where src='tia'"
)

puts "<h1>TIA</h1>"
puts "<table style='border:#000 1px solid;' cellspacing='20px'>"
puts "<tr><th>Navn</th><th>Type</th><th>Size</th><th>Specialprice</th><th>Oldprice</th></tr>"
for d in data
  puts "<tr>"
  puts "<td>", d["navn"], "</td>"
  puts "<td>", d["type"], "</td>"
  puts "<td>", d["size"], "</td>"
  puts "<td>", d["specialprice"].to_s, "</td>"
  puts "<td>", d["oldprice"].to_s, "</td>"
  puts "</tr>"
end
puts "</table>"

data = ScraperWiki.select(
    "* from test_92.swdata where src='dyt'"
)

puts "<h1>DYT</h1>"
puts "<table style='border:#000 1px solid;' cellspacing='20px'>"
puts "<tr><th>Navn</th><th>Type</th><th>Size</th><th>Specialprice</th><th>Oldprice</th></tr>"
for d in data
  puts "<tr>"
  puts "<td>", d["navn"], "</td>"
  puts "<td>", d["type"], "</td>"
  puts "<td>", d["size"], "</td>"
  puts "<td>", d["specialprice"].to_s, "</td>"
  puts "<td>", d["oldprice"].to_s, "</td>"
  puts "</tr>"
end
puts "</table>"








# Blank Ruby

ScraperWiki.attach("test_92")

data = ScraperWiki.select(
    "* from test_92.swdata where src='koa'"
)

puts "<h1>KOA</h1>"
puts "<table style='border:#000 1px solid;' cellspacing='20px'>"
puts "<tr><th>Navn</th><th>Type</th><th>Size</th><th>Specialprice</th><th>Oldprice</th></tr>"
for d in data
  puts "<tr>"
  puts "<td>", d["navn"], "</td>"
  puts "<td>", d["type"], "</td>"
  puts "<td>", d["size"], "</td>"
  puts "<td>", d["specialprice"].to_s, "</td>"
  puts "<td>", d["oldprice"].to_s, "</td>"
  puts "</tr>"
end

puts "</table>"

data = ScraperWiki.select(
    "* from test_92.swdata where src='tia'"
)

puts "<h1>TIA</h1>"
puts "<table style='border:#000 1px solid;' cellspacing='20px'>"
puts "<tr><th>Navn</th><th>Type</th><th>Size</th><th>Specialprice</th><th>Oldprice</th></tr>"
for d in data
  puts "<tr>"
  puts "<td>", d["navn"], "</td>"
  puts "<td>", d["type"], "</td>"
  puts "<td>", d["size"], "</td>"
  puts "<td>", d["specialprice"].to_s, "</td>"
  puts "<td>", d["oldprice"].to_s, "</td>"
  puts "</tr>"
end
puts "</table>"

data = ScraperWiki.select(
    "* from test_92.swdata where src='dyt'"
)

puts "<h1>DYT</h1>"
puts "<table style='border:#000 1px solid;' cellspacing='20px'>"
puts "<tr><th>Navn</th><th>Type</th><th>Size</th><th>Specialprice</th><th>Oldprice</th></tr>"
for d in data
  puts "<tr>"
  puts "<td>", d["navn"], "</td>"
  puts "<td>", d["type"], "</td>"
  puts "<td>", d["size"], "</td>"
  puts "<td>", d["specialprice"].to_s, "</td>"
  puts "<td>", d["oldprice"].to_s, "</td>"
  puts "</tr>"
end
puts "</table>"








