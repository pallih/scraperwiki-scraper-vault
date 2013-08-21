require 'scraperwiki'

puts 'Hello World'

data={
  "Movie"=>"Jaws",
  "Date"=>"1977",
  "Director"=>"Spielberg"
}

ScraperWiki.save([],data)