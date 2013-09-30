import scraperwiki
import sys
import time


scraperwiki.sqlite.attach('us_nuclear_power_reactor_status_reports')



x = scraperwiki.sqlite.get_var('last_item', 0)
line_count = 0
print 'Start - Setting offset to %s' % x

for line in scraperwiki.sqlite.select(" * from swdata order by date limit 50000 offset %s" % (x) ):
    line_count = line_count + 1
    x = x + 1
    print 'Updating last processed to %s' % x
    
    print line
    reason = line[u'Reason or Comment']
    if reason != None and '#' in reason:
        description = 'On %s, %s reactor had power output of %s because %s' % (line[u'date'], line[u'Unit'], line[u'Power'], reason)

scraperwiki.sqlite.save_var('last_item', x )
scraperwiki.sqlite.save(

select Unit as title, `Reason or Comment` as description,  `http://www.nrc.gov/info-finder/reactor/index.html`as link,  from `swdata` limit 10
import scraperwiki
import sys
import time


scraperwiki.sqlite.attach('us_nuclear_power_reactor_status_reports')



x = scraperwiki.sqlite.get_var('last_item', 0)
line_count = 0
print 'Start - Setting offset to %s' % x

for line in scraperwiki.sqlite.select(" * from swdata order by date limit 50000 offset %s" % (x) ):
    line_count = line_count + 1
    x = x + 1
    print 'Updating last processed to %s' % x
    
    print line
    reason = line[u'Reason or Comment']
    if reason != None and '#' in reason:
        description = 'On %s, %s reactor had power output of %s because %s' % (line[u'date'], line[u'Unit'], line[u'Power'], reason)

scraperwiki.sqlite.save_var('last_item', x )
scraperwiki.sqlite.save(

select Unit as title, `Reason or Comment` as description,  `http://www.nrc.gov/info-finder/reactor/index.html`as link,  from `swdata` limit 10
