# encoding: utf-8
require 'open-uri'
require 'nokogiri'

BASE_URL = 'http://www.rendiciondecuentas.es'
PREFIX_URL = '/es/consultadeentidadesycuentas/buscarEntidades/consultarEntidad.html?option=Informaci%F3n+Censal&idTipoEntidad=A'

ScraperWiki::attach("rendicion_cuentas_3")
entities = ScraperWiki::select("* from rendicion_cuentas_3.swdata where persExpense > 0")
entities.each do |entity|
  search_params="&ejercicio=#{entity['year']}&idComunidadAutonoma=#{entity['idRegion']}&idProvincia=#{entity['idProv']}&idEntidad=#{entity['idEntity']}"
  puts "#{BASE_URL}#{PREFIX_URL}#{search_params}"
  begin
    page = Nokogiri::HTML(open("#{BASE_URL}#{PREFIX_URL}#{search_params}"))
    cells = page.css('table.tabla01 tbody td')
    cells.each_with_index do |cell, index|       
      if (cell.text =~ /Población:\s*$/)
        tPopulation = cells[index+1].text
        population = tPopulation.gsub(".","").to_i
        percentage = entity['persExpense'] / population
        puts population, percentage        
        data = {
          idRegion: entity['idRegion'],
          idProv: entity['idProv'],
          idEntity: entity['idEntity'],
          name: entity['name'],
          year: entity['year'],
          persExpense: entity['persExpense'],
          population: population,
          percentage: percentage
        }
        ScraperWiki::save_sqlite(['idRegion','idProv','idEntity','year'], data)
        break
      end
    end
  rescue OpenURI::HTTPError => the_error
    # the_error.message is the numeric code and text in a string
    # Write to console: page does not exist
    puts("#{BASE_URL}#{PREFIX_URL}#{search_params}: Got a bad status code #{the_error.message}")
  end
  sleep(1)
end

