import scraperwiki
import lxml.html

# Blank Python
html = scraperwiki.scrape("http://www.bookdepository.com/Luigi-Ghirri-Its-Beautiful-Here-Isnt-it-Luigi-Ghirri/9781597110587")
root = lxml.html.fromstring(html)

#print lxml.html.tostring(html)

for span in root.cssselect('div[class=\"mainDetails\"] span[class=\"price\"] strong'):
    elem = span.cssselect("strong")
    for x in elem:
        print x.text_content()

#    print lxml.html.tostring(span)

#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        print dataimport scraperwiki
import lxml.html

# Blank Python
html = scraperwiki.scrape("http://www.bookdepository.com/Luigi-Ghirri-Its-Beautiful-Here-Isnt-it-Luigi-Ghirri/9781597110587")
root = lxml.html.fromstring(html)

#print lxml.html.tostring(html)

for span in root.cssselect('div[class=\"mainDetails\"] span[class=\"price\"] strong'):
    elem = span.cssselect("strong")
    for x in elem:
        print x.text_content()

#    print lxml.html.tostring(span)

#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        print data