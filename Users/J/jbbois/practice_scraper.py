import scraperwiki

# Blank Python
#download website
from lxml import html

#turn into boxes
boxes = html.parse('http://www.statistik.sachsen.de/foerderportal/VZB_20100930_20100930_2007DE161PO004.html')
    

#select each row
for row in boxes.findall('//tr'):

#select all cells of a row
    cell = list(row.findall('td'))
    print cell    
#assign names of cells
    if len(cell)==0:
        continue
    data = {
        'name' : cell[0].text_content(),
        'org' : cell[1].text_content(),
        'year' : int(cell[2].text_content()),
        'granted' : cell[3].text_content(),
        'paid' : cell[4].text_content(),
    }

#save database
    scraperwiki.sqlite.save(unique_keys=["name","year","org",], data=data)
    print data