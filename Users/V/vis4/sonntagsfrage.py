import scraperwiki
from lxml.html import fromstring

url = "http://www.wahlrecht.de/umfragen/index.htm"

html = scraperwiki.scrape(url)
root = fromstring(html)

head = []
for th in root.cssselect("table.wilko thead tr th")[2:8]:
    head.append(th.text_content())

last_date = []
for td in root.cssselect("table.wilko #datum td")[1:7]:
    d = '-'.join(reversed(td.text_content().split('.')))
    last_date.append(d)

parties = ['cdu','spd','gru','fdp','lin','pir','son']
party_results = dict()
for party in parties:
    party_results[party] = row = []
    for td in root.cssselect("table.wilko #%s td" % party)[1:7]:
        try:
            row.append(float(td.text_content()[:-2].replace(',','.')))
        except:
            row.append(None)

for i in range(len(head)):
    data = { 'inst': head[i], 'date': last_date[i] }
    for party in parties:
        data[party] = party_results[party][i]
    scraperwiki.sqlite.save(unique_keys=['inst', 'date'], data=data)    
    import scraperwiki
from lxml.html import fromstring

url = "http://www.wahlrecht.de/umfragen/index.htm"

html = scraperwiki.scrape(url)
root = fromstring(html)

head = []
for th in root.cssselect("table.wilko thead tr th")[2:8]:
    head.append(th.text_content())

last_date = []
for td in root.cssselect("table.wilko #datum td")[1:7]:
    d = '-'.join(reversed(td.text_content().split('.')))
    last_date.append(d)

parties = ['cdu','spd','gru','fdp','lin','pir','afd','son']
party_results = dict()
for party in parties:
    party_results[party] = row = []
    for td in root.cssselect("table.wilko #%s td" % party)[1:7]:
        try:
            row.append(float(td.text_content()[:-2].replace(',','.')))
        except:
            row.append(None)

for i in range(len(head)):
    data = { 'inst': head[i], 'date': last_date[i] }
    for party in parties:
        data[party] = party_results[party][i]
    scraperwiki.sqlite.save(unique_keys=['inst', 'date'], data=data)    
    