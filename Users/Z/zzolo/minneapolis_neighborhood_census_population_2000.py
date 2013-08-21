import scraperwiki
import lxml.html
import pprint
import re


url = 'http://www.ci.minneapolis.mn.us/census/2000/census_2000-race-and-ethnicity-by-neighborhood'

n_translate_keys = {
    'camden_ind_area': 'camden_industrial',
    'columbia': 'columbia_park',
    'east_phillips': 'phillips_east',
    'fowell': 'folwell',
    'humboldt_ind_area': 'humboldt_industrial_area',
    'midtown_phillips': 'phillips_midtown',
    'nicollet_island_east_bank': 'nicollet_island',
    'north_river_ind_area': 'north_river_industrial_area',
    'northrop': 'northrup',
    'prospect_park_east_river_rd': 'prospect_park',
    'prospect_park_east_river_road': 'prospect_park',
    'steven_s_square_loring_heights': 'stevens_square',
    'stevens_square_loring_heights': 'stevens_square',
    'stevens_square_loring_hgts': 'stevens_square',
    'u_of_m': 'university_of_minnesota',
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



# Start scraping
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

rowCount = 0
for tr in root.cssselect('#maincontent table tr'):
    if rowCount > 1:
        tds = tr.cssselect('td')
        data = {
            'neighborhood_key' : get_neighborhood_key(tds[0].text_content()),
            'neighborhood' : tds[0].text_content(),
            'total' : parse_num(tds[7].text_content()),
            'white' : parse_num(tds[1].text_content()),
            'black' : parse_num(tds[2].text_content()),
            'native' : parse_num(tds[3].text_content()),
            'asian' : parse_num(tds[4].text_content()),
            'other' : parse_num(tds[5].text_content()),
            'two' : parse_num(tds[6].text_content()),
            'dispanic' : parse_num(tds[8].text_content()),
        }
        #pprint.pprint(data)

        scraperwiki.sqlite.save(unique_keys=['neighborhood_key'], data=data)

    rowCount = rowCount + 1;