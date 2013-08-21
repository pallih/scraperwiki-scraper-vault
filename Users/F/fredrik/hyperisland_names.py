import scraperwiki
import requests
import lxml.html

for i in range(1,20):
    print i

def scrape_people():
    r = requests.get('http://www.hyperisland.com/people?filter=true&role=student').text
    dom = lxml.html.fromstring(r)
    for name in dom.cssselect('h6'):
        print name.text

scrape_people()
