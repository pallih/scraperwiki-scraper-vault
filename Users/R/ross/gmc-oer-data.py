import scraperwiki
import csv
import hashlib

scraperwiki.sqlite.attach( 'gmc-oer' )
csvs = scraperwiki.sqlite.select( 'name,csv from `gmc-oer`.links' )

for csvobj in csvs:           
    ctr = []
    data = scraperwiki.scrape( csvobj['csv'] )
    reader = csv.DictReader(data.splitlines())  
    id = 0
    for row in reader:
        print row
        id = id + 1
        row['Id'] = str(hashlib.sha224( '%s_%d' % (csvobj['csv'],id,) ).hexdigest())
        ctr.append(row)
    scraperwiki.sqlite.save(['Id'], data=ctr, table_name='report')import scraperwiki
import csv
import hashlib

scraperwiki.sqlite.attach( 'gmc-oer' )
csvs = scraperwiki.sqlite.select( 'name,csv from `gmc-oer`.links' )

for csvobj in csvs:           
    ctr = []
    data = scraperwiki.scrape( csvobj['csv'] )
    reader = csv.DictReader(data.splitlines())  
    id = 0
    for row in reader:
        print row
        id = id + 1
        row['Id'] = str(hashlib.sha224( '%s_%d' % (csvobj['csv'],id,) ).hexdigest())
        ctr.append(row)
    scraperwiki.sqlite.save(['Id'], data=ctr, table_name='report')import scraperwiki
import csv
import hashlib

scraperwiki.sqlite.attach( 'gmc-oer' )
csvs = scraperwiki.sqlite.select( 'name,csv from `gmc-oer`.links' )

for csvobj in csvs:           
    ctr = []
    data = scraperwiki.scrape( csvobj['csv'] )
    reader = csv.DictReader(data.splitlines())  
    id = 0
    for row in reader:
        print row
        id = id + 1
        row['Id'] = str(hashlib.sha224( '%s_%d' % (csvobj['csv'],id,) ).hexdigest())
        ctr.append(row)
    scraperwiki.sqlite.save(['Id'], data=ctr, table_name='report')import scraperwiki
import csv
import hashlib

scraperwiki.sqlite.attach( 'gmc-oer' )
csvs = scraperwiki.sqlite.select( 'name,csv from `gmc-oer`.links' )

for csvobj in csvs:           
    ctr = []
    data = scraperwiki.scrape( csvobj['csv'] )
    reader = csv.DictReader(data.splitlines())  
    id = 0
    for row in reader:
        print row
        id = id + 1
        row['Id'] = str(hashlib.sha224( '%s_%d' % (csvobj['csv'],id,) ).hexdigest())
        ctr.append(row)
    scraperwiki.sqlite.save(['Id'], data=ctr, table_name='report')