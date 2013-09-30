###############################################################################
# Craigslist scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
import json
import datetime
import dateutil.parser



# spam location text to look out for:
regexes = list()
regexes.append( r"silver[\s]*spring[s]?" )
regexes.append( r"temple hill[s]?" )
regexes.append( r"arlington" )
regexes.append( r"columbia[\s]m[\.]?d[\.]?" )
regexes.append( r"2[\s]*men[\s]*[\&(\&amp\;)]*[\s]*truck" )
regexes.append( r"crystal[\s]*city" )
regexes.append( r"pentagon[\s]*city" )
regexes.append( r"v[\s]*a[\s]*" )
regexes.append( r"m[\.]?[\s]*d[\.]?[\s]*" )
regexes.append( r"oxon[\s]*hill" )
regexes.append( r"sect[\s]*[\d][\s]*ok" )
regexes.append( r"NoMa" )
regexes.append( r"NoMd" )
regexes.append( r"palisades" )
regexes.append( r"hyattsville" )
regexes.append( r"maryland" )
regexes.append( r"virginia" )


# spam flagging URL
# http://washingtondc.craigslist.org/flag/?flagCode=15&postingID=<POST_ID>"

# apartment listing URL
aptURL = 'http://washingtondc.craigslist.org/doc/apa/'

# scraper run info URL
runURL = 'https://api.scraperwiki.com/api/1.0/scraper/getruninfo?format=jsondict&name=craigslist_flagger'

# retrieve a page
soup = BeautifulSoup( scraperwiki.scrape( aptURL ) )

today = datetime.datetime.today()

# grab all the apartment listings from the initial page
for p in soup('p' , {"align":None} ):
    record ={}
    record['title'] = "No Title"
    record['link'] = "No Link"
    record['id']="noid"
    record['location'] = "No Location"
    record['flag_url'] = "nourl"

    if p.font:
        # ditch the leading and trailing parentheses
        record['location'] =  re.subn(r"\(" , "" , re.subn(r"\)" , "" , p.font.text)[0] )[0]
    else:
        continue
    
    if p.a:
        record['title'] = p.a.text
        
        if p.a['href']:
            record['link'] = p.a['href']

            if re.search( r"/([\d]+)\.html" , p.a['href'] ):
                record['id'] = re.subn( r"\.html","", re.subn( r"/" ,"", re.search( r"/([\d]+)\.html" , p.a['href'] ).group(0) )[0] )[0]
                record['flag_url']="http://washingtondc.craigslist.org/flag/?flagcode=15&postingID="+record['id']
    else:
        continue
    
    record['date_scraped'] = today

    # test the location for spam
    for rx in regexes:
        if re.search( rx , record['location'] , re.I ):
            scraperwiki.sqlite.save( ["id"] , record )

    scraperwiki.sqlite.commit()


# now, go grab all the spam and 'click' the flagging URL
scrapes = scraperwiki.sqlite.select("* from 'swdata'")
for scrape in scrapes:
    if scrape['date_scraped'] == None or scrape['date_scraped'] == 'null' :
        print "BAD DATE -- " + scrape['date_scraped']
    else:
        print scraperwiki.scrape( scrape['flag_url'] )
        scraperwiki.sqlite.execute("DELETE FROM swdata WHERE id IN (?)", [ scrape['id'] ])


###############################################################################
# Craigslist scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
import json
import datetime
import dateutil.parser



# spam location text to look out for:
regexes = list()
regexes.append( r"silver[\s]*spring[s]?" )
regexes.append( r"temple hill[s]?" )
regexes.append( r"arlington" )
regexes.append( r"columbia[\s]m[\.]?d[\.]?" )
regexes.append( r"2[\s]*men[\s]*[\&(\&amp\;)]*[\s]*truck" )
regexes.append( r"crystal[\s]*city" )
regexes.append( r"pentagon[\s]*city" )
regexes.append( r"v[\s]*a[\s]*" )
regexes.append( r"m[\.]?[\s]*d[\.]?[\s]*" )
regexes.append( r"oxon[\s]*hill" )
regexes.append( r"sect[\s]*[\d][\s]*ok" )
regexes.append( r"NoMa" )
regexes.append( r"NoMd" )
regexes.append( r"palisades" )
regexes.append( r"hyattsville" )
regexes.append( r"maryland" )
regexes.append( r"virginia" )


# spam flagging URL
# http://washingtondc.craigslist.org/flag/?flagCode=15&postingID=<POST_ID>"

# apartment listing URL
aptURL = 'http://washingtondc.craigslist.org/doc/apa/'

# scraper run info URL
runURL = 'https://api.scraperwiki.com/api/1.0/scraper/getruninfo?format=jsondict&name=craigslist_flagger'

# retrieve a page
soup = BeautifulSoup( scraperwiki.scrape( aptURL ) )

today = datetime.datetime.today()

# grab all the apartment listings from the initial page
for p in soup('p' , {"align":None} ):
    record ={}
    record['title'] = "No Title"
    record['link'] = "No Link"
    record['id']="noid"
    record['location'] = "No Location"
    record['flag_url'] = "nourl"

    if p.font:
        # ditch the leading and trailing parentheses
        record['location'] =  re.subn(r"\(" , "" , re.subn(r"\)" , "" , p.font.text)[0] )[0]
    else:
        continue
    
    if p.a:
        record['title'] = p.a.text
        
        if p.a['href']:
            record['link'] = p.a['href']

            if re.search( r"/([\d]+)\.html" , p.a['href'] ):
                record['id'] = re.subn( r"\.html","", re.subn( r"/" ,"", re.search( r"/([\d]+)\.html" , p.a['href'] ).group(0) )[0] )[0]
                record['flag_url']="http://washingtondc.craigslist.org/flag/?flagcode=15&postingID="+record['id']
    else:
        continue
    
    record['date_scraped'] = today

    # test the location for spam
    for rx in regexes:
        if re.search( rx , record['location'] , re.I ):
            scraperwiki.sqlite.save( ["id"] , record )

    scraperwiki.sqlite.commit()


# now, go grab all the spam and 'click' the flagging URL
scrapes = scraperwiki.sqlite.select("* from 'swdata'")
for scrape in scrapes:
    if scrape['date_scraped'] == None or scrape['date_scraped'] == 'null' :
        print "BAD DATE -- " + scrape['date_scraped']
    else:
        print scraperwiki.scrape( scrape['flag_url'] )
        scraperwiki.sqlite.execute("DELETE FROM swdata WHERE id IN (?)", [ scrape['id'] ])


