# Extraer datos electorales de la página www.belge.net

# declarar array
$id_province={}

# Crear variable con identificador de provincia de la página html
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=turkish_provinces&query=select%20*%20from%20%60swdata%60%20limit%20100"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('tr').each do |datos|
  #puts datos
  if l==0 then
  else
    puts datos.css('td')[1].inner_text
    $id_province[l]=datos.css('td')[1].inner_text
  end
  l=l+1
end


for p in 1..l-1
  url= "http://www.belgenet.net/ayrinti.php?yil_id=15&il_id="+ $id_province[p].to_s()
  puts url
end
# Extraer datos electorales de la página www.belge.net

# declarar array
$id_province={}

# Crear variable con identificador de provincia de la página html
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=turkish_provinces&query=select%20*%20from%20%60swdata%60%20limit%20100"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('tr').each do |datos|
  #puts datos
  if l==0 then
  else
    puts datos.css('td')[1].inner_text
    $id_province[l]=datos.css('td')[1].inner_text
  end
  l=l+1
end


for p in 1..l-1
  url= "http://www.belgenet.net/ayrinti.php?yil_id=15&il_id="+ $id_province[p].to_s()
  puts url
end
