#from time import clock as t
from time import time as t 

t0=t()
import scraperwiki
t1=t()
print 'Scraperwiki import overhead:',t1-t0

t0=t()
g=scraperwiki.utils.swimport('geo_1')
t1=t()
print 'Swimport overhead', t1-t0
# Blank Python

t0=t()
for i in range(0,2):
    print g.Fetchdata('SW1A1AA')
t1=t()
print 'Fetchdata cost', t1-t0

t0=t()
for i in range(0,2):
    print scraperwiki.geo.gb_postcode_to_latlng('SW1A1AA')
t1=t()
print 'scraperwiki.geo cost', t1-t0#from time import clock as t
from time import time as t 

t0=t()
import scraperwiki
t1=t()
print 'Scraperwiki import overhead:',t1-t0

t0=t()
g=scraperwiki.utils.swimport('geo_1')
t1=t()
print 'Swimport overhead', t1-t0
# Blank Python

t0=t()
for i in range(0,2):
    print g.Fetchdata('SW1A1AA')
t1=t()
print 'Fetchdata cost', t1-t0

t0=t()
for i in range(0,2):
    print scraperwiki.geo.gb_postcode_to_latlng('SW1A1AA')
t1=t()
print 'scraperwiki.geo cost', t1-t0