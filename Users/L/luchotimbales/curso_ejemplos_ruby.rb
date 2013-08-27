# Curso web scraping avanzado
# sacar datos de varias páginas web http://www.izbori.ba/rezultati/konacni/parlament_bih/index.htm

id_areas={}
id_areas[0]="511"
id_areas[1]="512"
id_areas[2]="513"
id_areas[3]="514"
id_areas[4]="515"
id_areas[5]="521"
id_areas[6]="522"
id_areas[7]="523"

for i in 0..7
  URL="http://www.izbori.ba/rezultati/konacni/parlament_bih/bihMainPage.asp?jed="+ id_areas[i].to_s()
  html = ScraperWiki.scrape(URL)
  puts URL

  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('td[@valign="top"]> div[align="left"]> table[@class="style7"]> tr').each do |row|  
    puts row
    puts row.css('td')[2].text
    puts row.css('td')[3].text
    puts row.css('td')[4].text
    
    record={}
    record ['ID']= id_areas[i].to_s() +"_" +row.css('td')[2].text
    record ['Partido']=row.css('td')[2].text
    record ['Votos']=row.css('td')[3].text
    record ['Porcentaje']= row.css('td')[4].text
    ScraperWiki.save_sqlite(["ID"], record)

  end
end
# Curso web scraping avanzado
# sacar datos de varias páginas web http://www.izbori.ba/rezultati/konacni/parlament_bih/index.htm

id_areas={}
id_areas[0]="511"
id_areas[1]="512"
id_areas[2]="513"
id_areas[3]="514"
id_areas[4]="515"
id_areas[5]="521"
id_areas[6]="522"
id_areas[7]="523"

for i in 0..7
  URL="http://www.izbori.ba/rezultati/konacni/parlament_bih/bihMainPage.asp?jed="+ id_areas[i].to_s()
  html = ScraperWiki.scrape(URL)
  puts URL

  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('td[@valign="top"]> div[align="left"]> table[@class="style7"]> tr').each do |row|  
    puts row
    puts row.css('td')[2].text
    puts row.css('td')[3].text
    puts row.css('td')[4].text
    
    record={}
    record ['ID']= id_areas[i].to_s() +"_" +row.css('td')[2].text
    record ['Partido']=row.css('td')[2].text
    record ['Votos']=row.css('td')[3].text
    record ['Porcentaje']= row.css('td')[4].text
    ScraperWiki.save_sqlite(["ID"], record)

  end
end
# Curso web scraping avanzado
# sacar datos de varias páginas web http://www.izbori.ba/rezultati/konacni/parlament_bih/index.htm

id_areas={}
id_areas[0]="511"
id_areas[1]="512"
id_areas[2]="513"
id_areas[3]="514"
id_areas[4]="515"
id_areas[5]="521"
id_areas[6]="522"
id_areas[7]="523"

for i in 0..7
  URL="http://www.izbori.ba/rezultati/konacni/parlament_bih/bihMainPage.asp?jed="+ id_areas[i].to_s()
  html = ScraperWiki.scrape(URL)
  puts URL

  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('td[@valign="top"]> div[align="left"]> table[@class="style7"]> tr').each do |row|  
    puts row
    puts row.css('td')[2].text
    puts row.css('td')[3].text
    puts row.css('td')[4].text
    
    record={}
    record ['ID']= id_areas[i].to_s() +"_" +row.css('td')[2].text
    record ['Partido']=row.css('td')[2].text
    record ['Votos']=row.css('td')[3].text
    record ['Porcentaje']= row.css('td')[4].text
    ScraperWiki.save_sqlite(["ID"], record)

  end
end
