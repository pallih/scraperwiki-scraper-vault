###############################################################################
# Parses schedules on Disney's websites to get schedules for various Disney
# theme parks and store them in a common format.  The script only grabs the
# records for the current day.
###############################################################################

import scraperwiki
import datetime
from BeautifulSoup import BeautifulSoup
from types import *

currentDate = datetime.date.today().strftime("%A, %B %d")

#############################################
# Get the times for Disneyland (uses a different calendar format than Disney World)

starting_url = 'http://disneyland.disney.go.com/calendar/'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('td') 
for td in tds:
    record = { "td" : td.text }
    findRes = record['td'].find(":00")
    if(findRes > -1 ):
        if(record['td'].find("TODAY") > -1):            
            timeSplit =  record['td'].split("Disneyland Park")[1].split(" - ")
            open = timeSplit[0]
            closed = timeSplit[1][:6]
            
            parkHours = {"Park" : "Disneyland",
            "Date" : currentDate,
            "Open" : open,
            "Close" : closed,
            "Note" : ""}
            # save records to the datastore
            scraperwiki.sqlite.save(["Park", "Date", "Open", "Close", "Note"], parkHours)

#############################################
# Get the times for Disney World (uses a different calendar format than Disneyland)

disneyworld_url = 'http://disneyworld.disney.go.com/calendars/'
html = scraperwiki.scrape(disneyworld_url)
soup = BeautifulSoup(html)

# Get the DIV holding the dates, then the list of "h2" tags that contain each park 
h2s = soup.findAll("div", {"class":"themeParkHoursContent"})[0].findAll("h2")

# Iterate over the parks
for h2 in h2s:

    park = h2.text

    # Get all of the "tr" tags that hold the individual dates/times
    trs = h2.nextSibling.next.nextSibling.findAll("tr")

    date = ""
    for tr in trs:

        # Skip the "updates" (these are the blackout or dark days)
        if(tr['class'] == "updates"):
            continue

        # If the date is not empty, update the date (if it is empty, we'll use the same date for multiple iterations)
        if(tr.next.next.next != "&nbsp;"):
            date = tr.next.next.next

        if(date != currentDate):
            continue

        # Get the time and split it
        time = tr.next.next.next.next.next
        timeSplit = time.split(" - ")
        open = timeSplit[0]
        closed = timeSplit[1][:9]

        # Get the note for the open/close time.  This is sometimes special hours for the park.
        note = tr.next.next.next.next.next.next.next.string
        # If there was no note, just leave it an empty string
        if( type(note) is NoneType):
            note = ""

        # Build the record hash
        parkHours = {"Park" : park,
        "Date" : date,
        "Open" : open,
        "Close" : closed,
        "Note" : note}

        # Store it in the datastore
        scraperwiki.sqlite.save(["Park", "Date", "Open", "Close", "Note"], parkHours)

