# A view for the Scraper: "The 5 newest cd reviews from www.laut.de"
ScraperWiki::attach('the_5_newest_cd_reviews_from_wwwlautde')

# Fetch the data from the SQLite datastore attached to the scraper
reviews = ScraperWiki::select("Artist, Album, Teaser, Review FROM the_5_newest_cd_reviews_from_wwwlautde.swdata ORDER BY artist ASC" )

# Display an HTML view of the data

puts '<!doctype html>
      <html lang="de">
      
      <head>
        <meta charset="utf-8">
          <title>Web Data Extraction & Integration - Stage 2, Exercise 04_2</title>
          <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.2.1/css/bootstrap-combined.min.css" rel="stylesheet">
          <script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.2.1/js/bootstrap.min.js"></script>
      </head>'

puts '<body>
        <div class="container">
          <div class="page-header">
            <h2>Die 5 aktuellsten CD Kritiken von www.laut.de</h2>
          </div>
        <div class="row">
          <div class="span12">'

for r in reviews
  puts '<div class="well">'
  puts   '<div> <h2>', r['Artist'], ' - ', r['Album'], '</h2> </div>'
  puts   '<div> <h4>', r['Teaser'], '</h4> </div>'
  puts   '<div>', r['Review'] ,'</div>'
  puts '</div>'
end

puts        '</div>
          </div>
        </div>
      </body>'

puts '</html>'
