import scraperwiki
from threading import Thread

def worker(s):
    try:
        # scraperwiki.sqlite.save(unique_keys=['id'], data={'id': str(s[0]), 'url': str(s[1]) })
        print s
    except Exception as e:
        print "Error:", e
    print s
    return s[0]

# These are the parsing jobs we are going to queue up. It would be wonderful if this were
# a generator populated from a Queue as it would allow the worker function to add new urls
# to the ones being loaded.
urls = [ 'http://scraperwiki.com/hello_world.html?%d' % x for x in xrange(1,21)]


# We'll create two processes and pass in a tuple with an 'id' and a url for it to
# pretend to process. Note we fix the chunksize so that we don't end up with all jobs 
# sent to a single process.

threads = []
for i,u in enumerate(urls):
    t = Thread(target=worker, args=(u,))
    threads.append(t)
    t.start()
print "done?"
for t in threads: t.join()
print "done"
import scraperwiki
from threading import Thread

def worker(s):
    try:
        # scraperwiki.sqlite.save(unique_keys=['id'], data={'id': str(s[0]), 'url': str(s[1]) })
        print s
    except Exception as e:
        print "Error:", e
    print s
    return s[0]

# These are the parsing jobs we are going to queue up. It would be wonderful if this were
# a generator populated from a Queue as it would allow the worker function to add new urls
# to the ones being loaded.
urls = [ 'http://scraperwiki.com/hello_world.html?%d' % x for x in xrange(1,21)]


# We'll create two processes and pass in a tuple with an 'id' and a url for it to
# pretend to process. Note we fix the chunksize so that we don't end up with all jobs 
# sent to a single process.

threads = []
for i,u in enumerate(urls):
    t = Thread(target=worker, args=(u,))
    threads.append(t)
    t.start()
print "done?"
for t in threads: t.join()
print "done"
