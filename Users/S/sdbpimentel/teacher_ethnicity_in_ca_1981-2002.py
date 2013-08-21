###############################################################################
#
# Number of Teachers in California by Ethnicity 1981 to 2004
# Fields (each category has a count and percentage measurement):
#      year
#      native_ct - American Indian/Alaskan Native
#      native_pctg
#      asian_ct
#      asian_pctg
#      islander_ct - Pacific Islander (counted as Asian before 1985)
#      islander_pctg
#      filipino_ct
#      filipino_pctg
#      hispanic_ct
#      hispanic_pctg
#      black_ct - Black, not Hispanic
#      black_pctg
#      white_ct - White, not hispanic
#      white_pctg
#      multiple_ct - Multiple/No Response
#      multiple_pctg
#      total
#
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.cde.ca.gov/ds/sd/dr/ethteach.asp'
html = scraperwiki.scrape(starting_url)
#print html

## Aux fn

def get_index(list_, index_, default="NA"):
    try:
        res = list_[index_]
    except IndexError:
        res = default
    return res

##

soup = BeautifulSoup(html)
div = soup.find('div', {'id':'maincontent'})
table = div.find('table')

rows = table.findAll('tr')

for row in rows[1:]:

    ct_vect = []
    pctg_vect = []
    cells = row.findAll('td')

    cols = range(len(cells))
    for i in cols[1:]:
        #split out count from percentage and store in respective vectors
        matches = re.match(r"([0-9,]+)\s+\(([0-9.]+%)\)", cells[i].text)
        
        if matches:
            ct_vect.append(matches.group(1))
            pctg_vect.append(matches.group(2))
        else:
            ct_vect.append("NA")
            pctg_vect.append("NA")

        record = {
            'year' : cells[0].text,
            'native_ct' : get_index(ct_vect, 0),
            'native_pctg' : get_index(pctg_vect, 0),
            'asian_ct' : get_index(ct_vect, 1),
            'asian_pctg' : get_index(pctg_vect, 1),
            'islander_ct' : get_index(ct_vect, 2),
            'islander_pctg' : get_index(pctg_vect, 2),
            'filipino_ct' : get_index(ct_vect, 3),
            'filipino_pctg' : get_index(pctg_vect, 3),
            'hispanic_ct' : get_index(ct_vect, 4),
            'hispanic_pctg' : get_index(pctg_vect, 4),
            'black_ct' : get_index(ct_vect, 5),
            'black_pctg' : get_index(pctg_vect, 5),
            'white_ct' : get_index(ct_vect, 6),
            'white_pctg' : get_index(pctg_vect, 6),
            'multiple_ct' : get_index(ct_vect, 7),
            'multiple_pctg' : get_index(pctg_vect, 7),
            'total' : get_index(ct_vect, 8)
        }

        # "datastore" is deprecated, use "sqlite" instead
        scraperwiki.sqlite.save(['year'], record)
