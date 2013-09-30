import scraperwiki           
import lxml.html
html = scraperwiki.scrape("https://www.washington.edu/students/timeschd/SPR2013/geog.html")
root = lxml.html.fromstring(html)



for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td b") 
    

#if len(tds)==1:
    data = {  
#tds[0] = Course name/#/desc
#tds[1] = credit type
#tds[2] = indcation of prerequisites
        'title' : tds[0].text_content()
        #'hello' : tds[2].text_content()
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['title'], data=data)