# encoding: utf-8

require 'nokogiri'
require 'open-uri'

google = "http://www.google.co.jp/m/services/trends/get";
head = "http://ja.dbpedia.org/sparql?default-graph-uri=http://ja.dbpedia.org&query=SELECT+DISTINCT+*+WHERE+{+++?s+rdfs:label+\""
foot = "\"+@ja++.+}&debug=on&timeout=&text/html"

xml = Nokogiri::XML(open(google).read)
item_nodes = xml.xpath('//item/query')
 
item_nodes.each do |item|
  key = item.text

  url = head + key + foot
  doc = Nokogiri::HTML(open(URI.encode(url)).read)
  uri = "http://"
  items = doc.xpath('//uri')
  if items.size > 0
    uri = items[0].text
  end

  data = {
    keyword: key,
    uri: uri
  }
  puts data
  ScraperWiki::save_sqlite(['keyword'], data)
end

?>