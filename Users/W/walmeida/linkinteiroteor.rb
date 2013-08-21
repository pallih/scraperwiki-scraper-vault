# Script Ruby para obter associar o id da proposição a url dos pdf's
require 'mechanize'
require 'nokogiri'

require 'spreadsheet'
require 'open-uri'           

# Iterando sobre os 2 arquivos com ids previamente obtidos existentes no servidor
for ind in 2..3 do
  url = "http://ec2-184-72-90-149.compute-1.amazonaws.com/ids#{ind}.xls"
  book = nil
  open url do |f|
    book = Spreadsheet.open f
  end
  
  sheet = book.worksheet 0
  
  limite = (ind == 1) ? 65535 : 27386 
  
  
  # Iterando sobre as linhas de cada planilha
  for i in 1..limite do
    row  = sheet.row(i)
    id   = Integer(row[0])
    
    agent = Mechanize.new
    page = agent.get("http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=#{id}")
    doc = Nokogiri::XML(page.body)
  
    props = doc.xpath('//proposicao').map do |proposicao|
      data = {'id' => id, 
              'urlPdf' => proposicao.xpath('LinkInteiroTeor').text,
             }
    
      ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
      #p data.to_json
    
    end  
  end
end




