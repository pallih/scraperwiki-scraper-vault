import scraperwiki
from BeautifulSoup  import BeautifulSoup

print "The London Stock Exchange Market"

html = scraperwiki.scrape('http://www.londonstockexchange.com/home/homepage.htm')# this is the  target site
soup = BeautifulSoup(html)
scraperwiki.metadata.save('data_columns', ['Index', 'Value', 'Change'])# look for the  div!
data_table = soup.find("table", { "class" : "full" })# look above the  div to find the class
rows =data_table.findAll("tr")
m = 0
for row in rows:
    print m,row
    if m < 0:
        m = m + 1
        continue
    else:
        record = {}
        table_cells  = row.findAll("td")
        if table_cells:
            record['Index'] = table_cells[0].text
            record['Value'] = table_cells[1].text
            record['Change'] = table_cells[2].text
            print record, '------------'
            scraperwiki.datastore.save(["Index"], record)
