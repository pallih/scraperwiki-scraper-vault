import scraperwiki
import lxml.html

def scrapePageWise(listID):
    url="http://www.subsport.eu/listoflists?listid="+str(listID)
    print url
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    rowID=0
    listName=''
    try:
        listName = root.cssselect("div[style~='float:'] > h2")[0].text
    except:
        pass
    for el in root.cssselect("div[id='zeile']"):
        rowID+=1;id = str(listID)+str(rowID)
        try:
            substance_name = el.cssselect("div[id='det_substance_name']")[0].text
            cas_no = el.cssselect("div[id='det_cas_no']")[0].text
            ec_no = el.cssselect("div[id='det_ec_no']")[0].text
            scraperwiki.sqlite.save(unique_keys=['id'], data={'id':id,
                                      'name':substance_name,
                                      'cas_no':cas_no,
                                      'ec_no':ec_no,
                                      'list_name':listName,
                                      'list_id':listID,

                                      })
        except:
            pass


for i in range(1,2):
    print i
    try:
        scrapePageWise(i)
    except:
        pass
import scraperwiki
import lxml.html

def scrapePageWise(listID):
    url="http://www.subsport.eu/listoflists?listid="+str(listID)
    print url
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    rowID=0
    listName=''
    try:
        listName = root.cssselect("div[style~='float:'] > h2")[0].text
    except:
        pass
    for el in root.cssselect("div[id='zeile']"):
        rowID+=1;id = str(listID)+str(rowID)
        try:
            substance_name = el.cssselect("div[id='det_substance_name']")[0].text
            cas_no = el.cssselect("div[id='det_cas_no']")[0].text
            ec_no = el.cssselect("div[id='det_ec_no']")[0].text
            scraperwiki.sqlite.save(unique_keys=['id'], data={'id':id,
                                      'name':substance_name,
                                      'cas_no':cas_no,
                                      'ec_no':ec_no,
                                      'list_name':listName,
                                      'list_id':listID,

                                      })
        except:
            pass


for i in range(1,2):
    print i
    try:
        scrapePageWise(i)
    except:
        pass
