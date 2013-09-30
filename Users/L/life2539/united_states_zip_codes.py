#!/usr/bin/env python
from urllib2 import urlopen
from csv import reader, writer
from scraperwiki.sqlite import save, select

URL='http://www.census.gov/tiger/tms/gazetteer/zips.txt'
COLS=('state_num','zip','state','city','lng','lat','dunno1','dunno2')
#"01","35004","AL","ACMAR",86.51557,33.584132,6055,0.001499 

def main():
    get_zips(urlopen(URL))

def get_zips(source):
    zipCsv=reader(source)
    for row in zipCsv:
        d={}
        for i in range(len(COLS)):
            value=row[i]
            try:
                value=int(value)
            except ValueError:
                if '.' in value:
                    value=float(value)
            d[COLS[i]]=value
        save(['zip'],d,'zipcodes')

main()#!/usr/bin/env python
from urllib2 import urlopen
from csv import reader, writer
from scraperwiki.sqlite import save, select

URL='http://www.census.gov/tiger/tms/gazetteer/zips.txt'
COLS=('state_num','zip','state','city','lng','lat','dunno1','dunno2')
#"01","35004","AL","ACMAR",86.51557,33.584132,6055,0.001499 

def main():
    get_zips(urlopen(URL))

def get_zips(source):
    zipCsv=reader(source)
    for row in zipCsv:
        d={}
        for i in range(len(COLS)):
            value=row[i]
            try:
                value=int(value)
            except ValueError:
                if '.' in value:
                    value=float(value)
            d[COLS[i]]=value
        save(['zip'],d,'zipcodes')

main()