print "This is a <em>fragment</em> of HTML."

import scraperwiki

scraperwiki.sqlite.attach("sample_7")
data = scraperwiki.sqlite.select(
    '''select * from `swdata` limit 10'''
)

print data


print "This is a <em>fragment</em> of HTML."

import scraperwiki

scraperwiki.sqlite.attach("sample_7")
data = scraperwiki.sqlite.select(
    '''select * from `swdata` limit 10'''
)

print data


