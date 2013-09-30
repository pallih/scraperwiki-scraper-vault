import urllib2
from bs4 import BeautifulSoup
import re

url = "http://geniekids.com/pa"
#url = "http://geniekids.com/pa/Respect-Fundamentals-of-Disciplining"
import scraperwiki


def get_page(url):
    content = None
    try:
        content = urllib2.urlopen(url).read()
        return content
    except urllib2.URLError:
        return content

def extract_main (url):
    page = get_page(url)
    soup = BeautifulSoup(page)
    outlinks = [] 
    tags = []
    mainContent = soup.find('div', attrs={'id' : 'mainContent'})
    title = mainContent.find('h1', attrs={'class' : 'title'}).get_text()
    content = mainContent.find('div', attrs={'class': 'content'}).get_text()

    for tag_link in mainContent.findAll('li', attrs={'class': re.compile('tax.*')}):
        tags.append(str(tag_link.get_text()))
    
    for link in mainContent.find_all('a'):
        new_link = link.get('href')
        if new_link and new_link[0:4] == '/pa/'and new_link.find("comment")==-1:
            link_full = 'http://geniekids.com' + new_link
            outlinks.append(link_full)
    return title, content, outlinks, tags  # title, content, outlinks, tags

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    i = 0
    while tocrawl: 
        url = tocrawl.pop()
        if url not in crawled:
            title, content, outlinks, tags = extract_main(url)
            scraperwiki.sqlite.save(unique_keys=["id"], data={"id":i, "title":title, "content":content, "tags":tags, "url":url})
            print i
            i +=1
            graph[url] = outlinks
            union(tocrawl, outlinks)
            crawled.append(url)
    return 1

def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

print crawl_web(url)

data = scraperwiki.sqlite.select(
    '''* FROM swdata ORDER BY title '''
)
print data

import urllib2
from bs4 import BeautifulSoup
import re

url = "http://geniekids.com/pa"
#url = "http://geniekids.com/pa/Respect-Fundamentals-of-Disciplining"
import scraperwiki


def get_page(url):
    content = None
    try:
        content = urllib2.urlopen(url).read()
        return content
    except urllib2.URLError:
        return content

def extract_main (url):
    page = get_page(url)
    soup = BeautifulSoup(page)
    outlinks = [] 
    tags = []
    mainContent = soup.find('div', attrs={'id' : 'mainContent'})
    title = mainContent.find('h1', attrs={'class' : 'title'}).get_text()
    content = mainContent.find('div', attrs={'class': 'content'}).get_text()

    for tag_link in mainContent.findAll('li', attrs={'class': re.compile('tax.*')}):
        tags.append(str(tag_link.get_text()))
    
    for link in mainContent.find_all('a'):
        new_link = link.get('href')
        if new_link and new_link[0:4] == '/pa/'and new_link.find("comment")==-1:
            link_full = 'http://geniekids.com' + new_link
            outlinks.append(link_full)
    return title, content, outlinks, tags  # title, content, outlinks, tags

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    i = 0
    while tocrawl: 
        url = tocrawl.pop()
        if url not in crawled:
            title, content, outlinks, tags = extract_main(url)
            scraperwiki.sqlite.save(unique_keys=["id"], data={"id":i, "title":title, "content":content, "tags":tags, "url":url})
            print i
            i +=1
            graph[url] = outlinks
            union(tocrawl, outlinks)
            crawled.append(url)
    return 1

def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

print crawl_web(url)

data = scraperwiki.sqlite.select(
    '''* FROM swdata ORDER BY title '''
)
print data

