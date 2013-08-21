require 'open-uri'

web_contents = open('http://www.voyage.gc.ca/countries_pays/menu-eng.asp') {|f| f.read }
web_contents.scan(/<option value='\d*' >([\w()]*)<\/option>/m) { |match|
  ScraperWiki::save_sqlite(['country'], { country: match[0] })
}