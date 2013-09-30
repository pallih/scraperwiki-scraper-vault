import scraperwiki
import lxml.html
import urllib2
import json
import string

def read_and_store(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    container = root.find_class('bsd-contribForm-aboveContent')
    data = { 'fundraiser': container[0].text_content(), 'url': url }
    scraperwiki.sqlite.save(unique_keys=['fundraiser',], data=data)
    print container[0].text_content()


def process_results(result_list):
    for r in result_list:
        if string.find(r['url'], 'barackobama.com') > -1:
            try:
                read_and_store(r['url'])
            except:
                print "Something went wrong with %s" % r['url']
                continue

search_url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="To%20attend,%20please%20RSVP%20using%20the%20form%20to%20the%20right"'

response = urllib2.urlopen(search_url).read()
results = json.loads(response)
pages = results['responseData']['cursor']['pages'][1:]
process_results(results['responseData']['results'])
print results

for p in pages:
    response = urllib2.urlopen(search_url + '&start=%s' % p['start']).read()
    try:
        results = json.loads(response)
        process_results(results['responseData']['results'])
    except:
        continue 


import scraperwiki
import lxml.html
import urllib2
import json
import string

def read_and_store(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    container = root.find_class('bsd-contribForm-aboveContent')
    data = { 'fundraiser': container[0].text_content(), 'url': url }
    scraperwiki.sqlite.save(unique_keys=['fundraiser',], data=data)
    print container[0].text_content()


def process_results(result_list):
    for r in result_list:
        if string.find(r['url'], 'barackobama.com') > -1:
            try:
                read_and_store(r['url'])
            except:
                print "Something went wrong with %s" % r['url']
                continue

search_url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="To%20attend,%20please%20RSVP%20using%20the%20form%20to%20the%20right"'

response = urllib2.urlopen(search_url).read()
results = json.loads(response)
pages = results['responseData']['cursor']['pages'][1:]
process_results(results['responseData']['results'])
print results

for p in pages:
    response = urllib2.urlopen(search_url + '&start=%s' % p['start']).read()
    try:
        results = json.loads(response)
        process_results(results['responseData']['results'])
    except:
        continue 


