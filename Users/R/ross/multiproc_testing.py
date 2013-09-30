import sys
from multiprocessing import Pool

def expose_code(code):
    """
    So that we can use multiprocessing pools we need to
    make sure the code we want to run is loadable - and as we 
    can't have more than one file in scraperwiki we'll write it 
    to disk and then load it again :) If we just tried to use a 
    normal function it'd fail to pickle.
    """
    f = open('/tmp/worker.py', 'w')
    f.write( code )
    f.close()   
    sys.path.append('/tmp')

# This is the code we want to run.  I wanted this to be a
# normal function with the code loaded as a string using inspect, but 
# guess what - inspect doesn't like the code not being in a file.
# Once we've defined the code, we will call the expose func to write
# it to disk for us.
code = """
def worker(s):
    import os, scraperwiki
    try:
        scraperwiki.sqlite.save(unique_keys=['id'], data={'id': str(s[0]), 'url': str(s[1]) })
    except Exception as e:
        print "Error:", e
    print s
    return s[0]
"""
expose_code(code)

# And then import the code we just wrote
from worker import worker

# These are the parsing jobs we are going to queue up. It would be wonderful if this were
# a generator populated from a Queue as it would allow the worker function to add new urls
# to the ones being loaded.
urls = [ 'http://scraperwiki.com/hello_world.html?%d' % x for x in xrange(1,21)]


# We'll create two processes and pass in a tuple with an 'id' and a url for it to
# pretend to process. Note we fix the chunksize so that we don't end up with all jobs 
# sent to a single process.
pool = Pool(processes=2)  
responses = pool.map(worker,[(i,u,) for i,u in enumerate(urls)], chunksize=1) 
pool.close()
pool.join()
print '*' * 80
print 'We got a total of %d responses and a sum of %d' % (len(responses), sum(responses),)

import sys
from multiprocessing import Pool

def expose_code(code):
    """
    So that we can use multiprocessing pools we need to
    make sure the code we want to run is loadable - and as we 
    can't have more than one file in scraperwiki we'll write it 
    to disk and then load it again :) If we just tried to use a 
    normal function it'd fail to pickle.
    """
    f = open('/tmp/worker.py', 'w')
    f.write( code )
    f.close()   
    sys.path.append('/tmp')

# This is the code we want to run.  I wanted this to be a
# normal function with the code loaded as a string using inspect, but 
# guess what - inspect doesn't like the code not being in a file.
# Once we've defined the code, we will call the expose func to write
# it to disk for us.
code = """
def worker(s):
    import os, scraperwiki
    try:
        scraperwiki.sqlite.save(unique_keys=['id'], data={'id': str(s[0]), 'url': str(s[1]) })
    except Exception as e:
        print "Error:", e
    print s
    return s[0]
"""
expose_code(code)

# And then import the code we just wrote
from worker import worker

# These are the parsing jobs we are going to queue up. It would be wonderful if this were
# a generator populated from a Queue as it would allow the worker function to add new urls
# to the ones being loaded.
urls = [ 'http://scraperwiki.com/hello_world.html?%d' % x for x in xrange(1,21)]


# We'll create two processes and pass in a tuple with an 'id' and a url for it to
# pretend to process. Note we fix the chunksize so that we don't end up with all jobs 
# sent to a single process.
pool = Pool(processes=2)  
responses = pool.map(worker,[(i,u,) for i,u in enumerate(urls)], chunksize=1) 
pool.close()
pool.join()
print '*' * 80
print 'We got a total of %d responses and a sum of %d' % (len(responses), sum(responses),)

import sys
from multiprocessing import Pool

def expose_code(code):
    """
    So that we can use multiprocessing pools we need to
    make sure the code we want to run is loadable - and as we 
    can't have more than one file in scraperwiki we'll write it 
    to disk and then load it again :) If we just tried to use a 
    normal function it'd fail to pickle.
    """
    f = open('/tmp/worker.py', 'w')
    f.write( code )
    f.close()   
    sys.path.append('/tmp')

# This is the code we want to run.  I wanted this to be a
# normal function with the code loaded as a string using inspect, but 
# guess what - inspect doesn't like the code not being in a file.
# Once we've defined the code, we will call the expose func to write
# it to disk for us.
code = """
def worker(s):
    import os, scraperwiki
    try:
        scraperwiki.sqlite.save(unique_keys=['id'], data={'id': str(s[0]), 'url': str(s[1]) })
    except Exception as e:
        print "Error:", e
    print s
    return s[0]
"""
expose_code(code)

# And then import the code we just wrote
from worker import worker

# These are the parsing jobs we are going to queue up. It would be wonderful if this were
# a generator populated from a Queue as it would allow the worker function to add new urls
# to the ones being loaded.
urls = [ 'http://scraperwiki.com/hello_world.html?%d' % x for x in xrange(1,21)]


# We'll create two processes and pass in a tuple with an 'id' and a url for it to
# pretend to process. Note we fix the chunksize so that we don't end up with all jobs 
# sent to a single process.
pool = Pool(processes=2)  
responses = pool.map(worker,[(i,u,) for i,u in enumerate(urls)], chunksize=1) 
pool.close()
pool.join()
print '*' * 80
print 'We got a total of %d responses and a sum of %d' % (len(responses), sum(responses),)

import sys
from multiprocessing import Pool

def expose_code(code):
    """
    So that we can use multiprocessing pools we need to
    make sure the code we want to run is loadable - and as we 
    can't have more than one file in scraperwiki we'll write it 
    to disk and then load it again :) If we just tried to use a 
    normal function it'd fail to pickle.
    """
    f = open('/tmp/worker.py', 'w')
    f.write( code )
    f.close()   
    sys.path.append('/tmp')

# This is the code we want to run.  I wanted this to be a
# normal function with the code loaded as a string using inspect, but 
# guess what - inspect doesn't like the code not being in a file.
# Once we've defined the code, we will call the expose func to write
# it to disk for us.
code = """
def worker(s):
    import os, scraperwiki
    try:
        scraperwiki.sqlite.save(unique_keys=['id'], data={'id': str(s[0]), 'url': str(s[1]) })
    except Exception as e:
        print "Error:", e
    print s
    return s[0]
"""
expose_code(code)

# And then import the code we just wrote
from worker import worker

# These are the parsing jobs we are going to queue up. It would be wonderful if this were
# a generator populated from a Queue as it would allow the worker function to add new urls
# to the ones being loaded.
urls = [ 'http://scraperwiki.com/hello_world.html?%d' % x for x in xrange(1,21)]


# We'll create two processes and pass in a tuple with an 'id' and a url for it to
# pretend to process. Note we fix the chunksize so that we don't end up with all jobs 
# sent to a single process.
pool = Pool(processes=2)  
responses = pool.map(worker,[(i,u,) for i,u in enumerate(urls)], chunksize=1) 
pool.close()
pool.join()
print '*' * 80
print 'We got a total of %d responses and a sum of %d' % (len(responses), sum(responses),)

