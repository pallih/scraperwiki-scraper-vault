import scraperwiki

# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://vote.duma.gov.ru/vote/79438")

import lxml.html
root = lxml.html.fromstring(html)
P = root.cssselect('table tr')

print(P[1].text_content())

tRow = root.cssselect('div.table-page-fraction tr')
 
print(len(tRow))

for tr in P:
    tds = tr.cssselect("td")
    if len(tds)==3:
        data = {
            'Name' : tds[0].text_content(),
            'Fraction' : tds[0].text_content(),
            'VoteSt' : tds[0].text_content(),
        }
        print data

        scraperwiki.sqlite.save(unique_keys=['Name'], data=data)


