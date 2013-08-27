# Ruby script that grabs data from argentinian government website

expediente_id={}
title_info={}
counter=0

url= "http://www.march.es/recursos_web/Bibliotecas/data_clean3.html"
html= ScraperWiki.scrape(url)
require 'nokogiri'
puts html
    
doc = Nokogiri::HTML(html, nil, 'utf-8')
puts doc
doc.search('div[@class="Exp"]').each do |expediente|
  puts "expediente: "+ expediente.inner_html
  expediente_id[counter]= expediente.inner_html
  counter=counter+1
end

puts "numero de ids: "+ counter.to_s()
counter=0
doc.search('div[@class="Title"]').each do |title|
  puts "title: "+ title.inner_html
  title_info[counter]=title.inner_html
  counter=counter+1
end
puts "numero de titulos: "+ counter.to_s()

for i in 0..counter-1
puts "expediente "+ expediente_id[i]
puts "titulo "+ title_info[i]
ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> expediente_id[i], "Titulo"=> title_info[i]})

end

puts "total: "+ counter.to_s()
# Ruby script that grabs data from argentinian government website

expediente_id={}
title_info={}
counter=0

url= "http://www.march.es/recursos_web/Bibliotecas/data_clean3.html"
html= ScraperWiki.scrape(url)
require 'nokogiri'
puts html
    
doc = Nokogiri::HTML(html, nil, 'utf-8')
puts doc
doc.search('div[@class="Exp"]').each do |expediente|
  puts "expediente: "+ expediente.inner_html
  expediente_id[counter]= expediente.inner_html
  counter=counter+1
end

puts "numero de ids: "+ counter.to_s()
counter=0
doc.search('div[@class="Title"]').each do |title|
  puts "title: "+ title.inner_html
  title_info[counter]=title.inner_html
  counter=counter+1
end
puts "numero de titulos: "+ counter.to_s()

for i in 0..counter-1
puts "expediente "+ expediente_id[i]
puts "titulo "+ title_info[i]
ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> expediente_id[i], "Titulo"=> title_info[i]})

end

puts "total: "+ counter.to_s()
# Ruby script that grabs data from argentinian government website

expediente_id={}
title_info={}
counter=0

url= "http://www.march.es/recursos_web/Bibliotecas/data_clean3.html"
html= ScraperWiki.scrape(url)
require 'nokogiri'
puts html
    
doc = Nokogiri::HTML(html, nil, 'utf-8')
puts doc
doc.search('div[@class="Exp"]').each do |expediente|
  puts "expediente: "+ expediente.inner_html
  expediente_id[counter]= expediente.inner_html
  counter=counter+1
end

puts "numero de ids: "+ counter.to_s()
counter=0
doc.search('div[@class="Title"]').each do |title|
  puts "title: "+ title.inner_html
  title_info[counter]=title.inner_html
  counter=counter+1
end
puts "numero de titulos: "+ counter.to_s()

for i in 0..counter-1
puts "expediente "+ expediente_id[i]
puts "titulo "+ title_info[i]
ScraperWiki.save_sqlite(unique_keys=["ID"], data={"ID"=> expediente_id[i], "Titulo"=> title_info[i]})

end

puts "total: "+ counter.to_s()
