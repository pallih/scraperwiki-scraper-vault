import scraperwiki  
import lxml.html 
        
html = scraperwiki.scrape("http://reddit.com/r/WTF+pics")
root = lxml.html.fromstring(html)

for el in root.cssselect("p.title > a"):    
    if el.attrib['href'].find("imgur") > 0:
        data = {
            'title' : el.text,
            'url' : el.attrib['href']
        }
        #print el.text, el.attrib['href']
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
