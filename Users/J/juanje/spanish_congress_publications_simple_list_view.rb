# Spanish Congress' Publications simple list view

puts "<h1>Publicaciones del </em>Congreso de los Diputados</em> español</h1>"

sourcescraper = 'spanish_congress_publications'
ScraperWiki.attach(sourcescraper)

data = ScraperWiki.select("DISTINCT serie from swdata")

series = data.collect { |d| d["serie"] }

series.each do |serie|
  data = ScraperWiki.select(           
      "publication, url from swdata where serie = \"#{serie}\"
      order by publication limit 10"
  )
  puts "<h2>#{serie}</h2>"
  puts "<ul>"
  data.each do |d|
    puts "<li><a href=\"#{d['url']}\">#{d['publication']}</a></li>"
  end
  puts "</ul>"
end
