import scraperwiki

# Blank Python
import scraperwiki

html = scraperwiki.scrape("http://chathamsheriff.org/Corrections/Bookings24hrs.aspx")
print html
import lxml.html           
root = lxml.html.fromstring(html)

print unicode(unicode(u"Name:ÂADAME, TIMOTHYÂ FREDRICO").replace(unicode('Â'), ''))

for table in root.cssselect("div[id='gallery'] table"):
    tds = table.cssselect("td")
    
    data = {
      'picture' : tds[0].cssselect("img")[0].get("src"),
      'name' : tds[1].text_content().encode('utf8').replace(' ', '')
    }

    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

#.encode('Windows-1252')

