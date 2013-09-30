require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.milanexpress.com.br/GOL/Lotes/'
CIDADES = {"Aracajú (SE)"=>"AJU", "Belo Horizonte (MG) - Confins"=>"CNF", "Belo Horizonte (MG) - Pampulha"=>"PLU", "Belém (PA)"=>"BEL", "Boa Vista (RR)"=>"BVB", "Brasília (DF)"=>"BSB", "Cabo Frio (RJ)"=>"CFB", "Campina Grande (PB)"=>"CPV", "Campinas (SP)"=>"CPQ", "Campo Grande (MS)"=>"CGR", "Caxias do Sul (RS)"=>"CXJ", "Chapecó (SC)"=>"XAP", "Cruzeiro do Sul (AC)"=>"CZS", "Cuiabá (MT)"=>"CGB", "Curitiba (PR)"=>"CWB", "Florianópolis (SC)"=>"FLN", "Fortaleza (CE)"=>"FOR", "Foz do Iguaçu (PR)"=>"IGU", "Goiânia (GO)"=>"GYN", "Ilhéus (BA)"=>"IOS", "Imperatriz (MA)"=>"IMP", "Joinville (SC)"=>"JOI", "João Pessoa (PB)"=>"JPA", "Juazeiro do Norte (CE)"=>"JDO", "Londrina (PR)"=>"LDB", "Macapá (AP)"=>"MCP", "Maceió (AL)"=>"MCZ", "Manaus (AM)"=>"MAO", "Marabá (PA)"=>"MAB", "Maringá (PR)"=>"MGF", "Natal (RN)"=>"NAT", "Navegantes (SC)"=>"NVT", "Palmas (TO)"=>"PMW", "Petrolina (PE)"=>"PNZ", "Porto Alegre (RS)"=>"POA", "Porto Seguro (BA)"=>"BPS", "Porto Velho (RO)"=>"PVH", "Presidente Prudente (SP)"=>"PPB", "Recife (PE)"=>"REC", "Ribeirão Preto (SP)"=>"RAO", "Rio Branco (AC)"=>"RBR", "Rio de Janeiro (RJ) - Galeão"=>"GIG", "Rio de Janeiro (RJ) - Santos Dumont"=>"SDU", "Salvador (BA)"=>"SSA", "Santarém (PA)"=>"STM", "São José do Rio Preto (SP)"=>"SJP", "São Luis (MA)"=>"SLZ", "São Paulo (SP) - Congonhas"=>"CGH", "São Paulo (SP) - Guarulhos"=>"GRU", "Teresina (PI)"=>"THE", "Uberlândia (MG)"=>"UDI", "Vitória (ES)"=>"VIX"}


# define the order our columns are displayed in the datastore
ScraperWiki.save_metadata('data_columns', ['Lote', 'Origem', 'Destino', 'Data de Partida', 'Data de Retorno', 'Assentos', 'Lance minimo', 'Lance atual'])

# scrape_table function: gets passed an individual page to scrape
def scrape(html)
  doc = Nokogiri::HTML(html)
  doc.xpath("//table[@id='Rel']/tr[position() > 2]").each { |row|
    row = row.to_s.chomp
    row =~ /(\d{4}).*IDA: (.*) \/ (.*)<\/b>, (\d+ de \w+ de \d{4}), (\d{2}) assentos.*Saída (\d{2}h\d{2}), Chegada (\d{2}h\d{2}).*(\d+ de \w+ de \d{4}).*Saída (\d{2}h\d{2}), Chegada (\d{2}h\d{2}).*(\d{2},\d{2}).*(\d{3},\d{2})<\/td>/m

    record = Hash.new
    record['Lote'] = $1
    record['Origem'] = CIDADES[$2]
    record['Destino'] = CIDADES[$3]
    record['Data de Partida'] = $4
    record['Assentos'] = $5
    record['Data de Retorno'] = $8
    record['Lance minimo'] = -1
    record['Lance minimo'] = $12.gsub(',', '.').to_f if not $12.nil? 

    row =~ /Valor:.*(\d{3},\d+)/m

    record['Lance atual'] = -1
    record['Lance atual'] = $1.gsub(',', '.').to_f if not $1.nil? 

    ScraperWiki.save(["Lote"], record) if record['Lote']
  }
end

# //table[@id='Rel']/tbody/tr[position() > 2]
# //td[@id='Meio']/div/a/@href
html = ScraperWiki.scrape(BASE_URL + 'Relacao.asp')

# Pega as URLs de todas páginas de leilão
doc = Nokogiri::HTML(html)
pages = doc.xpath("//td[@id='Meio']/div/a/@href").to_a

scrape(html)

pages.each { |page|
  html = ScraperWiki.scrape(BASE_URL + page.to_s)
  scrape(html)
}require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.milanexpress.com.br/GOL/Lotes/'
CIDADES = {"Aracajú (SE)"=>"AJU", "Belo Horizonte (MG) - Confins"=>"CNF", "Belo Horizonte (MG) - Pampulha"=>"PLU", "Belém (PA)"=>"BEL", "Boa Vista (RR)"=>"BVB", "Brasília (DF)"=>"BSB", "Cabo Frio (RJ)"=>"CFB", "Campina Grande (PB)"=>"CPV", "Campinas (SP)"=>"CPQ", "Campo Grande (MS)"=>"CGR", "Caxias do Sul (RS)"=>"CXJ", "Chapecó (SC)"=>"XAP", "Cruzeiro do Sul (AC)"=>"CZS", "Cuiabá (MT)"=>"CGB", "Curitiba (PR)"=>"CWB", "Florianópolis (SC)"=>"FLN", "Fortaleza (CE)"=>"FOR", "Foz do Iguaçu (PR)"=>"IGU", "Goiânia (GO)"=>"GYN", "Ilhéus (BA)"=>"IOS", "Imperatriz (MA)"=>"IMP", "Joinville (SC)"=>"JOI", "João Pessoa (PB)"=>"JPA", "Juazeiro do Norte (CE)"=>"JDO", "Londrina (PR)"=>"LDB", "Macapá (AP)"=>"MCP", "Maceió (AL)"=>"MCZ", "Manaus (AM)"=>"MAO", "Marabá (PA)"=>"MAB", "Maringá (PR)"=>"MGF", "Natal (RN)"=>"NAT", "Navegantes (SC)"=>"NVT", "Palmas (TO)"=>"PMW", "Petrolina (PE)"=>"PNZ", "Porto Alegre (RS)"=>"POA", "Porto Seguro (BA)"=>"BPS", "Porto Velho (RO)"=>"PVH", "Presidente Prudente (SP)"=>"PPB", "Recife (PE)"=>"REC", "Ribeirão Preto (SP)"=>"RAO", "Rio Branco (AC)"=>"RBR", "Rio de Janeiro (RJ) - Galeão"=>"GIG", "Rio de Janeiro (RJ) - Santos Dumont"=>"SDU", "Salvador (BA)"=>"SSA", "Santarém (PA)"=>"STM", "São José do Rio Preto (SP)"=>"SJP", "São Luis (MA)"=>"SLZ", "São Paulo (SP) - Congonhas"=>"CGH", "São Paulo (SP) - Guarulhos"=>"GRU", "Teresina (PI)"=>"THE", "Uberlândia (MG)"=>"UDI", "Vitória (ES)"=>"VIX"}


# define the order our columns are displayed in the datastore
ScraperWiki.save_metadata('data_columns', ['Lote', 'Origem', 'Destino', 'Data de Partida', 'Data de Retorno', 'Assentos', 'Lance minimo', 'Lance atual'])

# scrape_table function: gets passed an individual page to scrape
def scrape(html)
  doc = Nokogiri::HTML(html)
  doc.xpath("//table[@id='Rel']/tr[position() > 2]").each { |row|
    row = row.to_s.chomp
    row =~ /(\d{4}).*IDA: (.*) \/ (.*)<\/b>, (\d+ de \w+ de \d{4}), (\d{2}) assentos.*Saída (\d{2}h\d{2}), Chegada (\d{2}h\d{2}).*(\d+ de \w+ de \d{4}).*Saída (\d{2}h\d{2}), Chegada (\d{2}h\d{2}).*(\d{2},\d{2}).*(\d{3},\d{2})<\/td>/m

    record = Hash.new
    record['Lote'] = $1
    record['Origem'] = CIDADES[$2]
    record['Destino'] = CIDADES[$3]
    record['Data de Partida'] = $4
    record['Assentos'] = $5
    record['Data de Retorno'] = $8
    record['Lance minimo'] = -1
    record['Lance minimo'] = $12.gsub(',', '.').to_f if not $12.nil? 

    row =~ /Valor:.*(\d{3},\d+)/m

    record['Lance atual'] = -1
    record['Lance atual'] = $1.gsub(',', '.').to_f if not $1.nil? 

    ScraperWiki.save(["Lote"], record) if record['Lote']
  }
end

# //table[@id='Rel']/tbody/tr[position() > 2]
# //td[@id='Meio']/div/a/@href
html = ScraperWiki.scrape(BASE_URL + 'Relacao.asp')

# Pega as URLs de todas páginas de leilão
doc = Nokogiri::HTML(html)
pages = doc.xpath("//td[@id='Meio']/div/a/@href").to_a

scrape(html)

pages.each { |page|
  html = ScraperWiki.scrape(BASE_URL + page.to_s)
  scrape(html)
}