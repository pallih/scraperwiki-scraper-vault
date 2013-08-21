import scraperwiki

# Blank Python

import scraperwiki           
import lxml.html           

urls = ["http://www.amazon.com/Best-Sellers-Home-Improvement/zgbs/hi/ref=zg_bs_nav_0","http://www.amazon.com/Best-Sellers-Home-Improvement-Appliances/zgbs/hi/13397451/ref=zg_bs_nav_hi_1_hi","http://www.amazon.com/Best-Sellers-Home-Improvement-Lighting-Ceiling-Fans/zgbs/hi/495224/ref=zg_bs_nav_hi_1_hi","http://www.amazon.com/Best-Sellers-Home-Improvement-Power-Tools-Hand/zgbs/hi/328182011/ref=zg_bs_nav_hi_1_hi","http://www.amazon.com/Best-Sellers-Home-Improvement-Safety-Security/zgbs/hi/3180231/ref=zg_bs_nav_hi_1_hi"]

for wurl in urls:
    error = True
    while error:
        try:
            html = scraperwiki.scrape(wurl)
            root = lxml.html.fromstring(html)
            for tr in root.cssselect("div[class='zg_title'] a"):    
                url = tr.get("href")
                html = scraperwiki.scrape(url ).lower()
                if html.find("out of stock") != -1:  
                    data = {
                        'url': url
                    }
                    scraperwiki.sqlite.save(unique_keys=['url'],data=data)
            error = False
        except:
            error = True

