import scraperwiki
import re
import time, datetime
import lxml.html
from lxml import etree
import sys, os
import urllib2
import uuid

# Blank Python



__source__ = "testVito"
uniqueId  = str(uuid.uuid4())
source = __source__ +  "__" + uniqueId
DAY = datetime.datetime.now().strftime('%G_%m_%d')



def khgprint(text):
    print text
    



def khgscrape(url):
    for i in range(1,6):
       try:
         html = scraperwiki.scrape(url,user_agent="Mozilla/5.0 (Windows NT 6.1; rv:17.0) Gecko/20100101 Firefox/17.0")
         break
       except:
         logError("Unexpected error: "+ str(sys.exc_info()[0]) + " (try number:" + str(i) + ")", iter_="url:"+url)
         if i==5:
           raise
    return html

def logError(msg,iter_=-1):
    global errors
    time_ = str(time.time())
    errdata = { "time":time_,"iter":iter_, "msg":msg, "source":source }
    scraperwiki.sqlite.save(unique_keys=['iter', 'time'], data=errdata, table_name="errors")
    text = time_ + ", ["+source+"]iter(" + str(iter_) + "): " + msg
    #errors += text + "\n"
    khgprint(text)
    
def logInfo(msg, iter_=-1):
    time_ = str(time.time())
    text = time_ + ", ["+__source__+"]iter(" + str(iter_) + "): " + msg
    khgprint(text)
    
def saveStatus(status, iter_=-1):
    time_ = str(time.time())
    statdata = { "time":time_, "iter":iter_, "source":source, "status":status}
    scraperwiki.sqlite.save(unique_keys=['iter', 'time'], data=statdata, table_name="status")



rg_url = re.compile('^.*?_(\d+)$', re.IGNORECASE|re.DOTALL)
rg_title = re.compile('(.*?)\s+(Mod\s+)?(\d+) (Diesel|Essence)', re.IGNORECASE|re.DOTALL)
rg_user = re.compile('', re.IGNORECASE|re.DOTALL)

CITY = "rabat-salé-zemmour-zaër"
QUERY = "voitures_doccasion?districtId=&min=&max=125000&f[4][from]=150&f[4][to]=&f[1][from]=&f[1][to]="
URL_BASE = "http://www.avito.ma/fr/" + CITY + "/" + QUERY + "&p="



def testEntryExists(scraper):
   pass

def parseDiv(div):
    infodiv = div.cssselect("div[class='catalog-item-info']")
    timediv = div.cssselect("div[class='catalog-item-date']")
    photodiv1 = div.cssselect("div[class='item-photo item-photo-multiple']")
    photodiv2 = div.cssselect("div[class='item-photo']")

    #infodiv
    a = infodiv[0].cssselect("a")[0]
    title = a.get("title")
    url = a.get("href")
    span = infodiv[0].cssselect("span")[0]
    price = int(span.text_content().replace(" ",""))
    infodata = infodiv[0].cssselect("div[class='catalog-item-info-data']")[0].text_content()
    ## url
    m = rg_url.search(url)
    id = -1
    if m:
        id = int(m.group(1))
    ## title
    m = rg_title.search(title)
    if m:
        car = m.group(1)
        model = int(m.group(3))
        carb = m.group(4)
    #timediv
    s_date = timediv[0].text_content()
    s_time = timediv[0].csselect("span")[0].text_content()
    #photodiv
    if len(photodiv1) > len(photodiv2):
        hasphoto = True
    else:
        hasphoto = False

    data = {"id":id, "title":title, "url":url, "price":price, "car":car, "model":model, "carb":carb, "hasphoto":hasphoto, "scrapetime":0l,"time":0l, "s_date":s_date, "s_time":s_time}
    return data


def scrape_page(page):
   logInfo("scraping page="+str(page),iter_=page)
   res = list()
   url = URL_BASE + str(page)
   html = khgscrape(url)
   html =  html.replace('"catalog-item catalog-item-odd"', '"catalog-item"')
   root=lxml.html.fromstring(html)
   divs = root.cssselect("div[class='catalog-item']")
   for div in divs:
        data = parseDiv(div)
        print data
        res.append(data)
   
   #  data = {"scraper":scraper,"scraperc":scraperc,"user":user,"userc":userc,"language":lang,"status":stat}
   #  res.append(data)
   return res
   

      
      
def main(offset=1,count=1):
   logInfo("start scraper: offset=" + str(offset) + ", count=" + str(count))
   if count<1:
      count =1
      logInfo("change count to:" + str(count))
   
   #count+=1
   time.sleep(5)
   for i in range(offset,offset + count):
      try:
        saveStatus("start", iter_ = i)
        data = scrape_page(i)
        for entry in data:
           if testScraperExists(entry['scraper']):
              saveStatus("scraper-exists", iter_=str(i) + ":" + entry['scraper'])
      except urllib2.HTTPError as e:
        logError("HTTPError: " +str(e) + ", " +  str(e.code), iter_=i)
      except urllib2.URLError as e:
        logError("URLError: "  +str(e) + ", " +  str(e.args), iter_=i)




main()
