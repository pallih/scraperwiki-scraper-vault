import scraperwiki

# Blank Python

import scraperwiki           
import lxml.html           

urls = ["http://www.ebay.com/sch/i.html?_sacat=0&_mPrRngCbx=1&_nkw=sunglasses&rt=nc&LH_TopRatedSellers=1"]

max_pages = 10

for wurl in urls:
    curr_url = wurl 
    page_idx = 1
    
    while page_idx <= max_pages :
        error = True
        while error:
            try:    
                html = scraperwiki.scrape(curr_url)
                root = lxml.html.fromstring(html)
                
                for tr in root.cssselect("div[class='ittl'] a"):    
                    url = tr.get("href")
                    html = scraperwiki.scrape(url)                
                    if html.find("channeladvisor_poweredby-en.gif") != -1 :
                        root2 = lxml.html.fromstring(html)
                        for mname in root2.cssselect("span[class='mbg-nw']"):
                            data = {
                                'url': url,
                                'merchant_name': mname.text
                            }
                            scraperwiki.sqlite.save(unique_keys=['url'],data=data)
    
                for next_page in root.cssselect("td[class='botpg-next'] a"):
                    print curr_url 
                    curr_url = next_page.get("href")
                    page_idx = page_idx +1             

                error = False
            except:
                print 'error'
                error = True
