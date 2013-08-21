# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['id','url','r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13'])

url = 'http://www.portaltransparencia.gob.mx/pot/contrataciones/exportToExcel.do?method=exporta&catalogoAExportar=contrato&_idDependencia=00625'
id = 625
html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

# extracts

subtree1 = soup.table.table
subtree1.extract()
subtree2 = soup.tr
subtree2.extract()
subtree3 = soup.tr
subtree3.extract()
subtree4 = soup.tr
subtree4.extract()
subtree5 = soup.tr
subtree5.extract()
subtree6 = soup.tr
subtree6.extract()


datatable = soup.table
rows = datatable.findAll('tr')

# scrape_table function: gets passed an individual page to scrape


for row in rows:
     # Set up our data record - we'll need it later
     record = {}
     table_cells = row.findAll('td')
     if table_cells:
         record['id'] = id 
         record['url'] = url
         record['r0'] = table_cells[0].text
         record['r1'] = table_cells[1].text
         record['r2'] = table_cells[2].text
         record['r3'] = table_cells[3].text
         record['r4'] = table_cells[4].text
         record['r5'] = table_cells[5].text
         record['r6'] = table_cells[6].text
         record['r7'] = table_cells[7].text
         record['r8'] = table_cells[8].text
         record['r9'] = table_cells[9].text
         record['r10'] = table_cells[10].text
         record['r11'] = table_cells[11].text
         record['r12'] = table_cells[12].text
         record['r13'] = table_cells[13].text
         scraperwiki.datastore.save(["r0"], record)
