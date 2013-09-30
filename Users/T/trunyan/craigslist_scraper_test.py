import scraperwiki
import lxml.etree
import lxml.html

html = scraperwiki.scrape("http://desmoines.craigslist.org/search/bik?zoomToPosting=&query=trek&srchType=A&minAsk=&maxAsk=&hasPic=1")

scraperwiki.sqlite.execute("drop table if exists RESULTS")
scraperwiki.sqlite.commit()

root = lxml.html.fromstring(html)  
listings = root.cssselect('p') 

for listing in listings:
    dataId = listing.cssselect('p.row')[0].attrib['data-pid']
    descrip = listing.cssselect('a')[1].text 
    date = listing.cssselect('span.date')[0].text 
    pri = listing.cssselect('span.price') 
    href  = listing.cssselect("a")[0].attrib['href']
    
    if len(pri) > 0:
        price = pri[0].text
    else:
        price = "0"    

    ###create data entry and record it in sqlite database
    data = {
        'ID' : dataId,
        'HREF': href,
        'DESCRIPTION' : descrip,        
        'DATE' : date,
        'PRICE' : price}
     
    #print data 
    scraperwiki.sqlite.save(unique_keys=['ID'], data = data, table_name="RESULTS", verbose=0) # save the records one by one


import scraperwiki
import lxml.etree
import lxml.html

html = scraperwiki.scrape("http://desmoines.craigslist.org/search/bik?zoomToPosting=&query=trek&srchType=A&minAsk=&maxAsk=&hasPic=1")

scraperwiki.sqlite.execute("drop table if exists RESULTS")
scraperwiki.sqlite.commit()

root = lxml.html.fromstring(html)  
listings = root.cssselect('p') 

for listing in listings:
    dataId = listing.cssselect('p.row')[0].attrib['data-pid']
    descrip = listing.cssselect('a')[1].text 
    date = listing.cssselect('span.date')[0].text 
    pri = listing.cssselect('span.price') 
    href  = listing.cssselect("a")[0].attrib['href']
    
    if len(pri) > 0:
        price = pri[0].text
    else:
        price = "0"    

    ###create data entry and record it in sqlite database
    data = {
        'ID' : dataId,
        'HREF': href,
        'DESCRIPTION' : descrip,        
        'DATE' : date,
        'PRICE' : price}
     
    #print data 
    scraperwiki.sqlite.save(unique_keys=['ID'], data = data, table_name="RESULTS", verbose=0) # save the records one by one


