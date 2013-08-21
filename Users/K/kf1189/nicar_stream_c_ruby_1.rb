require 'scraperwiki'

puts 'Hello World'

data={
  "firstname"=>"Kiana",
  "lastname"=>"Fitzgerald",
  "birthday"=>"1989-08-14"
}

ScraperWiki.save([],data)