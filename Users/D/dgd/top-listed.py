# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.sodis.ru/disp?s=city&id=11839')# this is the target site
soup = BeautifulSoup(html)
scraperwiki.metadata.save('data_columns', ['best'])# look for the div!
data_table = soup.find("left_column", { "class" : "best" })# look above the div to find the class
rows = data_table.findAll("ul")
k = 0
for row in rows:
    print k,row
    if k < 2:
        k = k +1
        continue
    else:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['best'] = table_cells[0].text
            #record['Use social networking sites, Q1 2009, %'] = table_cells[1].text
            #record['Use social networking sites, Q1 2008, %'] = table_cells[2].text
            print record, '------------'
            scraperwiki.datastore.save(["Category"], record)