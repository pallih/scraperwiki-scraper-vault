'''
Scrape http://www.ushospital.info to get all hospital categories per state
'''

import scraperwiki
import lxml.html
import re

# extract info from all (incl nested) li elements in specified ul element
def extractInfo(ulElement, category, state):
    print "... extracting info from ul"
    liCount = 0
    items = []
    for liChild in ulElement.iter("li"):
        liCount += 1
        item = extractItem(liChild, category, state)
        if (item != {}):
            "... appending hospital"
            items.append(item)
    print "liCount: ", liCount
    return items
    
# extract hospital info from specified li element, return as dict
# Hospital format of /Category/State page, e.g. http://www.ushospital.info/Animal/Arizona.htm
def extractItem(element, category, state):
    #print "... extracting info from li"
    item = {}
    item_text = element.text_content()
    # print "now parsing fields from: ", item_text

    p1 = re.compile("(?P<name>[^-]+)-(?P<city>[^,]+),(?P<state>[^,]+)$")
    case1 = p1.match(item_text)

    p2 = re.compile("(?P<name>[^-]+)-(?P<city>[^,]+),(?P<county>[^,]+), (?P<state>[^,]+)$")
    case2 = p2.match(item_text)
    
    if case1:
        item = {
            "hospitalName": "",
            "hospitalURL": "",
            "hospitalCity": "",
            "hospitalCounty": "",
            "hospitalState": state,
            "hospitalCategory": category,
        } 

        print "matched case1: ", case1.group('name'), case1.group('city'), case1.group('state')
        item["hospitalName"] = " ".join(case1.group('name').split())
        item["hospitalCity"] = " ".join(case1.group('city').split())
        item["hospitalState"] = " ".join(case1.group('state').split())

        if (len(element.findall("a")) > 0 ):
            item["hospitalURL"] = element.findall("a")[0].get("href")
    elif case2:
        item = {
            "hospitalName": "",
            "hospitalURL": "",
            "hospitalCity": "",
            "hospitalCounty": "",
            "hospitalState": state,
            "hospitalCategory": category,
        } 

        print "matched case2: ", case2.group('name'), case2.group('city'), case2.group('county'), case2.group('state')
        item["hospitalName"] = " ".join(case2.group('name').split())
        item["hospitalCity"] = " ".join(case2.group('city').split())
        item["hospitalCounty"] = " ".join(case2.group('county').split())
        item["hospitalState"] = " ".join(case2.group('state').split())

        if (len(element.findall("a")) > 0 ):
            item["hospitalURL"] = element.findall("a")[0].get("href")
    else:
        print "failed to parse text: ", item_text
    return item


##### MAIN #####

URLBase = "http://www.ushospital.info/"
URLExtension = ".htm"

states = ["Arizona", "Illinois", "Texas"]
#states = ["Texas"]

categories = {
    "Arizona": ["Animal", "Cancer", "Childrens", "Military", "Organizations", "Psychiatric", "Rehabilitation", "Teaching"],
    "Illinois": ["Animal", "Cancer", "Childrens", "Military", "Organizations", "Psychiatric", "Rehabilitation", "Teaching"],
    "Texas": ["Animal", "Cancer", "Childrens", "Eye-Optical", "Heart", "Military", "Organizations", "Psychiatric", "Rehabilitation", "Teaching"]
}
#categories = {"Texas": ["Animal"]}

hospitals = []

for state in states:
    for category in categories[state]:
        url =  URLBase + category + "/" +state + URLExtension
        print "... now scraping: ", url

        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        body = root[1]

        contentTable = body.get_element_by_id("AutoNumber5")[0][4]
        
        for child in contentTable:
            if child.tag == 'ul':
                scrapedHospitals = extractInfo(child, category,state)
                print "len(scrapedHospitals): ", len(scrapedHospitals)
                hospitals += scrapedHospitals

'''
category = "Animal"
state = "Arizona"
url =  URLBase + category + "/" +state + URLExtension
'''


# print first n records
n = min(5, len(hospitals))
print "len(hospitals): ", len(hospitals)
for j in range(n):
    print hospitals[j]


# save name, state, cat, etc in 1 table

# save scraped data to scraperwiki
my_keys = ["hospitalName", "hospitalURL", "hospitalCity", "hospitalCounty", "hospitalCategory"]
scraperwiki.sqlite.save(unique_keys=my_keys, data=hospitals)

