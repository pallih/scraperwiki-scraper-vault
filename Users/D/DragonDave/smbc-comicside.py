import scraperwiki,requests,dateutil.parser,lxml.html

# Blank Python
data=[]
for comicid in range(1,2534):
    url='http://www.smbc-comics.com/?id=%d'%comicid
    try:
        html=requests.get(url).content
    except Exception, e:
        print "Hmmm. Didn't like %d, %s"%(comicid,e)
        continue
    root = lxml.html.fromstring(html)
    datetext=root.cssselect("a[name='blog'] b")[0].text_content()
    try:
        date=dateutil.parser.parse(datetext).date()
    except Exception, e:
        print "Hmmm. Didn't like %d's '%s', %s"%(comicid, datetext, e)
        continue
    data={'id':comicid, 'date':date}
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

# TODO http://www.smbc-comics.com/smbcforum/viewtopic.php?f=1&t=45
# TODO http://www.smbc-comics.com/smbcforum/viewtopic.php?f=1&t=1289import scraperwiki,requests,dateutil.parser,lxml.html

# Blank Python
data=[]
for comicid in range(1,2534):
    url='http://www.smbc-comics.com/?id=%d'%comicid
    try:
        html=requests.get(url).content
    except Exception, e:
        print "Hmmm. Didn't like %d, %s"%(comicid,e)
        continue
    root = lxml.html.fromstring(html)
    datetext=root.cssselect("a[name='blog'] b")[0].text_content()
    try:
        date=dateutil.parser.parse(datetext).date()
    except Exception, e:
        print "Hmmm. Didn't like %d's '%s', %s"%(comicid, datetext, e)
        continue
    data={'id':comicid, 'date':date}
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

# TODO http://www.smbc-comics.com/smbcforum/viewtopic.php?f=1&t=45
# TODO http://www.smbc-comics.com/smbcforum/viewtopic.php?f=1&t=1289