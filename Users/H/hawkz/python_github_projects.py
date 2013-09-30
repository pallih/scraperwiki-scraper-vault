import scraperwiki        
import lxml.html
import time

html = scraperwiki.scrape("http://github.com/search?langOverride=&language=&q=language%3Apython&repo=&start_value=1&type=Repositories")

root = lxml.html.fromstring(html)

last_page = 0
for page in root.cssselect(".pagination a"):
    last_page = int(page.text_content())
print "Found %s pages!" % last_page
# -- was 3278

for results_page in range(last_page):
    html = scraperwiki.scrape("http://github.com/search?langOverride=&language=&q=language%%3Apython&repo=&start_value=%s&type=Repositories" % results_page) 
    root = lxml.html.fromstring(html)

    for result in root.cssselect("div.results div.result"):
        project = result.cssselect("a")
        data = {
          'project' : project[0].text_content(),
          'url' : project[0].get('href'),
          'page': results_page,
        }
        #print data
        scraperwiki.sqlite.save(unique_keys=['project'], data=data)

    #be polite!
    time.sleep(2)import scraperwiki        
import lxml.html
import time

html = scraperwiki.scrape("http://github.com/search?langOverride=&language=&q=language%3Apython&repo=&start_value=1&type=Repositories")

root = lxml.html.fromstring(html)

last_page = 0
for page in root.cssselect(".pagination a"):
    last_page = int(page.text_content())
print "Found %s pages!" % last_page
# -- was 3278

for results_page in range(last_page):
    html = scraperwiki.scrape("http://github.com/search?langOverride=&language=&q=language%%3Apython&repo=&start_value=%s&type=Repositories" % results_page) 
    root = lxml.html.fromstring(html)

    for result in root.cssselect("div.results div.result"):
        project = result.cssselect("a")
        data = {
          'project' : project[0].text_content(),
          'url' : project[0].get('href'),
          'page': results_page,
        }
        #print data
        scraperwiki.sqlite.save(unique_keys=['project'], data=data)

    #be polite!
    time.sleep(2)