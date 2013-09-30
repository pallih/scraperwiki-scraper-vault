import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.wam.fi/public/default.aspx?nodeid=13067&culture=fi-FI&contentlan=1")
baseurl = "http://www.wam.fi/public/"
root = lxml.html.fromstring(html)


for el in root.cssselect("div #lists span span ul li a"):
    nimi = el.text.partition(": ")[0]
    teos = el.text.partition(": ")[2]

    html2 = scraperwiki.scrape(baseurl + el.attrib['href'])
    root2 = lxml.html.fromstring(html2)

    otsikot = root2.cssselect("#content span span span h1")

    for otsikko in otsikot:
        print otsikko.text

        record = {}
        record['nimi'] = el.text.partition(": ")[0]
        record['teos'] = el.text.partition(": ")[2]

        scraperwiki.sqlite.save(["teos"], record) # save the records one by one

#for el in root.cssselect("div #lists span span ul li a"):
#    record = { "otsikko" : el.text } # column name and value
#    scraperwiki.sqlite.save(["otsikko"], record) # save the records one by one

#    record = { "nimi" : nimi } # column name and value
#    record2 = { "teos" : teos } # column name and valueimport scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.wam.fi/public/default.aspx?nodeid=13067&culture=fi-FI&contentlan=1")
baseurl = "http://www.wam.fi/public/"
root = lxml.html.fromstring(html)


for el in root.cssselect("div #lists span span ul li a"):
    nimi = el.text.partition(": ")[0]
    teos = el.text.partition(": ")[2]

    html2 = scraperwiki.scrape(baseurl + el.attrib['href'])
    root2 = lxml.html.fromstring(html2)

    otsikot = root2.cssselect("#content span span span h1")

    for otsikko in otsikot:
        print otsikko.text

        record = {}
        record['nimi'] = el.text.partition(": ")[0]
        record['teos'] = el.text.partition(": ")[2]

        scraperwiki.sqlite.save(["teos"], record) # save the records one by one

#for el in root.cssselect("div #lists span span ul li a"):
#    record = { "otsikko" : el.text } # column name and value
#    scraperwiki.sqlite.save(["otsikko"], record) # save the records one by one

#    record = { "nimi" : nimi } # column name and value
#    record2 = { "teos" : teos } # column name and value