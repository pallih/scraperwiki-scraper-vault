# encoding: utf-8

require 'nokogiri'
require 'open-uri'
require 'date'
require 'uri'

google = "http://www.google.co.jp/m/services/trends/get";
#head = "http://ja.dbpedia.org/sparql?default-graph-uri=http://ja.dbpedia.org&query=SELECT+DISTINCT+*+WHERE+{+++?s+rdfs:label+\""
head = "http://ja.dbpedia.org/sparql?default-graph-uri=http://ja.dbpedia.org&query=SELECT DISTINCT * WHERE { ?s rdfs:label+\""
#foot = "\"+@ja++.+}&debug=on&timeout=&format=text%2Fhtml"
foot = "\" @ja . }&format=text/html"

xml = Nokogiri::XML(open(google).read)
item_nodes = xml.xpath('//item/query')
 
item_nodes.each do |item|
  key = item.text

  sparql = head + key + foot
  doc = Nokogiri::HTML(open(URI.encode(sparql)).read)
#  uri = "http://"
  uri = ""
#  items = doc.xpath('//uri')
  items = doc.xpath('//table/tr/td')
  if items.size > 0
    uri = items[0].text
  end
#  puts key + ", " + URI.decode(key) + ", " + uri + ", " + URI.decode(uri)

  date = Date.today
  date = date -1

  data = {
    date: date.to_s,
    keyword: key,
    uri: uri
  }
  puts data
  ScraperWiki::save_sqlite(['date','keyword'], data)
end
