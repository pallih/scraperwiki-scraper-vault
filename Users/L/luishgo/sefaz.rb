require 'nokogiri'

hdnProx = nil
hdnMaiores = nil
txtMaiores = 999
cboLinha = 30
hdnContador = 0

i = 2
while i > 0
  params = {'hdnProx' => hdnProx, 'hdnMaiores' => hdnMaiores, 'txtMaiores' => txtMaiores, 'cboLinha' => cboLinha, 'hdnContador' => hdnContador}
  html = ScraperWiki.scrape("https://www.sefaz.rs.gov.br/ASP/AAE_root/DAT/SAT-WEB-DEV-JUR-CON_6.asp", params)
  doc = Nokogiri::HTML(html)
  
  doc.css('table.tabelainterna').each do |table|
    table.css('tr').each do |linha|
      colunas = linha.css('td')
      begin
        data = {
          'id' => colunas[0].text(),
          'Nome' => colunas[1].text(),
          'CNPJ' => colunas[2].text(),
          'FaseAdministrativa' => colunas[3].text(),
          'FaseJudicial' => colunas[4].text(),
          'EmDiscussaoJudicial' => colunas[5].text(),
          'Total' => colunas[6].text()
        }
      rescue
        puts 'Erro'
      end
      ScraperWiki.save_sqlite(unique_keys=["id"], data=data)
    end
  end
  
  hdnProx = doc.css('input[@name="hdnProx"]').attr('value')
  hdnContador += 30
  i = i - 1
end