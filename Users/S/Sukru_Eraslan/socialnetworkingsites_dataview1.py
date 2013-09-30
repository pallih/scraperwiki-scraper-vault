from scraperwiki.apiwrapper import getKeys, getData
from scraperwiki.apiwrapper import getDataByDate, getDataByLocation
from pygooglechart import PieChart3D


def drawPieChart(val1):
    #To draw a pie chart
    val2 = 100 - val1
    chart = PieChart3D(250, 100)
    chart.add_data([val1, val2])
    chart.set_pie_labels(['Use', 'Not Use'])
    print '<img src="%s"></img></td>' % chart.get_url()

sourcescraper = 'socialnetworkingsites_scraper'
limit = 12
offset = 0
keys = getKeys(sourcescraper)
keys.sort()#Sort keys

#CSS code
print "<style>"
print "<!--"
print "table.resulttable {"
print "font-family: Trebuchet MS,Trebuchet MS, Trebuchet MS;"
print "font-size:16px;"
print "border-style: solid;"
print "border-collapse: collapse;"
print "text-align: center;"
print "}"
print "table.resulttable th {"
print "border-style: solid;"
print "padding: 8px;"
print "background-color: #FF9900;"
print "color:#000000;"
print "}"
print "table.resulttable td {"
print "color:#FF6600;"
print "font-weight: bold;"
print "border-style: solid;"
print "padding: 8px;"
print "background-color: #FFFFFF;"
print "}"
print ".style2fortd {"
print "font-size:12px;"
print "}"
print "-->"
print "</style>"

print '<h1>Data from scraper: %s</h1>' % sourcescraper

#Columns' headers
headers = []#Hold columns' headers without '_'
for key in keys:
    head_title = ""#Hold header without '_'
    for i in str(key):
        if i != "_":
            head_title += i
        else:
            head_title += " "
    #add head_title in the headers list
    headers.append(head_title)

print '<table class=\"resulttable\">'
print "<tr>",
for header in headers:
    print "<th>%s</th>" % header,
print "</tr>"

# rows
for row in getData(sourcescraper, limit, offset):
    print "<tr>",
    for key in keys:
        if str(key) == "Category":
            print "<td>%s</td>" % row.get(key),
        else:
            print "<td class=\"style2fortd\">Use: ", int(row.get(key)), \
            "% | Not Use: ", 100 - int(row.get(key)), "%<br>"
            drawPieChart(int(row.get(key)))
    print "</tr>"
print "</table>"

from scraperwiki.apiwrapper import getKeys, getData
from scraperwiki.apiwrapper import getDataByDate, getDataByLocation
from pygooglechart import PieChart3D


def drawPieChart(val1):
    #To draw a pie chart
    val2 = 100 - val1
    chart = PieChart3D(250, 100)
    chart.add_data([val1, val2])
    chart.set_pie_labels(['Use', 'Not Use'])
    print '<img src="%s"></img></td>' % chart.get_url()

sourcescraper = 'socialnetworkingsites_scraper'
limit = 12
offset = 0
keys = getKeys(sourcescraper)
keys.sort()#Sort keys

#CSS code
print "<style>"
print "<!--"
print "table.resulttable {"
print "font-family: Trebuchet MS,Trebuchet MS, Trebuchet MS;"
print "font-size:16px;"
print "border-style: solid;"
print "border-collapse: collapse;"
print "text-align: center;"
print "}"
print "table.resulttable th {"
print "border-style: solid;"
print "padding: 8px;"
print "background-color: #FF9900;"
print "color:#000000;"
print "}"
print "table.resulttable td {"
print "color:#FF6600;"
print "font-weight: bold;"
print "border-style: solid;"
print "padding: 8px;"
print "background-color: #FFFFFF;"
print "}"
print ".style2fortd {"
print "font-size:12px;"
print "}"
print "-->"
print "</style>"

print '<h1>Data from scraper: %s</h1>' % sourcescraper

#Columns' headers
headers = []#Hold columns' headers without '_'
for key in keys:
    head_title = ""#Hold header without '_'
    for i in str(key):
        if i != "_":
            head_title += i
        else:
            head_title += " "
    #add head_title in the headers list
    headers.append(head_title)

print '<table class=\"resulttable\">'
print "<tr>",
for header in headers:
    print "<th>%s</th>" % header,
print "</tr>"

# rows
for row in getData(sourcescraper, limit, offset):
    print "<tr>",
    for key in keys:
        if str(key) == "Category":
            print "<td>%s</td>" % row.get(key),
        else:
            print "<td class=\"style2fortd\">Use: ", int(row.get(key)), \
            "% | Not Use: ", 100 - int(row.get(key)), "%<br>"
            drawPieChart(int(row.get(key)))
    print "</tr>"
print "</table>"

