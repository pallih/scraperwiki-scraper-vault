# Blank Python
sourcescraper = 'smbc-forum' # and 'smbc-comicside'

import cgi, os, scraperwiki

def politecrash(text="Sorry about that."):
    print """
<h1>Something went wrong.</h1>
<p>%s</p>
<p>If you want to raise the issue, email dave.mckee@gmail.com with the URL you used.</p>
"""%text
    exit()

try:
    query= dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
    comic=int(query['comic'])
except:
    politecrash("URLs are of the form https://views.scraperwiki.com/run/smbc-view/?comic=666")
try:
    scraperwiki.sqlite.attach('smbc-comicside')
    scraperwiki.sqlite.attach('smbc-forum')
    # get ALL: select * from `forum` where date in (select date from `swdata`)
    dates=scraperwiki.sqlite.select("date from `swdata` where id=%s limit 1"%comic)
    date=dates[0]['date']
    # next line old
    #data= scraperwiki.sqlite.select("url from forum where date in (select date from `swdata` where id=%s limit 1)"%comic)
    data=scraperwiki.sqlite.select("url from forum where date in (select max(date) from forum where date <= '%s')"%date)
    
except Exception,e:
    politecrash("It's something to do with the SQL database, it said '%s'."% e)
if not data:
    politecrash("""I can't find a forum discussion dated %s on the website: if you want to create one, start your thread title with [Date].<br>(Many older comics don't have forum discussions.)"""%str(date))
try:
    print """<html><head><meta HTTP-EQUIV="REFRESH" content="0; url=http://www.smbc-comics.com/smbcforum%s"></head><body>Redirecting you to <a href='%s'>the forums</a>...</html>""" % (data[0]['url'],data[0]['url'])
except Exception, e:
    politecrash("I've cocked something up, please email me with the text <b>'%s'</b> and the URL in your address bar."%e)
                