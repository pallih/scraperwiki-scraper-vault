import scraperwiki
import mechanize
import lxml.html
import cookielib
from bs4 import BeautifulSoup
import time,socket
import urllib,urllib2

#Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

#Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0, add Headers
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
br.addheaders = [('User-agent', 'Suffolk REU')]



def extractUserInfo(author_info):
    name = author_info.find('span', attrs = {'itemprop':'name'}).getText()
    title = ' '
    mem_title = author_info.find('p', attrs = {'class':'desc member_title'})
    if not mem_title is None:
        title = mem_title.getText()
    other_info = author_info.findAll('span', attrs = {'class':'fc'})
    gender, location = ' ', ' '
    if len(other_info) > 2:
        gender = other_info[1].getText()
        location = other_info[2].getText()
    return (name,title, gender, location)
    

def extractPostContent(post_body):
    commentTime = post_body.find('abbr', attrs = {'class':'published'}).getText()
    post_message = post_body.find('div', attrs = {'class':'post entry-content '}).getText()
    plus_sign = post_message.find('+')+5
    post_message = post_message[plus_sign:]
    return (commentTime, post_message)

def makeDictionary(userInfo, postInfo):
    dict_result = {}
    dict_result['Name'] = userInfo[0]
    dict_result['Member Title'] = userInfo[1]
    dict_result['Gender'] = userInfo[2]
    dict_result['Location'] = userInfo[3]
    dict_result['Comment Time'] = postInfo[0]
    dict_result['Comment Message'] = postInfo[1]
    return dict_result

def getPosts(new_url, response):
    soup = BeautifulSoup(response)
    results = soup.findAll('div', attrs = {'class':'post_block hentry clear clearfix '})
    for result in results:
        author_info = result.find('div', attrs = {'class': 'author_info'})
        post_body = result.find('div', attrs = {'class': 'post_body'})
        userInfo = extractUserInfo(author_info)
        postInfo = extractPostContent(post_body)
        dict_result = makeDictionary(userInfo,postInfo)
        post_id = result.get('id')
        dict_result['Post Id'] = post_id
        dict_result['Thread Url'] = new_url
        scraperwiki.sqlite.save(unique_keys=['Post Id'],data = dict_result)
    response = getMorePosts(soup)
    time.sleep(15)
    if not response is None:
        try:
            response = br.open(response)
            getPosts(new_url,response)
        except urllib2.HTTPError:
            pass



#Login to the website

url = 'http://gabrielle.self-injury.net/index.php?app=core&module=global&section=login'
response = br.open(url)

list_forms = [ form for form in br.forms() ]
br.select_form(nr=0)

br['ips_username'] = 'Researcher'
br['ips_password'] = 'research'

response = br.submit()

# Get a list of forum threads
def getThreads(response):
    soup = BeautifulSoup(response)
    threads = soup.findAll('a')
    forum_topics = []
    for link in threads:
        str_link = link.get('href')
        if isinstance(str_link,str) and str_link.find('.net/topic') != -1 and str_link.find('unread') != -1:
            forum_topics.append(str_link)
   # length = len(forum_topics)/2
   # forum_topics = forum_topics[::2]
    return forum_topics

def getMorePosts(soup):
    next = soup.find('a', attrs = {'rel':'next'})
    if next is None:
        return None
    else:
        return next.get('href')

topics = getThreads(response)
        
#Open up a random topic
for new_url in topics:
    try:
        response = br.open(new_url)
        getPosts(new_url,response)
    except urllib2.HTTPError:
        pass



    

    
    

import scraperwiki
import mechanize
import lxml.html
import cookielib
from bs4 import BeautifulSoup
import time,socket
import urllib,urllib2

#Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

#Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0, add Headers
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
br.addheaders = [('User-agent', 'Suffolk REU')]



def extractUserInfo(author_info):
    name = author_info.find('span', attrs = {'itemprop':'name'}).getText()
    title = ' '
    mem_title = author_info.find('p', attrs = {'class':'desc member_title'})
    if not mem_title is None:
        title = mem_title.getText()
    other_info = author_info.findAll('span', attrs = {'class':'fc'})
    gender, location = ' ', ' '
    if len(other_info) > 2:
        gender = other_info[1].getText()
        location = other_info[2].getText()
    return (name,title, gender, location)
    

def extractPostContent(post_body):
    commentTime = post_body.find('abbr', attrs = {'class':'published'}).getText()
    post_message = post_body.find('div', attrs = {'class':'post entry-content '}).getText()
    plus_sign = post_message.find('+')+5
    post_message = post_message[plus_sign:]
    return (commentTime, post_message)

def makeDictionary(userInfo, postInfo):
    dict_result = {}
    dict_result['Name'] = userInfo[0]
    dict_result['Member Title'] = userInfo[1]
    dict_result['Gender'] = userInfo[2]
    dict_result['Location'] = userInfo[3]
    dict_result['Comment Time'] = postInfo[0]
    dict_result['Comment Message'] = postInfo[1]
    return dict_result

def getPosts(new_url, response):
    soup = BeautifulSoup(response)
    results = soup.findAll('div', attrs = {'class':'post_block hentry clear clearfix '})
    for result in results:
        author_info = result.find('div', attrs = {'class': 'author_info'})
        post_body = result.find('div', attrs = {'class': 'post_body'})
        userInfo = extractUserInfo(author_info)
        postInfo = extractPostContent(post_body)
        dict_result = makeDictionary(userInfo,postInfo)
        post_id = result.get('id')
        dict_result['Post Id'] = post_id
        dict_result['Thread Url'] = new_url
        scraperwiki.sqlite.save(unique_keys=['Post Id'],data = dict_result)
    response = getMorePosts(soup)
    time.sleep(15)
    if not response is None:
        try:
            response = br.open(response)
            getPosts(new_url,response)
        except urllib2.HTTPError:
            pass



#Login to the website

url = 'http://gabrielle.self-injury.net/index.php?app=core&module=global&section=login'
response = br.open(url)

list_forms = [ form for form in br.forms() ]
br.select_form(nr=0)

br['ips_username'] = 'Researcher'
br['ips_password'] = 'research'

response = br.submit()

# Get a list of forum threads
def getThreads(response):
    soup = BeautifulSoup(response)
    threads = soup.findAll('a')
    forum_topics = []
    for link in threads:
        str_link = link.get('href')
        if isinstance(str_link,str) and str_link.find('.net/topic') != -1 and str_link.find('unread') != -1:
            forum_topics.append(str_link)
   # length = len(forum_topics)/2
   # forum_topics = forum_topics[::2]
    return forum_topics

def getMorePosts(soup):
    next = soup.find('a', attrs = {'rel':'next'})
    if next is None:
        return None
    else:
        return next.get('href')

topics = getThreads(response)
        
#Open up a random topic
for new_url in topics:
    try:
        response = br.open(new_url)
        getPosts(new_url,response)
    except urllib2.HTTPError:
        pass



    

    
    

