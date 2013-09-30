import scraperwiki
import lxml.html    
import dateutil.parser

# Blank Python

x=467331

while x<498331:
    x=x+1000
    url = "https://www.fanduel.com/e/User/_%d" % (x)
    print url
    try:
        html = scraperwiki.scrape(url)  
        root = lxml.html.fromstring(html)
        
        data = {
            'userid' : x,
            'username' : root.cssselect(".column-10 .left h1")[0].text_content(),
            'acq_date' : dateutil.parser.parse(root.cssselect(".column-10 .left p")[0].text_content().replace("Member since ","")).date()
        }
        
        scraperwiki.sqlite.save(unique_keys=['userid'], data=data)
    except:
        print "error"

scraperwiki.sqlite.select("* from swdata")
import scraperwiki
import lxml.html    
import dateutil.parser

# Blank Python

x=518331

while x<538331:
    x=x+1000
    url = "https://www.fanduel.com/e/User/_%d" % (x)
    print url
    try:
        html = scraperwiki.scrape(url)  
        root = lxml.html.fromstring(html)
        
        data = {
            'userid' : x,
            'username' : root.cssselect(".column-10 .left h1")[0].text_content(),
            'acq_date' : root.cssselect(".column-10 .left p")[0].text_content().replace("Member since ",""))
        }
        
        scraperwiki.sqlite.save(unique_keys=['userid'], data=data)
    except:
        print "error"

scraperwiki.sqlite.select("* from swdata")
