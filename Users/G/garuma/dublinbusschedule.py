# Fetch Dublin Bus schedule information from dublinbus.ie
#
# Code is placed under MIT/X11 licence
# (c) 2010 Jean-Paul Bonnet and Jérémie Laval

import scraperwiki
import re
import urllib2
import sys
import json
from BeautifulSoup import BeautifulSoup

# Contains the existing Dublin Bus lines 
#availableLines = ["11a", "16a", "128" ]
baseUrl = "http://www.dublinbus.ie/en/Your-Journey1/Timetables/All-Timetables/"
stopsUrl = "http://www.dublinbus.ie/Labs.EPiServer/GoogleMap/gmap_conf.aspx?custompageid=1219&routeNumber={0}&direction={1}&towards={2}"

# Some lines have just stupidly formatted, skip those
linesBlacklist = ('65', '7n', '15n', '17', '25', '25x', '25n', '27n', '27x', '29n', '31n', '32x', '33d', '33n', '33x', '39a', '39n', '40n', '41n', '41x', '42n', '44n', '46e', '46n', '48n', '49n', '51', '51d', '51x', '51n', '54n')

timetableIndexes = { "Monday" : ("ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl00_DataList1_ctl00_dlTimeTop", "ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl01_DataList1_ctl00_dlTimeTop"),
                     "Saturday" : ("ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl00_DataList1_ctl01_dlTimeTop", "ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl01_DataList1_ctl01_dlTimeTop"),
                     "Sunday": ("ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl00_DataList1_ctl02_dlTimeTop", "ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl01_DataList1_ctl02_dlTimeTop") }

# columns used 
# busNumber(string) from(string) stops(string, CSV{latitute|longitude}) to(string) mondayFriday(string,CSV{\d\d:\d\d}) saturday(string,CSV{\d\d:\d\d}) sunday(string,CSV{\d\d:\d\d}) isAirport(bool) isAccessible(bool)

def Main():
    availableLines = getAllRoutes()
    reAirport = re.compile("Airport_Icon.png$|Airlink_Web_Logo.png$")
    reAccessible = re.compile("Accessible_Icon.png$")
    reMap = re.compile("'(.+)','(.+)','(.+)'")
    reTravelTime = re.compile(">> (\d+)mins")

    for busData in availableLines:
        if busData[0] in linesBlacklist:
            continue
        try:
            soup = GetTimetableHtml(busData[1])
            bus = busData[0]
            
            route_desc = soup.find("div",  id="route_description").string.replace('From ', '')
            split_str = "Towards " if route_desc.find("Towards ") != -1 else " to "
            road_end_points = [e.strip() for e in route_desc.split(split_str)]
            fromPoint = road_end_points[0]
            toPoint = road_end_points[1]

            icons = soup.find("div", attrs={ 'class' : 'timtable_icon' })
            isAirport = icons.find("img", src=reAirport) != None
            isAccessible = icons.find("img", src=reAccessible) != None

            viewMaps = [reMap.search(div.a['onclick']) for div in soup.findAll('div', attrs={'class':'view_on_map'})]
            routeOverviews = soup.findAll('div', attrs={'class': 'route_overview'})

            # Get the two timetable for each direction
            for i in (0, 1):
                monday = GetTimetableFor(soup, timetableIndexes["Monday"][i])
                saturday = GetTimetableFor(soup, timetableIndexes["Saturday"][i])
                sunday = GetTimetableFor(soup, timetableIndexes["Sunday"][i])

                viewMap = viewMaps[i]
                stops = ','.join(getLatLngForStops(viewMap.group(1), viewMap.group(2), viewMap.group(3)))
                
                overview = [reTravelTime.search(val.string).group(1) for val in routeOverviews[i].findAll('span')]
                               
                scraperwiki.datastore.save(['busNumber', 'from', 'to'],
                                           { 'busNumber': bus,
                                             'from': fromPoint if i == 0 else toPoint,
                                             'stops': stops,
                                             'to': toPoint if i == 0 else fromPoint,
                                             'mondayFriday': monday,
                                             'saturday': saturday,
                                             'sunday': sunday,
                                             'journeyTime': reduce(lambda x,y: x+y, map(lambda x: int(x), overview)),
                                             'isAirport': isAirport,
                                             'isAccessible': isAccessible })
        except:
            print "For ", bus, ", error: ", sys.exc_info()[0]
            continue

def GetTimetableFor(soup, value):
    table = soup.find("div", id=value)
    times = ','.join([time.string.strip() for time in table.findAll("div", attrs={ 'class' : 'time' })])
    return times

def GetTimetableHtml(busNumber):
    url = baseUrl + busNumber + '/'
    page = urllib2.urlopen(url)
    return BeautifulSoup(page)

def getLatLngForStops(line, direction, terminus):
    xml = urllib2.urlopen(stopsUrl.format(line, direction, terminus))
    soup = BeautifulSoup(xml)
    pois = soup.findAll('poi')
    return [poi.gpoint.lat.string + '|' + poi.gpoint.lng.string for poi in pois]

def getAllRoutes():
    Lines = []
    i = 0
    while(True):
        i = i + 1
        try:
            Lines += getRoutes(i)  
        except:
            break
    return Lines

def getRoutes(page):
    routes = []
    routes_url = "http://www.dublinbus.ie/en/Your-Journey1/Timetables/?searchtype=&searchquery=&filter=&currentIndex=" + str(page)
    html = urllib2.urlopen(routes_url)
    soup = BeautifulSoup(html)
    pattern = re.compile(".+/(.+)/$")
    
    tds = soup.findAll("td", { "class" : "RouteNumberColumn" })
    for td in tds:
        a = td.find(True)
        routes.append((a.contents[0].strip().replace('/', ''), pattern.search(a['href']).group(1)))
    return routes
    
Main ()
