##################
#Note from creator(Yomal Mudalige)- I have been tried to create the link for excel sheets ('Analysis Link' field), however still it is not functioning.Thanks 
#Reference for scraper - scraperwiki Tutorial 3
##################

from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "government-expenditure"

limit = 20
offset = 0

keys = getKeys(sourcescraper)
keys.sort()  # sorting 

#print '<a href="https://spreadsheets.google.com/ccc?key=0AonYZs4MzlZbdHJLWXJfS1diemlnN084YlNSU0RjNWc&hl=en#gid=0">Entire Spread Sheet</a>'

print '<th><font color=336666 face=verdana size=5>Department wise %s </th>' % (sourcescraper)
print '</br>'
print '<table border="4" cellpadding="15" bgcolor ="#cc3333" color="FFFFFF" style="border-collapse:collapse;">'

print "<tr>",# column heading section
for key in keys:    
    #print "<th>%s</th>" % key,
    print "<th><font color=#ffcc00 face=verdana size=4>%s</th>" % key,
#print "<th>Deatil Link</th>"
print "</tr>"


for row in getData(sourcescraper, limit, offset):# rows heading section
    print "<tr>",
    for key in keys:
        print "<td><font color=#ccffff face=verdana size=3>%s</td>" % row.get(key),
        #print "*"
    print "</tr>"

print "</table>"

##################
#Note from creator(Yomal Mudalige)- I have been tried to create the link for excel sheets ('Analysis Link' field), however still it is not functioning.Thanks 
#Reference for scraper - scraperwiki Tutorial 3
##################

from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "government-expenditure"

limit = 20
offset = 0

keys = getKeys(sourcescraper)
keys.sort()  # sorting 

#print '<a href="https://spreadsheets.google.com/ccc?key=0AonYZs4MzlZbdHJLWXJfS1diemlnN084YlNSU0RjNWc&hl=en#gid=0">Entire Spread Sheet</a>'

print '<th><font color=336666 face=verdana size=5>Department wise %s </th>' % (sourcescraper)
print '</br>'
print '<table border="4" cellpadding="15" bgcolor ="#cc3333" color="FFFFFF" style="border-collapse:collapse;">'

print "<tr>",# column heading section
for key in keys:    
    #print "<th>%s</th>" % key,
    print "<th><font color=#ffcc00 face=verdana size=4>%s</th>" % key,
#print "<th>Deatil Link</th>"
print "</tr>"


for row in getData(sourcescraper, limit, offset):# rows heading section
    print "<tr>",
    for key in keys:
        print "<td><font color=#ccffff face=verdana size=3>%s</td>" % row.get(key),
        #print "*"
    print "</tr>"

print "</table>"

