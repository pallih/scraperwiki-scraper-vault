

import scraperwiki
import lxml.html
i,x,n=0,0,1
record={}
for j in range(1,600):
    try :
        html = scraperwiki.scrape("http://haverfordpafootball.stackvarsity.com/photos/Default.asp?page="+str(j))
        root = lxml.html.fromstring(html)
        n=n+1
        for el in root.cssselect(".album_collection img "):
            record["url"]= el.attrib['src']
            scraperwiki.sqlite.save(["url"], record)
            print el.attrib['src']
    except:
        print n
        break