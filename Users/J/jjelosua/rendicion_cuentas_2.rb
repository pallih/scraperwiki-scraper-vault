# encoding: utf-8
require 'open-uri'
require 'nokogiri'

BASE_URL = 'http://www.rendiciondecuentas.es'
PREFIX_URL = '/es/consultadeentidadesycuentas/buscarCuentas/consultarCuenta.html?'

#We are going to retrieve data for 2011
year = 2011

ScraperWiki::attach("rendicion_cuentas_1")
entities = ScraperWiki::select("* from rendicion_cuentas_1.swdata")
entities.each do |entity|
  search_params="&idEntidad=#{entity['idEntity']}&ejercicio=#{year}"
  puts "#{BASE_URL}#{PREFIX_URL}#{search_params}"
  begin
    page = Nokogiri::HTML(open("#{BASE_URL}#{PREFIX_URL}#{search_params}"))
    link = page.css('table.tabla01 td a')
    if link.length > 0
      rel = link[0]['href']
      url = "#{BASE_URL}#{rel}&option=vc"
      data = {
        idRegion: entity['idRegion'],
        idProv: entity['idProv'],
        idEntity: entity['idEntity'],
        name: entity['name'],
        year: year,
        url: url 
      }
      ScraperWiki::save_sqlite(['idRegion','idProv','idEntity','year'], data)
    else
      #Write to console: no budget available for this entity and year
      puts("#{BASE_URL}#{PREFIX_URL}#{search_params}: No available information")
    end
  rescue OpenURI::HTTPError => the_error
    # the_error.message is the numeric code and text in a string
    # Write to console: page does not exist
    puts("#{BASE_URL}#{PREFIX_URL}#{search_params}: Got a bad status code #{the_error.message}")
  end
  sleep(1)
end

