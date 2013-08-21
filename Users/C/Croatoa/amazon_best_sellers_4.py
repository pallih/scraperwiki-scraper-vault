import scraperwiki

# Blank Python

import scraperwiki           
import lxml.html           

urls = ["http://www.amazon.com/Best-Sellers-Watches/zgbs/watches/ref=zg_bs_unv_watch_1_378522011_1","http://www.amazon.com/Best-Sellers-Watches-Collectible/zgbs/watches/378522011/ref=zg_bs_nav_watch_1_watch","http://www.amazon.com/Best-Sellers-Watches-Fashion/zgbs/watches/378524011/ref=zg_bs_nav_watch_2_378522011","http://www.amazon.com/Best-Sellers-Watches-Pocket/zgbs/watches/378525011/ref=zg_bs_nav_watch_2_378524011","http://www.amazon.com/Best-Sellers-Watches-Sport/zgbs/watches/378526011/ref=zg_bs_nav_watch_2_378525011"]

for wurl in urls:
    error = True
    while error:
        try:
            html = scraperwiki.scrape(wurl)
            root = lxml.html.fromstring(html)
            for tr in root.cssselect("div[class='zg_title'] a"):    
                url = tr.get("href")
                html = scraperwiki.scrape(url ).lower()
                if html.find("left in stock") != -1 :
                    data = {
                        'url': url
                    }
                    scraperwiki.sqlite.save(unique_keys=['url'],data=data)
            error = False
        except:
            error = True
