import scraperwiki

# Blank Python

import scraperwiki           
import lxml.html           

urls = ["http://www.ebay.com/sch/Jewelry-Watches-/281/i.html?_sadis=200&LH_SALE_CURRENCY=0&_samihi&tokenstring=dHX8QQcAAAA%3D&_fpos&_oexkw&_sop=12&_nkw&_okw&_fsct&_ipg=50&LH_BIN=1&_samilow&_sofindtype=5&_udhi&_ftrt=901&_sabdhi&_ftrv=1&_udlo=1000&_sabdlo&_adv=1&_dmd=1&_mPrRngCbx=1&LH_LocatedIn=1&rt=nc&_pppn=r1&_fss=1&LH_TopRatedSellers=1"]

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
import scraperwiki

# Blank Python

import scraperwiki           
import lxml.html           

urls = ["http://www.ebay.com/sch/Jewelry-Watches-/281/i.html?_sadis=200&LH_SALE_CURRENCY=0&_samihi&tokenstring=dHX8QQcAAAA%3D&_fpos&_oexkw&_sop=12&_nkw&_okw&_fsct&_ipg=50&LH_BIN=1&_samilow&_sofindtype=5&_udhi&_ftrt=901&_sabdhi&_ftrv=1&_udlo=1000&_sabdlo&_adv=1&_dmd=1&_mPrRngCbx=1&LH_LocatedIn=1&rt=nc&_pppn=r1&_fss=1&LH_TopRatedSellers=1"]

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
