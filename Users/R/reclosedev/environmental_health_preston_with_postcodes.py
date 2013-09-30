#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests

import scraperwiki.sqlite as db


# All data from Zarino Zappia's scrapper https://scraperwiki.com/scrapers/environmental_health_preston/
DATA_URL = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=environmental_health_preston&query=select%20*%20from%20%60eateries%60'

def main():
    data = json.loads(requests.get(DATA_URL, verify=False).content)
    postcodes = json.loads(requests.get('http://pastebin.com/raw.php?i=XUXaUHwD').content)
    for entry in data:
        entry['postcode'] = postcodes[entry['url']]
    db.save(['url'], data, verbose=0)
main()#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests

import scraperwiki.sqlite as db


# All data from Zarino Zappia's scrapper https://scraperwiki.com/scrapers/environmental_health_preston/
DATA_URL = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=environmental_health_preston&query=select%20*%20from%20%60eateries%60'

def main():
    data = json.loads(requests.get(DATA_URL, verify=False).content)
    postcodes = json.loads(requests.get('http://pastebin.com/raw.php?i=XUXaUHwD').content)
    for entry in data:
        entry['postcode'] = postcodes[entry['url']]
    db.save(['url'], data, verbose=0)
main()