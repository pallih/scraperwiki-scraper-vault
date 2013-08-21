import scraperwiki
import lxml.html
import urllib2
import json
import string
def read_and_store(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    container = root.find_class("bsd-contribForm-aboveContent")
    data = {"fundraiser": container[0].text_content(), "url":url}
    scraperwiki.sqlite.save(unique_keys=["fundraiser",], data=data)
    print container[0].text_content()
def process_results(result_list):
    for n in result_list:
        if string.find(n['url'],'https://secure.dccc.org') > -1:
            try:
                read_and_store(n['url'])
            except:
                print "Something went wrong URL is: %s" % n['url']
                continue
searchUrl = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="Please%20join"'
response = urllib2.urlopen(searchUrl).read()
results = json.loads(response)
pages = results['responseData']['cursor']['pages'][1:]
process_results(results['responseData']['results'])
for p in pages:
    response = urllib2.urlopen(searchUrl + "&start=%s" % p['start']).read()
    print searchUrl + "&start=%s" % p['start']
    print response
    try:
        results = json.loads(response)
        process_results(results['responseData']['results'])
    except Exception as e:
        print e
        print "couldn't process page %s" % p['label']
        continue
    
print results


