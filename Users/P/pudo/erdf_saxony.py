import scraperwiki

# Blank Python

from lxml import html

doc = html.parse("http://www.statistik.sachsen.de/foerderportal/VZB_20100930_20100930_2007DE161PO004.html")
for row in doc.findall('//tr'):
    cells = list(row.findall('td'))
    if not len(cells):
        continue
    name = cells[0].text
    project = cells[1].text
    year = cells[2].text
    commitment = cells[3].text
    spent = cells[4].text
    
    scraperwiki.sqlite.save(unique_keys=["name", "project", "year"], 
        data={"name": name, 
              "project": project,
              "year": year,
              "commitment": commitment,
              "spent": spent})           

    #print name

    
import scraperwiki

# Blank Python

from lxml import html

doc = html.parse("http://www.statistik.sachsen.de/foerderportal/VZB_20100930_20100930_2007DE161PO004.html")
for row in doc.findall('//tr'):
    cells = list(row.findall('td'))
    if not len(cells):
        continue
    name = cells[0].text
    project = cells[1].text
    year = cells[2].text
    commitment = cells[3].text
    spent = cells[4].text
    
    scraperwiki.sqlite.save(unique_keys=["name", "project", "year"], 
        data={"name": name, 
              "project": project,
              "year": year,
              "commitment": commitment,
              "spent": spent})           

    #print name

    
