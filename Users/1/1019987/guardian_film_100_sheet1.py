##################
#Note from creator (-Anuj Kumar) I have been tried to 
#Reference - Scraperwiki Tutorial 3
##################
import scraperwiki
from BeautifulSoup import BeautifulSoup

print "Guardian film 100 : Sheet1 Tables"

html = scraperwiki.scrape('http://www.guardian.co.uk/news/datablog/2010/sep/24/guardian-film-100-full-list-spreadsheet')
soup = BeautifulSoup(html)
scraperwiki.sqlite.get_var('data_columns', ['Position', 'Name', 'Company, if appropriate' , 'Role 1(director, actor'])
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
            record['Position'] = table_cells[0].text
            record['Name'] = table_cells[1].text
            record['Company, if appropriate'] = table_cells[2].text
            record['Role 1(director, actor'] = table_cells[3].text
            print record, '------------'
            scraperwiki.datastore.save(["Position"], record)
