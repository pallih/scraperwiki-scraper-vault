##################
#Note from creator(Yomal Mudalige)- I have been tried to create the link for excel sheets ('Analysis Link' field), however still it is not  functioning.Thanks 
#Reference for scraper - scraperwiki Tutorial 3
##################

import scraperwiki
from BeautifulSoup import BeautifulSoup

print "Government Expenditure - Over £ 25,000 Departments"

html = scraperwiki.scrape('http://www.guardian.co.uk/news/datablog/2010/nov/19/government-spending-data')
soup = BeautifulSoup(html)
scraperwiki.metadata.save('data_columns', ['Department', 'Analysis link', 'Total spending covered, £'])
data_table = soup.find("table", { "class" : "in-article sortable" })
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
            record['Department'] = table_cells[0].text
            record['Analysis link'] = table_cells[1].text
            record['Total spending covered, £'] = table_cells[2].text
            print record, '------------'
            scraperwiki.datastore.save(["Department"], record)


