from pymaps import Map, PyMap
import csv

reader = csv.reader(open('http://scraperwiki.com/scrapers/export/swimming-attempt/'), delimiter=',', quotechar='"')


tmap = Map()
tmap.zoom = 3



for row, l in enumerate(reader):
    if row==0:
    #print "\t".join(l)
        pass
    else:
    #print "\t",l[1],l[2]
        pointhtml = l[0]
    point = (l[1], l[2], pointhtml, row)
    tmap.setpoint(point)    

gmap = PyMap(key="ABCDEFG", maplist=[tmap])
#gmap.addicon(icon)

# pymapjs exports all the javascript required to build the map!
mapcode = gmap.pymapjs()
print "<html><head>"
print mapcode
print "</head>"
print """<body onload="load()" onunload="GUnload()">
<div id="map" style="width: 760px; height: 460px"></div> 
</body>
</html>"""