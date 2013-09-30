import scraperwiki, lxml.html, re, time, random

nextpageurl = "http://news.ycombinator.com/newest"

while (nextpageurl):

    # for unbanning (needs to be done from other ip...)
    # print scraperwiki.scrape('http://www.whatsmyip.us/')
    # http://news.ycombinator.com/unban?ip=46.43.55.87

    html = scraperwiki.scrape(url=nextpageurl)
    root = lxml.html.fromstring(html)
    nextpageurl = ""

    print "connected"

    for td in root.cssselect("td .title"):
    
        text = td.text_content()
        
        if (text == "More") :
            nextpageurl = td.cssselect("a")[0].get("href")
            if re.match(r'/.*', nextpageurl):
                nextpageurl = "http://news.ycombinator.com" + nextpageurl
            else:
                nextpageurl = "http://news.ycombinator.com/" + nextpageurl
    
        # eliminate number cells and "more" link
        elif not re.match(r'\d+\.', text):
    
            # get domain from title (in brackets)
            domain = re.search(r'\([a-z0-9\.\-]+\)\s*$', text)
            # no domain = HN post, skip for now
            if domain is not None:
                domain = domain.group()
                domain = re.sub(r'[\(\)]', "", domain) # remove brackets from url
            else:
                continue

            url = td.cssselect("a")[0].get("href")
            
            # get meta data row
            metatd = td.getparent().getnext()
    
            title = text.replace("("+domain+")", "")
    
            points = int(re.search(r'^\d+', metatd.text_content()).group())
    
            submitter = metatd.cssselect("a")
            # no submitter = ad. skip
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
            print data
    
            # save
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)
            
            
            # get points     
            #print url
            #print td.text_content()
    
    # respect pg's wishes to only scrape a couple of pages each minute
    # see: http://news.ycombinator.com/item?id=1721105
    # random variation to look less like a bot
    time.sleep(90 + random.randint(0, 30))
    

import scraperwiki, lxml.html, re, time, random

nextpageurl = "http://news.ycombinator.com/newest"

while (nextpageurl):

    # for unbanning (needs to be done from other ip...)
    # print scraperwiki.scrape('http://www.whatsmyip.us/')
    # http://news.ycombinator.com/unban?ip=46.43.55.87

    html = scraperwiki.scrape(url=nextpageurl)
    root = lxml.html.fromstring(html)
    nextpageurl = ""

    print "connected"

    for td in root.cssselect("td .title"):
    
        text = td.text_content()
        
        if (text == "More") :
            nextpageurl = td.cssselect("a")[0].get("href")
            if re.match(r'/.*', nextpageurl):
                nextpageurl = "http://news.ycombinator.com" + nextpageurl
            else:
                nextpageurl = "http://news.ycombinator.com/" + nextpageurl
    
        # eliminate number cells and "more" link
        elif not re.match(r'\d+\.', text):
    
            # get domain from title (in brackets)
            domain = re.search(r'\([a-z0-9\.\-]+\)\s*$', text)
            # no domain = HN post, skip for now
            if domain is not None:
                domain = domain.group()
                domain = re.sub(r'[\(\)]', "", domain) # remove brackets from url
            else:
                continue

            url = td.cssselect("a")[0].get("href")
            
            # get meta data row
            metatd = td.getparent().getnext()
    
            title = text.replace("("+domain+")", "")
    
            points = int(re.search(r'^\d+', metatd.text_content()).group())
    
            submitter = metatd.cssselect("a")
            # no submitter = ad. skip
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
            print data
    
            # save
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)
            
            
            # get points     
            #print url
            #print td.text_content()
    
    # respect pg's wishes to only scrape a couple of pages each minute
    # see: http://news.ycombinator.com/item?id=1721105
    # random variation to look less like a bot
    time.sleep(90 + random.randint(0, 30))
    

