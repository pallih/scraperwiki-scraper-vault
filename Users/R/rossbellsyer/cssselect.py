import scraperwiki
import csv

# Restaurant Reviews

html = scraperwiki.scrape("http://www.menus.co.nz/restaurants/?f=New+Zealand")

import lxml.html
root = lxml.html.fromstring(html)

#busname

for topel in root.cssselect("div.vcardpad"):
#for topel in root.cssselect("div.rating"):    

    #print topel.tag, topel.attrib
    name = topel.attrib["title"]
    print name
        
    for el in topel:
        #print el.tag, el.attrib
        rate = el.cssselect("div.rating")
        
        print rate
        for sp in rate:
            #rev = sp.cssselect("span") 
            #reviews = rev.attrib["title"]       
            print sp.tag

        #rating = rate.text
        #reviews = el.tail
        #print rating

    #numrev = root.cssselect("div.rating span")[0]
    #numreview = nametail
    #rate = root.cssselect("div.rating span")
    #rating=rate.attrib["title"]

#record = {"name" : name}
    #scraperwiki.sqlite.save(["name"], name)


#get rating
#for rating in root.cssselect("div.rating span"):

#    numreviews = rating.tail 
#    rating = rating.attrib["title"]
    

#get numreviews
#for numreviews in root.cssselect("div.rating span"):

    #numreviews = numreviews.tail


    #record={"name": name, "rating": rating, "numreview": numreviews}

    #record={"name": name, "numreviews": numreview}
    #scraperwiki.sqlite.save(["name"],record)

