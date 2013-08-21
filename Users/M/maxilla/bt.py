import scraperwiki
import lxml.html

# Initialise


html = scraperwiki.scrape("http://www.bt.com.bn/news/national")
root = lxml.html.fromstring(html)

# Variables

date = ""



for el in root.cssselect("div.view-content a"):
    #print el
    #print lxml.html.tostring(el)
    #print el.attrib['href']
    print el.text