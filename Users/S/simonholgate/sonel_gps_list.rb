# -*- coding: utf-8 -*-
require 'rubygems'
require 'open-uri'
require 'nokogiri'
doc = Nokogiri::HTML(open("http://www.sonel.org/-GPS,28-.html?lang=en"))
cdata = doc.xpath("//html/head").text

parts = cdata.scan(/showGmapTabHtml\(this\, \'(\d+)\'\)\\\">(\w+)<\\\/span><div class=\'clsL\'><\\\/div><\\\/div><div style=\\\"display:block;\\\" class=\\\"tabGmapBody\\\" id=\\\"\w+\\\"><b>GPS : <\\\/b>(.*?)<br \\\/><b>Latitude : <\\\/b>(.*?)<br \\\/><b>Longitude : <\\\/b>(.*?)<br \\\/><b>Fournisseur : <\\\/b>(\w+)<br \\\/><a href=\\\"(.*?)\\\">/i)


for v in (0..(parts.length-1))
  data = {
    'name' => parts[v][2],
    'id' => parts[v][0].to_i,
    'lat' => parts[v][3].to_f,
    'lon' => parts[v][4].to_f,
    'code' => parts[v][1],
    'supplier' => parts[v][5],
    'path' => parts[v][6]
  }
  ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
end
# -*- coding: utf-8 -*-
require 'rubygems'
require 'open-uri'
require 'nokogiri'
doc = Nokogiri::HTML(open("http://www.sonel.org/-GPS,28-.html?lang=en"))
cdata = doc.xpath("//html/head").text

parts = cdata.scan(/showGmapTabHtml\(this\, \'(\d+)\'\)\\\">(\w+)<\\\/span><div class=\'clsL\'><\\\/div><\\\/div><div style=\\\"display:block;\\\" class=\\\"tabGmapBody\\\" id=\\\"\w+\\\"><b>GPS : <\\\/b>(.*?)<br \\\/><b>Latitude : <\\\/b>(.*?)<br \\\/><b>Longitude : <\\\/b>(.*?)<br \\\/><b>Fournisseur : <\\\/b>(\w+)<br \\\/><a href=\\\"(.*?)\\\">/i)


for v in (0..(parts.length-1))
  data = {
    'name' => parts[v][2],
    'id' => parts[v][0].to_i,
    'lat' => parts[v][3].to_f,
    'lon' => parts[v][4].to_f,
    'code' => parts[v][1],
    'supplier' => parts[v][5],
    'path' => parts[v][6]
  }
  ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
end
