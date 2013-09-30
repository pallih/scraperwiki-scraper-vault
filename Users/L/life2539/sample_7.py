#http://profit.ly/user/jasonbond/trades?page=1&size=25


print "Beginning scrape"

#                                                    ##                    BEGIN SETTINGS

profitlyuser = "jasonbond"

#                                                    #                    END   SETTINGS


import scraperwiki

import lxml.html
import lxml.etree

def pageloop(profitlyuser):
    
    pagecounter = 1
    url = "http://profit.ly/user/"+profitlyuser +"/trades?page="+ str(pagecounter) +"&size=25"

    finalpage = int(get_last_page(url))
    print "Processing", finalpage, "pages"
    pagesremaining = finalpage - pagecounter + 1
    while pagesremaining:
        print pagesremaining , "pages togo..."

        scrapetrades(url)
        
        pagecounter += 1
        url= "http://profit.ly/user/"+profitlyuser +"/trades?page="+ str(pagecounter) +"&size=25"
        pagesremaining = finalpage - pagecounter + 1
            
    return

def get_last_page(url):
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    pages = root.cssselect(".emm-paginate a[title='Last Page']")
    doc = lxml.html.document_fromstring(lxml.html.tostring(pages[0]))
    for elem in doc.iter():
        if elem.tag == 'a':
            for ii in elem.items():
                if ii[0] == 'href':
                    lastpage = ii[1].replace('?page=',"")
                    lastpage = lastpage.replace("""&size=25""","")
                    
    return int(lastpage)

def scrapetrades(url):
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    pages = root.cssselect(".emm-paginate a[title='Last Page']")

    for tr in root.cssselect(".trade .title"):
        a = tr.cssselect("a")
        span = tr.cssselect("span span")
            
    #                                                                        EXTRACTING ATTRIBUTES
        doc = lxml.html.document_fromstring(lxml.html.tostring(a[0]))
            
        for elem in doc.iter():
            if elem.tag == 'a':
                for ii in elem.items():
                    if ii[0] == 'href':
                        relatedlink = ii[1]
                            
    #                                                                        Insert trade details 
        #modify url
        relatedlink = "http://profit.ly"+ relatedlink
        details = trade_details(relatedlink)


        trades= {
              'LINK'         : relatedlink,
              'TICKER'       : a[2].text_content(),
              'DIRECTION'    : span[0].text_content(),
              'AMOUNT'       : a[0].text_content(),
              'ENTRY_DATE'   : details[0][0],
              'ENTRY_PRICE'  : details[0][1],
              'EXIT_DATE'    : details[1][0],
              'EXIT_PRICE'   : details[1][1],
              'POSITION_SIZE': details[2],
              'TRADER'       : a[3].text_content()
            }
        
        scraperwiki.sqlite.save(unique_keys=['LINK'], data=trades)
    return


def trade_details(url):
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    passcounter = 0 # for first table
    day_and_price = ()
    for div in root.cssselect("#trade-info"):
        
        for table in div.cssselect("table"):
            
            for tr in table.cssselect("tr"):
                
                if 1 < passcounter and passcounter < 4: 
                    th = tr.cssselect("th")
                    tds = tr.cssselect("td")
                    th = th[0].text_content()
                    if   th == "Entry":
                        entry = (tds[0].text_content(), tds[1].text_content())
                    elif th == "Exit":
                        exit  = (tds[0].text_content(), tds[1].text_content())

                elif passcounter == 4:
                    tds = tr.cssselect("td")                   
                    positionsize = tds[0].text_content()
                    onepass = True
                passcounter +=1


    trade_detail_list = (entry, exit, positionsize)
    #print trade_detail_list 

    return trade_detail_list    


#### run code
pageloop(profitlyuser)
print "done!"#http://profit.ly/user/jasonbond/trades?page=1&size=25


print "Beginning scrape"

#                                                    ##                    BEGIN SETTINGS

profitlyuser = "jasonbond"

#                                                    #                    END   SETTINGS


import scraperwiki

import lxml.html
import lxml.etree

def pageloop(profitlyuser):
    
    pagecounter = 1
    url = "http://profit.ly/user/"+profitlyuser +"/trades?page="+ str(pagecounter) +"&size=25"

    finalpage = int(get_last_page(url))
    print "Processing", finalpage, "pages"
    pagesremaining = finalpage - pagecounter + 1
    while pagesremaining:
        print pagesremaining , "pages togo..."

        scrapetrades(url)
        
        pagecounter += 1
        url= "http://profit.ly/user/"+profitlyuser +"/trades?page="+ str(pagecounter) +"&size=25"
        pagesremaining = finalpage - pagecounter + 1
            
    return

def get_last_page(url):
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    pages = root.cssselect(".emm-paginate a[title='Last Page']")
    doc = lxml.html.document_fromstring(lxml.html.tostring(pages[0]))
    for elem in doc.iter():
        if elem.tag == 'a':
            for ii in elem.items():
                if ii[0] == 'href':
                    lastpage = ii[1].replace('?page=',"")
                    lastpage = lastpage.replace("""&size=25""","")
                    
    return int(lastpage)

def scrapetrades(url):
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    pages = root.cssselect(".emm-paginate a[title='Last Page']")

    for tr in root.cssselect(".trade .title"):
        a = tr.cssselect("a")
        span = tr.cssselect("span span")
            
    #                                                                        EXTRACTING ATTRIBUTES
        doc = lxml.html.document_fromstring(lxml.html.tostring(a[0]))
            
        for elem in doc.iter():
            if elem.tag == 'a':
                for ii in elem.items():
                    if ii[0] == 'href':
                        relatedlink = ii[1]
                            
    #                                                                        Insert trade details 
        #modify url
        relatedlink = "http://profit.ly"+ relatedlink
        details = trade_details(relatedlink)


        trades= {
              'LINK'         : relatedlink,
              'TICKER'       : a[2].text_content(),
              'DIRECTION'    : span[0].text_content(),
              'AMOUNT'       : a[0].text_content(),
              'ENTRY_DATE'   : details[0][0],
              'ENTRY_PRICE'  : details[0][1],
              'EXIT_DATE'    : details[1][0],
              'EXIT_PRICE'   : details[1][1],
              'POSITION_SIZE': details[2],
              'TRADER'       : a[3].text_content()
            }
        
        scraperwiki.sqlite.save(unique_keys=['LINK'], data=trades)
    return


def trade_details(url):
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    passcounter = 0 # for first table
    day_and_price = ()
    for div in root.cssselect("#trade-info"):
        
        for table in div.cssselect("table"):
            
            for tr in table.cssselect("tr"):
                
                if 1 < passcounter and passcounter < 4: 
                    th = tr.cssselect("th")
                    tds = tr.cssselect("td")
                    th = th[0].text_content()
                    if   th == "Entry":
                        entry = (tds[0].text_content(), tds[1].text_content())
                    elif th == "Exit":
                        exit  = (tds[0].text_content(), tds[1].text_content())

                elif passcounter == 4:
                    tds = tr.cssselect("td")                   
                    positionsize = tds[0].text_content()
                    onepass = True
                passcounter +=1


    trade_detail_list = (entry, exit, positionsize)
    #print trade_detail_list 

    return trade_detail_list    


#### run code
pageloop(profitlyuser)
print "done!"