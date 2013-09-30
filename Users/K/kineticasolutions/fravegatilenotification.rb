require 'cgi'
params = CGI::parse( ENV['QUERY_STRING'] )
category = params["category"][0];
subCategory = params["subcategory"][0];
queryprefix = "REPLACE(REPLACE(REPLACE(pfregular,'.',''),'$',''),',00','') AS price, * from src.swdata"

if subCategory == "ofertas"
  #sourcescraper = "fravegaofertas_1"
  #query = "* from src.swdata limit ? offset ?"
  sourcescraper = "fravegaproductosporsubcategoria"
  query = queryprefix + " where price > '998' limit ? offset ?"
elsif subCategory == "masvendidos"
  sourcescraper = "fravegamasvendidos"
  query = queryprefix + " where price > '998' limit ? offset ?"
else
  sourcescraper = "fravegaproductosporsubcategoria"
  query = queryprefix + " where category='#{category}' and subCategory='#{subCategory}' order by 1 desc limit ? offset ?"
end

limit = 10
offset = 0
ScraperWiki::attach(sourcescraper, "src")

products = ScraperWiki::select(query, [limit, offset])
product = products.sample
ScraperWiki::httpresponseheader("Content-Type", "xml")
puts "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
puts "<tile>"
  puts "<visual>"
    puts "<binding template=\"TileWideImageAndText01\">"
      puts "<image id=\"1\" src=\"#{CGI::escapeHTML(product['imageUrl'])}\" alt=\"#{CGI::escapeHTML(product['name'])}\"/>"
      puts "<text id=\"1\">#{CGI::escapeHTML(product['name'])}</text>"
    puts "</binding>"
    puts "<binding template=\"TileSquarePeekImageAndText04\">"
      puts "<image id=\"1\" src=\"#{CGI::escapeHTML(product['imageUrl'])}\" alt=\"#{CGI::escapeHTML(product['name'])}\"/>"
      puts "<text id=\"1\">#{CGI::escapeHTML(product['name'])}</text>"
    puts "</binding>"
  puts "</visual>"
puts "</tile>"
require 'cgi'
params = CGI::parse( ENV['QUERY_STRING'] )
category = params["category"][0];
subCategory = params["subcategory"][0];
queryprefix = "REPLACE(REPLACE(REPLACE(pfregular,'.',''),'$',''),',00','') AS price, * from src.swdata"

if subCategory == "ofertas"
  #sourcescraper = "fravegaofertas_1"
  #query = "* from src.swdata limit ? offset ?"
  sourcescraper = "fravegaproductosporsubcategoria"
  query = queryprefix + " where price > '998' limit ? offset ?"
elsif subCategory == "masvendidos"
  sourcescraper = "fravegamasvendidos"
  query = queryprefix + " where price > '998' limit ? offset ?"
else
  sourcescraper = "fravegaproductosporsubcategoria"
  query = queryprefix + " where category='#{category}' and subCategory='#{subCategory}' order by 1 desc limit ? offset ?"
end

limit = 10
offset = 0
ScraperWiki::attach(sourcescraper, "src")

products = ScraperWiki::select(query, [limit, offset])
product = products.sample
ScraperWiki::httpresponseheader("Content-Type", "xml")
puts "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
puts "<tile>"
  puts "<visual>"
    puts "<binding template=\"TileWideImageAndText01\">"
      puts "<image id=\"1\" src=\"#{CGI::escapeHTML(product['imageUrl'])}\" alt=\"#{CGI::escapeHTML(product['name'])}\"/>"
      puts "<text id=\"1\">#{CGI::escapeHTML(product['name'])}</text>"
    puts "</binding>"
    puts "<binding template=\"TileSquarePeekImageAndText04\">"
      puts "<image id=\"1\" src=\"#{CGI::escapeHTML(product['imageUrl'])}\" alt=\"#{CGI::escapeHTML(product['name'])}\"/>"
      puts "<text id=\"1\">#{CGI::escapeHTML(product['name'])}</text>"
    puts "</binding>"
  puts "</visual>"
puts "</tile>"
