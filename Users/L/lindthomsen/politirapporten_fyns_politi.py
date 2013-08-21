import scraperwiki
import lxml.html 

baseUrl="https://www.politi.dk/Fyn/da/lokalnyt/Doegnrapporter/"
date="11042013"
html = scraperwiki.scrape("https://www.politi.dk/Fyn/da/lokalnyt/Doegnrapporter/doegnrapport-11042013.htm")
print(html))
root = lxml.html.fromstring(html)
print(root))
#rapport=root.cssselect("span[id='Articlewithindexpagecontrol_XMLliste1']")

#for p in rapport.cssselect("P"):
#    print(p.text_content())