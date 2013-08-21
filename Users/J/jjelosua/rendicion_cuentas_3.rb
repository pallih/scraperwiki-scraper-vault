# encoding: utf-8
require 'mechanize'

COOKIE_URL = 'http://www.rendiciondecuentas.es/es/consultadeentidadesycuentas/buscarCuentas/consultarCuenta.html?'\
             'dd=true&idEntidadPpal=276&idEntidad=276&idTipoEntidad=A&idModelo=3&ejercicio=2009&nifEntidad=P0400100D&option=vc'

#We will extract Resultado since it contains the personal expense for the local entity
accType = 'Resultado'

#method used to extract the personnel expenses from the page
def extractPersonnelExpense(doc)
  tables = doc.css('table.tablesorter')
  tables.each do |table|
    rows = table.css('tbody tr')
    for i in 0..rows.length-1 do
      expenseName = rows[i].css('td')[0].text
      if (expenseName =~ /Gastos de personal\s*$/)
        expenseAmount = rows[i].css('td')[1].text 
        amount = expenseAmount.gsub(".","").gsub(",",".").to_f
        return amount
      end
    end     
  end
  return nil
end

#Create the mechanize agent
agent = Mechanize.new 

#First we obtain the session cookie needed for the following scraping process
agent.get(COOKIE_URL)

count_ent = 1
ScraperWiki::attach("rendicion_cuentas_2")
entities = ScraperWiki::select("* from rendicion_cuentas_2.swdata")
entities.each do |entity|
  puts "parsed #{count_ent} entities" if (count_ent % 10 == 0)
  treePage = agent.get(entity['url'])
  link = treePage.link_with(:href => /id_form=#{accType}/)
  if link
    resPage = link.click
    nokogiriDoc= resPage.parser
    amount = extractPersonnelExpense(nokogiriDoc)
    if amount
      data = {
        idRegion: entity['idRegion'],
        idProv: entity['idProv'],
        idEntity: entity['idEntity'],
        name: entity['name'],
        year: entity['year'],
        persExpense: amount
      }
      ScraperWiki::save_sqlite(['idRegion','idProv','idEntity','year'], data)
    else
      puts "No personnel expense found for entity: #{entity['name']} and year: #{entity['year']}"
    end
    sleep(1)
  else
    #No accountType found for this entity and year
    puts("#{entity['url']}: No #{accType} found for this entity and year")
  end
  #Update counter
  count_ent += 1
end

