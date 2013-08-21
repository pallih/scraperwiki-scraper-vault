import scraperwiki
from BeautifulSoup import BeautifulSoup


start_dist = 1
end_dist = 19


html = scraperwiki.scrape("http://www.infarmed.pt/pt/licenciamento_inspeccao/registo_entidades/lista_locais_continente.php")

# print html

soup = BeautifulSoup(html, fromEncoding='utf-8')


for dist in range (start_dist ,end_dist):
    #find table class="reports"
    data_table = soup.findAll("table")[dist]
    #find each table row <tr>
    rows = data_table.findAll("tr")
    #for each row, loop through this
    for row in rows[1:]:
    #create a record to hold the data
        record = {}
        #find each cell <td>
        table_cells = row.findAll("td")
        #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
        if table_cells: 
            record['ENTIDADE'] = table_cells[0].text
            record['NOME'] = table_cells[1].text
            record['MORADA'] = table_cells[2].text
            record['LOCALIDADE'] = table_cells[3].text
            record['EMAIL'] = table_cells[4].text
            record['TELEFONE'] = table_cells[5].text
            record['RESPONSAVEL'] = table_cells[6].text
            record['N_REG'] = table_cells[7].text
            record['DISTRITO']= soup.findAll("b")[dist-1].text
            # Print out the data we've gathered
            # print record, '------------'
            # Save the record to the datastore - 'Name' is our unique key - 
        scraperwiki.sqlite.save(["N_REG"], record)

