import scraperwiki
import lxml.html

scrape_url = "http://unstats.un.org/unsd/demographic/products/socind/education.htm"
html = scraperwiki.scrape(scrape_url) 
root = lxml.html.fromstring(html)

for tr in root.cssselect("table[align='left'] tr.tcont"):
     tds = tr.cssselect("td")
     
     data = {
        "country": tds[0].text_content(),
        "years_in_school": int(tds[4].text_content())
     }
     
     scraperwiki.sqlite.save(unique_keys=["country"], data=data)
import scraperwiki
import lxml.html

scrape_url = "http://unstats.un.org/unsd/demographic/products/socind/education.htm"
html = scraperwiki.scrape(scrape_url) 
root = lxml.html.fromstring(html)

for tr in root.cssselect("table[align='left'] tr.tcont"):
     tds = tr.cssselect("td")
     
     data = {
        "country": tds[0].text_content(),
        "years_in_school": int(tds[4].text_content())
     }
     
     scraperwiki.sqlite.save(unique_keys=["country"], data=data)
