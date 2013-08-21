require 'scraperwiki'

puts 'Hello World'

data={
  "firstname"=>"Ashley",
  "lastname"=>"Hebler",
  "icecream"=>"cookie dough"
}

ScraperWiki.save([],data)