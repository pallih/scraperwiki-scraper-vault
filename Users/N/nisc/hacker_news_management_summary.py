import scraperwiki
import lxml.html
import re

POINT_THRESHOLD = 150


def scrape(link):
    html = unicode(scraperwiki.scrape(link), 'utf')
    root = lxml.html.fromstring(html)
    pattern = re.compile("(\d+ \D*) ago")
    
    for e in root.cssselect("table[bgcolor='#f6f6ef'] table td.title a"):
        link = unicode(e.get('href'))
        # only include links, no discussions, ask HN, etc
        if link.startswith("http"):   
            next_tr = e.getparent().getparent().getnext()
            td = next_tr.cssselect("td.subtext")[0]
            td_children = td.getchildren()

            # get age
            age = unicode(pattern.findall(td.text_content())[0])
    
            # get score
            points = int(td_children[0].text_content().split()[0])
    
            # get author
            author = unicode(td_children[1].text_content())
    
            # sometimes the number of comments is not shown on the page
            try:
                num_comments = int(td_children[2].text_content().split()[0])
            except:
                num_comments = '???'
    
            # get discussion link
            discussion = unicode('http://news.ycombinator.com/'+td_children[2].get('href'))
    
            # get title
            title = unicode(e.text_content())
            
            data = {
                'title' : title,
                'author' : author,
                'age' : age,
                'link' : link,
                'points' : points,
                'num_comments' : num_comments,
                'discussion' : discussion,
            }
            print data
            scraperwiki.sqlite.save(unique_keys=['link'], data=data)
    
    returnme = root.cssselect("a[rel='nofollow']")
    if len(returnme) > 0:
        return 'http://news.ycombinator.com'+returnme[0].get("href")
    else:
        return None


# start scraping
link = "http://news.ycombinator.com/over?points=%s" % POINT_THRESHOLD
while link:
    print link
    link = scrape(link)    
import scraperwiki
import lxml.html
import re

POINT_THRESHOLD = 150


def scrape(link):
    html = unicode(scraperwiki.scrape(link), 'utf')
    root = lxml.html.fromstring(html)
    pattern = re.compile("(\d+ \D*) ago")
    
    for e in root.cssselect("table[bgcolor='#f6f6ef'] table td.title a"):
        link = unicode(e.get('href'))
        # only include links, no discussions, ask HN, etc
        if link.startswith("http"):   
            next_tr = e.getparent().getparent().getnext()
            td = next_tr.cssselect("td.subtext")[0]
            td_children = td.getchildren()

            # get age
            age = unicode(pattern.findall(td.text_content())[0])
    
            # get score
            points = int(td_children[0].text_content().split()[0])
    
            # get author
            author = unicode(td_children[1].text_content())
    
            # sometimes the number of comments is not shown on the page
            try:
                num_comments = int(td_children[2].text_content().split()[0])
            except:
                num_comments = '???'
    
            # get discussion link
            discussion = unicode('http://news.ycombinator.com/'+td_children[2].get('href'))
    
            # get title
            title = unicode(e.text_content())
            
            data = {
                'title' : title,
                'author' : author,
                'age' : age,
                'link' : link,
                'points' : points,
                'num_comments' : num_comments,
                'discussion' : discussion,
            }
            print data
            scraperwiki.sqlite.save(unique_keys=['link'], data=data)
    
    returnme = root.cssselect("a[rel='nofollow']")
    if len(returnme) > 0:
        return 'http://news.ycombinator.com'+returnme[0].get("href")
    else:
        return None


# start scraping
link = "http://news.ycombinator.com/over?points=%s" % POINT_THRESHOLD
while link:
    print link
    link = scrape(link)    
