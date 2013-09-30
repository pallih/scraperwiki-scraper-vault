import scraperwiki
import pickle
import dateutil.parser
import xml.etree.ElementTree as et
from datetime import datetime
from hashlib import sha1

def eveapi_get(url, params=None):

    url_id = url.replace('://', '_').replace('/', '-')

    try:
        cachetime = pickle.loads(scraperwiki.sqlite.get_var(url_id))
    except:
        cachetime = datetime(2001,1,1)
    
    # Check cache expiry, if so scrape the page
    if datetime.utcnow() >= cachetime:
        print "Cache has expired, requesting new copy"
        xml = scraperwiki.scrape(url, params, 'ScraperWiki.com EVE API Cache Library')
        root = et.fromstring(xml)
        
        # Grab the relevant times from the parsed XML
        evetime = dateutil.parser.parse(root.find('currentTime').text)
        cachetime = dateutil.parser.parse(root.find('cachedUntil').text)
        
        # Calculate the local server / EVE time skew
        skew = datetime.utcnow() - evetime
        
        # Save the cache clock
        scraperwiki.sqlite.save_var(url_id, pickle.dumps(cachetime + skew))
        scraperwiki.sqlite.save_var(url_id + "_cachedoc", xml)
    else:
        print "Using cached version of %s" % url
        xml = scraperwiki.sqlite.get_var(url_id + "_cachedoc")
        root = et.fromstring(xml)
    return root

import scraperwiki
import pickle
import dateutil.parser
import xml.etree.ElementTree as et
from datetime import datetime
from hashlib import sha1

def eveapi_get(url, params=None):

    url_id = url.replace('://', '_').replace('/', '-')

    try:
        cachetime = pickle.loads(scraperwiki.sqlite.get_var(url_id))
    except:
        cachetime = datetime(2001,1,1)
    
    # Check cache expiry, if so scrape the page
    if datetime.utcnow() >= cachetime:
        print "Cache has expired, requesting new copy"
        xml = scraperwiki.scrape(url, params, 'ScraperWiki.com EVE API Cache Library')
        root = et.fromstring(xml)
        
        # Grab the relevant times from the parsed XML
        evetime = dateutil.parser.parse(root.find('currentTime').text)
        cachetime = dateutil.parser.parse(root.find('cachedUntil').text)
        
        # Calculate the local server / EVE time skew
        skew = datetime.utcnow() - evetime
        
        # Save the cache clock
        scraperwiki.sqlite.save_var(url_id, pickle.dumps(cachetime + skew))
        scraperwiki.sqlite.save_var(url_id + "_cachedoc", xml)
    else:
        print "Using cached version of %s" % url
        xml = scraperwiki.sqlite.get_var(url_id + "_cachedoc")
        root = et.fromstring(xml)
    return root

