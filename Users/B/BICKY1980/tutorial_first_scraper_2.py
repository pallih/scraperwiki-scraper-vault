import scraperwiki

# Blank Python
print "Hello, coding in the cloud!"
import scraperwiki
html = scraperwiki.scrape("http://www.saa.gov.uk/search.php?SEARCHED=1&SEARCH_TERM=ab10+1xy&DISPLAY_COUNT=100#results")
print html
print "test1"
import lxml.html
root = lxml.html.fromstring(html)
for td in root.cssselect("div * p"):
    print "1"
    print td
for el in root.cssselect("div.results *"): 
    print "2"
    print el
    print lxml.html.tostring(el)
    print el.attrib['href']
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'ref no.' : tds[0].text_content(),
            'Property Address' : tds[0].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['ref no.'], data=data)


