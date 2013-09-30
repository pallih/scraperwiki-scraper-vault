import scraperwiki

# Blank Python

print "Hello, coding in the cloud!"
import scraperwiki
html = scraperwiki.scrape("http://liveweb.archive.org/http://www.paginegialle.it/cinema-programmazione/Roma%20(RM)")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'titolo' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }                 
print data
import scraperwiki

# Blank Python

print "Hello, coding in the cloud!"
import scraperwiki
html = scraperwiki.scrape("http://liveweb.archive.org/http://www.paginegialle.it/cinema-programmazione/Roma%20(RM)")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'titolo' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }                 
print data
