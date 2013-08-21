import scraperwiki
html = scraperwiki.scrape("http://www.nationmaster.com/graph/imm_us_vis_lot_win-immigration-us-visa-lottery-winners")

import BeautifulSoup
soup = BeautifulSoup.BeautifulSoup(html)

for tr in soup.findAll('tr'):
    print tr.findAll('td')
ssss

for Countries_cell in soup.findAll('td'):
    scraperwiki.datastore.save(unique_keys=['Amount_cell', 'Date'], data={'Countries_cell':td.string}) 

def table_cell():
    record = {}

table= soup.findAll("td")
if table_cell:
            record['Countries'] = Countries_cell[0].text
            record['Amount'] = Amount_cell[1].text
            record['Year'] = Year_cell[2].text
            record['Ranking (m)'] = Gender_cell[4].text
table_cell()
