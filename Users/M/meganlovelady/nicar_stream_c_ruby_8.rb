require 'scraperwiki'

puts 'Hello World'

data={
  "firstname"=>"Thomas",
  "lastname"=>"Edison",
  "birthday"=>"1847-02-11"
}

ScraperWiki.save([],data)