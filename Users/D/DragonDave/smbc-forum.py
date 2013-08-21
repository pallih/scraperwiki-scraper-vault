import scraperwiki,requests,lxml.html,re,dateutil.parser

# Blank Python

oneshot=False
olddate=None

def parseforum(url,olddate):
    html=requests.get(url).content
    root=lxml.html.fromstring(html)
    for p in root.cssselect("p[class='author']"):
        datetext=p.cssselect('strong')[0].tail[2:]
        date=dateutil.parser.parse(datetext).date()
        if date==olddate:
            continue # skip ahead
        olddate=date
        url=p.cssselect('a')[0].attrib['href'].partition('&sid')[0][1:]
        cid=url.partition('=')[2]
        url=url+"#p"+cid
        #TODO: add #p12344 to end
        data={'url':url,'date':date}
        scraperwiki.sqlite.save(unique_keys=['url'], data=data, table_name="forum")
    return olddate

if oneshot:
    for page in range(0,15*292,15):
        print "2/%d"%page
        olddate=parseforum('http://www.smbc-comics.com/smbcforum/viewtopic.php?f=1&t=1289&start=%d'%page,olddate)
    olddate=None
    for page in range(0,15*77,15):
        print "1/%d"%page
        olddate=parseforum('http://www.smbc-comics.com/smbcforum/viewtopic.php?f=1&t=45&start=%d'%page,olddate)

if oneshot: 
    exit()

# 951 might want to change at some point, just saying, if we're complete scraping;
# if not, we almost might as well just do the front page!
#endscrape = 250                                
endscrape=1 # stop after first page
for start in range (0,endscrape,50):
    url="http://www.smbc-comics.com/smbcforum/viewforum.php?f=40&start=%d"%(start)
    html=requests.get(url).content
    root = lxml.html.fromstring(html)
    for a in root.cssselect("a[class='topictitle']"):
        aurl=a.attrib['href'].partition('&sid=')[0][1:]
        #./viewtopic.php?f=40&t=3650&sid=1c49a576f82f0c38ee76996ad02844f3
        text=a.text_content()
        #print text
        try:
            datetext=re.search(r'\[(.*)\]',text).group(1)
        except:
            print "Couldn't find a [] pair in '%s'"%text
            continue
        try:
            date=dateutil.parser.parse(datetext).date()
        except:
            print "No date in '%s'"%datetext
            continue
        data={'url':aurl,'date':date}
        scraperwiki.sqlite.save(unique_keys=['url'], data=data, table_name="forum")


# TODO http://www.smbc-comics.com/smbcforum/viewtopic.php?f=1&t=45
# TODO http://www.smbc-comics.com/smbcforum/viewtopic.php?f=1&t=1289

        