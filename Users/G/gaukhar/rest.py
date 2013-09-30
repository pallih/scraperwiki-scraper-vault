import scraperwiki
import lxml.html  

# Blank Python

html = scraperwiki.scrape("http://www.timeout.com/london/search/?tag_id=4256&submit=1&pageSize=50")

root = lxml.html.fromstring(html)


for image in root.cssselect("img.photo"):
    
   
        
    
    
    print image.get('src')
import scraperwiki
import lxml.html  

# Blank Python

html = scraperwiki.scrape("http://www.timeout.com/london/search/?tag_id=4256&submit=1&pageSize=50")

root = lxml.html.fromstring(html)


for image in root.cssselect("img.photo"):
    
   
        
    
    
    print image.get('src')
