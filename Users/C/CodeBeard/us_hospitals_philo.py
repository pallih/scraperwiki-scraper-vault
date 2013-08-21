import scraperwiki
import lxml.html
#Required Nodes look like this
#<li><a>name</a><a>city/town</a><a>county</a>state</li>
#or with a sub UL. Want all LI items that conform to structure.
#<li><a>name</a><a>city/town</a><a>county</a>state<ul><li><a>name</a><a>city/town</a><a>county</a>state</li>...</ul></li>

#state = "TX"
#url = "http://www.ushospital.info/Texas.htm"
#state = "IL"
#url = "http://www.ushospital.info/Illinois.htm"
state = "AZ"
url = "http://www.ushospital.info/Arizona.htm"

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

lenDict = {}

# extract info from all (incl nested) li elements in specified ul element
def extractInfo(ulElement,state):
    print "... extracting info from ul"
    liCount = 0
    items = []
    for liChild in ulElement.iter("li"):
        liCount += 1
        item = extractItem(liChild,state)
        if (item != {}):
            "... appending hospital"
            items.append(item)
    print "liCount: ", liCount
    return items

def tidy(text):
    return text.strip('\l\r\n\t\f').replace('\t','').replace('\r','').replace('\n','')

# extract hospital info from specified li element, return as dict
# TODO if case for different number of "a" tags.
# distribution of number of a tags: {1: 31, 2: 49, 4: 11, 6: 2}
def extractItem(element,state):
    #print "... extracting info from li"
    item = {}
    if len(element.findall("a")) == 3:
        #print "... extracting hospital info"
        if element[0].tag == "a":
            item["hospitalName"] = tidy(element[0].text)
            item["hospitalURL"] = tidy(element[0].get("href"))
            # explicitly blank to create key in dataDict
            item["hospitalCity"] = ""
        if element[1].tag == "a":
            item["hospitalCity"] = tidy(element[1].text)
        if element[2].tag == "a":
            item["hospitalCounty"] = tidy(element[2].text)
        item["State"] = state
    else:
        #TODO
        # print len(element.findall("a"))
        # DEBUG: track frequency of "a" counts
        if len(element.findall("a")) in lenDict:
            lenDict[len(element.findall("a"))] += 1
        else:
            lenDict[len(element.findall("a"))] = 1
    return item
    


##### MAIN #####

body = root[1]
contentTable = body[3][0][4]

i = 0
hospitals= []
for child in contentTable:
    if child.tag == 'ul':
        scrapedHospitals = extractInfo(child,state)
        print "len(scrapedHospitals): ", len(scrapedHospitals)
        hospitals += scrapedHospitals
        i += 1

# print first n records
n = 5
print "len(hospitals): ", len(hospitals)
for j in range(n):
    print hospitals[j]

# save scraped data to scraperwiki
my_keys = ["hospitalName", "hospitalURL", "hospitalCity", "hospitalCounty"]
scraperwiki.sqlite.save(unique_keys=my_keys, data=hospitals)

