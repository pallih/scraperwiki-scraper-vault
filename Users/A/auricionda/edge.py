import scraperwiki
import lxml.html
a=['http://www.edge.org/memberbio/barry_c_smith',
'http://www.edge.org/memberbio/alan_alda',
'http://www.edge.org/memberbio/gaetano_prisciantelli',
'http://www.edge.org/memberbio/joan_chiao',
'http://www.edge.org/memberbio/brewster_kahle',
'http://www.edge.org/memberbio/michael_goldberg',
'http://www.edge.org/memberbio/stewart_brand',
'http://www.edge.org/memberbio/larry_sanger',
'http://www.edge.org/memberbio/andrei_linde',
'http://www.edge.org/memberbio/iain_couzin'
]
b=0
while b !=7: 
    html = scraperwiki.scrape(str(a[b]))
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div[class=member-name]"):
        nombre=el.text
    scraperwiki.sqlite.save(unique_keys=['orden'],data={'orden':b,'nombre':nombre,'id':str(a[b])})
    b=b+1

import scraperwiki
import lxml.html
a=['http://www.edge.org/memberbio/barry_c_smith',
'http://www.edge.org/memberbio/alan_alda',
'http://www.edge.org/memberbio/gaetano_prisciantelli',
'http://www.edge.org/memberbio/joan_chiao',
'http://www.edge.org/memberbio/brewster_kahle',
'http://www.edge.org/memberbio/michael_goldberg',
'http://www.edge.org/memberbio/stewart_brand',
'http://www.edge.org/memberbio/larry_sanger',
'http://www.edge.org/memberbio/andrei_linde',
'http://www.edge.org/memberbio/iain_couzin'
]
b=0
while b !=7: 
    html = scraperwiki.scrape(str(a[b]))
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div[class=member-name]"):
        nombre=el.text
    scraperwiki.sqlite.save(unique_keys=['orden'],data={'orden':b,'nombre':nombre,'id':str(a[b])})
    b=b+1

