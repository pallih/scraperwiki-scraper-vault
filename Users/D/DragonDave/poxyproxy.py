"""A bad proxy."""
import os, scraperwiki

import scraperwiki, urllib2, base64,time

# a cutdown version of lazycache to avoid downloading more than we need

def lazycache(url, verbose=False):
    # html is the data from the webpage; it might not be html.

    def scrapesave(url):
        if verbose: print "Downloading %s"%url
        html=urllib2.urlopen(url).read()
        scraperwiki.sqlite.save(table_name='__lazycache', data={'url':url,'payload':base64.b64encode(html)}, unique_keys=['url'], verbose=0)
        return html

    try:
        r=scraperwiki.sqlite.select("* from __lazycache where url=?", url, verbose=0) # attempt grab from database.
    except scraperwiki.sqlite.SqliteError, e: # if table doesn't exist, don't bother checking
        if 'no such table: __lazycache' not in str(e):
            raise
        return scrapesave(url)
    if len(r)>0:
        if verbose: print "Cache hit for %s"%url
        return base64.b64decode(r[0]['payload'])
    else:
        if verbose: print "No cache held for %s"%url
        return scrapesave(url)

paramdict =os.getenv("QUERY_STRING", "")
scraperwiki.utils.httpresponseheader("Content-Type", "application/octetstream")
print lazycache(urllib2.unquote(paramdict))
