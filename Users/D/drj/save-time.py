import scraperwiki

import dateutil.parser

import timeit

setup="import scraperwiki;l = [dict(id=x) for x in range(1000)]"
t0 = timeit.timeit("scraperwiki.sqlite.save(['id'],l)", setup=setup, number=1)
print "bulk, verbose", t0
t1 = timeit.timeit("scraperwiki.sqlite.save(['id'],l,verbose=0)", setup=setup, number=1)
print "bulk, quiet", t1
t2 = timeit.timeit("for d in l: scraperwiki.sqlite.save(['id'],d,verbose=0)", setup=setup, number=1)
print "single, quiet", t2
t3 = timeit.timeit("for d in l: scraperwiki.sqlite.save(['id'],d,verbose=2)", setup=setup, number=1)
print "single, verbose", t3

import scraperwiki

import dateutil.parser

import timeit

setup="import scraperwiki;l = [dict(id=x) for x in range(1000)]"
t0 = timeit.timeit("scraperwiki.sqlite.save(['id'],l)", setup=setup, number=1)
print "bulk, verbose", t0
t1 = timeit.timeit("scraperwiki.sqlite.save(['id'],l,verbose=0)", setup=setup, number=1)
print "bulk, quiet", t1
t2 = timeit.timeit("for d in l: scraperwiki.sqlite.save(['id'],d,verbose=0)", setup=setup, number=1)
print "single, quiet", t2
t3 = timeit.timeit("for d in l: scraperwiki.sqlite.save(['id'],d,verbose=2)", setup=setup, number=1)
print "single, verbose", t3

