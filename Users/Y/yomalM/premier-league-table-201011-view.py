##################
#Note  from creator(Yomal Mudalige)- I have been tried to change column orders, however still it is not finalized. Hence I added prefix 'A', 'B'.....etc. Thanks 
#Reference for scraper- Scraperwiki Tutorial 3 and Python power!: the comprehensive guide By Matt Telles,pp.333.
##################

from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation 
import datetime #to display updatetime


sourcescraper = "premier-league-scraper-2"

limit = 100
offset = 0

keys = getKeys(sourcescraper)
keys.sort()  # alphabet order


#print '<img src="http://www.eplmatches.com/img/2010/05/chelsea-epl-winner-2009-10.jpg" width="152" height ="105"alt="" />'
#I'm not sure I can include this image without inform consent, hence commented the line..Thanks..Yomal Mudalige
d= datetime.datetime.today()
print '<th><font color =black face=verdana size=2>Last Update:</th>'
print d
print '</br>'
print '</br>'
print '<tr><font color=red face="verdana" size=5>POINTS TABLE</font></th></tr>' 
print '</br>'
print '</br>'
print '<a href="http://scraperwiki.com/views/jan11-match-result-premier-league/full/">January 2011 Results</a>'
print '</br>'
print '</br>'

print '<table border="5" bgcolor ="CCCCFF" cellpadding="15" style="border-collapse:collapse;">'

print "<tr>",#column headings section
for key in keys:
    print "<th><bgcolor=003366>%s</th>" % key,
print "</tr>"

for row in getData(sourcescraper, limit, offset):#row headings section
    print "<tr>",
    for key in keys:
        print "<td>%s</td>" % row.get(key),
        print "**"
    print "</tr>"
print "</table>"

print '<h4>Result from scraper: %s</h4>' % (sourcescraper)
print '<h5>Creator:1019053-Yomal A. Mudalige</h5>'
