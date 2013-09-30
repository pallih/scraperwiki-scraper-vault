import scraperwiki,requests,lxml.html

# Blank Python



# 951 might want to change at some point, just saying, if we're complete scraping;
# if not, we almost might as well just do the front page!
#endscrape = 951                                
endscrape=1 # stop after first page
for start in range (0,endscrape,50):
    url="http://forums.xkcd.com/viewforum.php?f=7&start=%d"%(start)
    html=requests.get(url).content
    root = lxml.html.fromstring(html)
    for a in root.cssselect("a[class='topictitle']"):
        text=a.text_content()
        # skip headers, I don't care about them.
        if 'xkcd Forum Rules' in text: continue
        if 'Rules for "Individual XKCD Comic Threads' in text: continue
        
        # attempt to autosplit on colon:
        anumber,colon,atitle=text.partition(':')
        # make the number a real number
        try:
            number=int(anumber)
        except:
            number=-1
        # make the title a real string without quotes or padded space
        title=atitle.strip(' "')
        aurl=a.attrib['href']
        # make url absolute, purge &sid=... ending
        end=aurl.find('&sid')
        url='http://forums.xkcd.com'+aurl[1:end]
        data={'url':url,'title':title,'number':number,'text':text}
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
import scraperwiki,requests,lxml.html

# Blank Python



# 951 might want to change at some point, just saying, if we're complete scraping;
# if not, we almost might as well just do the front page!
#endscrape = 951                                
endscrape=1 # stop after first page
for start in range (0,endscrape,50):
    url="http://forums.xkcd.com/viewforum.php?f=7&start=%d"%(start)
    html=requests.get(url).content
    root = lxml.html.fromstring(html)
    for a in root.cssselect("a[class='topictitle']"):
        text=a.text_content()
        # skip headers, I don't care about them.
        if 'xkcd Forum Rules' in text: continue
        if 'Rules for "Individual XKCD Comic Threads' in text: continue
        
        # attempt to autosplit on colon:
        anumber,colon,atitle=text.partition(':')
        # make the number a real number
        try:
            number=int(anumber)
        except:
            number=-1
        # make the title a real string without quotes or padded space
        title=atitle.strip(' "')
        aurl=a.attrib['href']
        # make url absolute, purge &sid=... ending
        end=aurl.find('&sid')
        url='http://forums.xkcd.com'+aurl[1:end]
        data={'url':url,'title':title,'number':number,'text':text}
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
