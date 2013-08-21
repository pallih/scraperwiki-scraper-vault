import scraperwiki, urllib2, datetime, base64,time, logging

# TODO: Implement time-based cache removal (some stubs in, 'age' and 'date'

def lazycache(url,age=datetime.timedelta(1), verbose=False, delay=0):
    # html is the data from the webpage; it might not be html.

    def scrapesave(url):
        if verbose: print "Downloading %s"%url
        try:
            html=urllib2.urlopen(url).read()
        except:
            html=urllib2.urlopen(url).read()
        scraperwiki.sqlite.save(table_name='__lazycache', data={'url':url,'payload':base64.b64encode(html),'date':datetime.datetime.now()}, unique_keys=['url'], verbose=0)
        return html

    if ' ' in url:
        logging.warn('URL "%s" contains spaces.'%url)
        url=url.replace(' ','%20')
        logging.warn('Using "%s"'%url)
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
        if delay:
            if verbose: print "sleeping"
            time.sleep(delay)
        return scrapesave(url)




#scraperwiki.sqlite.execute("drop table __lazycache;") # reset to new condition
#html=lazycache('http://placekitten.com/g/200/300')
#html=lazycache('http://www.everything2.net')
#print html
#html=lazycache('http://www.everything2.net')
#print html

