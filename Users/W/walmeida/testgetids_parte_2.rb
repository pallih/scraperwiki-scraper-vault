require 'mechanize'
require 'nokogiri'

require 'spreadsheet'
require 'open-uri'           

# Parte 2
url = "http://ec2-50-17-37-5.compute-1.amazonaws.com/ids3.xls"
book = nil
open url do |f|
  book = Spreadsheet.open f
end

sheet = book.worksheet 0

for i in 1..27386 do
  row  = sheet.row(i)
  id   = Integer(row[0])
  
  agent = Mechanize.new
  page = agent.get("http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=#{id}")
  doc = Nokogiri::XML(page.body)

  props = doc.xpath('//proposicao').map do |proposicao|
    valorData = proposicao.xpath('DataApresentacao').text
    arrayData = valorData.split('/')
    formatada = arrayData[2].to_s + '-' + arrayData[1].to_s + '-' + arrayData[0].to_s

    data = {'id' => id, 
            'title' => proposicao.xpath('nomeProposicao').text,
            'description' => proposicao.xpath('Ementa').text,
            'data' => formatada,
            'autor' => proposicao.xpath('Autor').text,
            'status' => 'Avaliada',
            'numero' => proposicao['numero'],
            'tipo' => proposicao['tipo'].strip,
            'ano' => proposicao['ano']
           }
  
    #ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
  p data.to_json
  
  end  
end

# The trick xD
#agent = Mechanize.new
#page = agent.get('http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=533533')
#page = agent.get('http://www.camara.gov.br/sileg/Prop_lista.asp?sigla=&Numero=&Ano=&Autor=&OrgaoOrigem=todos&Comissao=0&Situacao=&dtInicio=02%2F10%2F2007&dtFim=03%2F10%2F2007&Ass1=&co1=+AND+&Ass2=&co2=+AND+&Ass3=&Submit=Pesquisar&Relator='

require 'mechanize'
require 'nokogiri'

require 'spreadsheet'
require 'open-uri'           

# Parte 2
url = "http://ec2-50-17-37-5.compute-1.amazonaws.com/ids3.xls"
book = nil
open url do |f|
  book = Spreadsheet.open f
end

sheet = book.worksheet 0

for i in 1..27386 do
  row  = sheet.row(i)
  id   = Integer(row[0])
  
  agent = Mechanize.new
  page = agent.get("http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=#{id}")
  doc = Nokogiri::XML(page.body)

  props = doc.xpath('//proposicao').map do |proposicao|
    valorData = proposicao.xpath('DataApresentacao').text
    arrayData = valorData.split('/')
    formatada = arrayData[2].to_s + '-' + arrayData[1].to_s + '-' + arrayData[0].to_s

    data = {'id' => id, 
            'title' => proposicao.xpath('nomeProposicao').text,
            'description' => proposicao.xpath('Ementa').text,
            'data' => formatada,
            'autor' => proposicao.xpath('Autor').text,
            'status' => 'Avaliada',
            'numero' => proposicao['numero'],
            'tipo' => proposicao['tipo'].strip,
            'ano' => proposicao['ano']
           }
  
    #ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
  p data.to_json
  
  end  
end

# The trick xD
#agent = Mechanize.new
#page = agent.get('http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=533533')
#page = agent.get('http://www.camara.gov.br/sileg/Prop_lista.asp?sigla=&Numero=&Ano=&Autor=&OrgaoOrigem=todos&Comissao=0&Situacao=&dtInicio=02%2F10%2F2007&dtFim=03%2F10%2F2007&Ass1=&co1=+AND+&Ass2=&co2=+AND+&Ass3=&Submit=Pesquisar&Relator='

