'''
scrape surgeon's additional data from College of Surgeons' profile page
'''

import scraperwiki
import lxml.html
import re

def tidy(string):
    return " ".join(string.split())

def extractProfileInfo(contentTable, url):    
    item = {
        "itemURL": "",
        "itemName": "",
    }
    
    item["itemURL"] = url
    item["itemName"] = contentTable.find_class("subheading")[0].text_content()
    
    
    tableText = contentTable.text_content()
    print "now parsing fields from: ", tableText

    p1 = re.compile("Phone\s+Number:\s+(?P<phoneNumber>\(\d{3,3}\)\s[\d-]+)")
    case1 = p1.search(tableText)
    if case1:
        #print "matched case1: "
        print "matched case1: ", case1.group('phoneNumber')
        item["itemPhoneNumber"] = case1.group('phoneNumber')
    
    #p2 = re.compile("Hospital\s+Appointment\(s\):\s*(?P<hospitals>.*)\s*Academic\s+Appointment\(s\)")
    p2 = re.compile("Hospital\s+Appointment\(s\):\s*(?P<hospitals>.*)Appointment\(s\):", re.DOTALL)
    case2 = p2.search(tableText)
    print case2
    if case2:
        #print "matched case2: "
        print "matched case2: ", case2.group('hospitals')
        item["itemHospitals"] = tidy(case2.group('hospitals'))
    
    return item
    


##### MAIN #####

# http://www.reuters.com/search?blob=DePuy+orthopedics

URLs = [
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=40302423164",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=20319208322",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=60298604906",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=00308028740",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=70311786807",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=80313892318",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=70308789987",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=30299367023",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=00305004660",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=00313026420",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=80300838928"
]

URL = "http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=00308028740"
URLs = [URL]
profiles= []

for url in URLs:
    print "... now scraping: ", url
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    body = root[1]
    
    contentTable = body.get_element_by_id("mainContent")[0]
    scrapedProfile = extractProfileInfo(contentTable, url)
    profiles.append(scrapedProfile)

print profiles

# print first n records
"""
n = min(5, len(newsItems))
print "len(newsItems): ", len(newsItems)
for j in range(n):
    print newsItems[j]
"""
# save scraped data to scraperwiki
#my_keys = ["itemURL", "itemHeadline", "itemSearchBlurb", "itemTimestamp"]
#scraperwiki.sqlite.save(unique_keys=my_keys, data=newsItems)

'''
scrape surgeon's additional data from College of Surgeons' profile page
'''

import scraperwiki
import lxml.html
import re

def tidy(string):
    return " ".join(string.split())

def extractProfileInfo(contentTable, url):    
    item = {
        "itemURL": "",
        "itemName": "",
    }
    
    item["itemURL"] = url
    item["itemName"] = contentTable.find_class("subheading")[0].text_content()
    
    
    tableText = contentTable.text_content()
    print "now parsing fields from: ", tableText

    p1 = re.compile("Phone\s+Number:\s+(?P<phoneNumber>\(\d{3,3}\)\s[\d-]+)")
    case1 = p1.search(tableText)
    if case1:
        #print "matched case1: "
        print "matched case1: ", case1.group('phoneNumber')
        item["itemPhoneNumber"] = case1.group('phoneNumber')
    
    #p2 = re.compile("Hospital\s+Appointment\(s\):\s*(?P<hospitals>.*)\s*Academic\s+Appointment\(s\)")
    p2 = re.compile("Hospital\s+Appointment\(s\):\s*(?P<hospitals>.*)Appointment\(s\):", re.DOTALL)
    case2 = p2.search(tableText)
    print case2
    if case2:
        #print "matched case2: "
        print "matched case2: ", case2.group('hospitals')
        item["itemHospitals"] = tidy(case2.group('hospitals'))
    
    return item
    


##### MAIN #####

# http://www.reuters.com/search?blob=DePuy+orthopedics

URLs = [
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=40302423164",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=20319208322",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=60298604906",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=00308028740",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=70311786807",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=80313892318",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=70308789987",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=30299367023",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=00305004660",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=00313026420",
"http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=80300838928"
]

URL = "http://web2.facs.org/acsdir/public/DetailMember.cfm?CHKDGTS=00308028740"
URLs = [URL]
profiles= []

for url in URLs:
    print "... now scraping: ", url
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    body = root[1]
    
    contentTable = body.get_element_by_id("mainContent")[0]
    scrapedProfile = extractProfileInfo(contentTable, url)
    profiles.append(scrapedProfile)

print profiles

# print first n records
"""
n = min(5, len(newsItems))
print "len(newsItems): ", len(newsItems)
for j in range(n):
    print newsItems[j]
"""
# save scraped data to scraperwiki
#my_keys = ["itemURL", "itemHeadline", "itemSearchBlurb", "itemTimestamp"]
#scraperwiki.sqlite.save(unique_keys=my_keys, data=newsItems)

