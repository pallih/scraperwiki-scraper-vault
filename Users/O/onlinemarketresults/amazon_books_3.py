# bestsellers from the kindle book store
import scraperwiki           
import lxml.html
import time
import re

for x in range(1,6):
    html = scraperwiki.scrape("http://www.amazon.com/Best-Sellers-Kindle-Store-eBooks/zgbs/digital-text/154606011/ref=zg_bs_154606011_pg_" + str(x) + 
"?_encoding=UTF8&pg=" + str(x))
    root = lxml.html.fromstring(html)
    
    pos = 0
    for el in root.cssselect("div.zg_itemImmersion"):
        title   = el.cssselect("div.zg_title a")[0].text_content()
        link   = el.cssselect("div.zg_title a")[0].attrib['href'].rstrip('\n') # Strip newline characters, funky shit happens if you don't
        #rank   = el.cssselect("span.zg_rankNumber")[0].text_content()       
        price   = el.cssselect("strong.price")[0].text_content()
        #release   = el.cssselect("div.zg_releaseDate")[0].text_content()
        author   = el.cssselect("div.zg_byline")[0].text_content()
        days_in_list   = el.cssselect("td.zg_daysInList")[0].text_content()
        pos += 1
        booklink = scraperwiki.scrape(link)
        bookpage = lxml.html.fromstring(booklink)
        
        def get_rank(bookpage):
            ## For each book detail page, select the body element for scraping wizardy
            for el in bookpage.cssselect("body"):
                ## Scraping rank
                rank = el.cssselect("li#SalesRank b")[0].tail
                ## Extract rank number from book page using regex
                re1='.*?'    # Non-greedy match on filler
                re2='(\\d+)'    # Integer Number 1
                
                rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
                m = rg.search(rank)
                if m:
                    rank=m.group(1)
                    #print "("+int1+")"+"\n"
                print "Rank of book:" 
                print rank
                #print lxml.html.tostring(rank)
            return rank

        rank = get_rank(bookpage)
        print rank      
    
        record = {"Title"  : title,
                  "Author"  : author,
                  "Link"  : link,
                  "Ranking" : get_rank(bookpage), 
                  "Price" : price, 
                  "sdate"  : time.strftime( "%Y-%m-%d" )
                 }
        scraperwiki.sqlite.save(unique_keys=["sdate"], data=record)# bestsellers from the kindle book store
import scraperwiki           
import lxml.html
import time
import re

for x in range(1,6):
    html = scraperwiki.scrape("http://www.amazon.com/Best-Sellers-Kindle-Store-eBooks/zgbs/digital-text/154606011/ref=zg_bs_154606011_pg_" + str(x) + 
"?_encoding=UTF8&pg=" + str(x))
    root = lxml.html.fromstring(html)
    
    pos = 0
    for el in root.cssselect("div.zg_itemImmersion"):
        title   = el.cssselect("div.zg_title a")[0].text_content()
        link   = el.cssselect("div.zg_title a")[0].attrib['href'].rstrip('\n') # Strip newline characters, funky shit happens if you don't
        #rank   = el.cssselect("span.zg_rankNumber")[0].text_content()       
        price   = el.cssselect("strong.price")[0].text_content()
        #release   = el.cssselect("div.zg_releaseDate")[0].text_content()
        author   = el.cssselect("div.zg_byline")[0].text_content()
        days_in_list   = el.cssselect("td.zg_daysInList")[0].text_content()
        pos += 1
        booklink = scraperwiki.scrape(link)
        bookpage = lxml.html.fromstring(booklink)
        
        def get_rank(bookpage):
            ## For each book detail page, select the body element for scraping wizardy
            for el in bookpage.cssselect("body"):
                ## Scraping rank
                rank = el.cssselect("li#SalesRank b")[0].tail
                ## Extract rank number from book page using regex
                re1='.*?'    # Non-greedy match on filler
                re2='(\\d+)'    # Integer Number 1
                
                rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
                m = rg.search(rank)
                if m:
                    rank=m.group(1)
                    #print "("+int1+")"+"\n"
                print "Rank of book:" 
                print rank
                #print lxml.html.tostring(rank)
            return rank

        rank = get_rank(bookpage)
        print rank      
    
        record = {"Title"  : title,
                  "Author"  : author,
                  "Link"  : link,
                  "Ranking" : get_rank(bookpage), 
                  "Price" : price, 
                  "sdate"  : time.strftime( "%Y-%m-%d" )
                 }
        scraperwiki.sqlite.save(unique_keys=["sdate"], data=record)