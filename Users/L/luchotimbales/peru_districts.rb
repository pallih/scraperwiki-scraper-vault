# Ruby script to obtains electoral results from Peru @ http://www.infogob.com.pe

$id_region={}, $id_provincia={}, $id_distrito={}

puts "*********************STARTING***************"
puts "*********************GETTING REGIONS DATA***************"

#REGIONES
url= "http://www.infogob.com.pe/Localidad/Ubigeo/000000.xml"
html= ScraperWiki.scrape(url)
puts html

count_region=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('idubigeo').each do |area|
  #puts area.inner_html
  $id_region[count_region]=area.inner_html
  count_region=count_region+1
end

puts "Numero de regiones "+ count_region.to_s()

puts "*********************GETTING PROVINCES DATA***************"

#PROVINCIAS
count_prov=0
for j in 0..count_region-1
  url= "http://www.infogob.com.pe/Localidad/Ubigeo/"+ $id_region[j].to_s()  +".xml"
  html= ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('idubigeo').each do |area|
    #puts area.inner_html
    $id_provincia[count_prov]=area.inner_html
    count_prov=count_prov+1
  end
end

puts "Numero de provincias "+ count_prov.to_s()
puts "*********************GETTING DISTRICS DATA***************"

#DISTRITO
count_dis=0
for j in 0..count_prov-1
  url= "http://www.infogob.com.pe/Localidad/Ubigeo/"+ $id_provincia[j].to_s()  +".xml"
  puts url
  html= ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('idubigeo').each do |area|
    #puts area.inner_html
    $id_distrito[count_dis]=area.inner_html
    count_dis=count_dis+1
  end
end

puts "Numero de distritos "+ count_dis.to_s()

#Save to store
for i in 0..count_dis-1     
    ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_distrito[i]})    
end
# Ruby script to obtains electoral results from Peru @ http://www.infogob.com.pe

$id_region={}, $id_provincia={}, $id_distrito={}

puts "*********************STARTING***************"
puts "*********************GETTING REGIONS DATA***************"

#REGIONES
url= "http://www.infogob.com.pe/Localidad/Ubigeo/000000.xml"
html= ScraperWiki.scrape(url)
puts html

count_region=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('idubigeo').each do |area|
  #puts area.inner_html
  $id_region[count_region]=area.inner_html
  count_region=count_region+1
end

puts "Numero de regiones "+ count_region.to_s()

puts "*********************GETTING PROVINCES DATA***************"

#PROVINCIAS
count_prov=0
for j in 0..count_region-1
  url= "http://www.infogob.com.pe/Localidad/Ubigeo/"+ $id_region[j].to_s()  +".xml"
  html= ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('idubigeo').each do |area|
    #puts area.inner_html
    $id_provincia[count_prov]=area.inner_html
    count_prov=count_prov+1
  end
end

puts "Numero de provincias "+ count_prov.to_s()
puts "*********************GETTING DISTRICS DATA***************"

#DISTRITO
count_dis=0
for j in 0..count_prov-1
  url= "http://www.infogob.com.pe/Localidad/Ubigeo/"+ $id_provincia[j].to_s()  +".xml"
  puts url
  html= ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('idubigeo').each do |area|
    #puts area.inner_html
    $id_distrito[count_dis]=area.inner_html
    count_dis=count_dis+1
  end
end

puts "Numero de distritos "+ count_dis.to_s()

#Save to store
for i in 0..count_dis-1     
    ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_distrito[i]})    
end
# Ruby script to obtains electoral results from Peru @ http://www.infogob.com.pe

$id_region={}, $id_provincia={}, $id_distrito={}

puts "*********************STARTING***************"
puts "*********************GETTING REGIONS DATA***************"

#REGIONES
url= "http://www.infogob.com.pe/Localidad/Ubigeo/000000.xml"
html= ScraperWiki.scrape(url)
puts html

count_region=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('idubigeo').each do |area|
  #puts area.inner_html
  $id_region[count_region]=area.inner_html
  count_region=count_region+1
end

puts "Numero de regiones "+ count_region.to_s()

puts "*********************GETTING PROVINCES DATA***************"

#PROVINCIAS
count_prov=0
for j in 0..count_region-1
  url= "http://www.infogob.com.pe/Localidad/Ubigeo/"+ $id_region[j].to_s()  +".xml"
  html= ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('idubigeo').each do |area|
    #puts area.inner_html
    $id_provincia[count_prov]=area.inner_html
    count_prov=count_prov+1
  end
end

puts "Numero de provincias "+ count_prov.to_s()
puts "*********************GETTING DISTRICS DATA***************"

#DISTRITO
count_dis=0
for j in 0..count_prov-1
  url= "http://www.infogob.com.pe/Localidad/Ubigeo/"+ $id_provincia[j].to_s()  +".xml"
  puts url
  html= ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('idubigeo').each do |area|
    #puts area.inner_html
    $id_distrito[count_dis]=area.inner_html
    count_dis=count_dis+1
  end
end

puts "Numero de distritos "+ count_dis.to_s()

#Save to store
for i in 0..count_dis-1     
    ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_distrito[i]})    
end
# Ruby script to obtains electoral results from Peru @ http://www.infogob.com.pe

$id_region={}, $id_provincia={}, $id_distrito={}

puts "*********************STARTING***************"
puts "*********************GETTING REGIONS DATA***************"

#REGIONES
url= "http://www.infogob.com.pe/Localidad/Ubigeo/000000.xml"
html= ScraperWiki.scrape(url)
puts html

count_region=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('idubigeo').each do |area|
  #puts area.inner_html
  $id_region[count_region]=area.inner_html
  count_region=count_region+1
end

puts "Numero de regiones "+ count_region.to_s()

puts "*********************GETTING PROVINCES DATA***************"

#PROVINCIAS
count_prov=0
for j in 0..count_region-1
  url= "http://www.infogob.com.pe/Localidad/Ubigeo/"+ $id_region[j].to_s()  +".xml"
  html= ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('idubigeo').each do |area|
    #puts area.inner_html
    $id_provincia[count_prov]=area.inner_html
    count_prov=count_prov+1
  end
end

puts "Numero de provincias "+ count_prov.to_s()
puts "*********************GETTING DISTRICS DATA***************"

#DISTRITO
count_dis=0
for j in 0..count_prov-1
  url= "http://www.infogob.com.pe/Localidad/Ubigeo/"+ $id_provincia[j].to_s()  +".xml"
  puts url
  html= ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('idubigeo').each do |area|
    #puts area.inner_html
    $id_distrito[count_dis]=area.inner_html
    count_dis=count_dis+1
  end
end

puts "Numero de distritos "+ count_dis.to_s()

#Save to store
for i in 0..count_dis-1     
    ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> $id_distrito[i]})    
end
