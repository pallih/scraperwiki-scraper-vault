source_scraper = 'sutton_council_news'

ScraperWiki.attach(source_scraper)

data = ScraperWiki.select("url, pubdate, headline, image_url, image_width, image_height FROM #{source_scraper}.swdata  ORDER BY pubdate DESC LIMIT 10")

puts <<END
<style type="text/css">
  body {
    font-family: Helvetica, Arial, sans-serif;
    margin: 30px auto;
    width: 800px;
  }

  td {
    padding: 5px 5px;
  }
</style>

<h1>Sutton Council News</h1>
<table>
END

for d in data
  puts "<tr>"

  if d['image_url'].nil? 
    puts "<td>&nbsp;</td>"
  else
    puts %{ <td><a href="#{d['url']}"><img src="#{d['image_url']}" width="#{d['image_width'].to_i / 2}" height="#{d['image_height'].to_i / 2}" /></a></td> }
  end

  puts %{ <td><a href="#{d['url']}">#{d['headline']}</a></td><td>#{d['pubdate']}</td> }
  puts "</tr>"
end