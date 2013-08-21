import scraperwiki, urllib2, datetime, base64,re

# TODO: Catch exception better
# TODO: Implement time-based cache removal (some stubs in, 'age' and 'date'
# TODO: change to just lazycache() ?
# TODO: add utility functions like flagging as done [raises exception if flag], clearing all marks.

class DoneError(Exception):
    pass

def done(targets,done=True,verbose=False):
    if type(targets)==str:
        urls=[targets]
    else:
        urls=targets
    data=[{'url':u, 'done':done} for u in urls]
    if verbose:
        print data
    scraperwiki.sqlite.save(table_name='__lazydone', data=data, unique_keys=['url'])

def purge(urls):
    try:
        scraperwiki.sqlite.execute('drop table __lazydone')
    except scraperwiki.sqlite.SqliteError,e:
        if 'no such table: __lazydone' not in str(e):
            raise

        # TODO: should probably build list of URLs to match.

def lazycache(url,age=datetime.timedelta(1), verbose=False, todo=False):
    # html is the data from the webpage; it might not be html.

    def scrapesave(url):
        if verbose==2: print "Downloading %s"%url
        html=urllib2.urlopen(url).read()
        scraperwiki.sqlite.save(table_name='__lazycache', data={
            'url':url,
            'payload':base64.b64encode(html),
            'date':datetime.datetime.now(),
            'done':False}, unique_keys=['url'], verbose=0)
        return html

    url=url.replace(' ','%20') # TODO: FIX THIS HACK
    if todo:
        try:
            if scraperwiki.sqlite.select('done from __lazydone where url=?',url,verbose=0):
                raise DoneError
        except scraperwiki.sqlite.SqliteError:
            pass

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


def test():
    try:
        scraperwiki.sqlite.execute("drop table __lazycache;") # reset to new condition
    except:
        pass
    try:
        html=lazycache('http://placekitten.com/g/200/300')
    except urllib2.HTTPError,e:
        print e
        pass
    html=lazycache('http://www.everything2.net', todo=True)
    print html
    done('http://www.everything2.net')
    html=lazycache('http://www.everything2.net', todo=True)
    k=lazycache('http://www.google.com',todo=True)
    print html
    print scraperwiki.sqlite.select('url from __lazycache')
    print scraperwiki.sqlite.select('url from __lazycache')

#test()