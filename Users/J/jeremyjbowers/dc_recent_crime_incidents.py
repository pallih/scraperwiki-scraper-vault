"""
Welcome to my DC crime scraper.

ScraperWiki doesn't like all of the data, so
I've left in 2012 as the small (90-ish records)
to demonstrate what you can get out of it.

Set the years at the top, either one year, 
e.g., [2012] or a range of years, e.g., 
range(2007,2011).
"""
import scraperwiki
import requests
import datetime
from lxml.html.soupparser import fromstring

# Set up a range of years.
# This might be too much years. Try with less.
# years = range[2007,2012]
years = [2012]

def get_incidents(year):
    """
    Gets crime incidents from the DC Government XML.
    """
    print 'Downloading year: %s' % year
    
    # Build URL from year.
    # If the year is 2007-2011, download the XML straight from ... my S3 account.
    if year in range(2007, 2011):
        url = 'http://wapo-projects.s3.amazonaws.com/techathon/scraperwiki/xml/crime_incidents_%s_plain.xml' % year
    
    # If the year is 2012, get it from the DC government. This is NOT the whole year.
    if year == 2012:
        url = 'http://data.octo.dc.gov/feeds/crime_incidents/crime_incidents_current.xml'    
    
    # Request the data using the Requests library.
    request = requests.get(url)
    unzipped_request = request.content
    
    # Parse the XML using lxml's BeautifulSoup parser.
    crime_xml_parsed = fromstring(unzipped_request)

    # Return the parsed Element() objects by grabbing the xpath for <entry> tags.
    return crime_xml_parsed.xpath('//entry')

def parse_incidents(incidents):
    """
    Parses a list of incidents.
    Takes a list of lxml Element() classes.
    Returns a list of incident dicts.
    """
    print 'Parsing year: %s' % year
    
    # Set up our data structure.
    incident_list = []
    
    # Loop through the list of Element() objects that were <entry> tags.
    for incident in incidents:
        print 'Reading incident: %s' % int(incident.xpath('title')[0].text_content().replace('ReportedCrime ID:', ''))
        # Set up a data structure for this <entry>.
        incident_dict = {}

        # Grab some attributes from this crime incident, like id, date, lat/lon, offense and address.
        incident_dict['id'] = int(incident.xpath('title')[0].text_content().replace('ReportedCrime ID:', ''))
        incident_dict['date'] = incident.xpath('content')[0].getchildren()[0].getchildren()[3].text_content().split('T')[0]
        incident_dict['lat'] = float(incident.xpath('content')[0].getchildren()[0].getchildren()[9].text_content())
        incident_dict['lon'] = float(incident.xpath('content')[0].getchildren()[0].getchildren()[10].text_content())
        incident_dict['offense'] = incident.xpath('content')[0].getchildren()[0].getchildren()[5].text_content()
        incident_dict['address'] = incident.xpath('content')[0].getchildren()[0].getchildren()[8].text_content().strip('B/O ')
        incident_dict['anc'] = incident.xpath('content')[0].getchildren()[0].getchildren()[14].text_content()
        
        # Some of these don't have neighborhood clusters. Let's wrap a simple try/except to capture when they don't.
        try:
            incident_dict['neighborhood_cluster'] = int(incident.xpath('content')[0].getchildren()[0].getchildren()[18].text_content())
        except ValueError:
            incident_dict['neighborhood_cluster'] = None
        
        # Write the entries to our data structure above.
        incident_list.append(incident_dict)
    
    # Returns the list.
    return incident_list

def save_incidents(incident_list, year):
    """
    Loops through a list and saves the objects.
    """
    print 'Saving year: %s' % year
    
    # Loop through the incident list.
    for incident in incident_list:

        # If you don't have a lat/lon, don't save.
        if incident['lat'] == float(0.0):
            print 'Ignoring incident: %s' % incident['id']
            pass
            
        # Otherwise, save.
        else:
            scraperwiki.sqlite.save(['id'], incident, table_name='dc_crime_incidents_%s' % year)

# Loop through years to get crime data.
for year in years:
    
    # Get the entries
    incidents = get_incidents(year)

    # Parse the entries.
    parsed_incidents = parse_incidents(incidents)

    # Save the entries.
    save_incidents(parsed_incidents, year)