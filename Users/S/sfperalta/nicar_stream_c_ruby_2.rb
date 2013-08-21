require 'scraperwiki'

puts 'Hello World'

data={
  "firstname"=>"Sara",
  "lastname"=>"Peralta",
  "favoritecolor"=>"purple"
}

ScraperWiki.save([],data)