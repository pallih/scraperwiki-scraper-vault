import urllib

import scraperwiki
import requests

API_URL = 'http://is.gd/api.php?longurl='
LINKS_URL = 'http://make-bubbles.com/test.txt'
    
def shorten(uri):
    resp = requests.get(API_URL + urllib.quote(uri), timeout=30)
    if resp: 
        return resp.text
    else: 
        return False

links = requests.get(http://make-bubbles.com/test.txt).text.split('\n')
out = []
for one in filter(lambda x: x, links):    
    one = one.strip().strip('\r\n').strip('\n')
    scraperwiki.sqlite.save(unique_keys=['original'], data={'original': one, 'short': shorten(one)})
