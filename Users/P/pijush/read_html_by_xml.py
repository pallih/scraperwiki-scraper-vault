import scraperwiki

# Blank Python


html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
#print html
import lxml.html
root = lxml.html.fromstring(html)
print root
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'Year' : tds[1].text_content(),
             'Yearc' : tds[3].text_content(),
            'Totel' :int( tds[4].text_content()),
             'TotalC' : tds[6].text_content(),
            'Men' : int(tds[7].text_content()),
             'MenC' : tds[9].text_content(),
            'Women' : int(tds[10].text_content())
        }
       # print data
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
#select * from swdata order by Totel desc limit 10
