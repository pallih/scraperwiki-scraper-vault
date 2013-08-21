import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.mirror.co.uk/")
root = lxml.html.fromstring(html)

for i in root.cssselect(".headline-teaser li a"): 
    head = i.text   
    print i.text


    if head is not None:
            data = {
            'Headline' :head,
      
                }
            print data
            scraperwiki.sqlite.save(unique_keys=['Headline'], data=data)  


