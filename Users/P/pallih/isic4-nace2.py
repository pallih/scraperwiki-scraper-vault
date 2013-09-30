import scraperwiki
import urllib2
import csv



url = 'http://data2.d8tabit.net/ISIC4_NACE2.txt'

req = urllib2.Request(url)
response = urllib2.urlopen(req)
data = response.read()

#reader = csv.reader(data.splitlines())
reader = csv.DictReader(data.splitlines()) 
for row in reader:           
    #print row
    scraperwiki.sqlite.save(['ISIC4code', 'NACE2code'], data=row , table_name='ISIC4_vs_NACE2')

import scraperwiki
import urllib2
import csv



url = 'http://data2.d8tabit.net/ISIC4_NACE2.txt'

req = urllib2.Request(url)
response = urllib2.urlopen(req)
data = response.read()

#reader = csv.reader(data.splitlines())
reader = csv.DictReader(data.splitlines()) 
for row in reader:           
    #print row
    scraperwiki.sqlite.save(['ISIC4code', 'NACE2code'], data=row , table_name='ISIC4_vs_NACE2')

