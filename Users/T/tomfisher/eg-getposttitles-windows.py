import scraperwiki
import lxml.html

html = scraperwiki.scrape('http://www.edugeek.net/forums/windows/index1.html')

root = lxml.html.fromstring(html) # turn our HTML into an lxml object
print "Hello!"
print "hello world!"

error = 0
def GetPostTitles( url ):
    a = 1 

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object

    for el in root.cssselect("h3.threadtitle a"):
        if str(el.text) == "None" :
            continue
        #print "----------------------------"
        #print "This element's text is: " + str(el.text)
        #print "This element's href is: " + str(el.attrib['href'])
        scraperwiki.sqlite.save(unique_keys=["title"], data={"title":el.text, "link":el.attrib['href'], "ID":a})             
        a +=1
    return

b = 1
while (b < 10):
    print 'The count is:', b
    string = "http://www.edugeek.net/forums/mis-systems/index"
    #print b
    urls = string + str(b) + ".html"
    #print urls
    b = b + 1
    try:
        GetPostTitles(urls)
    except:
        error = error + 1
        pass

print "Number of total errors: " + str(error)


GetPostTitles("http://www.edugeek.net/forums/windows/index1.html")

