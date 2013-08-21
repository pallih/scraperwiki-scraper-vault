# -*- coding: utf-8 -*-
from lxml.html import parse
import urllib2
import scraperwiki
import pickle

def urlopen(url):
    req = urllib2.Request(url)
    req.add_unredirected_header('User-Agent', 'Mozilla/5.0')
    return urllib2.urlopen(req)

def getThread(url, thread_id):
    #url = "https://groups.google.com/group/baixocentro/browse_thread/thread/"
    #opts = "?noredirect=true"

    soup = urlopen(url)
    soup = parse(soup)

    thread = []
    for m in soup.xpath("//div[@id='msgs']/div"):
        msg = {}
        msg["id"] = m.xpath("//div[@id='inbdy']//a")[0].get("name")[4:]
        msg["name"] = m.xpath("//span[contains(@class,'author')]/span")[0].text
        msg["date"] = m.xpath("//div[contains(@class,'msg')]/input[@id='hdn_date']")[0].get("value")
        msg["partial_email"] = m.xpath("//div[contains(@class,'msg')]/input[@id='hdn_author']")[0].get("value")
        msg["subject"] = m.xpath("//div[contains(@class,'msg')]/input[@id='hdn_reply_to_subj']")[0].get("value")
        msg["thread"] = soup.xpath("//span[@id='thread_subject_site']")[0].text.strip()
        msg["thread_id"] = thread_id
        msg["thread_url"] = url+thread_id
        msg["content"] = m.xpath("//div[contains(@class,'mb')]")[0].text_content().strip()
        thread.append(msg)
    return thread

def save(thread, thread_id): 
    for m in thread:
        scraperwiki.sqlite.save(["id"], m)

    threads_done.append(thread_id)
    scraperwiki.sqlite.save_var("threads_done", pickle.dumps(threads_done))

def getThreads(url):
    print "Getting threads from " + url.split("start=")[1].split("&")[0]
    soup = urlopen(url)
    soup = parse(soup)
    for t in soup.xpath("//div[@class='maincontoutboxatt']//tr/td/a[not(@class='st')]"):
        thread_id = t.get("href").split("/")[5][:-7]
        thread_url = "https://groups.google.com" + t.get("href")
        if thread_id not in threads_done:
            print "Getting thread " + thread_id
            thread = getThread(thread_url, thread_id)
            save(thread, thread_id)

    older = "https://groups.google.com" + soup.xpath(u"//a[text()='Older »']")[0].get('href')+"&noredirect=true&gvc=2"
    if older:
        getThreads(older)

#Mude para mudar o grupo!
groupname = "baixocentro"

url = "https://groups.google.com/group/"+groupname+"/topics?hl=en&sa=N&noredirect=true&start=0&gvc=2"

if scraperwiki.sqlite.get_var("threads_done") == None:
    scraperwiki.sqlite.save_var("threads_done", pickle.dumps([]))
else:
    threads_done = pickle.loads(scraperwiki.sqlite.get_var("threads_done"))

getThreads(url)
