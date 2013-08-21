# Blank Ruby

require 'rexml/document'

url = 'http://ws.audioscrobbler.com/2.0/?method=chart.gethypedartists&api_key=b25b959554ed76058ac220b7b2e0a026'

html = ScraperWiki.scrape(url)

doc = REXML::Document.new(html)

doc.elements.each('lfm/artists/artist/name') do |ele|
    puts ele.text
end