import scraperwiki
import time
import sys
import sqlite3


#baseUrl = 'http://www.dublinked.ie/datastore/metadata'
baseUrl = 'http://www.dublinked.ie/datastore/dataset-'
#http://dublinked.com/datastore/datasets/dataset-059.php

from lxml.html import parse
from lxml.cssselect import CSSSelector

def cleanString(s):
    rem = '",;:.()'
    s = ''.join(x for x in s if x not in rem)
    return s


def scrapeDataset(index):
    try:
        record = {}
        record['id'] = index
        if i < 10:
            url = baseUrl + '00' + str(index) 
        elif (i >= 10 and i < 100):
            url = baseUrl + '0' + str(index) 
        else:
            url = baseUrl + str(index)
        record['url'] = url + ".php"
        website = parse(url).getroot()
        selector = website.cssselect('div.metadata-line')

        for element in selector:
            ch = element.getchildren()
            metatag = ''
            metacontent = ''

            for c in ch:
                if c.cssselect('div.metadata-tag'):
                    metatag = cleanString(''.join(c.text_content().split()))

                elif c.cssselect('div.metadata-content'):
                    metacontent = c.text
            record[metatag] = metacontent 

        print record
        scraperwiki.sqlite.save(unique_keys=['url'], data=[record])

    except:
        print sys.exc_info()[0]
        None
        #nothing

min = 201
max = 301
for i in range(min,max):
    scrapeDataset(i)
    time.sleep(1)

