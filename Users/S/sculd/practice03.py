import scraperwiki
html = scraperwiki.scrape("http://pdglive.lbl.gov/Rsummary.brl?nodein=S004&inscript=Y&sub=Yr&return=S003,S004,S035")

import lxml.html
root = lxml.html.fromstring(html)


for tr in root.cssselect("table.pdgLive tr"):
    tds = tr.cssselect("td")
    if len(tds) > 0:
        tds[0].text_content()
        '''
        for index, item in tds:
            print(tds[index].text_content())
        '''

for el in root.cssselect("div.tags a"):
    print el
    print lxml.html.tostring(el)
    print el.attrib['href']
import scraperwiki
html = scraperwiki.scrape("http://pdglive.lbl.gov/Rsummary.brl?nodein=S004&inscript=Y&sub=Yr&return=S003,S004,S035")

import lxml.html
root = lxml.html.fromstring(html)


for tr in root.cssselect("table.pdgLive tr"):
    tds = tr.cssselect("td")
    if len(tds) > 0:
        tds[0].text_content()
        '''
        for index, item in tds:
            print(tds[index].text_content())
        '''

for el in root.cssselect("div.tags a"):
    print el
    print lxml.html.tostring(el)
    print el.attrib['href']
