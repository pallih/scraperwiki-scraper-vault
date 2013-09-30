import scraperwiki

###############################################################################
# 
# Scrape the event sheffield site so we can reuse the data in other apps.
# 
###############################################################################

import mechanize 
import lxml.html
import urlparse
import datetime 


def scrape_table(root):
    # For each row in the results table
    for tr in root.cssselect("table[id='thedmsBrowseEvents'] tr"):
        # Grab the data elements
        tds = tr.cssselect("td")
        # The first row in the results table only contains headings, so skip it
        if len(tds) == 0:
            # print "No data"
            noop=1
        else:
            # print "Data row"
            # A real data row
            details_url = urlparse.urljoin(base_url, tds[1].getchildren()[0].attrib['href'])
            details_title = ""
            details_text = ""
            venue_id = ""
            try:
                parsed_details_url = urlparse.urlparse(details_url)
                details_url_qs = parsed_details_url.query
                parsed_qs = urlparse.parse_qs(details_url_qs)
                venue_id = parsed_qs['venue'][0]
                details_html = scraperwiki.scrape(details_url)
                details_root = lxml.html.fromstring(details_html)
                details_top_panel = details_root.cssselect("div[id='thedmsTopPanel']")[0]
                details_title = details_top_panel.cssselect("img")[0].attrib['title']
                details_panel = details_root.cssselect("div[id='thedmsDetailsPanel']")[0]
                details_text = details_panel.text_content()
            except:
                print "problem fetching ", details_url

            data = {
              'event_date' : tds[0].text_content(),
              'event_name' : tds[1].text_content(),
              'event_venue' : lxml.html.tostring(tds[2]).strip().replace('</td>&#13;', '').replace('<td>','').replace('<br>', ' ').strip(),
              'event_time' : tds[3].text_content(),
              'event_contact' : tds[4].text_content(),
              'details_title' : details_title,
              'details_url' : details_url,
              'details_text' : details_text,
              'venue' : venue_id
            }
            # Ideally here we need to go and fetch the details url and exract the full description
            # We also need to extract the venue id from the URL as it looks like a really useful identifier
            # for co-referencing once we have other data sets
            #
            # Finally, push the data into the sqlite store
            scraperwiki.sqlite.save(unique_keys=['details_url'], data=data)
            # Output the data for debugging
            # print details_url

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    # print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_links = root.cssselect("div.thedmsBrowsePaging")[0]
    a_links = next_links.cssselect("a")
    next_link = ""
    # After page 1 there are 2 anchors that move backwards and forwards.
    if ( len(a_links) == 1 ):
        next_link = a_links[0]
    else:
        next_link = a_links[1]
    # print next_link
    if next_link is not None:
        next_url = urlparse.urljoin(base_url, next_link.attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)
    else:
        print "No next link available"


# Set up the base URL
base_url = "http://www.welcometosheffield.co.uk"

from_date = datetime.datetime.today().strftime('%d/%m/%Y')
to_date = (datetime.datetime.today()+datetime.timedelta(days=+31)).strftime('%d/%m/%Y')

print "from ", from_date, "to", to_date

# esurl = "http://www.welcometosheffield.co.uk/dms-connect/search?dms=12&startdate="+from_date+"&enddate="+to_date
esurl = "http://www.welcometosheffield.co.uk/dms-connect/search?dms=12"
print esurl

scrape_and_look_for_next_link(esurl)
import scraperwiki

###############################################################################
# 
# Scrape the event sheffield site so we can reuse the data in other apps.
# 
###############################################################################

import mechanize 
import lxml.html
import urlparse
import datetime 


def scrape_table(root):
    # For each row in the results table
    for tr in root.cssselect("table[id='thedmsBrowseEvents'] tr"):
        # Grab the data elements
        tds = tr.cssselect("td")
        # The first row in the results table only contains headings, so skip it
        if len(tds) == 0:
            # print "No data"
            noop=1
        else:
            # print "Data row"
            # A real data row
            details_url = urlparse.urljoin(base_url, tds[1].getchildren()[0].attrib['href'])
            details_title = ""
            details_text = ""
            venue_id = ""
            try:
                parsed_details_url = urlparse.urlparse(details_url)
                details_url_qs = parsed_details_url.query
                parsed_qs = urlparse.parse_qs(details_url_qs)
                venue_id = parsed_qs['venue'][0]
                details_html = scraperwiki.scrape(details_url)
                details_root = lxml.html.fromstring(details_html)
                details_top_panel = details_root.cssselect("div[id='thedmsTopPanel']")[0]
                details_title = details_top_panel.cssselect("img")[0].attrib['title']
                details_panel = details_root.cssselect("div[id='thedmsDetailsPanel']")[0]
                details_text = details_panel.text_content()
            except:
                print "problem fetching ", details_url

            data = {
              'event_date' : tds[0].text_content(),
              'event_name' : tds[1].text_content(),
              'event_venue' : lxml.html.tostring(tds[2]).strip().replace('</td>&#13;', '').replace('<td>','').replace('<br>', ' ').strip(),
              'event_time' : tds[3].text_content(),
              'event_contact' : tds[4].text_content(),
              'details_title' : details_title,
              'details_url' : details_url,
              'details_text' : details_text,
              'venue' : venue_id
            }
            # Ideally here we need to go and fetch the details url and exract the full description
            # We also need to extract the venue id from the URL as it looks like a really useful identifier
            # for co-referencing once we have other data sets
            #
            # Finally, push the data into the sqlite store
            scraperwiki.sqlite.save(unique_keys=['details_url'], data=data)
            # Output the data for debugging
            # print details_url

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    # print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_links = root.cssselect("div.thedmsBrowsePaging")[0]
    a_links = next_links.cssselect("a")
    next_link = ""
    # After page 1 there are 2 anchors that move backwards and forwards.
    if ( len(a_links) == 1 ):
        next_link = a_links[0]
    else:
        next_link = a_links[1]
    # print next_link
    if next_link is not None:
        next_url = urlparse.urljoin(base_url, next_link.attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)
    else:
        print "No next link available"


# Set up the base URL
base_url = "http://www.welcometosheffield.co.uk"

from_date = datetime.datetime.today().strftime('%d/%m/%Y')
to_date = (datetime.datetime.today()+datetime.timedelta(days=+31)).strftime('%d/%m/%Y')

print "from ", from_date, "to", to_date

# esurl = "http://www.welcometosheffield.co.uk/dms-connect/search?dms=12&startdate="+from_date+"&enddate="+to_date
esurl = "http://www.welcometosheffield.co.uk/dms-connect/search?dms=12"
print esurl

scrape_and_look_for_next_link(esurl)
