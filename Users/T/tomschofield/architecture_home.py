import scraperwiki
import lxml.html
import string

#get html object
html = scraperwiki.scrape("http://www.ncl.ac.uk/apl/")

root = lxml.html.fromstring(html)
#to keep track of where we are
myVar=0
tableCount=0
level2Counter=0
#python for loops need a colon and then indentation to work! 
for el in lxml.html.iterlinks(html):
    #el[2] is the 3rd element returned in each link object list by interlinks
    print "top level ",el[2]
   #iterate through the links of this one
    myVar+=1
    level2Counter+=1
    explode1 = el[2].split(".")
    #test its a real link
    try:
         #get a new html object for each link
        html1 = scraperwiki.scrape(el[2])
        level3counter=0
        for el2 in lxml.html.iterlinks(html1):
        #blow it apart by the full stops
            print "next level at ", level2Counter, " which is this toplevel domain ", el[2]," ",el2[2]
            
            explode = el2[2].split(".")
            if explode[len(explode)-1]=="gif" or explode[len(explode)-1]=="jpg" or explode[len(explode)-1]=="jpeg" or explode[len(explode)-1]=="png":
                #save to the sql table - the syntax is a bit confusing but the "link" acts as a the key in the key value pair and then all following data is associated with that key
                scraperwiki.sqlite.save(unique_keys=["link"], data={"link":el2[2], "linkCount":tableCount, "fromSite":el[2], "topLevelCount":myVar})
                tableCount+=1
            else :
                html2 = scraperwiki.scrape(el2[2])
                for el3 in lxml.html.iterlinks(html2):
                    print "third level at ", level2Counter, " which is this  second level domain ", el2[2]," ",el3[2]

    except:
        print "found javascript"