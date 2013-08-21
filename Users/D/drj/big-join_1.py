# Slow queries (that have a small result) via big join.
# This one should produce a SqliteError ("Query timeout").
# If it actually runs to completion, try increasing *N*.
import random
import string
import time

import scraperwiki

# On 2012-01-11 this fails with a timeout when attempting i=15.
# Each successive query should be about 3 times slower (the number of rows in the table).
N = 17

# Note: idempotent.
for i in range(3):
    scraperwiki.sqlite.save(['id'], dict(id=i, val=random.choice(string.letters) * i))

def njoin(n):
    """Create a query that joins the swdata table n times;
    the id column is sum'd so the query should take time O(k**n),
    when the table has k rows, but the result will be small.
    """
    assert n >= 1
    # a subclause of our sql expression.
    s = "sum(" + "+".join(("j%d.id" % i) for i in range(n)) + ")"
    return "select " + s + " from swdata " + ' '.join("join swdata as j%d" % i  for i in range(n))

print time.asctime()
for i in range(1,N):
    for a in range(2):
        try:
            print i, scraperwiki.sqlite.execute(njoin(i))['data'], time.asctime()
        except Exception as e:
            print e
            if a > 0:
                break

# Haven't seen it get here
print "This script has finished"
