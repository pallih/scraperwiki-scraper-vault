import scraperwiki
import lxml.html 

# Blank Python



html = scraperwiki.scrape("http://www.norskeutslipp.no/Templates/NorskeUtslipp/Pages/listPage.aspx?id=50&epslanguage=no")
#print html

          
root = lxml.html.fromstring(html)
for tr in root.cssselect("tr[class='GridViewRowStyle']"):
    print tr
    tds = tr.cssselect("td[class='GridViewListItemStyle']")
    data = {
      'navn' : tds[0].text_content(),
    }
    print data