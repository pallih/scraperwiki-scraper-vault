###############################################################################
# Twitter srcaper for the term 'liverpool'.
###############################################################################

import scraperwiki
import simplejson
import datetime

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'liverpool'
options = '&rpp=100&page='
page = 1

while 1:
    try:
        url = base_url + q + options + str(page)
        html = scraperwiki.scrape(url)
        #print html
        soup = simplejson.loads(html)
        for result in soup['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['user_link'] = 'http://twitter.com/%s' % result['from_user']
            data['date_scraped'] = datetime.datetime.now()
            data['pic'] = results.get('profile_image_url', '')
            scraperwiki.sqlite.save(["id"], data) 
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        break
        
    ###############################################################################
# Twitter srcaper for the term 'liverpool'.
###############################################################################

import scraperwiki
import simplejson
import datetime

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'liverpool'
options = '&rpp=100&page='
page = 1

while 1:
    try:
        url = base_url + q + options + str(page)
        html = scraperwiki.scrape(url)
        #print html
        soup = simplejson.loads(html)
        for result in soup['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['user_link'] = 'http://twitter.com/%s' % result['from_user']
            data['date_scraped'] = datetime.datetime.now()
            data['pic'] = results.get('profile_image_url', '')
            scraperwiki.sqlite.save(["id"], data) 
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        break
        
    ###############################################################################
# Twitter srcaper for the term 'liverpool'.
###############################################################################

import scraperwiki
import simplejson
import datetime

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'liverpool'
options = '&rpp=100&page='
page = 1

while 1:
    try:
        url = base_url + q + options + str(page)
        html = scraperwiki.scrape(url)
        #print html
        soup = simplejson.loads(html)
        for result in soup['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['user_link'] = 'http://twitter.com/%s' % result['from_user']
            data['date_scraped'] = datetime.datetime.now()
            data['pic'] = results.get('profile_image_url', '')
            scraperwiki.sqlite.save(["id"], data) 
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        break
        
    ###############################################################################
# Twitter srcaper for the term 'liverpool'.
###############################################################################

import scraperwiki
import simplejson
import datetime

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'liverpool'
options = '&rpp=100&page='
page = 1

while 1:
    try:
        url = base_url + q + options + str(page)
        html = scraperwiki.scrape(url)
        #print html
        soup = simplejson.loads(html)
        for result in soup['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['user_link'] = 'http://twitter.com/%s' % result['from_user']
            data['date_scraped'] = datetime.datetime.now()
            data['pic'] = results.get('profile_image_url', '')
            scraperwiki.sqlite.save(["id"], data) 
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        break
        
    