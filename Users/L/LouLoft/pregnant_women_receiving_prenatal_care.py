# Blank Python
# Blank Python
print "Hello, coding in the cloud!"           
import scraperwiki          
html = scraperwiki.scrape("http://data.worldbank.org/indicator/SH.STA.ANVC.ZS")
print html
import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)       
