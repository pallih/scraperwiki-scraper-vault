import scraperwiki
import lxml.html
import re


def page_articles(page_root):
    
    articles_on_page = []
    for article in page_root.cssselect("div.item-list ul h4 a"):
        articles_on_page.append({"path" : article.get('href')})

    return articles_on_page  

def series_article_urls():
    html = scraperwiki.scrape('http://www.economist.com/blogs/charlemagne')
    root = lxml.html.fromstring(html)
     
    last_page_element = root.cssselect('li.pager-last a')
    
    if last_page_element:
        print last_page_element[0].get('href')
        regPat = re.compile('.*(\d{2,2})')
        found = re.match(regPat, last_page_element[0].get('href')) 
        if found: last_page_number = int(found.group(1))
        #print "Last page number:", last_page_number
    
    #http://www.economist.com/blogs/charlemagne/2012/12/french-muslims
    
    
    data = page_articles(root)
    
    for i in range(1,last_page_number+1):
        print "Page number:",i
        html = scraperwiki.scrape('http://www.economist.com/blogs/charlemagne?page=' + str(i))
        page_root = lxml.html.fromstring(html)
        new_articles = page_articles(page_root)
        #print data.items()
        #print new_article.items() 
        data = data + new_articles
        print "-------------------------"
    
    scraperwiki.sqlite.save(unique_keys=['path'], data=data)


import scraperwiki
import lxml.html
import re


def page_articles(page_root):
    
    articles_on_page = []
    for article in page_root.cssselect("div.item-list ul h4 a"):
        articles_on_page.append({"path" : article.get('href')})

    return articles_on_page  

def series_article_urls():
    html = scraperwiki.scrape('http://www.economist.com/blogs/charlemagne')
    root = lxml.html.fromstring(html)
     
    last_page_element = root.cssselect('li.pager-last a')
    
    if last_page_element:
        print last_page_element[0].get('href')
        regPat = re.compile('.*(\d{2,2})')
        found = re.match(regPat, last_page_element[0].get('href')) 
        if found: last_page_number = int(found.group(1))
        #print "Last page number:", last_page_number
    
    #http://www.economist.com/blogs/charlemagne/2012/12/french-muslims
    
    
    data = page_articles(root)
    
    for i in range(1,last_page_number+1):
        print "Page number:",i
        html = scraperwiki.scrape('http://www.economist.com/blogs/charlemagne?page=' + str(i))
        page_root = lxml.html.fromstring(html)
        new_articles = page_articles(page_root)
        #print data.items()
        #print new_article.items() 
        data = data + new_articles
        print "-------------------------"
    
    scraperwiki.sqlite.save(unique_keys=['path'], data=data)


