from urllib2 import urlopen, HTTPError
from lxml.html import fromstring, tostring
import scraperwiki
import datetime
from time import sleep
  
def getone(node, selector):
    results = node.cssselect(selector)
    assert len(results) == 1
    result = results[0]
    return result

def scrapeonepage(url):
    page = urlopen(url)
    html = page.read()
    x = fromstring(html)
    entries = x.cssselect('div.timeline-entry')
    

    for entry in entries:
        print tostring(entry)
        assert entry[1].tag == 'a'
        usrlink = entry[1].attrib.get('href')
        usrname = entry[1].text
    
        action = getone(entry, 'span.action').text
    
        if action == 'commented':
            comment = getone(entry, 'div.comment-text').text_content()
            comment_link = getone(entry, 'span.commenter > a').attrib.get('href')
        else:
            comment = None
            comment_link = None      
    
        date_string = getone(entry, 'span.date').text.strip()
        try:
            date = datetime.datetime.strptime (date_string, '%B %d %Y')
        except:
            date_string = date_string + ' ' + str(datetime.datetime.now().year)
            date = datetime.datetime.strptime (date_string, '%B %d %Y')
        print 
        
    
        print usrname
        assert usrlink[:7] == '/users/'
        if usrlink[-1] != '/':
            usrlink = usrlink + '/'
    
    
        data = { "usrlink":usrlink, "usernam":usrname, "action":action, "date": date.date(), "comment": comment, "comment_link": comment_link}
    
    
        scraperwiki.sqlite.save([], data)

def scrapeuserpage(usrlink):
    url = "http://wellcommons.com" + usrlink
    page = urlopen (url)
    html = page.read()
    x = fromstring(html)
    items = x.cssselect('#professional_info .item' )

    data = {
        "usrlink": usrlink,
        "usrname": getone(x, '#section_wrapper h2').text,
    }
    bionodes = x.cssselect('#user_bio > * > p')
    if len(bionodes) == 1:
        data["usrbio"] = bionodes[0].text_content()
    elif len(bionodes) == 0:
        pass
    else:
        assert False

    for item in items:
        key = getone(item, 'h4').text
        value = getone(item, 'div.text > p').text
        data[key] = value
        
    print data

def users():
    datarows = scraperwiki.sqlite.select('distinct usrlink from swdata')

    for data in datarows:
        usrlink = data['usrlink']
        scrapeuserpage(usrlink)

def activity(section):
    pagenum = 3
    while True:
        try:
            scrapeonepage("http://wellcommons.com/groups/" + section+ "/timeline/?page=" + str(pagenum))
        except HTTPError:
            break
        pagenum = pagenum + 1
        sleep(1)

#for section in ["wellness", "trauma","locavores","nosurance","kiddos","wise"]:
#    activity(section)
#users()

scrapeuserpage("/users/kbritt/")from urllib2 import urlopen, HTTPError
from lxml.html import fromstring, tostring
import scraperwiki
import datetime
from time import sleep
  
def getone(node, selector):
    results = node.cssselect(selector)
    assert len(results) == 1
    result = results[0]
    return result

def scrapeonepage(url):
    page = urlopen(url)
    html = page.read()
    x = fromstring(html)
    entries = x.cssselect('div.timeline-entry')
    

    for entry in entries:
        print tostring(entry)
        assert entry[1].tag == 'a'
        usrlink = entry[1].attrib.get('href')
        usrname = entry[1].text
    
        action = getone(entry, 'span.action').text
    
        if action == 'commented':
            comment = getone(entry, 'div.comment-text').text_content()
            comment_link = getone(entry, 'span.commenter > a').attrib.get('href')
        else:
            comment = None
            comment_link = None      
    
        date_string = getone(entry, 'span.date').text.strip()
        try:
            date = datetime.datetime.strptime (date_string, '%B %d %Y')
        except:
            date_string = date_string + ' ' + str(datetime.datetime.now().year)
            date = datetime.datetime.strptime (date_string, '%B %d %Y')
        print 
        
    
        print usrname
        assert usrlink[:7] == '/users/'
        if usrlink[-1] != '/':
            usrlink = usrlink + '/'
    
    
        data = { "usrlink":usrlink, "usernam":usrname, "action":action, "date": date.date(), "comment": comment, "comment_link": comment_link}
    
    
        scraperwiki.sqlite.save([], data)

def scrapeuserpage(usrlink):
    url = "http://wellcommons.com" + usrlink
    page = urlopen (url)
    html = page.read()
    x = fromstring(html)
    items = x.cssselect('#professional_info .item' )

    data = {
        "usrlink": usrlink,
        "usrname": getone(x, '#section_wrapper h2').text,
    }
    bionodes = x.cssselect('#user_bio > * > p')
    if len(bionodes) == 1:
        data["usrbio"] = bionodes[0].text_content()
    elif len(bionodes) == 0:
        pass
    else:
        assert False

    for item in items:
        key = getone(item, 'h4').text
        value = getone(item, 'div.text > p').text
        data[key] = value
        
    print data

def users():
    datarows = scraperwiki.sqlite.select('distinct usrlink from swdata')

    for data in datarows:
        usrlink = data['usrlink']
        scrapeuserpage(usrlink)

def activity(section):
    pagenum = 3
    while True:
        try:
            scrapeonepage("http://wellcommons.com/groups/" + section+ "/timeline/?page=" + str(pagenum))
        except HTTPError:
            break
        pagenum = pagenum + 1
        sleep(1)

#for section in ["wellness", "trauma","locavores","nosurance","kiddos","wise"]:
#    activity(section)
#users()

scrapeuserpage("/users/kbritt/")