#########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import re
import os
import urllib

sourcescraper = "courts-ni-judicial-decisions"

urlquery = os.getenv('URLQUERY')
searchterm = "Chief"
if urlquery:
    searchterm = urllib.unquote(urlquery[2:])

limit = 5000
offset = 0

keys = ['Date_Created', 'Title', 'judgename', 'Judgment', 'judgetitle']

print '<h2>Judicial decisions from <a href="http://www.courtsni.gov.uk/en-GB/Judicial+Decisions/">this page</a></h2>'


print '<form submit="#">Filter: <input type="text" name="a"> <input type="submit" value="Go"></form>'

print '<h2>Filtered on "%s"</h2>' % searchterm

# column headings
print "<table>"
print "<tr><th>Date</th><th>Judge</th><th>Title</th></tr>"

# rows
n = 0
for row in getData(sourcescraper, limit, offset):
    if not re.search(searchterm, row['Title']):
        continue

    print "<tr>"
    print "<td>%s</td>" % row['Date_Created'][:10]
    print "<td>%s</a></td>" % (row['judgename'])  # row['judgetitle'], 
    print "<td><a href=\"%s\">%s</a></td>" % (row['Judgment'], row['Title'])
    print "</tr>"
    n += 1

print "</table>"

print "<p>There were %d records</p>" % n
#########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import re
import os
import urllib

sourcescraper = "courts-ni-judicial-decisions"

urlquery = os.getenv('URLQUERY')
searchterm = "Chief"
if urlquery:
    searchterm = urllib.unquote(urlquery[2:])

limit = 5000
offset = 0

keys = ['Date_Created', 'Title', 'judgename', 'Judgment', 'judgetitle']

print '<h2>Judicial decisions from <a href="http://www.courtsni.gov.uk/en-GB/Judicial+Decisions/">this page</a></h2>'


print '<form submit="#">Filter: <input type="text" name="a"> <input type="submit" value="Go"></form>'

print '<h2>Filtered on "%s"</h2>' % searchterm

# column headings
print "<table>"
print "<tr><th>Date</th><th>Judge</th><th>Title</th></tr>"

# rows
n = 0
for row in getData(sourcescraper, limit, offset):
    if not re.search(searchterm, row['Title']):
        continue

    print "<tr>"
    print "<td>%s</td>" % row['Date_Created'][:10]
    print "<td>%s</a></td>" % (row['judgename'])  # row['judgetitle'], 
    print "<td><a href=\"%s\">%s</a></td>" % (row['Judgment'], row['Title'])
    print "</tr>"
    n += 1

print "</table>"

print "<p>There were %d records</p>" % n
#########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import re
import os
import urllib

sourcescraper = "courts-ni-judicial-decisions"

urlquery = os.getenv('URLQUERY')
searchterm = "Chief"
if urlquery:
    searchterm = urllib.unquote(urlquery[2:])

limit = 5000
offset = 0

keys = ['Date_Created', 'Title', 'judgename', 'Judgment', 'judgetitle']

print '<h2>Judicial decisions from <a href="http://www.courtsni.gov.uk/en-GB/Judicial+Decisions/">this page</a></h2>'


print '<form submit="#">Filter: <input type="text" name="a"> <input type="submit" value="Go"></form>'

print '<h2>Filtered on "%s"</h2>' % searchterm

# column headings
print "<table>"
print "<tr><th>Date</th><th>Judge</th><th>Title</th></tr>"

# rows
n = 0
for row in getData(sourcescraper, limit, offset):
    if not re.search(searchterm, row['Title']):
        continue

    print "<tr>"
    print "<td>%s</td>" % row['Date_Created'][:10]
    print "<td>%s</a></td>" % (row['judgename'])  # row['judgetitle'], 
    print "<td><a href=\"%s\">%s</a></td>" % (row['Judgment'], row['Title'])
    print "</tr>"
    n += 1

print "</table>"

print "<p>There were %d records</p>" % n
#########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import re
import os
import urllib

sourcescraper = "courts-ni-judicial-decisions"

urlquery = os.getenv('URLQUERY')
searchterm = "Chief"
if urlquery:
    searchterm = urllib.unquote(urlquery[2:])

limit = 5000
offset = 0

keys = ['Date_Created', 'Title', 'judgename', 'Judgment', 'judgetitle']

print '<h2>Judicial decisions from <a href="http://www.courtsni.gov.uk/en-GB/Judicial+Decisions/">this page</a></h2>'


print '<form submit="#">Filter: <input type="text" name="a"> <input type="submit" value="Go"></form>'

print '<h2>Filtered on "%s"</h2>' % searchterm

# column headings
print "<table>"
print "<tr><th>Date</th><th>Judge</th><th>Title</th></tr>"

# rows
n = 0
for row in getData(sourcescraper, limit, offset):
    if not re.search(searchterm, row['Title']):
        continue

    print "<tr>"
    print "<td>%s</td>" % row['Date_Created'][:10]
    print "<td>%s</a></td>" % (row['judgename'])  # row['judgetitle'], 
    print "<td><a href=\"%s\">%s</a></td>" % (row['Judgment'], row['Title'])
    print "</tr>"
    n += 1

print "</table>"

print "<p>There were %d records</p>" % n
