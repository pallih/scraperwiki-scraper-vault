import scraperwiki
import lxml.html
import string

html = scraperwiki.scrape("http://www.cobone.com/deals/dubai")
print html

root = lxml.html.fromstring(html)
for deals in root.cssselect("div.deal_secondary_fashion"):
    dealinfo = deals.cssselect("div.deal_secondary_fashion_info h1")[0]
    dealprice = deals.cssselect("div.deal_secondary_viewBtn a")[0]
    nosold = deals.cssselect("div.deal_secondary_boughtHangInfo p")[0]
    print string.split(dealprice.attrib["href"],"/")[4],dealinfo.text,dealprice.text,nosold.text
    #print lxml.html.tostring(dealinfo[0])
    #print lxml.html.tostring(price)
    #print price.text 
import scraperwiki
import lxml.html
import string

html = scraperwiki.scrape("http://www.cobone.com/deals/dubai")
print html

root = lxml.html.fromstring(html)
for deals in root.cssselect("div.deal_secondary_fashion"):
    dealinfo = deals.cssselect("div.deal_secondary_fashion_info h1")[0]
    dealprice = deals.cssselect("div.deal_secondary_viewBtn a")[0]
    nosold = deals.cssselect("div.deal_secondary_boughtHangInfo p")[0]
    print string.split(dealprice.attrib["href"],"/")[4],dealinfo.text,dealprice.text,nosold.text
    #print lxml.html.tostring(dealinfo[0])
    #print lxml.html.tostring(price)
    #print price.text 
