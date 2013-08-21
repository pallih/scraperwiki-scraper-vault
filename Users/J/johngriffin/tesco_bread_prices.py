import scraperwiki
import lxml.html      
import datetime
     
# html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
html = scraperwiki.scrape("http://www.tesco.com/groceries/product/browse/default.aspx?N=4294793220&Ne=4294793660&lvl=3&action=toggleProdListView_3&viewMode=list")

print html

root = lxml.html.fromstring(html)
for li in root.cssselect("div[class='productLists'] li"):
    print lxml.html.tostring(li)
    item = li.cssselect("h3[class='inBasketInfoContainer'] a")
    price = li.cssselect("span[class='linePrice']")
    data = {
        'item' : item[0].text_content(),
        'price' : float(price[0].text_content()[1:]),
        'date' : datetime.datetime.now()
    }
    scraperwiki.sqlite.save(unique_keys=['item', 'date'], data=data)
