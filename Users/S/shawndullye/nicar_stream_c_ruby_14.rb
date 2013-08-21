require 'scraperwiki'

puts 'Hello World'

data={
  "firstname"=>"Shawn",
  "lastname"=>"Dullye",
  "birthday"=>"Awesome Time"
}

ScraperWiki.save([],data)