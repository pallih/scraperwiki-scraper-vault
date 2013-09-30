require 'csv'
require 'nokogiri'

data = ScraperWiki::scrape("http://projetos.camarapoa.rs.gov.br/consultas/em_tramitacao.csv").force_encoding('UTF-8')

def find_project_href(number)
  data = ScraperWiki::scrape("http://informatica.camarapoa.rs.gov.br/search?q=#{number}&btnG=Buscar&site=camara_poa_projetos&client=projetos").force_encoding('UTF-8')
  xml = Nokogiri::XML(data)
  (xml / '//U').first.text
end

dump = []
csv = CSV.new(data, col_sep: ';', headers: true).each do |line|
  hash = line.to_hash.inject({}) do |a, kv|
    a.merge(kv[0].downcase.gsub(/[^0-9a-z]/, "_") => kv[1])
  end

  hash['link'] = find_project_href hash['numero']
  hash['updated_at'] = Time.now.to_i
  dump << hash
end

ScraperWiki.save_sqlite(['numero'], dump, 'projetos_em_tramitacao')
require 'csv'
require 'nokogiri'

data = ScraperWiki::scrape("http://projetos.camarapoa.rs.gov.br/consultas/em_tramitacao.csv").force_encoding('UTF-8')

def find_project_href(number)
  data = ScraperWiki::scrape("http://informatica.camarapoa.rs.gov.br/search?q=#{number}&btnG=Buscar&site=camara_poa_projetos&client=projetos").force_encoding('UTF-8')
  xml = Nokogiri::XML(data)
  (xml / '//U').first.text
end

dump = []
csv = CSV.new(data, col_sep: ';', headers: true).each do |line|
  hash = line.to_hash.inject({}) do |a, kv|
    a.merge(kv[0].downcase.gsub(/[^0-9a-z]/, "_") => kv[1])
  end

  hash['link'] = find_project_href hash['numero']
  hash['updated_at'] = Time.now.to_i
  dump << hash
end

ScraperWiki.save_sqlite(['numero'], dump, 'projetos_em_tramitacao')
