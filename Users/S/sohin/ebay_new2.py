import scraperwiki

# Blank Python

import scraperwiki           
import lxml.html           

urls = ["http://www.ebay.com/sch/i.html?_trksid=p5197.m570.l1313&_nkw=korean+war&_sacat=0"]

max_pages = 20

for wurl in urls:
    curr_url = wurl 
    page_idx = 1
    
    while page_idx <= max_pages :
        error = True
        while error:
            try:    
                html = scraperwiki.scrape(curr_url)
                root = lxml.html.fromstring(html)
                
                for tr in root.cssselect("div[class='ititle'] a"):    
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

urls = ["http://www.ebay.com/sch/i.html?_trksid=p5197.m570.l1313&_nkw=korean+war&_sacat=0"]

max_pages = 20

for wurl in urls:
    curr_url = wurl 
    page_idx = 1
    
    while page_idx <= max_pages :
        error = True
        while error:
            try:    
                html = scraperwiki.scrape(curr_url)
                root = lxml.html.fromstring(html)
                
                for tr in root.cssselect("div[class='ititle'] a"):    
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
