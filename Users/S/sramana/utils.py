"""Common utils that I use in my ScraperWiki scripts
"""

import atexit
import sys
import re
from datetime import datetime
import scraperwiki

scraperwiki.sqlite.execute("create table if not exists visited(url)")
visited = scraperwiki.sqlite.select("* from visited") or []
visited = set(rec['url'] for rec in visited)

batch_size = 100


# Used to save current state if CPU time exceeds
def cache(fn):
    def wrapper(url, *args, **kwargs):
        if url not in visited:
            try:
                #print "Processing", url
                fn(url, *args, **kwargs)
                visited.add(url)
            except Exception, e:
                print "Got exception '%s' (%s) while processing %s" % (str(e), type(e), url)
                if str(e) == 'ScraperWiki CPU time exceeded':
                    data = [dict(url=url) for url in list(visited)]
                    scraperwiki.sqlite.save(unique_keys=['url'], data=data, table_name="visited", verbose=0)
                    print "Saved the current state"
                    sys.exit(1)
    return wrapper


# Should decorate the main function
def clear_cache(fn):
    def wrapper(*args, **kwargs):
        fn(*args, **kwargs)
        scraperwiki.sqlite.execute("delete from visited")
    return wrapper


def clean_item(item):
    if type(item) is datetime:
        return item

    # Remove non-ascii characters
    item = unicode(item).encode("ascii", "ignore")

    # Remove escaped html characters like &nbsp;
    item = re.sub(r'&\S+;', '', item)

    # Remove extra whitespace
    item = ' '.join(item.split())

    # Convert to int/float if numeric
    try:
        item = float(item)
        if item.is_integer():
            item = int(item)
    except ValueError:
        pass

    return item


def clean_key(key):
    key = key.lower()
    key = clean_item(key)
    # Remove non-alnum chars
    key = ''.join(e if e.isalnum() else '_' for e in key)
    return key


def clean(data):
    cleaned_data = dict()
    cleaned_data['crawled_on'] = datetime.now()
    for k,v in data.iteritems():
        k = clean_key(k)
        v = clean_item(v)
        cleaned_data[k] = v
    return cleaned_data


def save(rec=None, flush=False, **kwargs):
    if rec:
        save.data.append(clean(rec))

    if len(save.data) >= batch_size or flush:
        scraperwiki.sqlite.save(unique_keys=save.unique_keys, data=save.data, verbose=0, **kwargs)
        save.data = []


save.data = []
save.unique_keys = []
atexit.register(save, flush=True)
