ScraperWiki.attach("school_life_expectancy_in_years")

data = ScraperWiki.select("* from school_life_expectancy_in_years.swdata order by years_in_school desc limit 10")

#puts "<table>"
#puts "<tr><th>Country</th><th>Years in school</th>"
#for d in data
#  puts "<tr>"
#  print "<td>",d["country"],"</td>"
#  print "<td>",d["years_in_school"].to_s,"</td>", "\n"
#  puts "</tr>"
#end
#puts "</table>"

ScraperWiki.httpresponseheader("Content-Type", "application/vnd.google-earth.kml+xml")

puts '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">'''

for d in data
    puts '<Placemark>'
    puts '<name>' + d['country'] + ' average ' + d['years_in_school'].to_s + ' years in school </name>'
    puts '<description>No description, but you can add one.</description>'
    puts '<address>' + d['country'] + '</address>'
    puts '</Placemark>'
end

puts '</kml>'

