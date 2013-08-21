import mechanize 
import lxml.html   
from bs4 import BeautifulSoup
from bs4.element import Tag
import Queue
import threading
import scrapemark
import time
import dateutil.parser   
import datetime
import scraperwiki
from itertools import chain
from urllib2 import URLError
from functools import wraps
import json
import requests
import traceback
import httplib, base64


THREADS = 30

count_public = 0
count_private = 0
count_failed = 0

# Condition for scraper to continue
def satisfy_process_condition(profile):
    uni_namen = ["WHU", "Wissenschaftliche Hochschule für Unternehmensführung", "Beisheim", "HSG", "Universität St. Gallen", "Universität St.Gallen", "Uni St.Gallen", "Uni St. Gallen", "Universität Mannheim", "Uni Mannheim"]
    for school in profile["schools"]:
        for needle in uni_namen:
            if needle in school["name"] and ( school["end_date"] == None or school["end_date"] > datetime.date.today() ):
                #print "satisfied condition"
                return True
    #print "didnt satifsy condition"    
    return False


# extract contact count
def get_contact_count(user_name):
    return scrapemark.scrape(
        """<a href=''>Kontakte ({{ |int }})</a>""", html=get_response(get_browser(cj_d), "https://www.xing.com/profile/" + user_name).read())
    
# process_user
def process_user(user_name):
    global count_public, count_private, count_failed
    try:
        user_profile = {"id": user_name, "contact_count": get_contact_count(user_name) }
        user_profile = dict(user_profile.items() + parse_profile(user_name).items())
        #print user_profile["id"] + " " + str(user_profile["contact_count"])
    
        
        if user_profile["contats_private"] == True:
            user_profile["contacts"] = []
            queueLock.acquire()
            count_private += 1
            queueLock.release()
        else:
            user_profile["contacts"]= extract_contacts(user_name, [], 1)
            queueLock.acquire()
            count_public += 1
            queueLock.release()
    
        print "%s/%s private ~%s , (%s failed)" % (count_private, count_private + count_public, float(count_private)/(count_private + count_public), count_failed)
    
        queueLock.acquire()
        user_profile["target_student"] = satisfy_process_condition(user_profile)
        #mongoQueue.put(user_profile)
        scraperwiki.sqlite.save(unique_keys=["id"], data={'id':user_profile['id'], 'contats_private':user_profile['contats_private'], 'target_student':user_profile['target_student'], 'json':str(user_profile)})
            
        
        if satisfy_process_condition(user_profile) == True:
            #print "scrape contacts.."
            
            processed_user_ids = list(chain.from_iterable(scraperwiki.sqlite.execute("SELECT `id` FROM`swdata`")["data"]))
            
            for contact in user_profile["contacts"]:
                if not(contact["user_name"] in processed_user_ids):
                    workQueue.put(contact["user_name"])
                    #print contact["user_name"]
            print "quesize " + str(workQueue.qsize())
    
        queueLock.release()

    except Exception as e:
        count_failed += 1
        workQueue.put(user_name)
        print "Exception while processsing " + user_name + " readded to queue: %user_name:"
        traceback.print_exc()
            

def extract_contacts(user_name, contacts=[], page=1):
    ##print "https://touch.xing.com/users/%s/contacts?page=%s" % (user_name, page)
    br_ec = get_browser(cj_m)
    response_m = get_response(br_ec, "https://touch.xing.com/users/%s/contacts?page=%s" % (user_name, page))
    soup_m = BeautifulSoup(response_m.read())
    
    for li in soup_m.find(id="contacts").ul.find_all("li"):
        #print " %s, %s (%s)" % (li.p.string, li.find_all("span")[1].string, li.find_all("span")[0].string)
        contacts.append({
             "user_name": li.a["href"].replace("/users/", "").encode('utf-8'), 
             "title": li.find_all("span")[0].string.encode('utf-8'), 
             "org": li.find_all("span")[1].string.encode('utf-8')
            })


    queueLock.acquire()
    if list(br_ec.links())[-1].text== "Nächste":
        queueLock.release()
        return extract_contacts(user_name, contacts, page+1)                    
    else:
        queueLock.release()
        return contacts
        

# parse profile
def parse_profile(user_name):
    profile = {}
    br_pp = get_browser(cj_m)
        
    response_m = get_response(br_pp , "https://touch.xing.com/users/" + user_name)
    soup_m = BeautifulSoup(response_m.read())


    profile["source"] = str(soup_m)
            
    profile["primary_org"] = get_string_tag(soup_m.find(class_="org"))
    profile["primary_title"] = get_string_tag(soup_m.find(class_="title"))
    profile["picture"] = soup_m.find_all("img")[1]['src']
    
    response_m = get_response(br_pp, "https://touch.xing.com/users/%s/contact_info" % user_name)
    soup_m = BeautifulSoup(response_m.read())

    if not ("<span data-contact-degree=" in str(soup_m)):
        raise Exception("Exception while asserting contacts private/public")
    
    print "https://touch.xing.com/users/%s/contact_info" % user_name
    print soup_m
    profile["contats_private"] =  not "Kontakte (" in str(soup_m)
    
    response_m = get_response(br_pp , "https://touch.xing.com/users/%s/data" % user_name)
    soup_m = BeautifulSoup(response_m.read())

    
    for section in soup_m.find_all(class_="section"):
        for case in switch(section.h2.string):
            if case("Ich suche"):
                profile["wants"] = section.p.string.encode("UTF-8")
                break
            if case("Ich biete"):
                profile["haves"] = section.p.string.encode("UTF-8")
                break
            if case("Interessen"):
                profile["interests"] = section.p.string.encode("UTF-8")
                break
            if case("Organisationen"):
                profile["organisations"] = [organisation.strip().encode("UTF-8") for organisation in section.p.string.split(";")]
                break
            if case("Sprachen"):
                profile["languages"] = [language.strip().encode("UTF-8") for language in section.p.string.split(",")] 
                break

            
            profile["schools"] = []
            for li in soup_m.find_all(class_="education"):
                profile["schools"].append({
                    "name": get_string_tag(li.find(class_="org")),
                    "begin_date": get_date(li.find(class_="dtstart")),
                    "end_date": get_date(li.find(class_="dtend")),
                    "degree": get_string_tag(li.find(class_="degree")),
                    "subject": get_string_tag(li.find(class_="subject")),
                    "description": get_string_tag(li.find(class_="description"))
                })

            profile["companies"] = []
            for li in soup_m.find_all(class_="experience"):
                profile["companies"].append({
                    "name": get_string_tag(li.find(class_="org")),
                    "type": get_string_tag(li.find(class_="info")),
                    "begin_date": get_date(li.find(class_="dtstart")),
                    "end_date": get_date(li.find(class_="dtend")),
                    "title": get_string_tag(li.find(class_="title")),
                    "description": get_string_tag(li.find(class_="description"))
                })


            profile["awards"] = []
            for li in soup_m.find_all(class_="award"):
                profile["awards"].append({
                    "name": get_string_tag(li.find_all("span")[0]),
                    "year": get_year(li.find_all("span")[1])
                })

            profile["qualifications"] = [li.string.encode("UTF-8") for li in soup_m.find_all(class_="qualification")]

    #print unicode( profile["schools"])
    #print profile["schools"]
    return profile

def get_string_tag(tag):
    if isinstance(tag, Tag):
        return tag.string.encode("UTF-8")
    else:
        return ""

def get_date(tag):
    try:
        return datetime.datetime.strptime(get_string_tag(tag), "%m/%Y").date()
    except:
        return None

def get_year(tag):
    try:
        return datetime.datetime.strptime(get_string_tag(tag), "%Y").date()
    except:
        return None

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


#@retry(Exception, tries=10, delay=1, backoff=2)
def save_nosql(data, id):
    def date_handler(obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj
    url = "https://xing:oVwcFShoCilg@xing.cloudant.com:443/xing/" + id

    headers = {'Content-Type':'application/json'}
    r = requests.put(url, data=json.dumps(data, default=date_handler), headers=headers, verify=False)
    
    print url
    print r.content

def get_browser(cookie_jar):
    br = mechanize.Browser()
    br.set_cookiejar(cookie_jar)
    br.set_handle_robots(False)   
    br.set_handle_refresh(False)  
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    return br

#@retry(URLError, tries=3, delay=1, backoff=5)
def get_response(browser, url):
    return browser.open(url)



exitFlag = 0
class myThread (threading.Thread):
    def __init__(self, threadID, q):
        self.threadID= threadID
        self.q = q
        threading.Thread.__init__(self)
    def run(self):
        print "Starting thread " + str(self.threadID)
        while not exitFlag == 1:
            if not workQueue.empty():
                print "%s processing" % (self.threadID)
                process_user(self.q.get())
            else:
                time.sleep(1)
        print "Exiting " + str(self.threadID)

class mongoThread (threading.Thread):
    def __init__(self, q):
        self.q = q
        threading.Thread.__init__(self)
    def run(self):
        print "Starting mongo thread "
        while not exitFlag == 1:
            if not mongoQueue.empty():
                print "processing mongo thread" 
                profile = self.q.get()
                print profile
                save_nosql(profile, profile["id"])
            else:
                time.sleep(1)
        print "Exiting mongo thread"


print "ip:" + scraperwiki.scrape('http://httpbin.org/ip')

# login mobile
cj_m = mechanize.CookieJar()
br_m = get_browser(cj_m)


response_m = br_m.open("https://touch.xing.com/session/new")
br_m.select_form(nr=0)
print br_m.form

br_m["user_login[email_or_username]"] = 'anettholzi@einrot.com'
br_m["user_login[password]"] = 'apfelsaft'

response_m = br_m.submit()
print response_m.read()

# login desktop
cj_d = mechanize.CookieJar()
br_d = get_browser(cj_d)


response_d = br_d.open("https://login.xing.com/login")
br_d.select_form(nr=0)
print br_d.form

br_d["login_form[username]"] = "anettholzi@einrot.com"
br_d["login_form[password]"] = "apfelsaft"

response_d = br_d.submit()

print response_d.read()

#print parse_profile("Christian_Siebert19")

mongoQueue = Queue.Queue()


queueLock = threading.Lock()
workQueue = Queue.Queue()
threads = []

for threadID in range(1, THREADS + 1):
    thread = myThread(threadID, workQueue)
    thread.start()
    threads.append(thread)

#mongoThread = mongoThread(mongoQueue)
#mongoThread.start()
#threads.append(mongoThread)

process_user("Zeno琦望_Ziemke2")


while not (workQueue.empty() and mongoQueue.empty()):
    pass

exitFlag = 1

for t in threads:
    t.join()
print "all threads completed"

