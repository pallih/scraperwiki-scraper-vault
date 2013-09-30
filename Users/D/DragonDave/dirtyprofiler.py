import scraperwiki,time,random

def r():
    return {'lucky':random.randint(0,1e7)}

d={'animal':'cat'}
c=[]
iter=1000

scraperwiki.sqlite.save(unique_keys=[], data=d, table_name='demo') # first call is relatively expensive.

t=time.time()
for a in range(iter):
    c.append(r())
print "%f ms"% (1e3*(time.time()-t))
scraperwiki.sqlite.save(unique_keys=[], data=c, table_name='demo')
print "%f ms"% (1e3*(time.time()-t))

t=time.time()
for a in range(iter):
    scraperwiki.sqlite.save(unique_keys=[], data=r(), table_name='demo')
print "%f ms"% (1e3*(time.time()-t))


    


#s = "scraperwiki.sqlite.save(unique_keys=[], data={'animal':'cat'}, table_name='demo')"
#s = "a=0"
#t = timeit.Timer(stmt=s, 'from scraperwiki import save')
#print "%.2f usec/pass" % (1e6*t.timeit(number=iter)/iterimport scraperwiki,time,random

def r():
    return {'lucky':random.randint(0,1e7)}

d={'animal':'cat'}
c=[]
iter=1000

scraperwiki.sqlite.save(unique_keys=[], data=d, table_name='demo') # first call is relatively expensive.

t=time.time()
for a in range(iter):
    c.append(r())
print "%f ms"% (1e3*(time.time()-t))
scraperwiki.sqlite.save(unique_keys=[], data=c, table_name='demo')
print "%f ms"% (1e3*(time.time()-t))

t=time.time()
for a in range(iter):
    scraperwiki.sqlite.save(unique_keys=[], data=r(), table_name='demo')
print "%f ms"% (1e3*(time.time()-t))


    


#s = "scraperwiki.sqlite.save(unique_keys=[], data={'animal':'cat'}, table_name='demo')"
#s = "a=0"
#t = timeit.Timer(stmt=s, 'from scraperwiki import save')
#print "%.2f usec/pass" % (1e6*t.timeit(number=iter)/iter