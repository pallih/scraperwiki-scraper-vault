# Scraper that gets the list of people and links that are commented
# on a Twin Cities Data Viz Meetup.
#
# For instance:
# http://www.meetup.com/Twin-Cities-Visualization-Group/events/93516392/

import scraperwiki
import lxml.html

def scrape_meetup_page(url, prefix):
    html = scraperwiki.scrape(url)
    dom = lxml.html.fromstring(html)
    key = 0
    
    # Find each comment
    for figures in dom.cssselect('div#event-comments-section ul#conversation li div.figureset-description'):
        members = figures.cssselect('a.memberinfo-widget')
    
        # Find each link
        for link in figures.cssselect('p a[target="_blank"]'):
    
            data = {
                'key': '%s-%s' % (prefix, key),
                'member': members[0].text_content(),
                'link': link.attrib['href']
            }
            print data
            scraperwiki.sqlite.save(unique_keys=['key'], data=data)
            key = key + 1


scrape_meetup_page('http://www.meetup.com/Twin-Cities-Visualization-Group/events/93516392/', 'jan')
scrape_meetup_page('http://www.meetup.com/Twin-Cities-Visualization-Group/events/100794032/', 'mar')# Scraper that gets the list of people and links that are commented
# on a Twin Cities Data Viz Meetup.
#
# For instance:
# http://www.meetup.com/Twin-Cities-Visualization-Group/events/93516392/

import scraperwiki
import lxml.html

def scrape_meetup_page(url, prefix):
    html = scraperwiki.scrape(url)
    dom = lxml.html.fromstring(html)
    key = 0
    
    # Find each comment
    for figures in dom.cssselect('div#event-comments-section ul#conversation li div.figureset-description'):
        members = figures.cssselect('a.memberinfo-widget')
    
        # Find each link
        for link in figures.cssselect('p a[target="_blank"]'):
    
            data = {
                'key': '%s-%s' % (prefix, key),
                'member': members[0].text_content(),
                'link': link.attrib['href']
            }
            print data
            scraperwiki.sqlite.save(unique_keys=['key'], data=data)
            key = key + 1


scrape_meetup_page('http://www.meetup.com/Twin-Cities-Visualization-Group/events/93516392/', 'jan')
scrape_meetup_page('http://www.meetup.com/Twin-Cities-Visualization-Group/events/100794032/', 'mar')