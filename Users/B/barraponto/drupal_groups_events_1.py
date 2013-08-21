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
for event in cal.walk('vevent'):

    # Create row.
    event = {
        'id': event['uid'],
        'url': event['url'],
        'start': event.get('DTSTART').dt.isoformat() if event.has_key('DTSTART') else nil
    }
    
    # Get full descritpion from event node.
    node_dom = lxml.html.parse(event['url']).getroot()

    if (node_dom):

        # Cleanup event description and add it to event dictionary
        node_content = node_dom.cssselect('.node .content')[0]
        node_content.make_links_absolute()
        cleanup = node_content.cssselect('.field, .vote-up-down-widget, .signup_anonymous_login')
        for element in cleanup:
            node_content.remove(element)
        event['description'] = lxml.html.tostring(node_content)

    data.append(event)

# Save the data
scraperwiki.sqlite.save(unique_keys=['id', 'url'], data=data)