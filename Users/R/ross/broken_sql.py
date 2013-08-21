# Blank Python
print 's'
import scraperwiki

scraperwiki.sqlite.save('id', {'id':1})
print scraperwiki.sqlite.execute( 'show tables') 