import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm") 


# Blank Python

print "hello world, this is my first scraper!"
#print html
root = lxml.html.fromstring(html)

for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    #print tds
    #print tds[0].text_content()
    print tds[:].text_content()
    data = {
        'country': tds[0].text_content(),
        'years_in_school' : int(tds[4].text_content())        
    }

    #print data

