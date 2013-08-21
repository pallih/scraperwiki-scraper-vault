###############################################################################
# This is a scraper to look for names and other information of spanish senators
# from the senate web site
###############################################################################
require 'nokogiri'
require 'open-uri'

html = ScraperWiki.scrape("http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados?_piref73_1333056_73_1333049_1333049.next_page=/wc/menuAbecedarioInicio&tipoBusqueda=completo&idLegislatura=7")
puts html

# define the order our columns are displayed in the datastore
mdc = SW_MetadataClient.new
mdc.save('data_columns', ['Nombre', 'Legislatura', 'URL']) 

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

doc = Nokogiri::HTML(html)
doc.css('div[@class = "listado_1"] > ul > li > a').each do |name|
    puts name.content
    #puts name['href']
    #ScraperWiki.save(['Nombre'], {'Nombre' => name.content})
    #ScraperWiki.save(['URL'], {'URL' => name['href']})
    record = {}
    record['Nombre']    = name.content
    record['Legislatura']     = '7'
    record['URL']  = name['href']
    # Print out the data we've gathered
    puts record
    # Finally, save the record to the datastore - 'Artist' is our unique key
    ScraperWiki.save(["Nombre"], record)
end

for i in 1..15
  URL= 'http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados?_piref73_2874067_73_1333049_1333049.next_page=/wc/busquedaAlfabeticaDiputados&paginaActual='+i.to_s() +'&idLegislatura=7&tipoBusqueda=completo'
  html= ScraperWiki.scrape(URL)
  doc = Nokogiri::HTML(html)
  doc.css('div[@class = "listado_1"] > ul > li > a').each do |name|
      puts name.content
      #ScraperWiki.save(['Nombre'], {'Nombre' => name.content})
      record = {}
      record['Nombre']    = name.content
      record['Legislatura']     = '7'
      record['URL']  = name['href']
      # Print out the data we've gathered
      puts record
      # Finally, save the record to the datastore - 'Artist' is our unique key
      ScraperWiki.save(["Nombre"], record)
  end
end




