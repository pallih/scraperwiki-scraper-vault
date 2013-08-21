# grab the webpage
import scraperwiki
html = scraperwiki.scrape("http://dailycrimelog.cupolice.cornell.edu/?RepID=2627")
print html

#download the html
import lxml.html
root = lxml.html.fromstring(html)

p = root.cssselect("div tr")
print lxml.etree.tostring(p)
for tr in root.cssselect("div tr"):
    tds = tr.cssselect("td")
    if len(tds)==4:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        print data
