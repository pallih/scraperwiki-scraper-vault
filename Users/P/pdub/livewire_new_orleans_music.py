import scraperwiki
import lxml.html           
from datetime import date, datetime, timedelta

# For the next 7 days, including today, grab the data
for i in range(0, 7):
    days = timedelta(days=i)
    the_date = date.today() + days
    
    html = scraperwiki.scrape("http://www.wwoz.org/new-orleans-community/music-calendar?start_date=" + str(the_date))

    root = lxml.html.fromstring(html)

    venue_link = ""
    venue_name = ""

    for row in root.cssselect("div.music-event"):
        venues = row.cssselect("div.venue-name")
        if len(venues) > 0:
            venue = venues[0]
            venue_link = venue.cssselect("a")[0].get("href")
            venue_name = venue.cssselect("a")[0].text_content()
        event = row.cssselect("div.event-name")[0]
        event_link = event.cssselect("a")[0].get("href")
        event_name = event.cssselect("a")[0].text_content()
        full_date = row.cssselect("div.full-date")[0].text_content()
        data = {
          'date' : datetime.strptime(full_date.strip() + " " + str(the_date.year), "%A %B %d at %I:%M %p %Y"),
          'date_string': full_date,
          'venue_name' : venue_name,
          'venue_link' : "http://www.wwoz.org" + venue_link,
          'event_name' : event_name,
          'event_link': "http://www.wwoz.org" + event_link
        }
        scraperwiki.sqlite.save(unique_keys=['date', 'venue_name', 'event_name'], data=data)
    
