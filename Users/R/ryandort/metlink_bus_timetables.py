import scraperwiki
import lxml.html
import dateutil.parser
import datetime

def scrapeRoute(routeInternalId, route, direction, directionId, days, dayId):
    
    entries = []
    stops = []

    html = scraperwiki.scrape("http://tt.ptv.vic.gov.au/tt/XSLT_TTB_REQUEST?command=direct&language=en&outputFormat=0&net=vic&line=" + routeInternalId + "&project=ttb&itdLPxx_selLineDir="+ directionId + "&itdLPxx_selWDType=" + dayId + "&sup=%20&itdLPxx_loadNTPs=1")
    
    root = lxml.html.fromstring(html)
    
    timeIndicatorSections = root.cssselect("div[id='ttHeader'] > div")[2]
    timeIndicatorSections = timeIndicatorSections.cssselect("div")
    
    timeIndicators = []
    for timeIndicator in timeIndicatorSections:
        timeIndicators.append(timeIndicator.text_content().strip())
    
    stopLinks = root.cssselect("div[id='ttMargin'] div div a")
    timeRows = root.cssselect("div[id='ttBody'] > div")
    
    startTimes = []
    
    i = 0
    for stopLink in stopLinks:
        
        stopHref = stopLink.get("href")
        stopId = int(stopHref[(stopHref.rfind("/") + 1):])
        stopName = stopLink.text_content()
        entry = { 'id' : stopId, 'name' : stopName }
        stops.append(entry)    
    
        stopEntry = timeRows[i]
        
        stopTimes = stopEntry.cssselect("div span")
        j = 0
        
        for stopTime in stopTimes:
            if stopTime == "" or stopTime == "-":
                continue
    
            stopTime = stopTime.text_content().strip()
            stopTime = stopTime.strip("H")
    
            stopTime = dateutil.parser.parse(stopTime)
    
            if timeIndicators[j] == "pm" and stopTime.hour < 12:
                stopTime = stopTime + datetime.timedelta(0, 0, 0, 0, 0, 12)
            if timeIndicators[j] == "am" and stopTime.hour == 12:
                stopTime = stopTime - datetime.timedelta(0, 0, 0, 0, 0, 12)
    
            if len(startTimes) < j + 1:
                startTimes.append(stopTime.time())

            if stopTime.time() < startTimes[j]:
                stopTime = stopTime + datetime.timedelta(0, 0, 0, 0, 0, 12)
    
            entry = { 'startTime' : startTimes[j],
                      'route' : route,
                      'stop' : stopId,
                      'time' : stopTime.time(),
                      'direction' : direction,
                      'days' : days }
            entries.append(entry)
    
            j = j + 1
        i = i + 1

    scraperwiki.sqlite.save(unique_keys=['id'], data=stops, table_name='BusStop')
    scraperwiki.sqlite.save(unique_keys=['startTime', 'route', 'stop', 'direction', 'days'], data=entries, table_name="BusRouteStops")

def scrapeRouteDaysDirections(routeInternalId, route):
    html = scraperwiki.scrape("http://tt.ptv.vic.gov.au/tt/XSLT_TTB_REQUEST?command=direct&language=en&outputFormat=0&net=vic&line=" + routeInternalId + "&project=ttb")
    root = lxml.html.fromstring(html)

    directionOptions = root.cssselect("select[class='direction'] option")
    directions = []

    directions.append(directionOptions[0].text_content())
    
    if len(directionOptions) > 1:
        directions.append(directionOptions[1].text_content())

    dayOptions = root.cssselect("select[class='date'] option")
    days = []
    dayIds = []
    for dayOption in dayOptions:
        print "Scraping " + route + ": " + directions[0] + " - " + dayOption.text_content()
        scrapeRoute(routeInternalId, route, directions[0], 'H', dayOption.text_content(), dayOption.get("value"))
        
        if len(directions) > 1:
            print "Scraping " + route + ": " + directions[1] + " - " + dayOption.text_content()
            scrapeRoute(routeInternalId, route, directions[1], 'R', dayOption.text_content(), dayOption.get("value"))

def scrapeRouteLine(internalRouteId):
    html = scraperwiki.scrape("http://tt.ptv.vic.gov.au/tt/XSLT_REQUEST?itdLPxx_lineMain=" + internalRouteId + "&itdLPxx_lineID=5642&itdLPxx_output=html")
    root = lxml.html.fromstring(html)

    metaTag = root.cssselect("meta[http-equiv='refresh']")
    routeLine = metaTag[0].get("content")
    routeLine = routeLine[(routeLine.find("line=") + len("line=")):]
    routeLine = routeLine[0:(routeLine.find("&"))]

    return routeLine

def scrapeRoutes(startPage):
    print "Scraping routes"

    html = scraperwiki.scrape(startPage)
    root = lxml.html.fromstring(html)

    routeOptions = root.cssselect("select[id='MainLineID'] > option")

    uptoRoute = scraperwiki.sqlite.get_var('running_route')

    if uptoRoute is not None:
        print "Restarting from route: " + uptoRoute

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

        entry = { 'id' : route, 'name' : routeName }
        scraperwiki.sqlite.save(unique_keys=['id'], data=entry, table_name="BusRoute")

        # store the route being done so that we can restart later
        scraperwiki.sqlite.save_var('running_route', route )

        routeLine = scrapeRouteLine(routeInternalId)

        print "Scraping " + route
        scrapeRouteDaysDirections(routeLine, route)
        
scrapeRoutes("http://ptv.vic.gov.au/timetables/metropolitan-buses/")
scraperwiki.sqlite.save_var('running_route', None )
