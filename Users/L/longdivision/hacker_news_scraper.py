import re
import time
import random

import lxml.html
import scraperwiki 

nextpageurl = "http://news.ycombinator.com/newest"

while nextpageurl:
    html = scraperwiki.scrape(url=nextpageurl)
    root = lxml.html.fromstring(html)
    nextpageurl = ""

    for td in root.cssselect("td .title"):
        text = td.text_content()

        if text == "More":
            nextpageurl = td.cssselect("a")[0].get("href")
            if re.match(r'/.*', nextpageurl):
                nextpageurl = "http://news.ycombinator.com" + nextpageurl
            else:
                nextpageurl = "http://news.ycombinator.com/" + nextpageurl
        
        elif not re.match(r'\d+\.', text): # eliminate numeric listing cells
            domain = re.search(r'\([a-z0-9\.\-]+\)\s*$', text) # get domain from title (last in brackets)

            # no domain -> Ask HN post, skip for now
            if domain is not None:
                domain = domain.group()
                domain = re.sub(r'[\(\)]', "", domain) # remove brackets from url
            else:
                continue

            url = td.cssselect("a")[0].get("href")
            metatd = td.getparent().getnext() # get meta data row
            title = text.replace("("+domain+")", "")
            points = int(re.search(r'^\d+', metatd.text_content()).group())
            submitter = metatd.cssselect("a")

            # no submitter -> Ad. skip for now
            if len(submitter) > 0:
                submitter = submitter[0].text_content()
            else:
                continue
    
            id = re.search(r'\d+', metatd.cssselect("a")[1].get("href")).group()
            commentsurl = "http://news.ycombinator.com/" + metatd.cssselect("a")[1].get("href")
    
            data = {
                'id': id,
                'title': title,
                'url': url,
                'domain': domain,
                'submitter': submitter,
                'points': points,
                'comments_url': commentsurl
            }
            print "Scraped post with id " + str(id) + ":"
            print data
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    
    # respect pg's wishes to only scrape a couple of pages each minute
    # see: http://news.ycombinator.com/item?id=1721105
    # random variation to look less like a bot
    time.sleep(90 + random.randint(0, 30))
import re
import time
import random

import lxml.html
import scraperwiki 

nextpageurl = "http://news.ycombinator.com/newest"

while nextpageurl:
    html = scraperwiki.scrape(url=nextpageurl)
    root = lxml.html.fromstring(html)
    nextpageurl = ""

    for td in root.cssselect("td .title"):
        text = td.text_content()

        if text == "More":
            nextpageurl = td.cssselect("a")[0].get("href")
            if re.match(r'/.*', nextpageurl):
                nextpageurl = "http://news.ycombinator.com" + nextpageurl
            else:
                nextpageurl = "http://news.ycombinator.com/" + nextpageurl
        
        elif not re.match(r'\d+\.', text): # eliminate numeric listing cells
            domain = re.search(r'\([a-z0-9\.\-]+\)\s*$', text) # get domain from title (last in brackets)

            # no domain -> Ask HN post, skip for now
            if domain is not None:
                domain = domain.group()
                domain = re.sub(r'[\(\)]', "", domain) # remove brackets from url
            else:
                continue

            url = td.cssselect("a")[0].get("href")
            metatd = td.getparent().getnext() # get meta data row
            title = text.replace("("+domain+")", "")
            points = int(re.search(r'^\d+', metatd.text_content()).group())
            submitter = metatd.cssselect("a")

            # no submitter -> Ad. skip for now
            if len(submitter) > 0:
                submitter = submitter[0].text_content()
            else:
                continue
    
            id = re.search(r'\d+', metatd.cssselect("a")[1].get("href")).group()
            commentsurl = "http://news.ycombinator.com/" + metatd.cssselect("a")[1].get("href")
    
            data = {
                'id': id,
                'title': title,
                'url': url,
                'domain': domain,
                'submitter': submitter,
                'points': points,
                'comments_url': commentsurl
            }
            print "Scraped post with id " + str(id) + ":"
            print data
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    
    # respect pg's wishes to only scrape a couple of pages each minute
    # see: http://news.ycombinator.com/item?id=1721105
    # random variation to look less like a bot
    time.sleep(90 + random.randint(0, 30))
