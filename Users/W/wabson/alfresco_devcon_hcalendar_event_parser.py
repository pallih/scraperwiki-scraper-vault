import scraperwiki
import lxml.html
import lxml.etree
import re
import urllib2

from datetime import date

data = { 'events': [] }
batch_size = 100
events_url = 'https://devcon.alfresco.com/sanjose/sessions'
events_keys = [ 'event_name' ]
events_unique_keys = [ 'event_name', 'event_location', 'start_time', 'end_time' ]
events_table_name = 'events'
timezone_override = "-08:00"

data_verbose=0
skip_events=0

def main():
    scrape_events_html(events_url)

def scrape_events_html(page_url):
    # Allow race URL to be overridden (e.g. results only posted on club website, not marathon site)
    try:
        #results_html = lxml.html.fromstring(scraperwiki.scrape(race_url).replace('UTF-8', 'iso-8859-1'))
        events_html = lxml.html.fromstring(scraperwiki.scrape(page_url))
        for table_el in events_html.cssselect('ul.events table'):
            hd_el = table_el.cssselect('thead')
            locations = []
            for hd_td_el in table_el.cssselect('thead tr th')[1:]:
                locations.append(hd_td_el.text_content().strip())
            for tr_el in table_el.cssselect('tbody tr'):
                start_time_el = tr_el.cssselect('.date-display-start')[0]
                end_time_el = tr_el.cssselect('.date-display-end')[0]
                colindex=0
                for td_el in tr_el.cssselect('td')[1:5]:
                    # Save result data
                    #save_data(event={})
                    st = start_time_el.get('content').replace("+00:00", timezone_override)
                    et = end_time_el.get('content').replace("+00:00", timezone_override)
                    locname = locations[colindex]
                    eventname = td_el.text_content().strip()
                    speakername = td_el.find('a').text_content().strip() if td_el.find('a') else ''
                    if len(eventname) > 0:
                        speakername = td_el.find('a').text_content().strip()
                        linkurl = td_el.find('a').get('href')
                        if len(speakername) > 0:
                            eventname = eventname.replace(speakername, speakername + " - ")
                        print eventname
                        save_data(event={ 'event_name': eventname, 'event_location': locname, 'start_time': st, 'end_time': et, 'url': linkurl })
                    colindex += 1

        # Flush all results in this division and the race itself to the datastore
        print "Saving %s events for %s" % (len(data['events']), page_url)
        save_data(force=True)
                
    except urllib2.HTTPError, e:
        if e.code == 404:
            print 'WARNING: Missing data for %s' % (page_url)
        else:
            raise e

# Save the data in batches
def save_data(event=None, force=False):
    global data
    if event is not None:
        data['events'].append(event)
    if len(data['events']) >= batch_size or force == True:
        scraperwiki.sqlite.save(unique_keys=events_unique_keys, data=data['events'], table_name=events_table_name, verbose=data_verbose)
        data['races'] = []
main()

import scraperwiki
import lxml.html
import lxml.etree
import re
import urllib2

from datetime import date

data = { 'events': [] }
batch_size = 100
events_url = 'https://devcon.alfresco.com/sanjose/sessions'
events_keys = [ 'event_name' ]
events_unique_keys = [ 'event_name', 'event_location', 'start_time', 'end_time' ]
events_table_name = 'events'
timezone_override = "-08:00"

data_verbose=0
skip_events=0

def main():
    scrape_events_html(events_url)

def scrape_events_html(page_url):
    # Allow race URL to be overridden (e.g. results only posted on club website, not marathon site)
    try:
        #results_html = lxml.html.fromstring(scraperwiki.scrape(race_url).replace('UTF-8', 'iso-8859-1'))
        events_html = lxml.html.fromstring(scraperwiki.scrape(page_url))
        for table_el in events_html.cssselect('ul.events table'):
            hd_el = table_el.cssselect('thead')
            locations = []
            for hd_td_el in table_el.cssselect('thead tr th')[1:]:
                locations.append(hd_td_el.text_content().strip())
            for tr_el in table_el.cssselect('tbody tr'):
                start_time_el = tr_el.cssselect('.date-display-start')[0]
                end_time_el = tr_el.cssselect('.date-display-end')[0]
                colindex=0
                for td_el in tr_el.cssselect('td')[1:5]:
                    # Save result data
                    #save_data(event={})
                    st = start_time_el.get('content').replace("+00:00", timezone_override)
                    et = end_time_el.get('content').replace("+00:00", timezone_override)
                    locname = locations[colindex]
                    eventname = td_el.text_content().strip()
                    speakername = td_el.find('a').text_content().strip() if td_el.find('a') else ''
                    if len(eventname) > 0:
                        speakername = td_el.find('a').text_content().strip()
                        linkurl = td_el.find('a').get('href')
                        if len(speakername) > 0:
                            eventname = eventname.replace(speakername, speakername + " - ")
                        print eventname
                        save_data(event={ 'event_name': eventname, 'event_location': locname, 'start_time': st, 'end_time': et, 'url': linkurl })
                    colindex += 1

        # Flush all results in this division and the race itself to the datastore
        print "Saving %s events for %s" % (len(data['events']), page_url)
        save_data(force=True)
                
    except urllib2.HTTPError, e:
        if e.code == 404:
            print 'WARNING: Missing data for %s' % (page_url)
        else:
            raise e

# Save the data in batches
def save_data(event=None, force=False):
    global data
    if event is not None:
        data['events'].append(event)
    if len(data['events']) >= batch_size or force == True:
        scraperwiki.sqlite.save(unique_keys=events_unique_keys, data=data['events'], table_name=events_table_name, verbose=data_verbose)
        data['races'] = []
main()

