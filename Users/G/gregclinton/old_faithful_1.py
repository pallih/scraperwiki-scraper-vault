import scraperwiki

scraperwiki.sqlite.attach('old_faithful') 
data = scraperwiki.sqlite.select('* from old_faithful.swdata')

print 'eruptions waiting'
for d in data:
    print d['eruptions'] + ' ' + d['waiting']
import scraperwiki

scraperwiki.sqlite.attach('old_faithful') 
data = scraperwiki.sqlite.select('* from old_faithful.swdata')

print 'eruptions waiting'
for d in data:
    print d['eruptions'] + ' ' + d['waiting']
