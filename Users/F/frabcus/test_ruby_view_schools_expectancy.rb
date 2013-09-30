ScraperWiki.attach("school_life_expectancy_in_years")

data = ScraperWiki.select("* from school_life_expectancy_in_years.swdata order by years_in_school desc limit 10")

puts "<table>"
puts "<tr><th>Country</th><th>Years in school</th>"
for d in data
  puts "<tr>"
  print "<td>",d["country"],"</td>"
  print "<td>",d["years_in_school"].to_s,"</td>", "\n"
  puts "</tr>"
end
puts "</table>"

ScraperWiki.attach("school_life_expectancy_in_years")

data = ScraperWiki.select("* from school_life_expectancy_in_years.swdata order by years_in_school desc limit 10")

puts "<table>"
puts "<tr><th>Country</th><th>Years in school</th>"
for d in data
  puts "<tr>"
  print "<td>",d["country"],"</td>"
  print "<td>",d["years_in_school"].to_s,"</td>", "\n"
  puts "</tr>"
end
puts "</table>"

