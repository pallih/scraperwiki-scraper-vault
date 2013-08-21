# bestsellers from readings.com.au
import scraperwiki           
import lxml.html
import time

for x in range(1,6):
    html = scraperwiki.scrape("http://www.amazon.com/Best-Sellers-Kindle-Store/zgbs/digital-text/ref=zg_bs_tab_t_bs" + str(x))
    root = lxml.html.fromstring(html)
    
    pos = 0
    
    for el in root.cssselect("div.zg_itemRightDiv_normal"):
        title   = el.cssselect("div.zg_title a")[0].text_content()
        rank   = el.cssselect("span.zg_rankNumber")[0].text_content()
        price   = el.cssselect("span.price")[0].text_content()
        release   = el.cssselect("div.zg_releaseDate")[0].text_content()
        author   = el.cssselect("div.zg_byline")[0].text_content()
    
        pos += 1
    
        record = {"Title"  : title,
                  "Author"  : author,
                  "Ranking" : rank, 
                  "Price" : price, 
                  "Release Date" : release, 
                  "sdate"  : time.strftime( "%Y-%m-%d" )
                 }
        scraperwiki.sqlite.save(unique_keys=["sdate"], data=record)