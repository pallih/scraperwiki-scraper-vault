import scraperwiki
import lxml.html

# Blank Python

baseURL = "http://www.cityofkingston.ca/residents/transportation/transit/"
regular = "schedules/Route_"
weekends = "schedules_evenings_sundays/Route_"
routes = ["1", "2", "3", "4", "5", "6", "7", "10", "12", "12A", "18", "19", "71", "A", "B", "C"]
routesw = ["1", "2", "E6", "7", "E12", "17", "18", "71", "EB", "C"]

#for r in routes:
html = scraperwiki.scrape(baseURL + regular + "1" + ".asp")
root = lxml.html.fromstring(html)
for el in root.cssselect("table.table .transLabelTxt"):           
    print el.text
    pass
pass

