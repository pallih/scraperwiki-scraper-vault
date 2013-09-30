# encoding: utf-8
require 'open-uri'
require 'nokogiri'

BASE_URL = 'http://www.rendiciondecuentas.es/es/consultadeentidadesycuentas/buscarEntidades/index.html?'\
           'denominacion=&idTipoEntidad=A'
SUFFIX_URL = '&submitFormBusquedaEntidades=Buscar#resultados'

#CCAA: Castilla y Leon
idRegion = 8
#idProv: Valladolid
idProv = 47

search_params = "&d-2677838-p=1&idComunidadAutonoma=#{idRegion}&idProvincia=#{idProv}"
page = Nokogiri::HTML(open("#{BASE_URL}#{search_params}#{SUFFIX_URL}"))
link = page.css('div.paginacion li.last a')[0]['href']
link =~ /d-2677838-p=(\d{1,2}).*$/
numPages = $1.to_i
for i in 1..numPages
  #Retrieve municipalities ids for each page of a given province
  search_params = "&d-2677838-p=#{i}&idComunidadAutonoma=#{idRegion}&idProvincia=#{idProv}"
  page = Nokogiri::HTML(open("#{BASE_URL}#{search_params}#{SUFFIX_URL}"))
  rows = page.css('table#resultados tbody tr')
  if rows.length > 0 
    rows[0..-1].each do |row|
      cells = row.css('td')
      idEntity = cells[0].css("input")[0]['value']
      name = cells[2].text.strip
      data = {
        idRegion: idRegion,
        idProv: idProv,
        idEntity: idEntity,
        name: name
      }
       ScraperWiki::save_sqlite(['idRegion','idProv','idEntity'], data)
    end # end of rows.each
  end
  sleep(1)
end

# encoding: utf-8
require 'open-uri'
require 'nokogiri'

BASE_URL = 'http://www.rendiciondecuentas.es/es/consultadeentidadesycuentas/buscarEntidades/index.html?'\
           'denominacion=&idTipoEntidad=A'
SUFFIX_URL = '&submitFormBusquedaEntidades=Buscar#resultados'

#CCAA: Castilla y Leon
idRegion = 8
#idProv: Valladolid
idProv = 47

search_params = "&d-2677838-p=1&idComunidadAutonoma=#{idRegion}&idProvincia=#{idProv}"
page = Nokogiri::HTML(open("#{BASE_URL}#{search_params}#{SUFFIX_URL}"))
link = page.css('div.paginacion li.last a')[0]['href']
link =~ /d-2677838-p=(\d{1,2}).*$/
numPages = $1.to_i
for i in 1..numPages
  #Retrieve municipalities ids for each page of a given province
  search_params = "&d-2677838-p=#{i}&idComunidadAutonoma=#{idRegion}&idProvincia=#{idProv}"
  page = Nokogiri::HTML(open("#{BASE_URL}#{search_params}#{SUFFIX_URL}"))
  rows = page.css('table#resultados tbody tr')
  if rows.length > 0 
    rows[0..-1].each do |row|
      cells = row.css('td')
      idEntity = cells[0].css("input")[0]['value']
      name = cells[2].text.strip
      data = {
        idRegion: idRegion,
        idProv: idProv,
        idEntity: idEntity,
        name: name
      }
       ScraperWiki::save_sqlite(['idRegion','idProv','idEntity'], data)
    end # end of rows.each
  end
  sleep(1)
end

