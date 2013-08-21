###############################################################################
# This is a scraper to look for names and other information of spanish senators
# from the senate web site
###############################################################################
require 'nokogiri'
require 'open-uri'


for j in 8..15
  URL= 'http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados?_piref73_2874067_73_1333049_1333049.next_page=/wc/busquedaAlfabeticaDiputados&paginaActual='+j.to_s() +'&idLegislatura=3&tipoBusqueda=completo'#this is the URL for the list of senators

  # the different years can be downloaded by changing the URL Legislatura=i with i=1..8
  html= ScraperWiki.scrape(URL)
  doc = Nokogiri::HTML(html)
  doc.css('div[@class = "listado_1"] > ul > li > a').each do |name|
    puts name.content
    record = {}
    record['Nombre']    = name.content
    record['Legislatura']     = 'III'
    record['URL']  = name['href']# this is the URL for each senator´s site with their info
    #puts name['href']
    $URL='http://www.congreso.es'+ name['href']
    html1 = ScraperWiki.scrape($URL)
    doc1 = Nokogiri::HTML(html1)
    $Prov = doc1.css('div[@class= "dip_rojo"]').first
    puts $Prov.content
    record['Provincia']=$Prov.content
    
    $Grup = doc1.css('div[@class= "dip_rojo"] > a').first
    unless $Grup.nil? 
      puts $Grup.content
      record['Grupo']=$Grup.content
    end

    i=1
    desc={}
    doc1.css('div[@class= "texto_dip"] > ul > li').each do |info|
      desc[i]=info.content
      puts i
      puts info.content
      i=i+1
    end
    record['Bio']=desc[3] #bio is normally on desc[3] but for legislatura=9 it´s on desc[4] 
    #record['FechaN']=desc[2]#this normally works but for legislatura=6 there is no birth date on the site
    # Print out the data we've gathered
    # puts record
    # Finally, save the record to the datastore - 'Nombre' is our unique key
    ScraperWiki.save(["Nombre"], record)  
  end
end