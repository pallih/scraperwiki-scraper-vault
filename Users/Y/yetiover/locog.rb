require 'nokogiri'

doc = Nokogiri::HTML(open("http://www.london2012.com/olympic-torch-relay-torchbearers/search.php?start=11", "User-Agent" => "Ruby/#{RUBY_VERSION}"))

#html = ScraperWiki.scrape("http://london2012.com/games/olympic-torch-relay/torchbearers/search.php?start=11")
puts html

require 'nokogiri'

doc = Nokogiri::HTML(open("http://www.london2012.com/olympic-torch-relay-torchbearers/search.php?start=11", "User-Agent" => "Ruby/#{RUBY_VERSION}"))

#html = ScraperWiki.scrape("http://london2012.com/games/olympic-torch-relay/torchbearers/search.php?start=11")
puts html

