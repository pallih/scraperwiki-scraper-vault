import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://oulu.ouka.fi/taidemuseo/veistos/veistoshaku/teoshaku/teokset.html")
baseurl = "http://www.wam.fi/public/"
root = lxml.html.fromstring(html)


for el in root.cssselect("p font"):
    print el.text
#    print lxml.html.tostring(el)
#    if el.cssselect("a")[0]:
#        fff = el.cssselect("a")[0]
#        print fff.attrib['href']
#    nimi = el.text.partition(": ")[0]
#    teos = el.text.partition(": ")[2]

#    html2 = scraperwiki.scrape(el.attrib['href'])
#    root2 = lxml.html.fromstring(html2)

#    otsikot = root2.cssselect("#content span span span h1")
