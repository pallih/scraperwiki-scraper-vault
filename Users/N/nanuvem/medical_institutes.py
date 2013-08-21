import scraperwiki
from BeautifulSoup import BeautifulSoup


url_check = BeautifulSoup(scraperwiki.scrape("http://open.dapper.net/RunDapp?dappName=Dataactualizaofarmcias&v=1&applyToUrl=http%3A%2F%2Fwww.infarmed.pt%2Fpt%2Flicenciamento_inspeccao%2Ffarmacias%2Fpesquisa%2Ffarmacias.php&filter=true"))

print url_check

date = url_check.find('act_farm').text

print date

html = scraperwiki.scrape("http://www.infarmed.pt/pt/licenciamento_inspeccao/farmacias/pesquisa/farmacia.php?valor=&var=NOME&submit=Pesquisar")

#print html

soup = BeautifulSoup(html, fromEncoding='utf-8')


#find table class="reports"
data_table = soup.findAll("table")[2] #, { "CELLSPACING" : "1" })
#find each table row <tr>
#rows = data_table.findAll("tr")
#for each row, igonring first line, loop through this
for row in data_table.findAll("tr")[1:]:
#create a record to hold the data
        record = {}
        #find each cell <td>
        table_cells = row.findAll("td")
        #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
        if table_cells:
            record['DT'] = date
            record['NOME'] = table_cells[0].text
            record['MORADA'] = table_cells[1].text
            record['LOCALIDADE'] = table_cells[2].text
            record['FREGUESIA'] = table_cells[3].text
            record['DISTRITO'] = table_cells[4].text
            record['RESPONSAVEL'] = table_cells[5].text
            record['CONCELHO'] = table_cells[6].text
            # Print out the data we've gathered
            # print record, '------------'
            # Save the record to the datastore - 'Name' is our unique key - 
            scraperwiki.sqlite.save(["DT","NOME","MORADA"], record)



#    data = {
#    'NOME': tds[0].text_content(),
#    'MORADA': tds[1].text_content(),
#    'LOCALIDADE': tds[2].text_content(),
#    'FREGUESIA': tds[3].text_content(),
#    'DISTRITO': tds[4].text_content(),
#   'RESPONSAVEL': tds[5].text_content(),
#    'CONCELHO': tds[6].text_content()
#    }

