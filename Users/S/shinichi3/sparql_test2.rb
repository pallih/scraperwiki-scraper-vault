# encoding: utf-8
# coding: utf-8

require 'nokogiri'
require 'open-uri'

key = "東京"
#url = "http://ja.dbpedia.org/sparql?default-graph-uri=http://ja.dbpedia.org&query=SELECT+DISTINCT+*+WHERE+{+++?s+rdfs:label+\"東京\"+@ja++.+}&debug=on&timeout=&text/html"
url1 = "http://ja.dbpedia.org/sparql?default-graph-uri=http://ja.dbpedia.org&query=SELECT+DISTINCT+*+WHERE+{+++?s+rdfs:label+\""
url2 = "\"+@ja++.+}&debug=on&timeout=&text/html"
url = url1 + key + url2

doc = Nokogiri::HTML(open(URI.encode(url)).read)

doc.xpath('//uri').each do |item|
  puts item.text
end

res = "http://"
items = doc.xpath('//uri')
if items.size > 0
  res = "a"
end

puts res
# encoding: utf-8
# coding: utf-8

require 'nokogiri'
require 'open-uri'

key = "東京"
#url = "http://ja.dbpedia.org/sparql?default-graph-uri=http://ja.dbpedia.org&query=SELECT+DISTINCT+*+WHERE+{+++?s+rdfs:label+\"東京\"+@ja++.+}&debug=on&timeout=&text/html"
url1 = "http://ja.dbpedia.org/sparql?default-graph-uri=http://ja.dbpedia.org&query=SELECT+DISTINCT+*+WHERE+{+++?s+rdfs:label+\""
url2 = "\"+@ja++.+}&debug=on&timeout=&text/html"
url = url1 + key + url2

doc = Nokogiri::HTML(open(URI.encode(url)).read)

doc.xpath('//uri').each do |item|
  puts item.text
end

res = "http://"
items = doc.xpath('//uri')
if items.size > 0
  res = "a"
end

puts res
