import scraperwiki
from bs4 import BeautifulSoup

import string
import urllib2
import urlparse
import re

## Starting with the studio page

url = "http://www.bicyclepaintings.com/studio10/flip-flop-tank/studioindex.html"

soup = BeautifulSoup(urllib2.urlopen(url))

path = urlparse.urlsplit(url).path.split("/")


top_table = BeautifulSoup(soup.find('table').prettify())
studio_img = top_table.find('img').attrs['src']

data = {
    "year"               : path[1],
    "painting_shortname" : path[2],
    "original_url"       : url,
    "painting_title"     : top_table.find('h1').text,
    "studio_img"         : urlparse.urljoin(url,studio_img)
}

## the blurbs need to get the breaks pulled out and the relative URLs made absolute.

ugly_blurb = top_table.p.font

# maybe we can make a list of tuples, replace this with that, to run on the blurb.
# http://stackoverflow.com/questions/1175540/iterative-find-replace-from-a-list-of-tuples-in-python

# start the replace list with <br> tags, which we know we want out. 
replace_list = [("<br/>"," ")]



for link in ugly_blurb.find_all('a'):
    if "../" in link.get('href'):
#        print urlparse.urljoin(url,link.get('href'))
        pair = link.get('href'), urlparse.urljoin(url,link.get('href'))
        replace_list.append(pair)
#    else:
#        print link.get('href')
    
print replace_list

REPLACEMENTS = dict(replace_list)

def replacer(m):
    return REPLACEMENTS[m.group(0)]

r = re.compile('|'.join(REPLACEMENTS.keys()))

blurb = r.sub(replacer, str(ugly_blurb))

pretty_blurb = re.sub('\s+',' ',str(blurb)).strip()

print pretty_blurb

for p in pretty_blurb.find('p'):
    print p.contents


scraperwiki.sqlite.save(table_name="studios", unique_keys=['original_url'], data=data)


cells = soup.find_all('td',{'valign':'bottom'})


