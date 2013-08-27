import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.metroscubicos.com/resultados/distrito-federal/en-renta?propertyType=Departamento&sid=1369407545")
print html


root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.metroscubicos.com/resultados/distrito-federal/en-renta?propertyType=Departamento&sid=1369407545")
print html


root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.metroscubicos.com/resultados/distrito-federal/en-renta?propertyType=Departamento&sid=1369407545")
print html


root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
