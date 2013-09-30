import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.metroscubicos.com/detalle/distrito-federal/venustiano-carranza/en-renta/calle-juan-guillermo-villasana-colonia-ampliacion-aviacion-civil/2001124545?pos=14&sid=1369407545")
root = lxml.html.fromstring(html)

for el in root.cssselect("p.precio span"):
    print el
    #print el.attrib[]
    #link = el.attrib['href']
    """#if len(link) > 50:
        record = { "Apt" : el.attrib['href'] } # column name and value
        scraperwiki.sqlite.save(["Apt"], record) # save the records one by one"""

import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.metroscubicos.com/detalle/distrito-federal/venustiano-carranza/en-renta/calle-juan-guillermo-villasana-colonia-ampliacion-aviacion-civil/2001124545?pos=14&sid=1369407545")
root = lxml.html.fromstring(html)

for el in root.cssselect("p.precio span"):
    print el
    #print el.attrib[]
    #link = el.attrib['href']
    """#if len(link) > 50:
        record = { "Apt" : el.attrib['href'] } # column name and value
        scraperwiki.sqlite.save(["Apt"], record) # save the records one by one"""

import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.metroscubicos.com/detalle/distrito-federal/venustiano-carranza/en-renta/calle-juan-guillermo-villasana-colonia-ampliacion-aviacion-civil/2001124545?pos=14&sid=1369407545")
root = lxml.html.fromstring(html)

for el in root.cssselect("p.precio span"):
    print el
    #print el.attrib[]
    #link = el.attrib['href']
    """#if len(link) > 50:
        record = { "Apt" : el.attrib['href'] } # column name and value
        scraperwiki.sqlite.save(["Apt"], record) # save the records one by one"""

import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.metroscubicos.com/detalle/distrito-federal/venustiano-carranza/en-renta/calle-juan-guillermo-villasana-colonia-ampliacion-aviacion-civil/2001124545?pos=14&sid=1369407545")
root = lxml.html.fromstring(html)

for el in root.cssselect("p.precio span"):
    print el
    #print el.attrib[]
    #link = el.attrib['href']
    """#if len(link) > 50:
        record = { "Apt" : el.attrib['href'] } # column name and value
        scraperwiki.sqlite.save(["Apt"], record) # save the records one by one"""

