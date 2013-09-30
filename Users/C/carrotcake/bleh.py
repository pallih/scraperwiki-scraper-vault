import scraperwiki  
import lxml.html 
        
html = scraperwiki.scrape("http://www.reddit.com/r/wheredidthesodago/?count=25&after=t3_15ycl9")
root = lxml.html.fromstring(html)

for el in root.cssselect("p.title > a"):    
    if el.attrib['href'].find(".com") > 0:
        data = {
            'title' : el.text,
            'url' : el.attrib['href']
        }
        #print el.text, el.attrib['href']
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
import scraperwiki  
import lxml.html 
        
html = scraperwiki.scrape("http://www.reddit.com/r/wheredidthesodago/?count=25&after=t3_15ycl9")
root = lxml.html.fromstring(html)

for el in root.cssselect("p.title > a"):    
    if el.attrib['href'].find(".com") > 0:
        data = {
            'title' : el.text,
            'url' : el.attrib['href']
        }
        #print el.text, el.attrib['href']
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
