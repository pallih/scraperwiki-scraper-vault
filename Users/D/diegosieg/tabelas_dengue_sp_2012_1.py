import scraperwiki

from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://www.cve.saude.sp.gov.br/htm/zoo/den12_import_autoc.htm")
soup = BeautifulSoup(html)

tables = soup.find_all("table", {"border" : "0", "cellspacing": "0", "cellpadding": "0"})
print len(tables)

print tables

for table in tables:
    for row in table.find_all('tr'):
        for cell in row.find_all("td"):
            print cell.get_text().strip()

rows = tables[0].find_all('tr')

for row in rows:
    for cell in row.find_all("td"):
        print cell.get_text().strip()
for row in rows:
    cells = row.find_all("td")
    if len(cells) > 24:
        data = {
            'drs' : cells[0].get_text().strip(),
            'drs_nome' : cells[1].get_text().strip(),
            'empty' : cells[2].get_text().strip(),
            'gve' : cells[3].get_text().strip(),
            'municipio' : cells[4].get_text().strip(),
            'jan_auto' : cells[5].get_text().strip(),
            'jan_impo' : cells[6].get_text().strip(),
            'fev_auto' : cells[7].get_text().strip(),
            'fev_impo' : cells[8].get_text().strip(),
            'mar_auto' : cells[9].get_text().strip(),
            'mar_impo' : cells[10].get_text().strip(),
            'abr_auto' : cells[11].get_text().strip(),
            'abr_impo' : cells[12].get_text().strip(),
            'mai_auto' : cells[13].get_text().strip(),
            'mai_impo' : cells[14].get_text().strip(),
            'jun_auto' : cells[15].get_text().strip(),
            'jun_impo' : cells[16].get_text().strip(),
            'jul_auto' : cells[17].get_text().strip(),
            'jul_impo' : cells[18].get_text().strip(),
            'ago_auto' : cells[19].get_text().strip(),
            'ago_impo' : cells[20].get_text().strip(),
            'set_auto' : cells[21].get_text().strip(),
            'set_impo' : cells[22].get_text().strip(),
            #'out_auto' : cells[23].get_text().strip(),
            #'out_impo' : cells[24].get_text().strip(),
            #'nov_auto' : cells[25].get_text().strip(),
            #'nov_impo' : cells[26].get_text().strip(),
            #'dez_auto' : cells[27].get_text().strip(),
            #'dez_impo' : cells[28].get_text().strip(),
            'tot_auto' : cells[23].get_text().strip(),
            'tot_impo' : cells[24].get_text().strip()
        }
        scraperwiki.sqlite.save(unique_keys=['municipio'],data=data)

import scraperwiki

from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://www.cve.saude.sp.gov.br/htm/zoo/den12_import_autoc.htm")
soup = BeautifulSoup(html)

tables = soup.find_all("table", {"border" : "0", "cellspacing": "0", "cellpadding": "0"})
print len(tables)

print tables

for table in tables:
    for row in table.find_all('tr'):
        for cell in row.find_all("td"):
            print cell.get_text().strip()

rows = tables[0].find_all('tr')

for row in rows:
    for cell in row.find_all("td"):
        print cell.get_text().strip()
for row in rows:
    cells = row.find_all("td")
    if len(cells) > 24:
        data = {
            'drs' : cells[0].get_text().strip(),
            'drs_nome' : cells[1].get_text().strip(),
            'empty' : cells[2].get_text().strip(),
            'gve' : cells[3].get_text().strip(),
            'municipio' : cells[4].get_text().strip(),
            'jan_auto' : cells[5].get_text().strip(),
            'jan_impo' : cells[6].get_text().strip(),
            'fev_auto' : cells[7].get_text().strip(),
            'fev_impo' : cells[8].get_text().strip(),
            'mar_auto' : cells[9].get_text().strip(),
            'mar_impo' : cells[10].get_text().strip(),
            'abr_auto' : cells[11].get_text().strip(),
            'abr_impo' : cells[12].get_text().strip(),
            'mai_auto' : cells[13].get_text().strip(),
            'mai_impo' : cells[14].get_text().strip(),
            'jun_auto' : cells[15].get_text().strip(),
            'jun_impo' : cells[16].get_text().strip(),
            'jul_auto' : cells[17].get_text().strip(),
            'jul_impo' : cells[18].get_text().strip(),
            'ago_auto' : cells[19].get_text().strip(),
            'ago_impo' : cells[20].get_text().strip(),
            'set_auto' : cells[21].get_text().strip(),
            'set_impo' : cells[22].get_text().strip(),
            #'out_auto' : cells[23].get_text().strip(),
            #'out_impo' : cells[24].get_text().strip(),
            #'nov_auto' : cells[25].get_text().strip(),
            #'nov_impo' : cells[26].get_text().strip(),
            #'dez_auto' : cells[27].get_text().strip(),
            #'dez_impo' : cells[28].get_text().strip(),
            'tot_auto' : cells[23].get_text().strip(),
            'tot_impo' : cells[24].get_text().strip()
        }
        scraperwiki.sqlite.save(unique_keys=['municipio'],data=data)

