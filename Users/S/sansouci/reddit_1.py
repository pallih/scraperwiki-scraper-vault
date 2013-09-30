import scraperwiki  
import lxml.html
        
html = scraperwiki.scrape("http://www.reddit.com/search?q=title%3Aadvice+animal&restrict_sr=off&sort=relevance&t=all&limit=100")
root = lxml.html.fromstring(html)


data = []
counter = root.cssselect("div.thing")

for curr in counter:

    time = curr.cssselect("time")[0].attrib['datetime']
    author = curr.cssselect("a.author")[0].text
    title = curr.cssselect("a.title")[0].text
    subreddit = curr.cssselect("a.subreddit")[0].text
    comments = curr.cssselect("a.comments")[0].text
    downs = curr.cssselect("div.thing")[0].attrib['data-downs']
    ups =  curr.cssselect("div.thing")[0].attrib['data-ups']
    url = curr.cssselect("a.title")[0].attrib['href']



    data = {
            'time' : time,
            'author' : author,
            'title' : title,
            'subreddit' : subreddit,
            'url' : url,
            'comments' : comments,
            'downs' : downs,
            'ups' : ups,
        }

    scraperwiki.sqlite.save(unique_keys=['time'], data=data)










import scraperwiki  
import lxml.html
        
html = scraperwiki.scrape("http://www.reddit.com/search?q=title%3Aadvice+animal&restrict_sr=off&sort=relevance&t=all&limit=100")
root = lxml.html.fromstring(html)


data = []
counter = root.cssselect("div.thing")

for curr in counter:

    time = curr.cssselect("time")[0].attrib['datetime']
    author = curr.cssselect("a.author")[0].text
    title = curr.cssselect("a.title")[0].text
    subreddit = curr.cssselect("a.subreddit")[0].text
    comments = curr.cssselect("a.comments")[0].text
    downs = curr.cssselect("div.thing")[0].attrib['data-downs']
    ups =  curr.cssselect("div.thing")[0].attrib['data-ups']
    url = curr.cssselect("a.title")[0].attrib['href']



    data = {
            'time' : time,
            'author' : author,
            'title' : title,
            'subreddit' : subreddit,
            'url' : url,
            'comments' : comments,
            'downs' : downs,
            'ups' : ups,
        }

    scraperwiki.sqlite.save(unique_keys=['time'], data=data)










