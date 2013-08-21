import scraperwiki

# Blank Python

import scraperwiki           
import lxml.html           

urls = ["http://www.amazon.com/Best-Sellers-Watches-Collectible/zgbs/watches/378522011/ref=zg_bs_nav_watch_1_watch"]

for wurl in urls:
    error = True
    while error:
        try:
            html = scraperwiki.scrape(wurl)
            root = lxml.html.fromstring(html)
            for tr in root.cssselect("div[class='zg_title'] a"):    
                url = tr.get("href")
                html = scraperwiki.scrape(url ).lower()
                if html.find("left in stock") != -1 or html.find("out of stock") != -1:  
                    data = {
                        'url': url
                    }
                    scraperwiki.sqlite.save(unique_keys=['url'],data=data)
            error = False
        except:
            error = True
