ciclo=String.new
url_ciclo=String.new
interpretes=String.new
compositores=String.new
record={}

for i in 10..12
  url= "http://www.march.es/calendario/?p3=1&p1="+ i.to_s()+"&p0=2013&l=1"
  html= ScraperWiki.scrape(url,encoding="utf-8")     
  puts html
        
  require 'nokogiri'
  doc = Nokogiri::HTML(html , nil, 'utf-8')
  puts doc
  doc.search('li[@class="otrosciclos"]').each do |row|
    
    puts row
    puts row.css('p').attr('content')
    puts row.css('a').text
    puts row.css('a').attr('href')
    puts row.css('li[@itemprop="performers"]').text
    puts row.css('li[@itemprop="description"]').text
    fecha=row.css('p').attr('content')
    ciclo = row.css('a').text
    url_ciclo= "http://www.march.es"+ row.css('a').attr('href')
    interpretes=row.css('li[@itemprop="performers"]').text
    compositores=row.css('li[@itemprop="description"]').text
  
    
    record ['URL ciclo']= url_ciclo
    record ['Titulo Ciclo']= ciclo
    record ['Fecha']= fecha
    record ['Interpretes']= interpretes
    record ['Compositores']= compositores
    ScraperWiki.save_sqlite(["URL ciclo"], record)
  
  end

end