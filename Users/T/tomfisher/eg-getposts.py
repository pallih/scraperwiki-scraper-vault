import scraperwiki
import lxml.html
import lxml.etree
scraperwiki.sqlite.attach("eg-collectposttitles", "src")

superdictionary = {}
superlist       = []
forumpostid = 0



def save(): #saves all the data stored in superdictionary into SQLite db
    for subdictionary in superdictionary:
        superlist.append(superdictionary[subdictionary])
    scraperwiki.sqlite.save(["link"], superlist)
    return



def getposts( url ): #this function collects all posts from the forum post passed to it in the URL and stores them in the superdictionary 
    html = scraperwiki.scrape(url) # bind the relevant url
    root = lxml.html.fromstring(html) # turn it into an lxml object
    global forumpostid
    forumpostid = forumpostid + 1 
    #print "________________________________NEW URL___________________________________________"
    posttitle = root.cssselect("h2.title.icon") #select the post title
    for el in posttitle:
        title = el.text_content() #save post title
    #print title
    postdate = root.cssselect("span.postdate.old") #select the post date
    for el in postdate:
        date = el.text_content() #save post date
    #print date
    postpages = root.cssselect("div.postpagestats") #select total number of replies
    for el in postpages:
        pages = el.text_content() 
    list_of_replies = pages.split(" ")
    total_replies = int(list_of_replies[5]) #save number of replies
    #print "The total number of replies is " + str(total_replies)

    superdictionary[forumpostid] = {"title":title, "date":date, "no of replies":total_replies, "ID":forumpostid, "link":url} #save basic info to superdictionary

    if total_replies <= 15: #determine how many pages the post has and call another function to actually save the posts
        #print "This post lives on one page only"
        getpage(url)    
    elif total_replies <= 30:
        #print "This post lives on two pages"
        getpage(url, 2)
    elif total_replies <=45:
        #print "This post lives on three pages"
        getpage(url, 3)
    elif total_replies <=60:
        #print "This post lives on four pages"
        getpage(url, 4)
    elif total_replies <=75:
        #print "This post lives on five pages"
        getpage(url, 5)
    elif total_replies <=90:
        #print "This post lives on six pages"
        getpage(url, 6)
    elif total_replies <=105:
        #print "This post lives on seven pages"
        getpage(url, 7)
    else:
        #print "This post lives on too many pages"
    
    #a = "0123"
    #b = "yomama"

    #scraperwiki.sqlite.save(unique_keys=["link"], data={"link":url, "title":title, "date":date, "replies":total_replies, a:b})
    
    
    #getpage(url)


     return

def getpage( url, no_of_pages = 1 ): #this function collects the replies on a specific post with a given url and a certain number of pages
    html = scraperwiki.scrape(url) # bind the relevant url
    root = lxml.html.fromstring(html) # turn it into an lxml object
    a = 0 
    for el in root.cssselect("blockquote.postcontent.restore"):
        children = el.getchildren()
        answerno = "post number " + str(a)
        superdictionary[forumpostid].update({answerno:el.text_content()})
        #print el.text_content()
        #print url
        #scraperwiki.sqlite.update(unique_keys=["link"], data={"link":url, "test":url})
        a = a+1
    if no_of_pages > 1:
        url_base = url.replace(' ', '')[:-5]
        for i in range (2, no_of_pages + 1):
            page_url = url_base + "-" + str(i) + ".html"
            html = scraperwiki.scrape(page_url) # bind the relevant url
            root = lxml.html.fromstring(html) # turn it into an lxml object
            for el in root.cssselect("blockquote.postcontent.restore"):
                children = el.getchildren()
                answerno = "post number " + str(a)
                superdictionary[forumpostid].update({answerno:el.text_content()})
                a = a+1
    return


#links = scraperwiki.sqlite.select("link from src.swdata limit 100 offset 0")
links = scraperwiki.sqlite.select("link from src.swdata")


for i, link in enumerate(links): #change links to appropriate format
    stringlink = str(link)
    stringlink = stringlink.replace(' ', '')[:-2]
    stringlink = stringlink[11:]
    links[i] = stringlink


nidsdone = scraperwiki.sqlite.get_var("nidsdone", 0)

for i, link in enumerate(links):
    try:
        #print "i is: " + str(i)
        if i < nidsdone:
            print "Skipping link number " + str(i)
            continue
        #if ( i%10 == 0 and i > 1):
        #    save()
        #    print "---------------SAVED--------------"
        print "Processing link number " + str(i) + " of " + str(len(links))
        getposts(link)
        #save()
        scraperwiki.sqlite.save_var("nidsdone", i)
    except scraperwiki.CPUTimeExceededError:
        scraperwiki.sqlite.save_var("nidsdone", i)
        save()
        print "CPU runtime exceeded. Progress saved. Aborting now..."
        break
    except Exception as e:
        scraperwiki.sqlite.save_var("nidsdone", i)
        save()
        print "Progress has been saved but some other error occured, namely..."
        print str(type(e))
        print str(e)
save()

