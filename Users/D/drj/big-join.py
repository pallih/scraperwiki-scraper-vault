# slow queries via big join.
import random
import string
import time

import scraperwiki
 

# Equivalent to the api call.  This produces no load on the sql engine itself.  
# It's all about importing the data, which may require an IBodyProducer
#curl "http://localhost:9003/api?format=csv&name=big_join&query=select%20*%20from%20swdata%20join%20swdata+as%20j1+join+swdata+as+j2+join+swdata+as+j3+join+swdata+as+j4+join+swdata+as+j5+join+swdata+as+j6+join+swdata+as+j7+join+swdata+as+j8"



if 1:
    for i in range(3):
        scraperwiki.sqlite.save(['id'], dict(id=i, val=random.choice(string.letters) * i))

def njoin(n):
    """Create a query that joins the swdata table n times;
    if the table has k rows then we can expect the query
    to return k**n results.
    """
    assert n >= 1
    return "select * from swdata " + ' '.join("join swdata as j%d" % i  for i in range(n))

print time.asctime()
for i in range(1,13):
    print i, len(scraperwiki.sqlite.execute(njoin(i))['data']), time.asctime()

# Haven't seen it get here
print "This script has finished"
# slow queries via big join.
import random
import string
import time

import scraperwiki
 

# Equivalent to the api call.  This produces no load on the sql engine itself.  
# It's all about importing the data, which may require an IBodyProducer
#curl "http://localhost:9003/api?format=csv&name=big_join&query=select%20*%20from%20swdata%20join%20swdata+as%20j1+join+swdata+as+j2+join+swdata+as+j3+join+swdata+as+j4+join+swdata+as+j5+join+swdata+as+j6+join+swdata+as+j7+join+swdata+as+j8"



if 1:
    for i in range(3):
        scraperwiki.sqlite.save(['id'], dict(id=i, val=random.choice(string.letters) * i))

def njoin(n):
    """Create a query that joins the swdata table n times;
    if the table has k rows then we can expect the query
    to return k**n results.
    """
    assert n >= 1
    return "select * from swdata " + ' '.join("join swdata as j%d" % i  for i in range(n))

print time.asctime()
for i in range(1,13):
    print i, len(scraperwiki.sqlite.execute(njoin(i))['data']), time.asctime()

# Haven't seen it get here
print "This script has finished"
