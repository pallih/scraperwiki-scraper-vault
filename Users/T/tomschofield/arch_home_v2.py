import scraperwiki
import lxml.html
import string
links =[]
levels =[]
baseURLs=[]

#get html object
url = "http://www.ncl.ac.uk/apl/about/news/item/new-masters-programme-ma-architectural-design-research-starts-sept"
html = scraperwiki.scrape(url)

root = lxml.html.fromstring(html)
#to keep track of where we are
myVar=0
tableCount=0
#python for loops need a colon and then indentation to work! 
#counter for each individual domain on each level - reset at each level
domainID=0

#GET LINKS FROM FIRST PAGE
for el in lxml.html.iterlinks(html):
    
    #el[2] is the 3rd element returned in each link object list by interlinks
    
    #iterate through the links of this first page (the architecture home page)
    explode = el[2].split(".")
    #test its a real link
    
    try:
        
        #get images from this page
        if explode[len(explode)-1]=="gif" or explode[len(explode)-1]=="jpg" or explode[len(explode)-1]=="jpeg" or explode[len(explode)-1]=="png":
            #save to sql
            # scraperwiki.sqlite.save(unique_keys=["link"], data={"link":el[2], "linkCount":tableCount, "fromSite":el[2], "topLevelCount":1})
            links.append(el[2])
            levels.append("1")
            baseURLs.append(url)
            #print url
            print "level 1", el[2]
        #or if not, get a new html object for each link
        else:
            
            html1 = scraperwiki.scrape(el[2])
            #GET LINKS FROM SECOND LEVEL PAGES
            
            domainID+=1

            for el2 in lxml.html.iterlinks(html1):
                explode2 = el2[2].split(".")
                
                if explode2[len(explode2)-1]=="gif" or explode2[len(explode2)-1]=="jpg" or explode2[len(explode2)-1]=="jpeg" or explode2[len(explode2)-1]=="png":
                    #scraperwiki.sqlite.save(unique_keys=["link"], data={"link":el2[2], "linkCount":tableCount, "fromSite":el[2], "topLevelCount":2})
                    links.append(el2[2])
                    levels.append("2")
                    baseURLs.append(el[2])
                    #print el[2]
                    
                    print "level 2", el[2], " ", el2[2]
                else:
                    
                    html2 = scraperwiki.scrape(el2[2])
                        #GET LINKS FROM THIRD LEVEL PAGES
                    for el3 in lxml.html.iterlinks(html2):
                        explode3 = el3[2].split(".")
                        if explode3[len(explode3)-1]=="gif" or explode3[len(explode3)-1]=="jpg" or explode3[len(explode3)-1]=="jpeg" or explode3[len(explode3)-1]=="png":
                            #scraperwiki.sqlite.save(unique_keys=["link"], data={"link":el3[2], "linkCount":tableCount, "fromSite":el2[2], "topLevelCount":3})
                            print "level 3",el2[2]," ", el3[2]
                            links.append(el3[2])
                            levels.append("3")
                            baseURLs.append(el2[2])
                            #print el2[2]
    except:
        print "found bad link", el[2]

counter = 0
print "size of links", len(links), "size of levels", len(levels), "size of baseURLs", len(baseURLs)
for li in links:
    try:
        scraperwiki.sqlite.save(unique_keys=["link"], data={"link":counter, "linkCount":li, "fromSite":baseURLs[counter], "topLevelCount":levels[counter]})
        print "printing to file", baseURLs[counter]
        counter+=1
    except:
        print "out of range"import scraperwiki
import lxml.html
import string
links =[]
levels =[]
baseURLs=[]

#get html object
url = "http://www.ncl.ac.uk/apl/about/news/item/new-masters-programme-ma-architectural-design-research-starts-sept"
html = scraperwiki.scrape(url)

root = lxml.html.fromstring(html)
#to keep track of where we are
myVar=0
tableCount=0
#python for loops need a colon and then indentation to work! 
#counter for each individual domain on each level - reset at each level
domainID=0

#GET LINKS FROM FIRST PAGE
for el in lxml.html.iterlinks(html):
    
    #el[2] is the 3rd element returned in each link object list by interlinks
    
    #iterate through the links of this first page (the architecture home page)
    explode = el[2].split(".")
    #test its a real link
    
    try:
        
        #get images from this page
        if explode[len(explode)-1]=="gif" or explode[len(explode)-1]=="jpg" or explode[len(explode)-1]=="jpeg" or explode[len(explode)-1]=="png":
            #save to sql
            # scraperwiki.sqlite.save(unique_keys=["link"], data={"link":el[2], "linkCount":tableCount, "fromSite":el[2], "topLevelCount":1})
            links.append(el[2])
            levels.append("1")
            baseURLs.append(url)
            #print url
            print "level 1", el[2]
        #or if not, get a new html object for each link
        else:
            
            html1 = scraperwiki.scrape(el[2])
            #GET LINKS FROM SECOND LEVEL PAGES
            
            domainID+=1

            for el2 in lxml.html.iterlinks(html1):
                explode2 = el2[2].split(".")
                
                if explode2[len(explode2)-1]=="gif" or explode2[len(explode2)-1]=="jpg" or explode2[len(explode2)-1]=="jpeg" or explode2[len(explode2)-1]=="png":
                    #scraperwiki.sqlite.save(unique_keys=["link"], data={"link":el2[2], "linkCount":tableCount, "fromSite":el[2], "topLevelCount":2})
                    links.append(el2[2])
                    levels.append("2")
                    baseURLs.append(el[2])
                    #print el[2]
                    
                    print "level 2", el[2], " ", el2[2]
                else:
                    
                    html2 = scraperwiki.scrape(el2[2])
                        #GET LINKS FROM THIRD LEVEL PAGES
                    for el3 in lxml.html.iterlinks(html2):
                        explode3 = el3[2].split(".")
                        if explode3[len(explode3)-1]=="gif" or explode3[len(explode3)-1]=="jpg" or explode3[len(explode3)-1]=="jpeg" or explode3[len(explode3)-1]=="png":
                            #scraperwiki.sqlite.save(unique_keys=["link"], data={"link":el3[2], "linkCount":tableCount, "fromSite":el2[2], "topLevelCount":3})
                            print "level 3",el2[2]," ", el3[2]
                            links.append(el3[2])
                            levels.append("3")
                            baseURLs.append(el2[2])
                            #print el2[2]
    except:
        print "found bad link", el[2]

counter = 0
print "size of links", len(links), "size of levels", len(levels), "size of baseURLs", len(baseURLs)
for li in links:
    try:
        scraperwiki.sqlite.save(unique_keys=["link"], data={"link":counter, "linkCount":li, "fromSite":baseURLs[counter], "topLevelCount":levels[counter]})
        print "printing to file", baseURLs[counter]
        counter+=1
    except:
        print "out of range"