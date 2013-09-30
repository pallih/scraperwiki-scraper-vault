# Blank Python

import scraperwiki
import lxml.html
i=1
record={}
for i in range(1,11):
    html = scraperwiki.scrape("http://haverfordpafootball.stackvarsity.com/photos/Default.asp?page="+str(i))


    root = lxml.html.fromstring(html)
    divs=root.cssselect(" .album_collection img")
    print 'len of divs ',len(divs)
    for div in divs:
    
    #for el in root.cssselect("div.collection_wrapper img "):
    #print lxml.html.tostring(el)
        record["url"]= div.attrib['src']
        imageName=record["url"].find(".jpg")
        print imageName
       # print div.find("scr")
        print 'Image url',record["url"] 
         

        #scraperwiki.sqlite.save(["url"], record)
    print 'len of record ',i  