require 'mechanize'
ua = Mechanize.new

(1..36).each do |i|
  page = ua.get("http://www.portaltransparencia.gov.br/PortalTransparenciaPesquisaFavorecido.asp?hidIdTipoFavorecido=2&hidNumCodigoTipoNaturezaJuridica=3&Exercicio=2012&Pagina=#{i}")

  page.search('//div[@id="listagem"]//table/tr').each do |row|
    puts row.search('td').map {|n| n.text }
  end

end

