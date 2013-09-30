import scraperwiki
import time
import datetime
html = scraperwiki.scrape('http://www.wmata.com/rider_tools/metro_service_status/elevator_escalator.cfm?')

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
rows = root.cssselect('table.tabular tr.even') # get all the <td> tags
for row in rows:
    # Set up our data record - we'll need it later
    record = {}
    table_cells = row.cssselect("td[align='center']")
    if table_cells:
        record['Date'] = datetime.date.today()
        record['Escalators Operating'] = table_cells[0].text
        record['Escalators Under Repair'] = table_cells[1].text
        record['Escalators Total'] = table_cells[2].text
        record['Elevators Under Repair'] = table_cells[3].text
        record['Elevators Operating'] = table_cells[4].text
        record['Elevators Total'] = table_cells[5].text
        # Print out the data we've gathered
        print record
        # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(["Date"], record)import scraperwiki
import time
import datetime
html = scraperwiki.scrape('http://www.wmata.com/rider_tools/metro_service_status/elevator_escalator.cfm?')

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
rows = root.cssselect('table.tabular tr.even') # get all the <td> tags
for row in rows:
    # Set up our data record - we'll need it later
    record = {}
    table_cells = row.cssselect("td[align='center']")
    if table_cells:
        record['Date'] = datetime.date.today()
        record['Escalators Operating'] = table_cells[0].text
        record['Escalators Under Repair'] = table_cells[1].text
        record['Escalators Total'] = table_cells[2].text
        record['Elevators Under Repair'] = table_cells[3].text
        record['Elevators Operating'] = table_cells[4].text
        record['Elevators Total'] = table_cells[5].text
        # Print out the data we've gathered
        print record
        # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(["Date"], record)