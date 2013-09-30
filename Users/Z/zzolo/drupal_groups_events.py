# Parses groups.drupal.org iCal feed and adds content from individual events.

import scraperwiki
import lxml.html 
from icalendar import Calendar, Event

# Variables
data = []

# Get main iCal feed
ical = scraperwiki.scrape('http://groups.drupal.org/ical')
cal = Calendar.from_string(ical)

# Go through events
for component in cal.walk('vevent'):
    #print dir(component)
    #print component.values()
    #print component['url']

    # Get full descritpion from event node.
    node = scraperwiki.scrape(component['url'])
    node_dom = lxml.html.fromstring(node)
    node_content = node_dom.cssselect("div.node div.content")

    # Create row.
    add = {
        'uid': component['uid'],
        'url': component['url'],
        'description': node_content[0].text_content()
    }
    data.append(add)

# Save the data
scraperwiki.sqlite.save(unique_keys=['uid', 'url'], data=data)# Parses groups.drupal.org iCal feed and adds content from individual events.

import scraperwiki
import lxml.html 
from icalendar import Calendar, Event

# Variables
data = []

# Get main iCal feed
ical = scraperwiki.scrape('http://groups.drupal.org/ical')
cal = Calendar.from_string(ical)

# Go through events
for component in cal.walk('vevent'):
    #print dir(component)
    #print component.values()
    #print component['url']

    # Get full descritpion from event node.
    node = scraperwiki.scrape(component['url'])
    node_dom = lxml.html.fromstring(node)
    node_content = node_dom.cssselect("div.node div.content")

    # Create row.
    add = {
        'uid': component['uid'],
        'url': component['url'],
        'description': node_content[0].text_content()
    }
    data.append(add)

# Save the data
scraperwiki.sqlite.save(unique_keys=['uid', 'url'], data=data)