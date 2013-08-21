import scraperwiki

# Blank Python

print 'Creating index'
try:
    scraperwiki.sqlite.execute( 'create index id on swdata(id)' )
    scraperwiki.sqlite.commit()
except:
    pass
print 'Done'

for x in range(700,10000):
    scraperwiki.sqlite.save(['id'], {'id':x})import scraperwiki

# Blank Python

print 'Creating index'
try:
    scraperwiki.sqlite.execute( 'create index id on swdata(id)' )
    scraperwiki.sqlite.commit()
except:
    pass
print 'Done'

for x in range(700,10000):
    scraperwiki.sqlite.save(['id'], {'id':x})