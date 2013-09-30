import scraperwiki
from BeautifulSoup import BeautifulSoup

print "Goverenemt Expenditure"

html = scraperwiki.scrape('http://jobs.guardian.co.uk/')
soup = BeautifulSoup(html)
scraperwiki.metadata.save('data_columns', ['&middot;'])
data_table = soup.find("table", { "class" : "tall" })
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
            record['&middot;'] = table_cells[0].text
            #record['Analysis link'] = table_cells[1].text
            #record['Total spending covered, £'] = table_cells[2].text
            print record, '------------'
            scraperwiki.datastore.save(["Department"], record)



import scraperwiki
from BeautifulSoup import BeautifulSoup

print "Goverenemt Expenditure"

html = scraperwiki.scrape('http://jobs.guardian.co.uk/')
soup = BeautifulSoup(html)
scraperwiki.metadata.save('data_columns', ['&middot;'])
data_table = soup.find("table", { "class" : "tall" })
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
            record['&middot;'] = table_cells[0].text
            #record['Analysis link'] = table_cells[1].text
            #record['Total spending covered, £'] = table_cells[2].text
            print record, '------------'
            scraperwiki.datastore.save(["Department"], record)



