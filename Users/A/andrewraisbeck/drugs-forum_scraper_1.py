from __future__ import division
from lxml import etree
import lxml.html
from urllib import FancyURLopener
import urllib2
import nltk, re, pprint
import httplib
import StringIO
import scraperwiki

#Turn on debugging
#httplib.HTTPConnection.debuglevel = 1

#Spoof header and get HTML of thread page
def download_html(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = urllib2.Request(url, headers=hdr)

    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
        return None

    content = page.read()

    #Convert html to tree structure
    return lxml.html.fromstring(content)

def node_text(node):
    if node.text:
        result = node.text
    else:
        result = ''
    for child in node:
        if child.tail is not None:
            result += child.tail
    return result
    

#START HERE
tree = download_html("http://www.drugs-forum.com/forum/forumdisplay.php?f=172")

cntr = 2
cntr2=2
id = 0

#Start crawling the subforum...
while True :
    
    #Use XPath to find all the threads
    r = tree.xpath('//tr/td[2]/div[1]/a[2]')
    
    for link in r:
        subtree = download_html("http://www.drugs-forum.com/forum/"+link.get("href"))
        while True:
            posts = subtree.xpath("//div[starts-with(@id, 'post_message')]")
            users = subtree.xpath("//a[starts-with(@class, 'bigusername')]")
            user_cntr = 0
            thread = subtree.xpath('//td[@class="navbar"]/strong')
            userVal = ""
            if len(users) > user_cntr:
                userVal = node_text(users[user_cntr])
            else :
                userVal = "Error"
            for post in posts:
                data = {
                    'ID' : id,
                    'THREAD' : node_text(thread[0]),
                    'USER-ID' : userVal,
                    'POST' : node_text(post)
                }
                scraperwiki.sqlite.save(unique_keys=['ID' ], data=data)
                print str(id)+". "+node_text(thread[0])+": "+userVal+"\n"
                user_cntr += 1
                id += 1
            next = subtree.xpath("//a[starts-with(@rel, 'next')]")
            if len(next) != 0:
                subtree = download_html("http://www.drugs-forum.com/forum/"+link.get("href")+"&page="+str(cntr2))
                cntr2+=1
            else :
                cntr2=2
                break
    next = tree.xpath("//a[starts-with(@rel, 'next')]")
    if len(next) != 0:
        tree = download_html("http://www.drugs-forum.com/forum/forumdisplay.php?f=172&order=desc&page="+str(cntr))
        cntr+=1
    else :
        break

print("DONE CREEPING WEBSITE!")