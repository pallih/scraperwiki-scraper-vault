import scraperwiki
import lxml.html 

url = 'http://www.omgdiscount.com/'
           
html = scraperwiki.scrape(url)
          
root = lxml.html.fromstring(html)
for node in root.cssselect("div[class='date-outer']"):
    title = node.cssselect("h3[class='post-title entry-title'] > a")[0].text_content()
    code = node.cssselect("div[class='coupon']")[0].text_content()
    desc = node.cssselect("div[class='coupon_description']")[0].text_content()
    
    data = {
        'title' : title,
        'code' : code,
        'desc' : desc
    }
    #print data
    scraperwiki.sqlite.save(unique_keys=['title'], data=data)