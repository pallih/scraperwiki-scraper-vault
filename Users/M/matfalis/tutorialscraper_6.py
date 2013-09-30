import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.pikachu.cz/main/") 
root = lxml.html.fromstring(html) 
for tr in root.cssselect("div[class=articles] h3"):
    if 1==1:    
        data = { 
        'heading' : tr.text_content(), 
        } 
        scraperwiki.sqlite.save(unique_keys=['heading'], data=data)
        print data
import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.pikachu.cz/main/") 
root = lxml.html.fromstring(html) 
for tr in root.cssselect("div[class=articles] h3"):
    if 1==1:    
        data = { 
        'heading' : tr.text_content(), 
        } 
        scraperwiki.sqlite.save(unique_keys=['heading'], data=data)
        print data
