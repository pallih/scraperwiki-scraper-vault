import scraperwiki
from geopy import geocoders  


print "Hello, coding in the cloud!"

g = geocoders.Google(domain='maps.google.ru')  
place, (lat, lng) = g.geocode("119415 Москва, Ленинский проспект 110к1")  
print "%s: %.5f, %.5f" % (place, lat, lng)

#import scraperwiki
#html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
#print html

#import lxml.html
#root = lxml.html.fromstring(html)
#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        scraperwiki.sqlite.save(unique_keys=['country'], data=data)



