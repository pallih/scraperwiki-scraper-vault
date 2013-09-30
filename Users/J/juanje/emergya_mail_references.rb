puts "<h1>This is the <em>Emergya maillists activities</em> from Markmail.</h1>"

sourcescraper = 'markmail-emergya'
ScraperWiki.attach(sourcescraper)

data = ScraperWiki.select("DISTINCT year from swdata")

years = []
data.each { |d| years.push d["year"] }


puts "<table  cellspacing=\"30\"><tr>"
years.each do |year|
  data = ScraperWiki.select(           
      "* from swdata where year = \"#{year}\"
      order by list desc limit 10"
  )
  puts "<td valign=\"top\">"
  puts "<h2>Mails about Emergya on #{year}</h2>"
  puts "<table>"           
  puts "<tr><th>Mail list</th><th>emails</th>"
  data.each do |d|
    puts "<tr>"
    puts "<td>", d["list"], "</td>"
    puts "<td align=\"center\">", d["mails"].to_s, "</td>"
    puts "</tr>"
  end
  puts "</table>"
  puts "</td>"
end
puts "</tr></table>"

puts "<h1>This is the <em>Emergya maillists activities</em> from Markmail.</h1>"

sourcescraper = 'markmail-emergya'
ScraperWiki.attach(sourcescraper)

data = ScraperWiki.select("DISTINCT year from swdata")

years = []
data.each { |d| years.push d["year"] }


puts "<table  cellspacing=\"30\"><tr>"
years.each do |year|
  data = ScraperWiki.select(           
      "* from swdata where year = \"#{year}\"
      order by list desc limit 10"
  )
  puts "<td valign=\"top\">"
  puts "<h2>Mails about Emergya on #{year}</h2>"
  puts "<table>"           
  puts "<tr><th>Mail list</th><th>emails</th>"
  data.each do |d|
    puts "<tr>"
    puts "<td>", d["list"], "</td>"
    puts "<td align=\"center\">", d["mails"].to_s, "</td>"
    puts "</tr>"
  end
  puts "</table>"
  puts "</td>"
end
puts "</tr></table>"

