require 'mechanize'
require 'nokogiri'


# The trick xD
agent = Mechanize.new
page = agent.get('http://www.camara.gov.br/sitcamaraws/deputados.asmx/ObterDeputados')

doc = Nokogiri::XML(page.body)

deputados = doc.xpath('//deputados/deputado').map do |deputado|
  aux = deputado.xpath('nomeParlamentar').text.split(' ') 
  
  data = {'id' => deputado.xpath('idParlamentar').text, 'pnome' => aux.first, 'unome' => aux.last, 'partido' => deputado.xpath('partido').text }
  ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
end
require 'mechanize'
require 'nokogiri'


# The trick xD
agent = Mechanize.new
page = agent.get('http://www.camara.gov.br/sitcamaraws/deputados.asmx/ObterDeputados')

doc = Nokogiri::XML(page.body)

deputados = doc.xpath('//deputados/deputado').map do |deputado|
  aux = deputado.xpath('nomeParlamentar').text.split(' ') 
  
  data = {'id' => deputado.xpath('idParlamentar').text, 'pnome' => aux.first, 'unome' => aux.last, 'partido' => deputado.xpath('partido').text }
  ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
end
