import scraperwiki
import lxml.html           
from datetime import date, datetime, timedelta

# Grab data for March 
for i in range(13, 19):
    the_date = date(2012, 03, i)
    
    html = scraperwiki.scrape("http://schedule.sxsw.com/2012/?conference=music&lsort=name&day=" + str(i) + "&category=")

    root = lxml.html.fromstring(html)

    for row in root.cssselect("div.music"):
        link = row.cssselect("a.link_item")[0]
        event_link = link.get("href")
        event_name = link.text_content().strip()
        category_element = row.cssselect(".col2 .type")[0]
        event_category = category_element.text_content().strip('" \t\n\r')
        event_subcategory = None
        subcategory_elements = category_element.cssselect("i")
        if len(subcategory_elements) > 0:
            event_subcategory = subcategory_elements[0].text_content().strip()
        event_venue = row.cssselect(".col3 .location")[0].text_content().strip('" \t\n\r')
        event_room = None
        room_elements = row.cssselect(".col3 .location i")
        if len(room_elements) > 0:
            event_room = room_elements[0].text_content().strip()
        date_time = row.cssselect(".col4 .date_time")[0].text_content().strip('" \t\n\r')
        date_parts = date_time.split('-')
        if len(date_parts) < 2:
            continue
        start_time = date_parts[0].strip()
        end_time = date_parts[1].strip()
        
        data = {
          'link': event_link,
          'name': event_name,
          'venue_name': event_venue,
          'venue_room': event_room,
          'start_date' : datetime.strptime("2012-03-" + str(i) + start_time, "%Y-%m-%d%I:%M%p"),
          'end_date' : datetime.strptime("2012-03-" + str(i) + end_time, "%Y-%m-%d%I:%M%p")
        }
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)

import scraperwiki
import lxml.html           
from datetime import date, datetime, timedelta

# Grab data for March 
for i in range(13, 19):
    the_date = date(2012, 03, i)
    
    html = scraperwiki.scrape("http://schedule.sxsw.com/2012/?conference=music&lsort=name&day=" + str(i) + "&category=")

    root = lxml.html.fromstring(html)

    for row in root.cssselect("div.music"):
        link = row.cssselect("a.link_item")[0]
        event_link = link.get("href")
        event_name = link.text_content().strip()
        category_element = row.cssselect(".col2 .type")[0]
        event_category = category_element.text_content().strip('" \t\n\r')
        event_subcategory = None
        subcategory_elements = category_element.cssselect("i")
        if len(subcategory_elements) > 0:
            event_subcategory = subcategory_elements[0].text_content().strip()
        event_venue = row.cssselect(".col3 .location")[0].text_content().strip('" \t\n\r')
        event_room = None
        room_elements = row.cssselect(".col3 .location i")
        if len(room_elements) > 0:
            event_room = room_elements[0].text_content().strip()
        date_time = row.cssselect(".col4 .date_time")[0].text_content().strip('" \t\n\r')
        date_parts = date_time.split('-')
        if len(date_parts) < 2:
            continue
        start_time = date_parts[0].strip()
        end_time = date_parts[1].strip()
        
        data = {
          'link': event_link,
          'name': event_name,
          'venue_name': event_venue,
          'venue_room': event_room,
          'start_date' : datetime.strptime("2012-03-" + str(i) + start_time, "%Y-%m-%d%I:%M%p"),
          'end_date' : datetime.strptime("2012-03-" + str(i) + end_time, "%Y-%m-%d%I:%M%p")
        }
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)

