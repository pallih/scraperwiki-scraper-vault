import scraperwiki, csv,urllib

url='http://transactionalservices.alphagov.co.uk/?orderBy=volume&direction=desc&format=csv'
# Blank Python

def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass

dropper('transactions')

nReader = csv.DictReader(urllib.urlopen(url))
for nrow in nReader:
    scraperwiki.sqlite.save(unique_keys=[], table_name='transactions', data=nrow)import scraperwiki, csv,urllib

url='http://transactionalservices.alphagov.co.uk/?orderBy=volume&direction=desc&format=csv'
# Blank Python

def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass

dropper('transactions')

nReader = csv.DictReader(urllib.urlopen(url))
for nrow in nReader:
    scraperwiki.sqlite.save(unique_keys=[], table_name='transactions', data=nrow)