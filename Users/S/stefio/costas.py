###############################################################################
# Waitrose scraper
# http://www.localstore.co.uk/stores/83005/costa/
###############################################################################

from pyparsing import Literal, quotedString, removeQuotes, delimitedList






import scraperwiki,re
from BeautifulSoup import BeautifulSoup

record = {}

for i in range(1,162):
    print i
    # retrieve a page
    starting_url = 'http://www.localstore.co.uk/stores/83005/costa/p' + str(i) +'.html'
    #print starting_url
    try:
        html = scraperwiki.scrape(starting_url)
    except:
        print "Page not found"
    else:
        #print "Page found"
        soup = BeautifulSoup(html)
        #print soup
        matches  = soup.findAll(text=re.compile('postcode'))
        for match in matches:
            #print match
            tds = match.split(",")
            #print tds
            
            for td in tds:
                
                matched = td.split(':')
                #print matched[0]
    
                if (matched[0]=='"address"'):
                    #print "found"
                    record['id'] = matched[1]
    
                if (matched[0]=='"postcode"'):
                    #print "found"
                    record['postcode'] = matched[1]
                    scraperwiki.sqlite.save(['id'], record)


###############################################################################
# Waitrose scraper
# http://www.localstore.co.uk/stores/83005/costa/
###############################################################################

from pyparsing import Literal, quotedString, removeQuotes, delimitedList






import scraperwiki,re
from BeautifulSoup import BeautifulSoup

record = {}

for i in range(1,162):
    print i
    # retrieve a page
    starting_url = 'http://www.localstore.co.uk/stores/83005/costa/p' + str(i) +'.html'
    #print starting_url
    try:
        html = scraperwiki.scrape(starting_url)
    except:
        print "Page not found"
    else:
        #print "Page found"
        soup = BeautifulSoup(html)
        #print soup
        matches  = soup.findAll(text=re.compile('postcode'))
        for match in matches:
            #print match
            tds = match.split(",")
            #print tds
            
            for td in tds:
                
                matched = td.split(':')
                #print matched[0]
    
                if (matched[0]=='"address"'):
                    #print "found"
                    record['id'] = matched[1]
    
                if (matched[0]=='"postcode"'):
                    #print "found"
                    record['postcode'] = matched[1]
                    scraperwiki.sqlite.save(['id'], record)


