import scraperwiki
import time
import urllib2
import json

max_tries = 100
tries = 0

json_url = 'http://wildliferescue.herokuapp.com/all.json'

def get_data(json_url):
    """
        fetch json data from fussy remote url
    """
    try:
        return json.loads(urllib2.urlopen(json_url).read())
    except:
        # couldn't connect to scraperwiki, chill for a few secs and try again
        tries = tries + 1
        if tries < max_tries:
            time.sleep(randrange(10))  # wait time is random bt 1-10 seconds
            get_data(json_url)
        else:
            import sys
            sys.exit("max tries get_data")


data = get_data(json_url)
unique = 0
for d in data:
    unique = unique + 1
    d['id'] = unique
    scraperwiki.sqlite.save(unique_keys=['id'], data=d)
import scraperwiki
import time
import urllib2
import json

max_tries = 100
tries = 0

json_url = 'http://wildliferescue.herokuapp.com/all.json'

def get_data(json_url):
    """
        fetch json data from fussy remote url
    """
    try:
        return json.loads(urllib2.urlopen(json_url).read())
    except:
        # couldn't connect to scraperwiki, chill for a few secs and try again
        tries = tries + 1
        if tries < max_tries:
            time.sleep(randrange(10))  # wait time is random bt 1-10 seconds
            get_data(json_url)
        else:
            import sys
            sys.exit("max tries get_data")


data = get_data(json_url)
unique = 0
for d in data:
    unique = unique + 1
    d['id'] = unique
    scraperwiki.sqlite.save(unique_keys=['id'], data=d)
import scraperwiki
import time
import urllib2
import json

max_tries = 100
tries = 0

json_url = 'http://wildliferescue.herokuapp.com/all.json'

def get_data(json_url):
    """
        fetch json data from fussy remote url
    """
    try:
        return json.loads(urllib2.urlopen(json_url).read())
    except:
        # couldn't connect to scraperwiki, chill for a few secs and try again
        tries = tries + 1
        if tries < max_tries:
            time.sleep(randrange(10))  # wait time is random bt 1-10 seconds
            get_data(json_url)
        else:
            import sys
            sys.exit("max tries get_data")


data = get_data(json_url)
unique = 0
for d in data:
    unique = unique + 1
    d['id'] = unique
    scraperwiki.sqlite.save(unique_keys=['id'], data=d)
