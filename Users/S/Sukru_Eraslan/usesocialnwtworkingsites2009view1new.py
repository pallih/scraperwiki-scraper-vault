from scraperwiki.apiwrapper import getKeys, getData
from scraperwiki.apiwrapper import getDataByDate, getDataByLocation
import scraperwiki.sqlite

def calculate_rate(values):
    #Calculate the rate by using data from the table
    a = (100 * values[1]) / values[0]
    if a > 100:
        return a - 100
    elif a < 100:
        return 100 - a
    else:
        return 0

sourcescraper = 'usesocialnetworkingsites2009new'
scraperwiki.sqlite.attach(sourcescraper, "src")
limit = 12
offset = 0
scraperdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
keys = scraperdata.get("keys")

#CSS code
print "<style>"
print "<!--"
print ".style0 {"
print "font-family: Trebuchet MS;"
print "color: #FF0000;"
print "}"
print ".style1 {"
print "font-size:16px;"
print "font-weight:bold;"
print "font-family: Trebuchet MS;"
print "font-size:16px;"
print "color: #FF9900;"
print "}"
print ".style2 {"
print "font-size:14px;"
print "font-family: Trebuchet MS;"
print "font-size:14px;"
print "color: #000000;"
print "}"
print "-->"
print "</style>"

print '<h1>Data from scraper: %s</h1>' % sourcescraper
print "<h2 class=\"style0\">The Use of Social Networking Websites</h2>"

# rows
for row in getData(sourcescraper, limit, offset):
    values = []#Hold the percentages of use of social networking websites
    #in 2008 and 2009 for each category
    for key in keys:
        if str(key) == "Category":
            print "<p class=\"style1\">%s: %s</p>" % (key, row.get(key))
        elif str(key) == "date_scraped":
            continue
        else:
            values.append(int(row.get(key)))
    if values[0] > values[1]:
        print "<p class=\"style2\">The use of social networking websites was \
        DECREASED by %s percent from 2008 to 2009</p>" % calculate_rate(values)
    elif values[0] < values[1]:
        print "<p class=\"style2\">The use of social networking websites was \
        INCREASED by %s percent from 2008 to 2009</p>" % calculate_rate(values)
    else:
        print "<p class=\"style2\">The use of social networking websites in \
        2008 was the SAME as the use of social networking websites in 2009</p>"


from scraperwiki.apiwrapper import getKeys, getData
from scraperwiki.apiwrapper import getDataByDate, getDataByLocation
import scraperwiki.sqlite

def calculate_rate(values):
    #Calculate the rate by using data from the table
    a = (100 * values[1]) / values[0]
    if a > 100:
        return a - 100
    elif a < 100:
        return 100 - a
    else:
        return 0

sourcescraper = 'usesocialnetworkingsites2009new'
scraperwiki.sqlite.attach(sourcescraper, "src")
limit = 12
offset = 0
scraperdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
keys = scraperdata.get("keys")

#CSS code
print "<style>"
print "<!--"
print ".style0 {"
print "font-family: Trebuchet MS;"
print "color: #FF0000;"
print "}"
print ".style1 {"
print "font-size:16px;"
print "font-weight:bold;"
print "font-family: Trebuchet MS;"
print "font-size:16px;"
print "color: #FF9900;"
print "}"
print ".style2 {"
print "font-size:14px;"
print "font-family: Trebuchet MS;"
print "font-size:14px;"
print "color: #000000;"
print "}"
print "-->"
print "</style>"

print '<h1>Data from scraper: %s</h1>' % sourcescraper
print "<h2 class=\"style0\">The Use of Social Networking Websites</h2>"

# rows
for row in getData(sourcescraper, limit, offset):
    values = []#Hold the percentages of use of social networking websites
    #in 2008 and 2009 for each category
    for key in keys:
        if str(key) == "Category":
            print "<p class=\"style1\">%s: %s</p>" % (key, row.get(key))
        elif str(key) == "date_scraped":
            continue
        else:
            values.append(int(row.get(key)))
    if values[0] > values[1]:
        print "<p class=\"style2\">The use of social networking websites was \
        DECREASED by %s percent from 2008 to 2009</p>" % calculate_rate(values)
    elif values[0] < values[1]:
        print "<p class=\"style2\">The use of social networking websites was \
        INCREASED by %s percent from 2008 to 2009</p>" % calculate_rate(values)
    else:
        print "<p class=\"style2\">The use of social networking websites in \
        2008 was the SAME as the use of social networking websites in 2009</p>"


