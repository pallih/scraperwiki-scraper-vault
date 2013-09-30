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
    if row[1] == '*':
        li['ddv_payer'] = 1
    else:
        li['ddv_payer'] = 0
    
    li['type'] = 'individual'
    li['uid'] = row[2] # maticna stevilka
    li['tax_number'] = row[3]
    li['main_aspect'] = row[5]
    li['company_name'] = row[6]
    li['address'] = row[7]
    
    ns = row[7].split(',')
    
    nk = ns.pop().strip().split(' ')
    nu = " ".join(ns).strip().split(' ')
    naslov_stevilka = nu.pop()
    naslov_ulica = " ".join(nu).strip()
    naslov_zip = nk.pop(0)
    naslov_kraj = " ".join(nk).strip()
    
    li['street'] = naslov_ulica
    li['street_number'] = naslov_stevilka
    li['zip_name'] = naslov_kraj
    li['zip'] = naslov_zip    
    li['tax_authority'] = row[8]

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
    if row[1] == '*':
        li['ddv_payer'] = 1
    else:
        li['ddv_payer'] = 0
    
    li['type'] = 'legal entity'
    li['uid'] = row[2] # maticna stevilka
    li['tax_number'] = row[3]
    li['main_aspect'] = row[5]
    li['company_name'] = row[6]
    li['address'] = row[7]
    
    ns = row[7].split(',')
     
    if len(re.sub("[^0-9]", "", row[3].strip())) == 10:
         nk = ns.pop().strip().split(' ')
         nu = " ".join(ns).strip().split(' ')
         naslov_stevilka = nu.pop()
         naslov_ulica = " ".join(nu).strip()
         naslov_zip = nk.pop(0)
         naslov_kraj = " ".join(nk).strip()
    else:
         naslov_stevilka = ''
         naslov_zip = ''
         naslov_ulica = ''
         naslov_kraj = ''
    
    li['street'] = naslov_ulica
    li['street_number'] = naslov_stevilka
    li['zip_name'] = naslov_kraj
    li['zip'] = naslov_zip    
    li['tax_authority'] = row[8]

    scraperwiki.sqlite.save(unique_keys=['uid'], data=li)

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
    if row[1] == '*':
        li['ddv_payer'] = 1
    else:
        li['ddv_payer'] = 0
    
    li['type'] = 'individual'
    li['uid'] = row[2] # maticna stevilka
    li['tax_number'] = row[3]
    li['main_aspect'] = row[5]
    li['company_name'] = row[6]
    li['address'] = row[7]
    
    ns = row[7].split(',')
    
    nk = ns.pop().strip().split(' ')
    nu = " ".join(ns).strip().split(' ')
    naslov_stevilka = nu.pop()
    naslov_ulica = " ".join(nu).strip()
    naslov_zip = nk.pop(0)
    naslov_kraj = " ".join(nk).strip()
    
    li['street'] = naslov_ulica
    li['street_number'] = naslov_stevilka
    li['zip_name'] = naslov_kraj
    li['zip'] = naslov_zip    
    li['tax_authority'] = row[8]

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
    if row[1] == '*':
        li['ddv_payer'] = 1
    else:
        li['ddv_payer'] = 0
    
    li['type'] = 'legal entity'
    li['uid'] = row[2] # maticna stevilka
    li['tax_number'] = row[3]
    li['main_aspect'] = row[5]
    li['company_name'] = row[6]
    li['address'] = row[7]
    
    ns = row[7].split(',')
     
    if len(re.sub("[^0-9]", "", row[3].strip())) == 10:
         nk = ns.pop().strip().split(' ')
         nu = " ".join(ns).strip().split(' ')
         naslov_stevilka = nu.pop()
         naslov_ulica = " ".join(nu).strip()
         naslov_zip = nk.pop(0)
         naslov_kraj = " ".join(nk).strip()
    else:
         naslov_stevilka = ''
         naslov_zip = ''
         naslov_ulica = ''
         naslov_kraj = ''
    
    li['street'] = naslov_ulica
    li['street_number'] = naslov_stevilka
    li['zip_name'] = naslov_kraj
    li['zip'] = naslov_zip    
    li['tax_authority'] = row[8]

    scraperwiki.sqlite.save(unique_keys=['uid'], data=li)

