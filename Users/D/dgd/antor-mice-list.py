# Blank Python
# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.antormice.com/en/index.php?b=3')# this is the target site simple table scrape
soup = BeautifulSoup(html)
scraperwiki.metadata.save('data_columns', ['best'])# look for the div!

    # get second table that is marked with id=pm
data_table = soup.findAll("table", {"id":"pm"})[1] 
rows = data_table.findAll("tr") 

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
            record['company'] = table_cells[0].text
            record['country'] = table_cells[1].text
            print record, '------------'
            scraperwiki.datastore.save(["company", "country"], record)