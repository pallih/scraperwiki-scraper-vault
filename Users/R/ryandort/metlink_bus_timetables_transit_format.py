import scraperwiki
import lxml.html
import dateutil.parser
import datetime
import time

def timeToMinutes(timeObj):
    return timeObj.hour * 60 + timeObj.minute

def scrapeTrip(routeInternalId, route, service_id, direction, directionNum, directionId, days, dayId):
    
    entries = []
    stops = []

    html = scraperwiki.scrape("http://tt.ptv.vic.gov.au/tt/XSLT_TTB_REQUEST?command=direct&language=en&outputFormat=0&net=vic&line=" + routeInternalId + "&project=ttb&itdLPxx_selLineDir="+ directionId + "&itdLPxx_selWDType=" + dayId + "&sup=%20&itdLPxx_loadNTPs=1")
    
    root = lxml.html.fromstring(html)
    
    timeIndicatorSections = root.cssselect("div[id='ttHeader'] > div")[2]
    timeIndicatorSections = timeIndicatorSections.cssselect("div > div")
    
    timeIndicators = []
    for timeIndicator in timeIndicatorSections:
        timeIndicators.append(timeIndicator.text_content().strip())

    stopLinks = root.cssselect("div[id='ttMargin'] div div a")
    timeRows = root.cssselect("div[id='ttBody'] > div")

    # should be a trip for every span in the rows
    trips = []
    startTimes = []
    tripSeqNum = []

    if len(timeRows) > 0:
        # encode the start times into the trips
        stopTimes = timeRows[0].cssselect("div span")

        for stopTime in stopTimes:
            stopTime = stopTime.text_content().strip()

            i = 1
            while stopTime == "" or stopTime == "-" and i < len(timeRows):
                stopTimes = timeRows[i].cssselect("div span")
                stopTime = stopTimes[len(trips)].text_content().strip()
                i = i + 1
            
            startStop = i - 1
            
            if stopTime == "" or stopTimes == "-":
                raise Exception("Could not find start time...")
            
            ''.join(ch for ch in stopTime if not ch.isalpha())
            tripId = route + "_" + service_id + "_" + direction + "_" + stopTime + timeIndicators[len(trips)] + "_" + str(startStop)
            trip = { 'trip_id' : tripId, 'route_id' : routeInternalId, 'service_id' : service_id, 'headsign' : direction, 'direction_id' : directionNum }
            trips.append(trip)
            tripSeqNum.append(0)

            stopTime = dateutil.parser.parse(stopTime)
            
            if timeIndicators[len(startTimes)] == "pm" and stopTime.hour < 12:
                stopTime = stopTime + datetime.timedelta(0, 0, 0, 0, 0, 12)
            if timeIndicators[len(startTimes)] == "am" and stopTime.hour == 12:
                stopTime = stopTime - datetime.timedelta(0, 0, 0, 0, 0, 12)
            startTimes.append(stopTime.time())

        scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `Trip` (`direction_id` integer, `route_id` text, `trip_id` text, `headsign` text, `service_id` text, PRIMARY KEY(trip_id))")
        scraperwiki.sqlite.execute("CREATE INDEX IF NOT EXISTS TRIP_ROUTE_ID_IDX ON Trip (route_id)")
        scraperwiki.sqlite.commit()  

        scraperwiki.sqlite.save(unique_keys=['trip_id'], data=trips, table_name="Trip")

    i = 0
    for stopLink in stopLinks:
        
        stopHref = stopLink.get("href")
        stopId = int(stopHref[(stopHref.rfind("/") + 1):])
        stopName = stopLink.text_content()
        entry = { 'stop_id' : stopId, 'stop_name' : stopName, 'stop_lat' : 0, 'stop_lon' : 0 }
        stops.append(entry)    
    
        stopEntry = timeRows[i]
        
        stopTimes = stopEntry.cssselect("div span")
        j = 0
        
        for stopTime in stopTimes:
            stopTime = stopTime.text_content().strip()
            ''.join(ch for ch in stopTime if not ch.isalpha())

            if stopTime == "" or stopTime == "-":
                j = j + 1
                continue
    
            stopTime = dateutil.parser.parse(stopTime)
    
            if timeIndicators[j] == "pm" and stopTime.hour < 12:
                stopTime = stopTime + datetime.timedelta(0, 0, 0, 0, 0, 12)
            if timeIndicators[j] == "am" and stopTime.hour == 12:
                stopTime = stopTime - datetime.timedelta(0, 0, 0, 0, 0, 12)
    
            if stopTime.time() < startTimes[j]:
                stopTime = stopTime + datetime.timedelta(0, 0, 0, 0, 0, 12)
    
            stopTimeMin = timeToMinutes(stopTime.time())

            entry = { 'trip_id' : trips[j]['trip_id'],
                      'stop_id' : stopId,
                      'time' : int(stopTimeMin),
                      'stop_sequence' : tripSeqNum[j] }
            entries.append(entry)
            
            tripSeqNum[j] = tripSeqNum[j] + 1
            j = j + 1
        i = i + 1

    scraperwiki.sqlite.save(unique_keys=['stop_id'], data=stops, table_name='Stop')
    
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `StopTime` (`time` integer, `trip_id` text, `stop_sequence` integer, `stop_id` integer, PRIMARY KEY (trip_id, stop_sequence))")
    scraperwiki.sqlite.execute("CREATE INDEX IF NOT EXISTS STOPTIME_STOP_ID_IDX ON StopTime (stop_id)")
    scraperwiki.sqlite.commit()  

    scraperwiki.sqlite.save(unique_keys=['trip_id', 'stop_sequence'], data=entries, table_name="StopTime")

def scrapeRouteOptions(routeInternalId, route):
    html = scraperwiki.scrape("http://tt.ptv.vic.gov.au/tt/XSLT_TTB_REQUEST?command=direct&language=en&outputFormat=0&net=vic&line=" + routeInternalId + "&project=ttb")
    root = lxml.html.fromstring(html)

    # get the dates this is valid for
    periodOptions = root.cssselect("select[class='period'] option")
    thisPeriod = periodOptions[0].text_content()

    if thisPeriod.endswith(" until further notice"):
        thisPeriod = thisPeriod[0:(thisPeriod.find(" until further notice"))]
    
    # work out what days this is valid for
    dayOptions = root.cssselect("select[class='date'] option")

    # get directions
    directionOptions = root.cssselect("select[class='direction'] option")
    directions = []

    directions.append(directionOptions[0].text_content())
    
    if len(directionOptions) > 1:
        directions.append(directionOptions[1].text_content())

    calendars = []
    
    for dayOption in dayOptions:
        calendarObject = {}
        calendarObject['monday'] = False
        calendarObject['tuesday'] = False
        calendarObject['wednesday'] = False
        calendarObject['thursday'] = False
        calendarObject['friday'] = False
        calendarObject['saturday'] = False
        calendarObject['sunday'] = False

        if dayOption.text_content() == "Melbourne Cup Day":
            # special case
            # cup day is first tuesday in November.. hardcode for 2012 for now
            calendarObject['start_date'] = int(time.mktime(datetime.datetime(2012, 11, 5).timetuple()))
            calendarObject['end_date'] = calendarObject['start_date']
            calendarObject['tuesday'] = True
        else:
            if dayOption.text_content() == "Mon - Fri":
                calendarObject['monday'] = True
                calendarObject['tuesday'] = True
                calendarObject['wednesday'] = True
                calendarObject['thursday'] = True
                calendarObject['friday'] = True
            elif dayOption.text_content() == "Saturday":
                calendarObject['saturday'] = True
            elif dayOption.text_content() == "Sunday":
                calendarObject['sunday'] = True
            else:
                # unknown days - raise error
                raise Exception("Don't know how to handle day: " + dayOption.text_content())

            # set the start/end dates
            periodDate = dateutil.parser.parse(thisPeriod)
            calendarObject['start_date'] = int(time.mktime(periodDate.timetuple()))
            # set the end date to end of next year
            calendarObject['end_date'] = int(time.mktime(datetime.date(datetime.date.today().year + 1, 12, 31).timetuple()))

        # create a service ID by combining start date with day option text
        calendarObject['service_id'] = thisPeriod + "_" + dayOption.text_content()
        
        calendars.append(calendarObject)

    scraperwiki.sqlite.save(unique_keys=['service_id'], data=calendars, table_name="Calendar")
    
    
    for dayOption in dayOptions:
        print "Scraping " + route + ": " + directions[0] + " - " + dayOption.text_content()
        service_id = thisPeriod + "_" + dayOption.text_content()
        scrapeTrip(routeInternalId, route, service_id, directions[0], 0, 'H', dayOption.text_content(), dayOption.get("value"))
        
        if len(directions) > 1:
            print "Scraping " + route + ": " + directions[1] + " - " + dayOption.text_content()
            service_id = thisPeriod + "_" + dayOption.text_content()
            scrapeTrip(routeInternalId, route, service_id, directions[1], 1, 'R', dayOption.text_content(), dayOption.get("value"))


def scrapeRouteLine(internalRouteId):
    html = scraperwiki.scrape("http://tt.ptv.vic.gov.au/tt/XSLT_REQUEST?itdLPxx_lineMain=" + str(internalRouteId) + "&itdLPxx_lineID=5642&itdLPxx_output=html")
    root = lxml.html.fromstring(html)

    metaTag = root.cssselect("meta[http-equiv='refresh']")
    routeLine = metaTag[0].get("content")
    routeLine = routeLine[(routeLine.find("line=") + len("line=")):]
    routeLine = routeLine[0:(routeLine.find("&"))]

    return routeLine

def scrapeRoute(routeInternalId, route):        
    
    print "Scraping " + route
    scrapeRouteOptions(routeInternalId, route)


def scrapeRoutes(startPage):
    print "Scraping routes"

    html = scraperwiki.scrape(startPage)
    root = lxml.html.fromstring(html)

    routeOptions = root.cssselect("select[id='MainLineID'] > option")

    uptoRoute = scraperwiki.sqlite.get_var('running_route')

    uptoRoute = '693'

    if uptoRoute is not None:
        print "Restarting from route: " + uptoRoute

    routes = []

    for routeOption in routeOptions:
        routeInternalId = routeOption.get("value")

        if routeInternalId == "-1":
            continue

        routeName = routeOption.text_content()

        routeSplit = routeName.split(" - ")
        route = routeSplit[0]
        routeName = " - ".join(routeSplit[1:])

        if uptoRoute is not None and route != uptoRoute:
            continue

        uptoRoute = None

        routeInternalId = scrapeRouteLine(routeInternalId)
        
        entry = { 'route_id' : routeInternalId, 'route_short_name' : route, 'route_long_name' : routeName }
        routes.append(entry)

        # store the route being done so that we can restart later
        scraperwiki.sqlite.save_var('running_route', route)

        scrapeRoute(routeInternalId, route)
        # raise Exception("Debug")
        break

    scraperwiki.sqlite.save(unique_keys=['route_id'], data=routes, table_name="Route")

scrapeRoutes("http://ptv.vic.gov.au/timetables/metropolitan-buses/")
scraperwiki.sqlite.save_var('running_route', None )
