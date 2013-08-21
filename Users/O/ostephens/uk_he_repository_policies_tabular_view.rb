# Blank Ruby
sourcescraper = 'uk_he_institutional_repository_policies'
ScraperWiki.attach(sourcescraper) 
data = ScraperWiki.select(           
    "* from "+sourcescraper+".swdata"
)
puts "<table>"           
puts "<tr><th>Repository ID</th><th>Repository Name</th><th>Repository URL</th><th>Repository OAI-PMH base</th><th>Metadata Policy Short</th><th>Metadata Policy Full</th><th>Data Policy short</th><th>Data Policy Full</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["Repository ID"], "</td>"
  puts "<td>", d["Repository Name"], "</td>"
  puts "<td>", d["Repository URL"], "</td>"
  puts "<td>", d["Repository OAI-PMH base"], "</td>"
  puts "<td>", d["Metadata Policy Summary"], "</td>"
  puts "<td>", d["Metadata Policy Detail"], "</td>"
  puts "<td>", d["Data Policy Summary"], "</td>"
  puts "<td>", d["Data Policy Detail"], "</td>"
  puts "</tr>"
end
puts "</table>"
