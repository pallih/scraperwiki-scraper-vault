require 'scraperwiki'

puts 'Hello World'

data={
  "firstname"=>"Taylor",
  "lastname"=>"Thompson",
  "birthday"=>"1987-01-29"
}

ScraperWiki.save([],data)