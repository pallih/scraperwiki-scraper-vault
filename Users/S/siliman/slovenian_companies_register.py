import urllib2
import csv
import codecs
import scraperwiki
import re

str = '- - -------- ---------- ---------- ------ ---------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------- --'
csizes = [len(cticks) for cticks in str.split()]

fileFo = urllib2.urlopen('http://datoteke.durs.gov.si/DURS_zavezanci_DEJ.txt') # fizicne osebe

counter = 0;

for st2 in fileFo:

    start, row = 0, []

    for csize in csizes:
        column = st2[start:start+csize]
        row.append(column.strip().decode('cp1250').encode('utf8'))
        start = start + csize + 1

    li = {}
    
    li['tip'] = '0'
    li['davcna_stevilka'] = row[3]
    li['naziv'] = row[6]
    li['naslov'] = row[7]
    
    scraperwiki.sqlite.save(unique_keys=['uid'], data=li)
    


str = '-  -  -------- ---------- ----------  ------  ----------------------------------------------------------------------------------------------------     -----------------------------------------------------------------------------------------------------------------  --'
csizes = [len(cticks) for cticks in str.split()]

filePo = urllib2.urlopen('http://datoteke.durs.gov.si/DURS_zavezanci_PO.txt') # pravne osebe

counter = 0;

for st2 in filePo:

    start, row = 0, []

    for csize in csizes:
        column = st2[start:start+csize]
        row.append(column.strip().decode('cp1250').encode('utf8'))
        start = start + csize + 1

    li = {}
    
    li['tip'] = '1'
    li['davcna_stevilka'] = row[3]
    li['naziv'] = row[6]
    li['naslov'] = row[7]

    scraperwiki.sqlite.save(unique_keys=['uid'], data=li)

