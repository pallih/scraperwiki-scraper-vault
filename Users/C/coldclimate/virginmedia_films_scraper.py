import scraperwiki
import sys
import urllib
import lxml.html

count = 1
base_url = "http://moviesondemand.virginmedia.com/movies/list/all"



def ToSeoFriendly(s):
    t = '-'.join(s.split())                                
    u = ''.join([c for c in t if c.isalnum() or c=='-'])
    return u.rstrip('-').lower()

html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)
paginator = root.cssselect("div[id='full-pagination'] div a span")
pages = paginator[3].text_content()
for i in range(int(pages)):
    start_url = base_url + "/" + str(count)
    print start_url
    html = scraperwiki.scrape(start_url)
    root = lxml.html.fromstring(html)
    for film in root.cssselect("div[class='artist-information'] ul li"):
        temp={}
        temp['title']=film[1].text_content()
        scraperwiki.sqlite.save(unique_keys=['title'], data=temp)
    count = count +1
    