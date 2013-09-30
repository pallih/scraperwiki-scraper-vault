#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scraperwiki
import lxml.html
import re
from datetime import datetime

#this could use enum, not sure if scraperwiki supports it
statusDict = \
    {
    "zastavená": 0, #"stopped",
    "v konaní": 1, #"in_progress",
    "zapísaná": 2, #"registered",
    "zamietnutá": 3, #"rejected",
    }

overviewUrl="http://registre.indprop.gov.sk/registre/search.do?value%28register%29=oz&value%28sortorder%29=desc&value%28page%29=1&value%28sortorder%29=desc&value%28search%29=true&value%28sortby%29=datum_prihlasky"
detailUrl = "http://registre.indprop.gov.sk/registre/detail/popup.do?register=oz&puv_id=%d"

def toDate(s):
    try:
        date = datetime.strptime(s, "%Y-%m-%d").date()
    except:
        date = None
    return date
    
def toText(s):
    return s.strip()

def toStatus(s):
    return statusDict.get(s.encode("utf-8"))

def fetchHtml(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    return root

def getMaxId():
    """Get max id from the overview page"""
    root = fetchHtml(overviewUrl)
    rows = root.cssselect("div[class='listItemTitle'] span a")
    max_id = 0
    
    for row in rows:
        m = re.search("puv_id=(\d+)", str(row.attrib['href']))
        id = int(m.group(1))
        max_id = max(max_id, id)
    return max_id

#maps human caption to tuple (db_field, conversion_function)
caption2field = \
    {
    "Znenie OZ / Reprodukcia známky": ("name", toText),
    "Číslo prihlášky": ("application_no", toText),
    "Dátum podania prihlášky": ("date_submitted", toDate),
    "Číslo zápisu": ("registration_no", toText),
    "Dátum zápisu": ("registration_date", toDate),
    "Stav": ("status", toStatus),
    #following two deliberately map to the same field, one is used before
    #trademark is accepted, the other after accepting
    "Meno a adresa majiteľa (-ov)": ("owner_name", toText),
    "Meno a adresa prihlasovateľa (-ov)": ("owner_name", toText),
    "Medzinárodné triedenie tovarov a služieb": ("international_classification", toText),
    "Predpokladaný dátum platnosti ochrannej známky": ("expiration_date", toDate),
    }

# recover after interruptions (e.g., CPUTimeExceededError)
min_id = scraperwiki.sqlite.get_var("min_id")
if not min_id:
    min_id = 1
print "Start or continue from id: ", min_id

max_id = getMaxId()

for id in xrange(min_id, max_id+1):
    try:
        root = fetchHtml(detailUrl % id)
    except:
        #print "Failed to fetch id %d" % id
        continue
    rows = root.cssselect("table tr")
    
    if len(rows) < 1:
        #print "No data for id %d" % id
        continue
    
    dbData = {'id': id}
    for row in rows:
        tds = row.cssselect("td")
        caption = tds[1].text_content().encode("utf-8")
        value = tds[2].text_content()
        
        field_conversion = caption2field.get(caption)
        if field_conversion is None:
            continue #ignored field
        (field, conversion) = field_conversion
        if field:
            dbData[field] = conversion(value)
    
    if len(dbData) > 1: #skip page in case no data for id is returned
        scraperwiki.sqlite.save(unique_keys=['id'], data = dbData)
    scraperwiki.sqlite.save_var("min_id", id+1)

scraperwiki.sqlite.save_var("min_id", 1)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scraperwiki
import lxml.html
import re
from datetime import datetime

#this could use enum, not sure if scraperwiki supports it
statusDict = \
    {
    "zastavená": 0, #"stopped",
    "v konaní": 1, #"in_progress",
    "zapísaná": 2, #"registered",
    "zamietnutá": 3, #"rejected",
    }

overviewUrl="http://registre.indprop.gov.sk/registre/search.do?value%28register%29=oz&value%28sortorder%29=desc&value%28page%29=1&value%28sortorder%29=desc&value%28search%29=true&value%28sortby%29=datum_prihlasky"
detailUrl = "http://registre.indprop.gov.sk/registre/detail/popup.do?register=oz&puv_id=%d"

def toDate(s):
    try:
        date = datetime.strptime(s, "%Y-%m-%d").date()
    except:
        date = None
    return date
    
def toText(s):
    return s.strip()

def toStatus(s):
    return statusDict.get(s.encode("utf-8"))

def fetchHtml(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    return root

def getMaxId():
    """Get max id from the overview page"""
    root = fetchHtml(overviewUrl)
    rows = root.cssselect("div[class='listItemTitle'] span a")
    max_id = 0
    
    for row in rows:
        m = re.search("puv_id=(\d+)", str(row.attrib['href']))
        id = int(m.group(1))
        max_id = max(max_id, id)
    return max_id

#maps human caption to tuple (db_field, conversion_function)
caption2field = \
    {
    "Znenie OZ / Reprodukcia známky": ("name", toText),
    "Číslo prihlášky": ("application_no", toText),
    "Dátum podania prihlášky": ("date_submitted", toDate),
    "Číslo zápisu": ("registration_no", toText),
    "Dátum zápisu": ("registration_date", toDate),
    "Stav": ("status", toStatus),
    #following two deliberately map to the same field, one is used before
    #trademark is accepted, the other after accepting
    "Meno a adresa majiteľa (-ov)": ("owner_name", toText),
    "Meno a adresa prihlasovateľa (-ov)": ("owner_name", toText),
    "Medzinárodné triedenie tovarov a služieb": ("international_classification", toText),
    "Predpokladaný dátum platnosti ochrannej známky": ("expiration_date", toDate),
    }

# recover after interruptions (e.g., CPUTimeExceededError)
min_id = scraperwiki.sqlite.get_var("min_id")
if not min_id:
    min_id = 1
print "Start or continue from id: ", min_id

max_id = getMaxId()

for id in xrange(min_id, max_id+1):
    try:
        root = fetchHtml(detailUrl % id)
    except:
        #print "Failed to fetch id %d" % id
        continue
    rows = root.cssselect("table tr")
    
    if len(rows) < 1:
        #print "No data for id %d" % id
        continue
    
    dbData = {'id': id}
    for row in rows:
        tds = row.cssselect("td")
        caption = tds[1].text_content().encode("utf-8")
        value = tds[2].text_content()
        
        field_conversion = caption2field.get(caption)
        if field_conversion is None:
            continue #ignored field
        (field, conversion) = field_conversion
        if field:
            dbData[field] = conversion(value)
    
    if len(dbData) > 1: #skip page in case no data for id is returned
        scraperwiki.sqlite.save(unique_keys=['id'], data = dbData)
    scraperwiki.sqlite.save_var("min_id", id+1)

scraperwiki.sqlite.save_var("min_id", 1)
