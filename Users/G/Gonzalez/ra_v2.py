import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.metroscubicos.com/resultados/distrito-federal/en-renta?propertyType=Departamento&sid=1369407545")
root = lxml.html.fromstring(html)

for el in root.cssselect("div.resultado a"):
    #print el
    print el.attrib['href']
    link = el.attrib['href']
    if len(link) > 50:
        path = str("www.metroscubicos.com") +  str(el.attrib['href'])
        record = { "Apt" : path }
        #record = { "Apt" : el.attrib['href'] } # column name and value
        scraperwiki.sqlite.save(["Apt"], record) # save the records one by one

import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.metroscubicos.com/resultados/distrito-federal/en-renta?propertyType=Departamento&sid=1369407545")
root = lxml.html.fromstring(html)

for el in root.cssselect("div.resultado a"):
    #print el
    print el.attrib['href']
    link = el.attrib['href']
    if len(link) > 50:
        path = str("www.metroscubicos.com") +  str(el.attrib['href'])
        record = { "Apt" : path }
        #record = { "Apt" : el.attrib['href'] } # column name and value
        scraperwiki.sqlite.save(["Apt"], record) # save the records one by one

import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.metroscubicos.com/resultados/distrito-federal/en-renta?propertyType=Departamento&sid=1369407545")
root = lxml.html.fromstring(html)

for el in root.cssselect("div.resultado a"):
    #print el
    print el.attrib['href']
    link = el.attrib['href']
    if len(link) > 50:
        path = str("www.metroscubicos.com") +  str(el.attrib['href'])
        record = { "Apt" : path }
        #record = { "Apt" : el.attrib['href'] } # column name and value
        scraperwiki.sqlite.save(["Apt"], record) # save the records one by one

import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.metroscubicos.com/resultados/distrito-federal/en-renta?propertyType=Departamento&sid=1369407545")
root = lxml.html.fromstring(html)

for el in root.cssselect("div.resultado a"):
    #print el
    print el.attrib['href']
    link = el.attrib['href']
    if len(link) > 50:
        path = str("www.metroscubicos.com") +  str(el.attrib['href'])
        record = { "Apt" : path }
        #record = { "Apt" : el.attrib['href'] } # column name and value
        scraperwiki.sqlite.save(["Apt"], record) # save the records one by one

