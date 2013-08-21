import datetime
import time
import scraperwiki
#from BeautifulSoup import BeautifulSoup
import lxml.html



for place in places:
    print 'Current Place :', place

    currentPlace = place
    url     = "http://www.funda.nl/koop/tilburg/appartement/"

    print url 

    html    = scraperwiki.scrape(url)

    #soup = BeautifulSoup(html)
    root = lxml.html.fromstring(html)

    theTime = datetime.datetime.now()
    theTime = theTime.replace(second=0, microsecond=0)

    #get nr of houses
    #nrHouses = soup.findAll('h1').string.replace(' huizen te koop', '').replace('.','')
    
    forSaleOrSold = []
    counter = 0
    houses_forsale = ""
    houses_sold = ""
    elResult = ""
    for el in root.cssselect("ul.tab-list li a span.hits"):           
        elResult = el.text_content()
        forSaleOrSold.append(elResult)
        counter += 1
    
    houses_forsale = forSaleOrSold[0].replace('(','').replace(')','').strip()
    houses_sold = forSaleOrSold[1].replace('(','').replace(')','').strip()


    # SAVE to SQLITE
    scraperwiki.sqlite.save(unique_keys=[], table_name='funda_nl',
            data={
                    'huizen_te_koop' : houses_forsale,
                    'huizen_verkocht' : houses_sold,
                    'plaats' : currentPlace,
                    'url' : url,
                    'datum' : theTime
            }
    )





print scraperwiki.sqlite.show_tables()
