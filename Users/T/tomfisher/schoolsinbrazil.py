import scraperwiki
import lxml.html
import re

a = 0
b = 0
print "Welcome! Script starting now..."

def getschooldata( str ): #this function retrieves data on one particular school passed as a url and then stores it in the SQLite db
    html = scraperwiki.scrape(str)
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    fullsite = "not found"
    global b
    b = b+1
    print "Working on school number", b

    h1s = root.cssselect('h1') #get the name of school
    for h1 in h1s:
        name = h1.text

    el = root.cssselect("div#tabs-icons-5 strong")[0] #get the minimum price
    minprice = el.text

    el = root.cssselect("div#tabs-icons-5 strong")[1] #get the maximum price
    if len(root.cssselect("div#tabs-icons-5 strong")) > 3:
        maxprice = el.text
    else:
        maxprice = "not given"
        yearoffeereference = el.text  

    el = root.cssselect("div#tabs-icons-5 strong")[2] #get the year the price was last updated
    
    if len(root.cssselect("div#tabs-icons-5 strong")) > 3:
        yearoffeereference= el.text
    else:
        numberofstudents= el.text
        studentsreferencetext = el.getparent().text
        studentsreferencenumber = re.sub("[^0-9]", "", studentsreferencetext)



    if len(root.cssselect("div#tabs-icons-5 strong")) > 3: #only execute this code if the info is actually available
        el = root.cssselect("div#tabs-icons-5 strong")[3] #get the number of students and the year in which the number was recorded
        numberofstudents= el.text
        studentsreferencetext = el.getparent().text
        studentsreferencenumber = re.sub("[^0-9]", "", studentsreferencetext)
    else:
        print "Here's one that doesn't fit the bill...   "
        global a    
        a += 1
        #numberofstudents= "not found"
        #studentsreferencenumber = "not found"

    listoftrs = root.cssselect("div#tabs-icons-2 tr") #get the city & website
    global numberofcampuses
    global fullsite
    numberofcampuses = 0
    for eachtr in listoftrs:
        children = eachtr.getchildren()
        if children[0].text is not None and "Cidade" in children[0].text: 
            numberofcampuses += 1 
            state = children[1].text
        if children[0].text is not None and "Site" in children[0].text: 
            website = children[1].getchildren()
            fullsite = website[0].text


    #The command below saves all the collected info in the SQLite database
    scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, "min price":minprice, "max price":maxprice, "year of refernce for fees":yearoffeereference, "total students":numberofstudents, "year of reference for students":studentsreferencenumber, "number of campuses":numberofcampuses, "State":state, "website":fullsite})
    return


scraperwiki.sqlite.attach("fulllist", "src")


list = scraperwiki.sqlite.select("link from src.swdata limit 40 offset 380")


for link in list:
    stringlink = str(link)
    stringlink = stringlink.replace(' ', '')[:-2]
    stringlink = stringlink[11:]
    getschooldata(stringlink)

print "Number that didn't fit the bill: ", a
import scraperwiki
import lxml.html
import re

a = 0
b = 0
print "Welcome! Script starting now..."

def getschooldata( str ): #this function retrieves data on one particular school passed as a url and then stores it in the SQLite db
    html = scraperwiki.scrape(str)
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    fullsite = "not found"
    global b
    b = b+1
    print "Working on school number", b

    h1s = root.cssselect('h1') #get the name of school
    for h1 in h1s:
        name = h1.text

    el = root.cssselect("div#tabs-icons-5 strong")[0] #get the minimum price
    minprice = el.text

    el = root.cssselect("div#tabs-icons-5 strong")[1] #get the maximum price
    if len(root.cssselect("div#tabs-icons-5 strong")) > 3:
        maxprice = el.text
    else:
        maxprice = "not given"
        yearoffeereference = el.text  

    el = root.cssselect("div#tabs-icons-5 strong")[2] #get the year the price was last updated
    
    if len(root.cssselect("div#tabs-icons-5 strong")) > 3:
        yearoffeereference= el.text
    else:
        numberofstudents= el.text
        studentsreferencetext = el.getparent().text
        studentsreferencenumber = re.sub("[^0-9]", "", studentsreferencetext)



    if len(root.cssselect("div#tabs-icons-5 strong")) > 3: #only execute this code if the info is actually available
        el = root.cssselect("div#tabs-icons-5 strong")[3] #get the number of students and the year in which the number was recorded
        numberofstudents= el.text
        studentsreferencetext = el.getparent().text
        studentsreferencenumber = re.sub("[^0-9]", "", studentsreferencetext)
    else:
        print "Here's one that doesn't fit the bill...   "
        global a    
        a += 1
        #numberofstudents= "not found"
        #studentsreferencenumber = "not found"

    listoftrs = root.cssselect("div#tabs-icons-2 tr") #get the city & website
    global numberofcampuses
    global fullsite
    numberofcampuses = 0
    for eachtr in listoftrs:
        children = eachtr.getchildren()
        if children[0].text is not None and "Cidade" in children[0].text: 
            numberofcampuses += 1 
            state = children[1].text
        if children[0].text is not None and "Site" in children[0].text: 
            website = children[1].getchildren()
            fullsite = website[0].text


    #The command below saves all the collected info in the SQLite database
    scraperwiki.sqlite.save(unique_keys=["name"], data={"name":name, "min price":minprice, "max price":maxprice, "year of refernce for fees":yearoffeereference, "total students":numberofstudents, "year of reference for students":studentsreferencenumber, "number of campuses":numberofcampuses, "State":state, "website":fullsite})
    return


scraperwiki.sqlite.attach("fulllist", "src")


list = scraperwiki.sqlite.select("link from src.swdata limit 40 offset 380")


for link in list:
    stringlink = str(link)
    stringlink = stringlink.replace(' ', '')[:-2]
    stringlink = stringlink[11:]
    getschooldata(stringlink)

print "Number that didn't fit the bill: ", a
