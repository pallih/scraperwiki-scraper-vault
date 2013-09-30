import scraperwiki
import urllib
import urllib2
from cookielib import CookieJar
from lxml import etree
from pprint import pprint 
from pyquery import PyQuery as pq
from time import sleep

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))


DOMAIN = 'http://www.byliner.com'
START_URL = "%s%s" % (DOMAIN, '/spotlights/102-spectacular-nonfiction-articles-2012')
d = pq(url=START_URL)
articles = d(".anthology--story-listing")
for i, article in enumerate(articles):
    #if i < 30: continue
    listing = d(article)
    details = {}
    details['heading'] = listing('h1').text()
    details['author'] = listing('.by_writer').text().replace('by','').strip()
    details['subheading'] = listing('.subheading').text()
    details['byliner_url'] = "%s%s%s" % (DOMAIN, listing('a.hit_area').attr('href'), '/read_offsite')
    details['publication'] = listing('.publication').text()
    # Broken URL. 
    if details['byliner_url'] == 'http://www.byliner.com/pamela-colloff/stories/the-innocent-man-part-one/read_offsite':
        details['url'] = 'http://www.texasmonthly.com/story/innocent-man-part-one'
    elif details['byliner_url'] == 'http://www.byliner.com/michael-hall/stories/trigger/read_offsite':
        details['url'] = 'http://www.texasmonthly.com/story/trigger'
    else:
        try: 
            p = opener.open(details['byliner_url'])
            details['url'] = p.url
            pprint(details)
        except urllib2.HTTPError:
            print 'Error found with url %s, waiting...' % details['byliner_url']
            sleep(10)
            p = opener.open(details['byliner_url'])
            details['url'] = p.url
            pprint(details)
    scraperwiki.sqlite.save(['url'], details)
    


import scraperwiki
import urllib
import urllib2
from cookielib import CookieJar
from lxml import etree
from pprint import pprint 
from pyquery import PyQuery as pq
from time import sleep

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))


DOMAIN = 'http://www.byliner.com'
START_URL = "%s%s" % (DOMAIN, '/spotlights/102-spectacular-nonfiction-articles-2012')
d = pq(url=START_URL)
articles = d(".anthology--story-listing")
for i, article in enumerate(articles):
    #if i < 30: continue
    listing = d(article)
    details = {}
    details['heading'] = listing('h1').text()
    details['author'] = listing('.by_writer').text().replace('by','').strip()
    details['subheading'] = listing('.subheading').text()
    details['byliner_url'] = "%s%s%s" % (DOMAIN, listing('a.hit_area').attr('href'), '/read_offsite')
    details['publication'] = listing('.publication').text()
    # Broken URL. 
    if details['byliner_url'] == 'http://www.byliner.com/pamela-colloff/stories/the-innocent-man-part-one/read_offsite':
        details['url'] = 'http://www.texasmonthly.com/story/innocent-man-part-one'
    elif details['byliner_url'] == 'http://www.byliner.com/michael-hall/stories/trigger/read_offsite':
        details['url'] = 'http://www.texasmonthly.com/story/trigger'
    else:
        try: 
            p = opener.open(details['byliner_url'])
            details['url'] = p.url
            pprint(details)
        except urllib2.HTTPError:
            print 'Error found with url %s, waiting...' % details['byliner_url']
            sleep(10)
            p = opener.open(details['byliner_url'])
            details['url'] = p.url
            pprint(details)
    scraperwiki.sqlite.save(['url'], details)
    


