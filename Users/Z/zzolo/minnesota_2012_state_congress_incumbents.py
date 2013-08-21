import re
import scraperwiki
import lxml.html
import demjson
import string
import urllib


def get_os_id(params):
    """
    Function to get Open States ID.  Please do not abuse API key.
    """
    apikey = '49c5c72c157d4b37892ddb52c63d06be'
    params['apikey'] = apikey

    os_url = create_os_url(params)
    raw = scraperwiki.scrape(os_url)
    os_data = demjson.decode(raw)
    os_found = len(os_data)
    os_id = ''

    # Use first if any found, if not remove last name
    if os_found > 0:
        os_id = os_data[0]['id']
    else:
        del params['first_name']
        os_url = create_os_url(params)
        raw = scraperwiki.scrape(os_url)
        os_data = demjson.decode(raw)
        os_found = str(len(os_data)) + '-removed-first'
        if len(os_data) > 0:
            os_id = os_data[0]['id']

    return {
        'found': os_found,
        'id': os_id
    }


def create_os_url(params):
    """
    Function to create Open States URL.
    """
    os_url = 'http://openstates.org/api/v1/legislators/?state=MN'
    os_url = os_url + '&active=true'
    os_url = os_url + '&' + urllib.urlencode(params)

    return os_url


def scrape_chamber(params):
    """
    Function to scrape chamber page.
    """

    chamber = params['chamber']
    year = params['year']
    url = 'http://www.gis.leg.mn/php/redist2010/incumbents.php?file=L' + params['year'] + '&type=' + params['chamber']
         
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    count = 0
    
    for tr in root.cssselect('table#matrix tr'):
        count = count + 1
        if count > 1:
            tds = tr.cssselect('td')
            if tds[1].text_content() != ' ' and tds[1].text_content() != '':
                # Make some values
                if tds[2].text_content().strip() == 'DFL':
                    os_party_name = 'Democratic-Farmer-Labor'
                else:
                    os_party_name = 'Republican'
    
                data_chamber = params['chamber']
                if data_chamber == 'senate':
                    os_chamber = 'upper'
                else:
                    os_chamber = 'lower'
    
                name_id = re.sub(r'\W+', '', tds[1].text_content()).strip().upper()
    
                split = tds[1].text_content().strip().split()
                last = split[-1]
                first = split[0]
                os_last = split[-1]
                os_first = split[0]
    
                # Massage data for OS
                if first == 'Gen' and last == 'Olson':
                    os_last = 'Gen'
                    os_first = 'Olson,'
                if first == 'Patricia' and last == 'Ray':
                    os_last = 'Torres Ray'
                    last = 'Torres Ray'
                # Moved to Senate
                if first == 'Lyle' and last == 'Koenen':
                    data_chamber = 'senate'
                    os_chamber = 'upper'
                
                # Passed away
                #if first == 'Gary' and last == 'Kubly':
                if first == 'Gene' and last == 'Jr':
                    os_last = 'Pelowski'
                    last = 'Pelowski'
                if first == 'Lyndon' and last == 'Sr.':
                    os_last = 'Carlson'
                    last = 'Carlson'
                if first == 'Tim' and last == 'Kelly':
                    party = 'R'
                    party_name = 'Republican'
                    os_party_name = 'Republican'
                    
    
                # Try to find Open States ID.  Please do not abuse this API Key
                os_results = get_os_id({
                    'party': os_party_name,
                    'chamber': os_chamber,
                    'first_name': os_first,
                    'last_name': os_last
                })
    
                data = {
                    'district' : tds[0].text_content().strip(),
                    'name' : tds[1].text_content().strip(),
                    'party' : tds[2].text_content().strip(),
                    'party_name' : os_party_name,
                    'previous_district' : tds[3].text_content().strip(),
                    'chamber' : data_chamber,
                    'year' : year,
                    'name_id': name_id,
                    'first': first,
                    'last': last,
                    'openstates_found': os_results['found'],
                    'openstates_id': os_results['id'],
                    'id': chamber + '-' + year + '-' + tds[2].text_content() + '-' + name_id
                }
    
                scraperwiki.sqlite.save(unique_keys=['id'], data=data)


# Make it happen!
scrape_chamber({
    'chamber': 'senate',
    'year': '2012'
})
scrape_chamber({
    'chamber': 'house',
    'year': '2012'
})