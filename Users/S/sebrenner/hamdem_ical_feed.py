# 
# Scrapes the Hamilton county Dem's page and creates a ics freed of the events.
# http://hamiltoncountydems.org/index.php?page=events
#
# http://hamiltoncountydems.org/index.php?page=events&m=11&y=2011
# 


import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import time, datetime
from pytz import timezone
from BeautifulSoup import BeautifulSoup
from icalendar import Calendar, Event
from icalendar import UTC # timezone

now = datetime.datetime.now()


def makeListOfMonthUrls():
    """
    Takes no arguments.
    Returns a list of 13 urls.  Each one links to a monthly
    calendar of Hamilton County Democratic Party Events.
    The list starts with last month and goes out 12 months.
    """
    listOfURI = []
    if now.month == 1:
        upcomingMonth = 1
        upcomingYear = now.year - 1
    else:
        upcomingMonth = now.month - 1
        upcomingYear = now.year
        
    for i in xrange(13):
        urlString = 'http://hamiltoncountydems.org/index.php?page=events&m=' + str( upcomingMonth) + '&y=' + str( upcomingYear )
        upcomingMonth, upcomingYear = getNextMonth( upcomingMonth, upcomingYear )
        listOfURI.append(urlString)

    #print listOfURI
    return listOfURI


def getNextMonth( month, year ):
    """
    Takes a month and year.
    Returns the next month and year
    """
    if month == 12:
        return 1, (year + 1)
    else:
        return (month + 1), year


def getEventURI(monthURI):
    """
    Takes a URI to a ham dem calendar page , returns a list of URI to events listed on that page.

    """
    html = scraperwiki.scrape(monthURI)

    soup = BeautifulSoup(html)
    partyEvents = soup.findAll('a', { "class" : "eventlink"})
    # print partyEvents

    #    create list of urls
    myList = []
    for each in partyEvents:
        # print each['href']
        myList.append(each['href'])
        # print myList[-1]
    return myList

def parseDateTime(dtString):
    """
    Takes a list of dateTime related data and returns the first date time as a string.

    Wednesday, September 21st 2011, at 7:00 PM


    """
    month_dict = {"January":1,"February":2,"March":3,"April":4, "May":5, "June":6, "July":7,"August":8,"September":9,"October":10,"November":11,"December":12}

    #print "in ParseDateTime"
    items = dtString.split()

    year = items[3][:-1]
    month = month_dict[items[1]]
    day = items[2][0:-2]
    # convert hours to 24 hour clock
    if items[6] == "PM":
        if items[5][:-3] == "12":
            hour = int(items[5][:-3])
        else:
            hour = int(items[5][:-3]) + 12
    else:
        hour = items[5][:-3]
    minutes = items[5][-2:]

    #print items
    
    startDT = datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes))

    if len(items) > 8:
        if items[7] == "-":
            # convert hours to 24 hour clock
            if items[9] =="PM":
                hour = int(items[8][:-3]) + 12
            else:
                hour = items[8][:-3]
            minutes = items[8][-2:]
            endDT = datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes))
        elif items[7] == "through":
            # Multiday case.  For now this creates a single 
            # event from the start of day one to end of last day.
            year = items[11][:-1]
            month = month_dict[items[9]]
            day = items[10][0:-2]
            # convert hours to 24 hour clock
            if items[14] == "PM":
                hour = int(items[13][:-3]) + 12
            else:
                hour = items[13][:-3]
            minutes = items[13][-2:]
            
            endDT = startDT + datetime.timedelta(minutes=60)
        else:
            print "What do we do with:\n\t",
            print items
    else:
            endDT = startDT + datetime.timedelta(minutes=60)

    #print startDT, endDT
    return startDT, endDT

def importEventDetails(eventURI):
    """
    Takes a URI to an event and returns a list of events. 
    Usually it will return a list with a single event, 
    but if the event itself spand many days, 
    the function will try to parse out the various days. 

    Event details:
        Name
        When
        Where
        Info
        Notes
    """

    eventName, eventLocation, eventStart, eventEnd, eventInfo, eventNotes, eventContact, eventHost = "","","","","","","",""
    eventDescription = eventURI + "\n\n"

    html = scraperwiki.scrape(eventURI)
    soup = BeautifulSoup(html)
    
    # Get the name from the h2 tag
    eventName = soup.find('h1').contents[0]

    # Get the location data and convert it to a string.
    start=soup.find(text='Where:')    
    eventLocationCell = start.findNext('td')
    eventLocationList = eventLocationCell.findAll(text=True)
    eventLocationString = ""
    for each in eventLocationList:
        eventLocationString += each + ", "
    eventLocationString = eventLocationString.strip(" , ")
    eventLocation = eventLocationString.strip(" ")

    # Get the start time for this event
    start=soup.find(text='When:')
    eventStart, eventEnd  = parseDateTime(start.findNext('td').contents[0])
    eventDescription += "\nWhen: " + start.findNext('td').contents[0]
    
    start=soup.find(text='Info:')
    if start:
        eventInfo = start.findNext('td', text=True)
        eventDescription += "Info: " + eventInfo 

    start=soup.find(text='Notes:')
    if start:
        eventNotes = start.findNext('td', text=True)
        eventDescription += "\n\nNotes: " + eventNotes

    start=soup.find(text='Contact:')
    if start:
        eventContact = start.findNext('td', text=True)
        eventDescription += "\n\nContact: " + eventContact

    start=soup.find(text='Host:')
    if start:
        eventHost = start.findNext('td', text=True)
        eventDescription += "\n\nHost: " + eventHost

    scraperwiki.sqlite.save(unique_keys=["eventURI"], data={ "eventURI": eventURI, "eventName": eventName, "eventStart":eventStart, "eventEnd": eventEnd, "eventLocation": eventLocationString, "eventDescription": eventDescription })


# make a list of urls to monthly pages
monthUriList = makeListOfMonthUrls()

# make a list of urls to event pages
eventUriList = []
for each in monthUriList:
    eventUriList += getEventURI(each)


#print scraperwiki.sqlite.show_tables() 
scraperwiki.sqlite.execute("drop table if exists swdata")
       

#for i in xrange(42):
for i in eventUriList:
    importEventDetails("http://hamiltoncountydems.org" + i)

# 
# Scrapes the Hamilton county Dem's page and creates a ics freed of the events.
# http://hamiltoncountydems.org/index.php?page=events
#
# http://hamiltoncountydems.org/index.php?page=events&m=11&y=2011
# 


import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import time, datetime
from pytz import timezone
from BeautifulSoup import BeautifulSoup
from icalendar import Calendar, Event
from icalendar import UTC # timezone

now = datetime.datetime.now()


def makeListOfMonthUrls():
    """
    Takes no arguments.
    Returns a list of 13 urls.  Each one links to a monthly
    calendar of Hamilton County Democratic Party Events.
    The list starts with last month and goes out 12 months.
    """
    listOfURI = []
    if now.month == 1:
        upcomingMonth = 1
        upcomingYear = now.year - 1
    else:
        upcomingMonth = now.month - 1
        upcomingYear = now.year
        
    for i in xrange(13):
        urlString = 'http://hamiltoncountydems.org/index.php?page=events&m=' + str( upcomingMonth) + '&y=' + str( upcomingYear )
        upcomingMonth, upcomingYear = getNextMonth( upcomingMonth, upcomingYear )
        listOfURI.append(urlString)

    #print listOfURI
    return listOfURI


def getNextMonth( month, year ):
    """
    Takes a month and year.
    Returns the next month and year
    """
    if month == 12:
        return 1, (year + 1)
    else:
        return (month + 1), year


def getEventURI(monthURI):
    """
    Takes a URI to a ham dem calendar page , returns a list of URI to events listed on that page.

    """
    html = scraperwiki.scrape(monthURI)

    soup = BeautifulSoup(html)
    partyEvents = soup.findAll('a', { "class" : "eventlink"})
    # print partyEvents

    #    create list of urls
    myList = []
    for each in partyEvents:
        # print each['href']
        myList.append(each['href'])
        # print myList[-1]
    return myList

def parseDateTime(dtString):
    """
    Takes a list of dateTime related data and returns the first date time as a string.

    Wednesday, September 21st 2011, at 7:00 PM


    """
    month_dict = {"January":1,"February":2,"March":3,"April":4, "May":5, "June":6, "July":7,"August":8,"September":9,"October":10,"November":11,"December":12}

    #print "in ParseDateTime"
    items = dtString.split()

    year = items[3][:-1]
    month = month_dict[items[1]]
    day = items[2][0:-2]
    # convert hours to 24 hour clock
    if items[6] == "PM":
        if items[5][:-3] == "12":
            hour = int(items[5][:-3])
        else:
            hour = int(items[5][:-3]) + 12
    else:
        hour = items[5][:-3]
    minutes = items[5][-2:]

    #print items
    
    startDT = datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes))

    if len(items) > 8:
        if items[7] == "-":
            # convert hours to 24 hour clock
            if items[9] =="PM":
                hour = int(items[8][:-3]) + 12
            else:
                hour = items[8][:-3]
            minutes = items[8][-2:]
            endDT = datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes))
        elif items[7] == "through":
            # Multiday case.  For now this creates a single 
            # event from the start of day one to end of last day.
            year = items[11][:-1]
            month = month_dict[items[9]]
            day = items[10][0:-2]
            # convert hours to 24 hour clock
            if items[14] == "PM":
                hour = int(items[13][:-3]) + 12
            else:
                hour = items[13][:-3]
            minutes = items[13][-2:]
            
            endDT = startDT + datetime.timedelta(minutes=60)
        else:
            print "What do we do with:\n\t",
            print items
    else:
            endDT = startDT + datetime.timedelta(minutes=60)

    #print startDT, endDT
    return startDT, endDT

def importEventDetails(eventURI):
    """
    Takes a URI to an event and returns a list of events. 
    Usually it will return a list with a single event, 
    but if the event itself spand many days, 
    the function will try to parse out the various days. 

    Event details:
        Name
        When
        Where
        Info
        Notes
    """

    eventName, eventLocation, eventStart, eventEnd, eventInfo, eventNotes, eventContact, eventHost = "","","","","","","",""
    eventDescription = eventURI + "\n\n"

    html = scraperwiki.scrape(eventURI)
    soup = BeautifulSoup(html)
    
    # Get the name from the h2 tag
    eventName = soup.find('h1').contents[0]

    # Get the location data and convert it to a string.
    start=soup.find(text='Where:')    
    eventLocationCell = start.findNext('td')
    eventLocationList = eventLocationCell.findAll(text=True)
    eventLocationString = ""
    for each in eventLocationList:
        eventLocationString += each + ", "
    eventLocationString = eventLocationString.strip(" , ")
    eventLocation = eventLocationString.strip(" ")

    # Get the start time for this event
    start=soup.find(text='When:')
    eventStart, eventEnd  = parseDateTime(start.findNext('td').contents[0])
    eventDescription += "\nWhen: " + start.findNext('td').contents[0]
    
    start=soup.find(text='Info:')
    if start:
        eventInfo = start.findNext('td', text=True)
        eventDescription += "Info: " + eventInfo 

    start=soup.find(text='Notes:')
    if start:
        eventNotes = start.findNext('td', text=True)
        eventDescription += "\n\nNotes: " + eventNotes

    start=soup.find(text='Contact:')
    if start:
        eventContact = start.findNext('td', text=True)
        eventDescription += "\n\nContact: " + eventContact

    start=soup.find(text='Host:')
    if start:
        eventHost = start.findNext('td', text=True)
        eventDescription += "\n\nHost: " + eventHost

    scraperwiki.sqlite.save(unique_keys=["eventURI"], data={ "eventURI": eventURI, "eventName": eventName, "eventStart":eventStart, "eventEnd": eventEnd, "eventLocation": eventLocationString, "eventDescription": eventDescription })


# make a list of urls to monthly pages
monthUriList = makeListOfMonthUrls()

# make a list of urls to event pages
eventUriList = []
for each in monthUriList:
    eventUriList += getEventURI(each)


#print scraperwiki.sqlite.show_tables() 
scraperwiki.sqlite.execute("drop table if exists swdata")
       

#for i in xrange(42):
for i in eventUriList:
    importEventDetails("http://hamiltoncountydems.org" + i)

