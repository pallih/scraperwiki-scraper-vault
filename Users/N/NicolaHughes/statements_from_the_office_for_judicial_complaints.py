import scraperwiki
import lxml.html
import urllib2, json
import datetime, time

scraper_run = time.mktime(datetime.datetime.now().timetuple())

def shorten_target(target_url):
    """
    Error checking left as an exercise
    """
    shorten_svc = 'https://www.googleapis.com/urlshortener/v1/url'
    data = '{"longUrl": "%s"}' % target_url
    request = urllib2.Request(shorten_svc,  data, 
                              {'Content-Type': 'application/json'})
    print 'Made short req'
    response = json.loads( urllib2.urlopen(request).read() )
    print 'response'
    return response[u'id']

def process(p):
    title = p.text_content()
    title = title[:title.find('(')].strip()

    #print title
    link = 'http://judicialcomplaints.judiciary.gov.uk' + p[0].get('href')

    print title, link

    # Check whether we have already scraped the url in 'link' and don't 
    # do it again.
    
    # results will be a list of dictionaries, in this case will look like 
    # [ { 'count(*)': 1 } ]
    try:
        results = scraperwiki.sqlite.select( 'count(*) from swdata where `Link`=?', [link])
        print results
        # Get the first dictionary from the results
        first_dict = results[0]

        # The key in the dictionary is the first term in the select statement above
        count = first_dict['count(*)']
        if count > 0:
            print 'We have already scraped this link', link, ' so not doing it again'
            return
        else:
            print 'We need this item'
    except:
        pass # No data yet

    #shortlink = shorten_target(link)
    #print shortlink
    #print shortlink
    data={'Title':title, 'Link':link, 'Short link': link, 'AddDate': scraper_run }
    scraperwiki.sqlite.save(unique_keys=['Title'], data=data)

html = scraperwiki.scrape("http://judicialcomplaints.judiciary.gov.uk/publications/news.htm")

root = lxml.html.fromstring(html)
h = root.cssselect("h2")[1]

while True:
    h = h.getnext()
    if h is None:
        break
    if h.tag == 'p':
        process(h)

import scraperwiki
import lxml.html
import urllib2, json
import datetime, time

scraper_run = time.mktime(datetime.datetime.now().timetuple())

def shorten_target(target_url):
    """
    Error checking left as an exercise
    """
    shorten_svc = 'https://www.googleapis.com/urlshortener/v1/url'
    data = '{"longUrl": "%s"}' % target_url
    request = urllib2.Request(shorten_svc,  data, 
                              {'Content-Type': 'application/json'})
    print 'Made short req'
    response = json.loads( urllib2.urlopen(request).read() )
    print 'response'
    return response[u'id']

def process(p):
    title = p.text_content()
    title = title[:title.find('(')].strip()

    #print title
    link = 'http://judicialcomplaints.judiciary.gov.uk' + p[0].get('href')

    print title, link

    # Check whether we have already scraped the url in 'link' and don't 
    # do it again.
    
    # results will be a list of dictionaries, in this case will look like 
    # [ { 'count(*)': 1 } ]
    try:
        results = scraperwiki.sqlite.select( 'count(*) from swdata where `Link`=?', [link])
        print results
        # Get the first dictionary from the results
        first_dict = results[0]

        # The key in the dictionary is the first term in the select statement above
        count = first_dict['count(*)']
        if count > 0:
            print 'We have already scraped this link', link, ' so not doing it again'
            return
        else:
            print 'We need this item'
    except:
        pass # No data yet

    #shortlink = shorten_target(link)
    #print shortlink
    #print shortlink
    data={'Title':title, 'Link':link, 'Short link': link, 'AddDate': scraper_run }
    scraperwiki.sqlite.save(unique_keys=['Title'], data=data)

html = scraperwiki.scrape("http://judicialcomplaints.judiciary.gov.uk/publications/news.htm")

root = lxml.html.fromstring(html)
h = root.cssselect("h2")[1]

while True:
    h = h.getnext()
    if h is None:
        break
    if h.tag == 'p':
        process(h)

