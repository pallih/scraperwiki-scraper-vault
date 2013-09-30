import scraperwiki

# Blank Python

print "Hello, coding in the cloud!"

import scraperwiki
html = scraperwiki.scrape("http://www.cochilco.cl/productos/boletin.asp?anio=2013&mes=03&tabla=tabla22")
print html





import lxml.html
root = lxml.html.fromstring(html)

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")

    if len(tds)==23:
        tiempo = tds[0].text_content().split('\r\n')
        chuqui = tds[1].text_content().split('\r\n')

        print tiempo
        print chuqui

        scraperwiki.sqlite.save(unique_keys=['country'], data=data)import scraperwiki

# Blank Python

print "Hello, coding in the cloud!"

import scraperwiki
html = scraperwiki.scrape("http://www.cochilco.cl/productos/boletin.asp?anio=2013&mes=03&tabla=tabla22")
print html





import lxml.html
root = lxml.html.fromstring(html)

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")

    if len(tds)==23:
        tiempo = tds[0].text_content().split('\r\n')
        chuqui = tds[1].text_content().split('\r\n')

        print tiempo
        print chuqui

        scraperwiki.sqlite.save(unique_keys=['country'], data=data)