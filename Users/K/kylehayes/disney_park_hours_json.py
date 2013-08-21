#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import cgi, os
import datetime

currentDate = datetime.date.today().strftime("%A, %B %d")

qs = cgi.parse_qs(os.getenv("QUERY_STRING"))

callbackParam = ''
if 'callback' in qs:
    callbackParam = qs['callback'][0]
showCallback = False
if(len(callbackParam.strip()) > 0):
    showCallback = True

sourcescraper = "disneyland_hours"
limit = 20
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select Park, Date, Open, Close, Note from src.swdata where Date = ? limit ? offset ?", (currentDate,limit, offset))

keys = sdata.get("keys")
rows = sdata.get("data")

if showCallback:
    print callbackParam + "(",

print '['

# column headings
for rIdx,row in enumerate(rows):
    print "{"
    for kIdx,key in enumerate(keys):
        print '"' + key + '" : ',
        print '"' + row[kIdx] + '"',
        if(kIdx != len(keys)-1):
            print ","
    print "}",
    if (rIdx != len(rows)-1):
        print ","
    
print "]"
if showCallback:
    print ")",