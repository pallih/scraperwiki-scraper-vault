###############################################################################
# This is a scraper to look for names of spanish senators that left their seat
# from the senate web site
###############################################################################
require 'nokogiri'
require 'open-uri'


for j in 0..15
  URL= 'http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados?_piref73_2874067_73_1333049_1333049.next_page=/wc/busquedaAlfabeticaDiputados&paginaActual='+j.to_s() +'&idLegislatura=2&tipoBusqueda=completo'#this is the URL for the list of senators
  puts URL

  # the different years can be downloaded by changing the URL Legislatura=i with i=1..8
  html= ScraperWiki.scrape(URL)
  doc = Nokogiri::HTML(html)
  doc.css('div[@class = "listado_1"] > ul > li > a').each do |name|
    puts name.content
    record = {}
    URL1= 'http://www.congreso.es'+name['href']
    puts URL1
    # http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado&idDiputado=366&idLegislatura=6
    html1 = ScraperWiki.scrape(URL1)
    puts html1
    doc1 = Nokogiri::HTML(html1)
    i=1
    desc={}
    doc1.css('div[@class= "dip_rojo"]').each do |info|
      desc[i]=info.content
      i=i+1
    end
    doc1.css('p[@class= "dip_rojo"]').each do |info|
      desc[i]= info.content
      i=i+1
    end
    #desc[1] y desc[2] have information that is not relevant; desc[3]#fecha de baja y desc[4]#Diputado que lo sustituye
    if i==5
      record['Nombre']    = name.content
      record['Legislatura']     = 'II'
      record['URL']  = name['href']# this is the URL for each senator´s site with their info
      record['Fecha']=desc[3]
      record['NombreNuevo']=desc[4]
      puts record
      ScraperWiki.save(["Nombre"], record) 
    end
  end
end  

###############################################################################
# This is a scraper to look for names of spanish senators that left their seat
# from the senate web site
###############################################################################
require 'nokogiri'
require 'open-uri'


for j in 0..15
  URL= 'http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados?_piref73_2874067_73_1333049_1333049.next_page=/wc/busquedaAlfabeticaDiputados&paginaActual='+j.to_s() +'&idLegislatura=2&tipoBusqueda=completo'#this is the URL for the list of senators
  puts URL

  # the different years can be downloaded by changing the URL Legislatura=i with i=1..8
  html= ScraperWiki.scrape(URL)
  doc = Nokogiri::HTML(html)
  doc.css('div[@class = "listado_1"] > ul > li > a').each do |name|
    puts name.content
    record = {}
    URL1= 'http://www.congreso.es'+name['href']
    puts URL1
    # http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado&idDiputado=366&idLegislatura=6
    html1 = ScraperWiki.scrape(URL1)
    puts html1
    doc1 = Nokogiri::HTML(html1)
    i=1
    desc={}
    doc1.css('div[@class= "dip_rojo"]').each do |info|
      desc[i]=info.content
      i=i+1
    end
    doc1.css('p[@class= "dip_rojo"]').each do |info|
      desc[i]= info.content
      i=i+1
    end
    #desc[1] y desc[2] have information that is not relevant; desc[3]#fecha de baja y desc[4]#Diputado que lo sustituye
    if i==5
      record['Nombre']    = name.content
      record['Legislatura']     = 'II'
      record['URL']  = name['href']# this is the URL for each senator´s site with their info
      record['Fecha']=desc[3]
      record['NombreNuevo']=desc[4]
      puts record
      ScraperWiki.save(["Nombre"], record) 
    end
  end
end  

