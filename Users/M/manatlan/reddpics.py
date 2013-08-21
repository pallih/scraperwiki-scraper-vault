import scraperwiki  
import lxml.html 
        
root = lxml.html.fromstring( scraperwiki.scrape("http://reddpics.com") )

for i in root.cssselect("div#content div ul li em a img"):    
    
    data = {
            'url' : i.getparent().attrib['href'],
            'mini' : "http://reddpics.com"+i.attrib['src'],
            'title' : i.attrib['alt'],
            'age' : i.getparent().getparent().getparent().attrib['created'],
        }
    #print data
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)

