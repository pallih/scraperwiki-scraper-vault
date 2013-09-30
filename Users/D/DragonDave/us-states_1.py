import scraperwiki
import lxml.html
# Blank Python

html=scraperwiki.scrape('http://www.statcan.gc.ca/subjects-sujets/standard-norme/sgc-cgt/us-eu-eng.htm')
root=lxml.html.fromstring(html)
rows=root.xpath('//table//tr')
data=[]
for row in rows:
    cells=[x.text_content() for x in row.cssselect('td')]
    if len(cells)<3: continue
    data.append({'name':cells[0],'abbr':cells[1],'short':cells[2],'number':cells[3]})
scraperwiki.sqlite.save(table_name='states', data=data, unique_keys=['abbr'])
import scraperwiki
import lxml.html
# Blank Python

html=scraperwiki.scrape('http://www.statcan.gc.ca/subjects-sujets/standard-norme/sgc-cgt/us-eu-eng.htm')
root=lxml.html.fromstring(html)
rows=root.xpath('//table//tr')
data=[]
for row in rows:
    cells=[x.text_content() for x in row.cssselect('td')]
    if len(cells)<3: continue
    data.append({'name':cells[0],'abbr':cells[1],'short':cells[2],'number':cells[3]})
scraperwiki.sqlite.save(table_name='states', data=data, unique_keys=['abbr'])
