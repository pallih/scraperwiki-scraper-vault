import scraperwiki
import lxml.html
import re

city = "New York"
state = "NY"

apartments = []

for start in range(0, 10 * 100, 100):
    html = scraperwiki.scrape("http://newjersey.craigslist.org/search/apa?query=&srchType=A&minAsk=1600&maxAsk=2200&bedrooms=1&s=%s" % start)
    root = lxml.html.fromstring(html)
    
    
    for p in root.cssselect("p"):
        link = p.xpath("a")
        location = p.xpath("font[@size=-1]")
        if not (link and location): continue
        
        link = link[0]
        url = link.get("href")
        title = link.text_content()
        location = re.sub("\s+", " ", re.sub("([^A-Z]|%s)" % state, " ", location[0].text_content(), flags=(re.I | re.M)), flags=re.M).strip().title()
        if location.find(city) == -1: continue
        
        text = p.text_content()
        date = text.split("-", 2)[0].strip()
        last = text.rsplit(" ", 2)[-1].strip().lower()
        img = last == "img"
        pic = last == "pic"

        apartments.append({
            "date": date ,
            "img": img ,
            "location": location,
            "pic": pic ,
            "title": title,
            "url": url
        })


print "Found %s apartments" % len(apartments)
scraperwiki.sqlite.save(unique_keys=['url'], data=apartments)
import scraperwiki
import lxml.html
import re

city = "New York"
state = "NY"

apartments = []

for start in range(0, 10 * 100, 100):
    html = scraperwiki.scrape("http://newjersey.craigslist.org/search/apa?query=&srchType=A&minAsk=1600&maxAsk=2200&bedrooms=1&s=%s" % start)
    root = lxml.html.fromstring(html)
    
    
    for p in root.cssselect("p"):
        link = p.xpath("a")
        location = p.xpath("font[@size=-1]")
        if not (link and location): continue
        
        link = link[0]
        url = link.get("href")
        title = link.text_content()
        location = re.sub("\s+", " ", re.sub("([^A-Z]|%s)" % state, " ", location[0].text_content(), flags=(re.I | re.M)), flags=re.M).strip().title()
        if location.find(city) == -1: continue
        
        text = p.text_content()
        date = text.split("-", 2)[0].strip()
        last = text.rsplit(" ", 2)[-1].strip().lower()
        img = last == "img"
        pic = last == "pic"

        apartments.append({
            "date": date ,
            "img": img ,
            "location": location,
            "pic": pic ,
            "title": title,
            "url": url
        })


print "Found %s apartments" % len(apartments)
scraperwiki.sqlite.save(unique_keys=['url'], data=apartments)
