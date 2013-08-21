import scraperwiki

# Blank Python

print "Running fhfa.gov City Area Codes for Housing Price Index"

# imports

import csv
import scraperwiki


html = scraperwiki.scrape("http://www.fhfa.gov/Default.aspx?Page=216")

import lxml.html
root = lxml.html.fromstring(html)

for el in root.cssselect("select option"):
    StartTrigger = 'MSA 1'
    EndTrigger = 'MSA 2'
    if StartTrigger in lxml.html.tostring(el):
        pass
    elif EndTrigger in lxml.html.tostring(el):
        break
    else:
        Str = lxml.html.tostring(el).replace('<option value=\"', "")
        Str = Str.replace("</option>", "")
        Str = Str.replace('\">', ", ")
        reader = Str.split(", ")
        
        data = {
        'areacode' : reader[0],
        'city' : reader[1],
        'state' : reader[2]
        }
        scraperwiki.sqlite.save(unique_keys=['areacode'],data=data)
        
        

    