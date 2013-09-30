import scraperwiki
html = scraperwiki.scrape("http://www.annauniversitybe.info/TNEA-2011/AutomobileEngineeringCutoff2011.php")
print html



import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
     
print tr.cssselect("td")
  
import scraperwiki
html = scraperwiki.scrape("http://www.annauniversitybe.info/TNEA-2011/AutomobileEngineeringCutoff2011.php")
print html



import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
     
print tr.cssselect("td")
  
