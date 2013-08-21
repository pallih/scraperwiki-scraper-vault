import scraperwiki
import lxml.html
import pprint
import re


url = 'http://www.minneapolismn.gov/maps/neighborhoods'
domain = 'http://www.minneapolismn.gov'
last_updated = '2006-01-01'

n_translate_keys = {
}

# For the shapefile that we have, the name is off, so
# put it here so we can join it later.  Why would
# organizations want to be consistent?
n_shape_key = {
    'como': 'Como (Minneapolis)',
    'prospect_park_east_river': 'Prospect Park - East River Road',
    'stevens_square_loring_heights': "Steven's Square - Loring Heights"
}


def parse_num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return int(float(s))
        except ValueError:
            return 0


def string_to_key(str):
    str = re.sub('[^0-9a-zA-Z]+', '_', str)
    str = str.replace('__', '_')
    str = str.replace('__', '_')
    return str.lower()


def get_neighborhood_key(str):
    key = string_to_key(str)
    if key in n_translate_keys:
        key = n_translate_keys[key]
        
    return key


def get_shape_name(key, neighborhood):
    if key in n_shape_key:
        neighborhood = n_shape_key[key]

    return neighborhood



# Start scraping
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

rowCount = 0
for tda in root.cssselect('#maincontent table[cellpadding="4"] tr td a'):
    if rowCount >= 0:
        key = get_neighborhood_key(tda.text_content())

        data = {
            'neighborhood_key' : key,
            'neighborhood' : tda.text_content(),
            'shape_name': get_shape_name(key, tda.text_content()),
            'last_updated' : last_updated,
            'url' : domain + tda.attrib['href'],
        }
        #pprint.pprint(data)

        scraperwiki.sqlite.save(unique_keys=['neighborhood_key'], data=data)

    rowCount = rowCount + 1;