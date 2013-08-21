import json
import re
import time
from BeautifulSoup import BeautifulSoup
import scraperwiki

# get the data currently in the db
db_data = scraperwiki.sqlite.select("* from swdata")
db_data = {x['id']:x for x in db_data}

# URL containing a full list of courts
list_page_url = 'http://hmctscourtfinder.justice.gov.uk/HMCTS/'

# partial URL for court pages
court_page_url = 'http://hmctscourtfinder.justice.gov.uk/HMCTS/Search.do?court_id='

# fetch all the IDs for the court pages
soup = BeautifulSoup(scraperwiki.scrape(list_page_url))
options = soup.find('select', {'name': 'court_id'}).findAll('option')
ids = [option['value'] for option in options]
ids = ids[1:]

for x in ids:
    soup = BeautifulSoup(scraperwiki.scrape(court_page_url + x))
    
    # At least one court page returns a weird ServletException error.
    # Report it and carry on
    if soup.find(text=re.compile('ServletException')):
        print "ServletException error - court ID: " + x
        continue

    # initialise a dict for this row
    values = {
        'divorce': False,
        'id': int(x),
        'address': '',
    }

    # the court name
    values['name'] = soup.find('div', {'class': 'steps'}).find('h2').string

    # figure out whether this court handles divorce cases
    try:
        if soup.find(text=re.compile("Work type")).parent.parent.find(text=re.compile("Divorce")).strip() == "Divorce":
            # the current court does handle divorce cases, so we note this
            values['divorce'] = True
    except AttributeError:
        pass

    # the court address
    address = soup.find(text=re.compile("Postal Address")).parent.parent
    # remove child tags e.g. <br>s
    [remove.replaceWith('') for remove in address.findAll()]
    for address_line in address.contents:
        # clean up the address
        address_line = re.sub('(\t|\n|\r)+', '\n', address_line.strip(' \t\n\r'))
        if address_line:
            values['address'] += address_line + '\n'
            postcode = scraperwiki.geo.extract_gb_postcode(address_line)
            if postcode:
                if db_data[int(x)] and db_data[int(x)]['postcode'] == postcode and db_data[int(x)]['lat']:
                    # the postcode hasn't changed and we have a geocode, so don't geocode again
                    values['lat'] = db_data[int(x)]['lat']
                    values['lng'] = db_data[int(x)]['lng']
                else:
                    # use the scraperwiki geocoder
                    values['lat'], values['lng'] = scraperwiki.geo.gb_postcode_to_latlng(postcode)
                values['postcode'] = postcode
                # stop when we hit the postcode
                break

    # save as a row in the db
    scraperwiki.sqlite.save(["id"], values, table_name="swdata")

    # rate limit to one per second
    time.sleep(1)
