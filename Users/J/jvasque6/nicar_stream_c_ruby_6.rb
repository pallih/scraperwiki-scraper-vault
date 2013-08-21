require 'scraperwiki'

puts 'Hello World'

data={
  "firstname"=>"Jon",
  "lastname"=>"Jordan",
  "birthday"=>"1888-05-10"
}

ScraperWiki.save([],data)