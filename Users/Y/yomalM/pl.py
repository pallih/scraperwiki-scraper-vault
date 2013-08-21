import scraperwiki
from BeautifulSoup import BeautifulSoup

print "Premier League Football 2011/2011 Points Tables"

html = scraperwiki.scrape('http://www.guardian.co.uk/football/premierleague')
soup = BeautifulSoup(html)
scraperwiki.metadata.save('data_columns', ['Team', 'Pld', 'GD' , 'Pts'])
data_table = soup.find("table", { "class" : "full" })
rows = data_table.findAll("tr")
m = 0
for row in rows:
    print m,row
    if m < 0:
        m = m + 1
        continue
    else:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['a'] = table_cells[0].text
            record['b'] = table_cells[1].text
            record['c'] = table_cells[2].text
            record['d'] = table_cells[3].text
            print record, '------------'
            scraperwiki.datastore.save(["a"], record)


