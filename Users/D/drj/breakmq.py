import scraperwiki

import random
import string
import time
import urllib2
import uuid

def isodate():
    import time
    return time.strftime("%Y%m%dT%H%M%S")

session = uuid.uuid4()
scraperwiki.sqlite.save(['session', 'stage'], dict(session=session, stage='start', time=isodate()), table_name='lifecycle')
try:
    for i in range(99999):
        p = ''.join(random.choice(string.letters) for _ in range(4))
        urllib2.urlopen("http://open.mapquestapi.com/nominatim/v1/search?format=json&json_callback=&q=%s" % p)
        scraperwiki.sqlite.save(['session'], dict(session=session, state=i, time=isodate()), verbose=False)
        time.sleep(random.random() * 0.2)
    scraperwiki.sqlite.save(['session'], dict(session=session, state='finished', time=isodate()))
except Exception as e:
    scraperwiki.sqlite.save(['session'], dict(session=session, exception=str(e), time=isodate()), table_name='exception')
scraperwiki.sqlite.save(['session', 'stage'], dict(session=session, stage='stop', time=isodate()), table_name='lifecycle')
import scraperwiki

import random
import string
import time
import urllib2
import uuid

def isodate():
    import time
    return time.strftime("%Y%m%dT%H%M%S")

session = uuid.uuid4()
scraperwiki.sqlite.save(['session', 'stage'], dict(session=session, stage='start', time=isodate()), table_name='lifecycle')
try:
    for i in range(99999):
        p = ''.join(random.choice(string.letters) for _ in range(4))
        urllib2.urlopen("http://open.mapquestapi.com/nominatim/v1/search?format=json&json_callback=&q=%s" % p)
        scraperwiki.sqlite.save(['session'], dict(session=session, state=i, time=isodate()), verbose=False)
        time.sleep(random.random() * 0.2)
    scraperwiki.sqlite.save(['session'], dict(session=session, state='finished', time=isodate()))
except Exception as e:
    scraperwiki.sqlite.save(['session'], dict(session=session, exception=str(e), time=isodate()), table_name='exception')
scraperwiki.sqlite.save(['session', 'stage'], dict(session=session, stage='stop', time=isodate()), table_name='lifecycle')
