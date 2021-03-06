import scraperwiki
import lxml.etree
import lxml.html
import time
from itertools import groupby

#init
baseURL      = "http://www.freelancer.com/d/skills/all/"
maxPages     = 1000 # unclear about max.
listOfSkills = []
idCounter    = 0
scraperwiki.sqlite.execute("drop table if exists swdata")

#scrape pages and collect all skills
for pageNumber in range(maxPages):
    pageNumber = pageNumber + 1
    url = baseURL + str(pageNumber) + "/"
    print url
    
    html = scraperwiki.scrape(url)     # Load HTML from URL
    root = lxml.html.fromstring(html)  # Extract parsable code from web page

    for item in root.cssselect("li.ns_result p.bold"):
        for skill in item.cssselect("a"):
            listOfSkills.append(skill.text)

print len(listOfSkills), " skills in total."

# count number of users with this skill (for prioritization)
listOfSkills.sort()
countOfSkills = [len(list(group)) for key, group in groupby(listOfSkills)]

# gets rid of duplicates by turning list into a set and back
listOfSkills = list(set(listOfSkills))
#listOfSkills.sort()

for skill in listOfSkills:
    record = {}      
    record["id"] = idCounter
    record["skill"]=skill.replace('-', ' ')
    record["occurrences"]=countOfSkills[idCounter]
    scraperwiki.sqlite.save(["id"], record)
    idCounter=idCounter+1

print idCounter, " skills scraped."import scraperwiki
import lxml.etree
import lxml.html
import time
from itertools import groupby

#init
baseURL      = "http://www.freelancer.com/d/skills/all/"
maxPages     = 1000 # unclear about max.
listOfSkills = []
idCounter    = 0
scraperwiki.sqlite.execute("drop table if exists swdata")

#scrape pages and collect all skills
for pageNumber in range(maxPages):
    pageNumber = pageNumber + 1
    url = baseURL + str(pageNumber) + "/"
    print url
    
    html = scraperwiki.scrape(url)     # Load HTML from URL
    root = lxml.html.fromstring(html)  # Extract parsable code from web page

    for item in root.cssselect("li.ns_result p.bold"):
        for skill in item.cssselect("a"):
            listOfSkills.append(skill.text)

print len(listOfSkills), " skills in total."

# count number of users with this skill (for prioritization)
listOfSkills.sort()
countOfSkills = [len(list(group)) for key, group in groupby(listOfSkills)]

# gets rid of duplicates by turning list into a set and back
listOfSkills = list(set(listOfSkills))
#listOfSkills.sort()

for skill in listOfSkills:
    record = {}      
    record["id"] = idCounter
    record["skill"]=skill.replace('-', ' ')
    record["occurrences"]=countOfSkills[idCounter]
    scraperwiki.sqlite.save(["id"], record)
    idCounter=idCounter+1

print idCounter, " skills scraped."