import scraperwiki
import re

from BeautifulSoup import BeautifulSoup

homepage = "http://www.dublinbus.ie"
startingUrl = "http://www.dublinbus.ie/en/Your-Journey1/Timetables/?searchtype=&searchquery=&filter=&currentIndex=1"


def scrapeFacebookProfiles(pageLink):
    html = scraperwiki.scrape(pageLink)
    soup = BeautifulSoup(html)
    conName = soup.html.head.title
    links = soup.findAll(title=re.compile("Facebook$"))
    for link in links:
        words = link['title'].split(' on Facebook')
        print words[0] + "," + link.text + "," + link['href'] + "," + conName.text
        record = { "link" : words[0] + "," + link.text + "," + link['href'] + "," + conName.text }
        scraperwiki.datastore.save(["link"], record)


def scrapeRoutesData(routesMap):
    for routeLink in routesMap:
        weekdaytimes = []
        sattimes = []
        suntimes = []
        routeHtml = scraperwiki.scrape(routeLink.split(',')[1])
        routeSoup = BeautifulSoup(routeHtml)
        froms = routeSoup.findAll("div", attrs={'class' : 'TT_Title_left'})
        weekdaytimes.append(getTimes(routeSoup,"ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl00_DataList1_ctl00_dlTimeTop"))
        sattimes.append(getTimes(routeSoup, "ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl00_DataList1_ctl01_dlTimeTop"))
        suntimes.append(getTimes(routeSoup, "ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl00_DataList1_ctl02_dlTimeTop"))
        weekdaytimes.append(getTimes(routeSoup, "ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl01_DataList1_ctl00_dlTimeTop"))
        sattimes.append(getTimes(routeSoup, "ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl01_DataList1_ctl01_dlTimeTop"))
        suntimes.append(getTimes(routeSoup, "ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl01_DataList1_ctl02_dlTimeTop"))
        #froms1text = froms[0].text.split('&nbsp;')
        #froms2text = froms[1].text.split('&nbsp;')
        try:
            if froms[0]:
                froms1text = froms[0].text.split('&nbsp;')
                print "----------------------------"
                print routeLink.split(',')[0] + " - " + froms1text [1] + " to " + froms1text [3]
                print "Mon-Fri:  " + weekdaytimes[0]
                print "Sat:      " + sattimes[0]
                print "Sun:      " + suntimes[0]
            if froms[1]:
                froms2text = froms[1].text.split('&nbsp;')
                print froms2text [1] + " to " + froms2text [3]
                print "Mon-Fri:  " + weekdaytimes[1]
                print "Sat:      " + sattimes[1]
                print "Sun:      " + suntimes[1]
        except:
            break

def getTimes(soup, theId):
    weekDayTimetable = soup.find("div", id=theId)
    if weekDayTimetable:
        times = weekDayTimetable.findAll("div", attrs={ 'class' : 'time' })
        timesList = ""
        for time in times:
            timesList = timesList + time.text + ","
        return timesList
    else:
        return ""


def scrapeRouteLinks(pageUrl):
    routesMap = []
    pageHtml = scraperwiki.scrape(pageUrl)
    pageSoup = BeautifulSoup(pageHtml)
    routes = pageSoup.findAll("td", attrs={'class' : re.compile("RouteNumberColumn")})
    for route in routes:
        #print route.text + "," + homepage + route.a['href']
        routesMap.append(route.text + "," + homepage + route.a['href'])
    nextPage = pageSoup.find('a', title=re.compile("Next to Page"))
    if nextPage:
        newUrl = homepage + nextPage['href']
        scrapeRouteLinks(newUrl)
    else:
        print "ROUTE LINKS GOT"
    scrapeRoutesData(routesMap)
    #print(routesMap)


scrapeRouteLinks(startingUrl)

import scraperwiki
import re

from BeautifulSoup import BeautifulSoup

homepage = "http://www.dublinbus.ie"
startingUrl = "http://www.dublinbus.ie/en/Your-Journey1/Timetables/?searchtype=&searchquery=&filter=&currentIndex=1"


def scrapeFacebookProfiles(pageLink):
    html = scraperwiki.scrape(pageLink)
    soup = BeautifulSoup(html)
    conName = soup.html.head.title
    links = soup.findAll(title=re.compile("Facebook$"))
    for link in links:
        words = link['title'].split(' on Facebook')
        print words[0] + "," + link.text + "," + link['href'] + "," + conName.text
        record = { "link" : words[0] + "," + link.text + "," + link['href'] + "," + conName.text }
        scraperwiki.datastore.save(["link"], record)


def scrapeRoutesData(routesMap):
    for routeLink in routesMap:
        weekdaytimes = []
        sattimes = []
        suntimes = []
        routeHtml = scraperwiki.scrape(routeLink.split(',')[1])
        routeSoup = BeautifulSoup(routeHtml)
        froms = routeSoup.findAll("div", attrs={'class' : 'TT_Title_left'})
        weekdaytimes.append(getTimes(routeSoup,"ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl00_DataList1_ctl00_dlTimeTop"))
        sattimes.append(getTimes(routeSoup, "ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl00_DataList1_ctl01_dlTimeTop"))
        suntimes.append(getTimes(routeSoup, "ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl00_DataList1_ctl02_dlTimeTop"))
        weekdaytimes.append(getTimes(routeSoup, "ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl01_DataList1_ctl00_dlTimeTop"))
        sattimes.append(getTimes(routeSoup, "ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl01_DataList1_ctl01_dlTimeTop"))
        suntimes.append(getTimes(routeSoup, "ctl00_FullRegion_MainRegion_MainContentRegion_MainBodyRegion_Timetable1_ctl01_DataList1_ctl02_dlTimeTop"))
        #froms1text = froms[0].text.split('&nbsp;')
        #froms2text = froms[1].text.split('&nbsp;')
        try:
            if froms[0]:
                froms1text = froms[0].text.split('&nbsp;')
                print "----------------------------"
                print routeLink.split(',')[0] + " - " + froms1text [1] + " to " + froms1text [3]
                print "Mon-Fri:  " + weekdaytimes[0]
                print "Sat:      " + sattimes[0]
                print "Sun:      " + suntimes[0]
            if froms[1]:
                froms2text = froms[1].text.split('&nbsp;')
                print froms2text [1] + " to " + froms2text [3]
                print "Mon-Fri:  " + weekdaytimes[1]
                print "Sat:      " + sattimes[1]
                print "Sun:      " + suntimes[1]
        except:
            break

def getTimes(soup, theId):
    weekDayTimetable = soup.find("div", id=theId)
    if weekDayTimetable:
        times = weekDayTimetable.findAll("div", attrs={ 'class' : 'time' })
        timesList = ""
        for time in times:
            timesList = timesList + time.text + ","
        return timesList
    else:
        return ""


def scrapeRouteLinks(pageUrl):
    routesMap = []
    pageHtml = scraperwiki.scrape(pageUrl)
    pageSoup = BeautifulSoup(pageHtml)
    routes = pageSoup.findAll("td", attrs={'class' : re.compile("RouteNumberColumn")})
    for route in routes:
        #print route.text + "," + homepage + route.a['href']
        routesMap.append(route.text + "," + homepage + route.a['href'])
    nextPage = pageSoup.find('a', title=re.compile("Next to Page"))
    if nextPage:
        newUrl = homepage + nextPage['href']
        scrapeRouteLinks(newUrl)
    else:
        print "ROUTE LINKS GOT"
    scrapeRoutesData(routesMap)
    #print(routesMap)


scrapeRouteLinks(startingUrl)

