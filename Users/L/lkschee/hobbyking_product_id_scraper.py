#SQLite quirks, system takes query and wraps it in such a way that special things cannot happen
#scraperwiki does not allow indexes or require setting up cursors or committing
#also automatically opens your database

#Important Links,
#http://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=$productId

#Hobyking link mapping,
#Categories, __488__484__Cars_Parts-1_10th_Scale.html -> pc=484&idCategory=488

#Use dictionaries for core storage because you can store initial values and then
#when updating records you can update the dictionary and the commit it

#Dicts can update Dicts...
#Converting dicts to lists the dict gets sorted

#Create unique index does not work


import scraperwiki as scraper
import scraperwiki.sqlite as lite
import lxml.html as parser
from datetime import datetime
from urlparse import parse_qsl, urlparse
from datetime import date
import re
import Queue
import threading

queue = Queue.Queue()


######################### GLOBAL PARAMETERS #################################

scrapesite = "http://www.hobbyking.com/hobbyking/store/uh_listCategoriesAndProducts.asp"
scrapeprod = "http://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct="

catpagesrx  = "curPage"
prodpagesrx = "(?<![0-9])__([0-9]*)__(?![0-9])"

scrapecat = [   #ukpc, ukipcategory, ukcurpage, lstdate
               ('86',         1,       "date")
            ]

CoreKeys = [
            ['ukPrId'      , 'INT' ],   #Product ID
            ['Price'       , 'REAL'],   #$
            ['Capacity'    , 'INT' ],   #milliAmp Hours
            ['Volt'        , 'REAL'],   #Voltage
            ['Energy'      , 'REAL'],   #Volt * Capacity
    
            ['Config'      , 'INT' ],   #Number of Cells
            ['Charge'      , 'INT' ],   #Charge Rate
            ['Discharge'   , 'INT' ],   #Discharge Rate
    
            ['Weight'      , 'REAL'],   #Grams
    
            ['Height'      , 'INT' ],   #mm
            ['Length'      , 'INT' ],   #mm
            ['Width'       , 'INT' ],   #mm
            ['Date'        , 'TEXT']    #Date First Seen
           ]

PageParser = [
            ['ukLink'      , 'TEXT'],   #Product links yet to be explored
            ['LstDate'     , 'TEXT']    #Last date parsed, parse once per month
             ]

CategoryParser = [
            ['ukidCategory', 'INT' ],   #url parameter
            ['ukcurPage'   , 'INT' ],   #Page that has been parsed
            ['LstDate'     , 'TEXT']    #Last date parsed, parse once per day
                 ]

########################       CLASSES        ################################


class core_store(object):
    def __init__(self,table,keys):
        self._table = table
        self._keys = keys
        #self.core_reset()
        self.setup()


    def setup(self):
        if len(lite.table_info(self._table)) > 0: return 0
        
        query = "CREATE TABLE IF NOT EXISTS "+self._table+" ("

        for key in self._keys:
            query = query+" "+key[0]+" "+key[1]

        unique = ""
        for key in self._keys:
            if "uk" in key[0]:
                unique = unique+" "+key[0]+","
        print "Unique Keys in",self._table+":",unique

        query = query+" UNIQUE("+unique+") ON CONFLICT IGNORE)"
        query = query.replace("INT ","INT, ")
        query = query.replace("REAL ","REAL, ")
        query = query.replace("TEXT ","TEXT, ")
        query = query.replace(",)", ")")

        print query
        lite.execute(query)

    def core_reset(self):
        lite.execute("DROP TABLE if exists "+self._table)

    def additem(self,data):
        lite.execute("INSERT into "+self._table+" values (?"+(len(self._keys)-1)*", ?"+")", data+('0',)*(len(self._keys)-len(data)))

    def updateitem(self,data):
        print "Updating:",data
        lite.execute("INSERT or REPLACE into "+self._table+" values (?"+(len(self._keys)-1)*", ?"+")", data+('0',)*(len(self._keys)-len(data)))

    def getdata(self):
        return lite.execute("select * from "+self._table)

    def commit(self):
        lite.commit()

    def __close__(self):
        lite.commit()



class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            host = self.queue.get()
            url = urllib2.urlopen(host)

            self.queue.task_done()
        
########################      FUNCTIONS       ################################

def urltodict(url):              #convert url parameters to a dict
    keylist = list()
    valuelist = list()
    urldict = dict()
        
    for item in parse_qsl(urlparse(url).query):
        keylist.append(item[0])
        valuelist.append(item[1])
        
    urldict.update(zip(keylist,valuelist))

    return urldict

def dicttourl(url,urldict):     #Convert a query in a dict to a useable url
    query = ""
    del urldict['LstDate']
    for key in urldict:
        query = query+"&"+key+"="+str(urldict[key])
    out = url+"?"+query
    out = out.replace("?&","?")
    return out

def querytodictlist(data):
    out = list()
    for value in data['data']:
        newval = dict()
        for key in data['keys']:
            newval[key] = value[data['keys'].index(key)]
        out.append(newval)
    return out

#http://hobbyking.com/hobbyking/store/uh_listCategoriesAndProducts.asp?whl=XX&pc=&idCategory=86&curPage=2&v=&sortlist=&sortMotor=&LiPoConfig=&CatSortOrder=desc
def ParseCat(link):
    CatData = urltodict(link)
    CatStore.additem((CatData['idCategory'], CatData['curPage'], 0))

def ParseLink(link):
    LinkStore.additem((link, 0))

def ParsePage(page):
    print "Parseing Page"
    for link in page.iterlinks():
        url = link[2]
        if   type(CatRegex.search(url)).__name__  == 'SRE_Match': ParseCat(url)
        elif type(PageRegex.search(url)).__name__ == 'SRE_Match': ParseLink(url)

########################         CODE        ################################

#1) Load scrapecat into db
#2) Load category page
#3) Look at the bottom of a page for links to more pages in category
#4) Store a list of the categories and the pages contained
#5) Page parser reads the list of known categories
#6) Page parser gets the product links from each category page
#7) Page parser gets desired information from product page
#8) Loops till complete


#a) Setup Environment
ProductStore = core_store('ProductLinks', CoreKeys)
LinkStore = core_store('ScrapedLinks', PageParser)
CatStore = core_store('CatPages', CategoryParser)

CatRegex  = re.compile(catpagesrx)
PageRegex = re.compile(prodpagesrx)


#1) Load scrapecat into db
for item in scrapecat:
    CatStore.additem(item)


#2) Load category pages
CategoryPages = querytodictlist(CatStore.getdata())


for page in CategoryPages:
    if not page['LstDate']==str(date.today()):
        url = dicttourl(scrapesite,page).replace('uk','')
        print "URL:",url
    
        html = scraper.scrape(url)
        rawpage = parser.fromstring(html)

        ParsePage(rawpage)

        LinkStore.commit()
        CatStore.updateitem((page['ukidCategory'], page['ukcurPage'], str(date.today())))




ProductStore.__close__()
LinkStore.__close__()
CatStore.__close__() #SQLite quirks, system takes query and wraps it in such a way that special things cannot happen
#scraperwiki does not allow indexes or require setting up cursors or committing
#also automatically opens your database

#Important Links,
#http://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=$productId

#Hobyking link mapping,
#Categories, __488__484__Cars_Parts-1_10th_Scale.html -> pc=484&idCategory=488

#Use dictionaries for core storage because you can store initial values and then
#when updating records you can update the dictionary and the commit it

#Dicts can update Dicts...
#Converting dicts to lists the dict gets sorted

#Create unique index does not work


import scraperwiki as scraper
import scraperwiki.sqlite as lite
import lxml.html as parser
from datetime import datetime
from urlparse import parse_qsl, urlparse
from datetime import date
import re
import Queue
import threading

queue = Queue.Queue()


######################### GLOBAL PARAMETERS #################################

scrapesite = "http://www.hobbyking.com/hobbyking/store/uh_listCategoriesAndProducts.asp"
scrapeprod = "http://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct="

catpagesrx  = "curPage"
prodpagesrx = "(?<![0-9])__([0-9]*)__(?![0-9])"

scrapecat = [   #ukpc, ukipcategory, ukcurpage, lstdate
               ('86',         1,       "date")
            ]

CoreKeys = [
            ['ukPrId'      , 'INT' ],   #Product ID
            ['Price'       , 'REAL'],   #$
            ['Capacity'    , 'INT' ],   #milliAmp Hours
            ['Volt'        , 'REAL'],   #Voltage
            ['Energy'      , 'REAL'],   #Volt * Capacity
    
            ['Config'      , 'INT' ],   #Number of Cells
            ['Charge'      , 'INT' ],   #Charge Rate
            ['Discharge'   , 'INT' ],   #Discharge Rate
    
            ['Weight'      , 'REAL'],   #Grams
    
            ['Height'      , 'INT' ],   #mm
            ['Length'      , 'INT' ],   #mm
            ['Width'       , 'INT' ],   #mm
            ['Date'        , 'TEXT']    #Date First Seen
           ]

PageParser = [
            ['ukLink'      , 'TEXT'],   #Product links yet to be explored
            ['LstDate'     , 'TEXT']    #Last date parsed, parse once per month
             ]

CategoryParser = [
            ['ukidCategory', 'INT' ],   #url parameter
            ['ukcurPage'   , 'INT' ],   #Page that has been parsed
            ['LstDate'     , 'TEXT']    #Last date parsed, parse once per day
                 ]

########################       CLASSES        ################################


class core_store(object):
    def __init__(self,table,keys):
        self._table = table
        self._keys = keys
        #self.core_reset()
        self.setup()


    def setup(self):
        if len(lite.table_info(self._table)) > 0: return 0
        
        query = "CREATE TABLE IF NOT EXISTS "+self._table+" ("

        for key in self._keys:
            query = query+" "+key[0]+" "+key[1]

        unique = ""
        for key in self._keys:
            if "uk" in key[0]:
                unique = unique+" "+key[0]+","
        print "Unique Keys in",self._table+":",unique

        query = query+" UNIQUE("+unique+") ON CONFLICT IGNORE)"
        query = query.replace("INT ","INT, ")
        query = query.replace("REAL ","REAL, ")
        query = query.replace("TEXT ","TEXT, ")
        query = query.replace(",)", ")")

        print query
        lite.execute(query)

    def core_reset(self):
        lite.execute("DROP TABLE if exists "+self._table)

    def additem(self,data):
        lite.execute("INSERT into "+self._table+" values (?"+(len(self._keys)-1)*", ?"+")", data+('0',)*(len(self._keys)-len(data)))

    def updateitem(self,data):
        print "Updating:",data
        lite.execute("INSERT or REPLACE into "+self._table+" values (?"+(len(self._keys)-1)*", ?"+")", data+('0',)*(len(self._keys)-len(data)))

    def getdata(self):
        return lite.execute("select * from "+self._table)

    def commit(self):
        lite.commit()

    def __close__(self):
        lite.commit()



class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            host = self.queue.get()
            url = urllib2.urlopen(host)

            self.queue.task_done()
        
########################      FUNCTIONS       ################################

def urltodict(url):              #convert url parameters to a dict
    keylist = list()
    valuelist = list()
    urldict = dict()
        
    for item in parse_qsl(urlparse(url).query):
        keylist.append(item[0])
        valuelist.append(item[1])
        
    urldict.update(zip(keylist,valuelist))

    return urldict

def dicttourl(url,urldict):     #Convert a query in a dict to a useable url
    query = ""
    del urldict['LstDate']
    for key in urldict:
        query = query+"&"+key+"="+str(urldict[key])
    out = url+"?"+query
    out = out.replace("?&","?")
    return out

def querytodictlist(data):
    out = list()
    for value in data['data']:
        newval = dict()
        for key in data['keys']:
            newval[key] = value[data['keys'].index(key)]
        out.append(newval)
    return out

#http://hobbyking.com/hobbyking/store/uh_listCategoriesAndProducts.asp?whl=XX&pc=&idCategory=86&curPage=2&v=&sortlist=&sortMotor=&LiPoConfig=&CatSortOrder=desc
def ParseCat(link):
    CatData = urltodict(link)
    CatStore.additem((CatData['idCategory'], CatData['curPage'], 0))

def ParseLink(link):
    LinkStore.additem((link, 0))

def ParsePage(page):
    print "Parseing Page"
    for link in page.iterlinks():
        url = link[2]
        if   type(CatRegex.search(url)).__name__  == 'SRE_Match': ParseCat(url)
        elif type(PageRegex.search(url)).__name__ == 'SRE_Match': ParseLink(url)

########################         CODE        ################################

#1) Load scrapecat into db
#2) Load category page
#3) Look at the bottom of a page for links to more pages in category
#4) Store a list of the categories and the pages contained
#5) Page parser reads the list of known categories
#6) Page parser gets the product links from each category page
#7) Page parser gets desired information from product page
#8) Loops till complete


#a) Setup Environment
ProductStore = core_store('ProductLinks', CoreKeys)
LinkStore = core_store('ScrapedLinks', PageParser)
CatStore = core_store('CatPages', CategoryParser)

CatRegex  = re.compile(catpagesrx)
PageRegex = re.compile(prodpagesrx)


#1) Load scrapecat into db
for item in scrapecat:
    CatStore.additem(item)


#2) Load category pages
CategoryPages = querytodictlist(CatStore.getdata())


for page in CategoryPages:
    if not page['LstDate']==str(date.today()):
        url = dicttourl(scrapesite,page).replace('uk','')
        print "URL:",url
    
        html = scraper.scrape(url)
        rawpage = parser.fromstring(html)

        ParsePage(rawpage)

        LinkStore.commit()
        CatStore.updateitem((page['ukidCategory'], page['ukcurPage'], str(date.today())))




ProductStore.__close__()
LinkStore.__close__()
CatStore.__close__() 