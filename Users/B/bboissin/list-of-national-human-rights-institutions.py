import scraperwiki
import BeautifulSoup
import re

from scraperwiki import datastore

#scrape page
html = scraperwiki.scrape('http://www.nhri.net/NationaldataListPrint.asp')

s = BeautifulSoup.BeautifulSoup(html, convertEntities=BeautifulSoup.BeautifulStoneSoup.ALL_ENTITIES)


data = {}
maingroup = None
d = {}

table = s.find('table', attrs={'id': 'Table1'})
for row in table.findAll('tr'):
    first = row.find('td')
    if first.get('class') == 'CHMainGroup':
        maingroup = first.find(text=True)
    elif first.get('class') == 'CHSubSubGroup': # end of entry
        datastore.save(unique_keys=['country'], data=d)
    elif first.get('colspan') != '2':
        second = first.findNextSibling('td')
        if first.get('class') == 'CHSubGroup':
            d = {
                    'country': first.find(text=True),
                    'region': maingroup,
                    'name': second.find(text=True),
                }
        else:
            text = [re.sub(u'(?u)\s+', u' ', e.strip()) for e in second.findAll(text=True) if e.strip()]
            d[first.find(text=True).lower()] = '\n'.join(text)
