# encoding: utf-8
require 'open-uri'
require 'addressable/uri'

uri = Addressable::URI.parse("http://marttimölsä.fi")
puts uri.normalize.to_s
puts uri.to_s

t = 'å'
puts t
data = {
  test: t,
  uri: uri.normalize.to_s
}
ScraperWiki::save_sqlite(['test'], data)# encoding: utf-8
require 'open-uri'
require 'addressable/uri'

uri = Addressable::URI.parse("http://marttimölsä.fi")
puts uri.normalize.to_s
puts uri.to_s

t = 'å'
puts t
data = {
  test: t,
  uri: uri.normalize.to_s
}
ScraperWiki::save_sqlite(['test'], data)