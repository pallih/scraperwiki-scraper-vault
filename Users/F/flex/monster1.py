#!/usr/bin/env python

import scraperwiki
import sys
import lxml.etree
import lxml.html
from lxml.html.clean import clean_html
import urllib
import urllib2
from urlparse import urlparse
import json
import csv
#import time
import dateutil.parser
from datetime import datetime, date, time
import re
from pytz import timezone 

# start: initialize variables
countNew = 0
maxPages = 50
baseURL  = "http://jobsearch.monster.com/search/"
states=[ 'Colorado', 'Connecticut','District+of+Columbia', 'Delaware',  'Kansas','Louisiana', 'New+York','New+Jersey',  'Nebraska', 'Oregon', 'South+Carolina', 'Washington',   'Wisconsin',  'Wyoming']
degrees=[ 'High-School', 'Associate-Degree', "Bachelor's-Degree", 'Advanced-Degree']
experiences=['0','3', '5', '10','15']
careers=[  'Student-High-School',  'Student-Undergraduate-Graduate',  'Entry-Level', 'Experienced-Non-Manager', 'Manager-Manager-Supervisor-of-Staff','Executive-SVP-VP-Department-Head-etc','Senior-Executive-President-CFO-etc']
industry=['Accounting-Auditing-Services','Advertising-PR-Services','Aerospace-Defense','Agriculture-Forestry-Fishing','Architectural-Design-Services', 'Automotive-Parts-Mfg','Automotive-Sales-Repair-Services','Banking','Biotechnology-Pharmaceuticals','Broadcasting-Music-Film','Business-Services-Other','Chemicals-Petro-Chemicals','Clothing-Textile-Manufacturing','Computer-Hardware','Computer-Software','Computer-IT-Services','Construction-Industrial-Facilities-Infrastructure','Construction-Residential-&amp;-Commercial-Office','Consumer-Packaged-Goods-Manufacturing','Education','Electronics-Components-Semiconductor-Mfg','Energy-Utilities','Engineering-Services','Entertainment-Venues-Theaters','Financial-Services','Food-Beverage-Production','Government-Military','Healthcare-Services','Hotels-Lodging','Insurance','Internet-Services','Legal-Services','Management-Consulting-Services','Manufacturing-Other','Marine-Mfg-Services','Medical-Devices-Supplies','Metals-Minerals','Nonprofit-Charitable-Organizations','Other-Not-Classified','Performing-Fine-Arts','Personal-Household-Services','Printing-Publishing','Real-Estate-Property-Management','Rental-Services','Restaurant-Food-Services','Retail','Security-Surveillance','Sports-Physical-Recreation','Staffing-Employment-Agencies','Telecommunications-Services','Transport-Storage-Materials','Travel-Transportation-Tourism','Waste-Management','Wholesale-Trade-Import-Export']

class vacancy(object):
    def __init__(self, idn=None, name=None, region=None, date=None, company=None, wage=None, description=None, degree=None, exper=None, career=None, indu=None, state=None, duration=None, jobDetail=None):
        self.idn=idn
        self.name=name
        self.state=state
        self.date=date
        self.wage=wage
        self.company=company
        self.description=description
        self.degree=degree
        self.experience=exper
        self.career=career
        self.industry=indu
        self.region=region
        self.degree=degree
        self.duration=duration
        self.jobDetail=jobDetail
        
# List of text phrases to be removed from data (how to handle "(Raum "...")" ?)
redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    try:    redundantText.append(row[0].decode('utf-8'))
    except: print sys.exc_info() #pass

def fix_encoding_mistakes(unistr):
    import itertools
    l = [(0b11000010, i) for i in range(0b10100000, 0b10111111 + 1)]
    l += [(0b11000011, i) for i in range(0b10000000, 0b10111111 + 1)]
    for a, b in l:
        l1_mistake = ('%s%s' % (chr(a), chr(b))).decode('latin1')
        l9_mistake = ('%s%s' % (chr(a), chr(b))).decode('latin9')
        l1_fix = ('%s%s' % (chr(a), chr(b))).decode('utf-8')
        unistr = unistr.replace(l1_mistake, l1_fix)
        if l9_mistake != l1_mistake:
            l9_fix = ('%s%s' % (chr(a), chr(b))).decode('utf-8').encode('latin1').decode('latin9')
            unistr = unistr.replace(l9_mistake, l9_fix)
    unistr = unistr.replace(u'\xe2\x82\xac', u'\u20ac')
    return unistr

def scrapeTable(root, locale, vaclist, degree, exper, career, indu):
    
    for job in root.cssselect("div#primaryResults table tr.odd, div#primaryResults table tr.even"): 
        jobName = job.cssselect("div.jobTitleContainer a")
        try:    jobName[0]
        except: jobName = []
        idNumber                      = " ".join(jobName[0].attrib['name'].strip().split())
        saved=False
        for vac in vaclist:
            if idNumber in vac.idn:
                print "vac saved:", idNumber
                vac.industry+='/+ '+ indu
                saved=True
                break
            else:  pass 
        if saved:
            continue
        dataAlreadySaved=False 
        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where idn='"+idNumber+"'")
        silliconTime=timezone('US/Pacific')
        pst = datetime.now(silliconTime)
        duration = str(pst.strftime('%Y-%m-%d_%H-%M-%S'))
        if dataAlreadySaved: 
            print "in database"
            try:
                scraperwiki.sqlite.execute("UPDATE swdata SET duration = '%s' WHERE idn = '%s'" % (duration, idNumber))
                scraperwiki.sqlite.commit()           
                print "database updated"
            except: pass
            continue
        print "new vac", idNumber
        name            = " ".join(jobName[0].text.strip().split())
        description=""
        duration = "0"
        try:
            pageHTML              = scraperwiki.scrape(jobName[0].attrib['href'])
            pageRoot              = lxml.html.fromstring(clean_html(pageHTML))
            descrip = " ".join(pageRoot.text_content().strip().split())
            descrition=''.join(descrip.partition("#monsterAppliesPageWrapper")[2:])
            print description
            if description==[]:
                description=descrip
                
        except: print sys.exc_info() # pass
        jobDetail      = jobName[0].attrib['onclick']
        index1       = str(jobDetail).index("AVSDM") + 6
        try:    date = jobDetail[index1:index1 + 16]
        except: date = ""
        date           = dateutil.parser.parse(date)  #time.strptime(date, '%Y-%m-%d %H:%M')
        company=''
        region=''
         
        
        try:
            company = " ".join(fix_encoding_mistakes(job.cssselect("div.companyContainer a[href]")[0].text.strip()).split())
            company = re.sub("^- ", "", comapny).strip()
            for phrase in redundantText:
                company  = comapny.replace(phrase, " ").strip()
        except: pass
        region = ""
        wage=""
        try:
            region     = fix_encoding_mistakes(job.cssselect(".jobLocationSingleLine a")[0].attrib['title'])
            regionText = region
            for phrase in redundantText:
                region  = region.replace(phrase, " ").strip()
                region     = re.sub("^- ", "", region).strip()
                region     = re.sub("^, ", "", region).strip()
        except: pass
        try:
            wage    = fix_encoding_mistakes(job.cssselect(".fnt13")[0].text.strip())
            print wage
        except: pass 
        
        #save in vaclist
        vaclist.append(vacancy(idNumber, name, region, date, company, wage, description, degree, exper, career, indu, locale, duration, jobDetail))
            
    return vaclist

# recover after interruptions (e.g., CPUTimeExceededError)
firstLocale = scraperwiki.sqlite.get_var("lastLocale", states[0])
if firstLocale == None: firstLocale="Alaska"
startFound  = False
print "Start or continue from locale: ", firstLocale

def scrape(locale, degree, exper, career):
    vaclist = []
    vaclist.append(vacancy('idn', 'name', 'region', 'date', 'company', 'wage', 'description', 'degree', 'exper', 'career', 'indu', 'state'))
    for indu in industry:
        for page in range(maxPages):
            page  = page + 1
            sUrl  = baseURL + str(indu)+"_3?lv="+str(career)+"&eid="+str(degree)+"&ye="+str(exper)+"-year&pg="+str(page)+"&where="+str(locale)+"&rad=5-miles&sort=dt.rv.di" 
            print sUrl
            html  = scraperwiki.scrape(sUrl)
            root  = lxml.html.fromstring(html)
            try:
                currentPage = int(root.cssselect(".navLinks .boxWrap.selected a")[0].text.strip())
                if page != currentPage: break
            except:
                print "Problems with locale: ", locale, " - no data? ", sUrl 
                break
            record = scrapeTable(root, locale, vaclist, degree, exper, career, indu)
    return vaclist

for locale in states:
    if firstLocale == locale or startFound:
        startFound = True   
        for degree in degrees:
            print degree
            for exper in experiences:
                print exper
                for career in careers:
                    print career
                    vaclist=scrape(locale, degree, exper, career)
                    for vac in vaclist:
                        result={}
                        result["idn"]=vac.idn
                        result["name"]=vac.name
                        result["state"]=vac.state
                        result["date"]=vac.date
                        result["wage"]=vac.wage
                        result["company"]=vac.company
                        result["description"]=vac.description
                        result["experience"]=vac.experience
                        result["career"]=vac.career
                        result["industry"]=vac.industry
                        result["region"]=vac.region
                        result["degree"]=vac.degree
                        result["duration"]=vac.duration
                        result["jobDetail"]=vac.jobDetail
                        result["uploadDate"]=vac.date
                        
                        scraperwiki.sqlite.save(["idn"], result)
        scraperwiki.sqlite.save_var("lastLocale", locale) # store the last locale that was scraped
        print "Completed locale: ", locale
    else:
        print "Skipped locale: ", locale
scraperwiki.sqlite.save_var("lastLocale", states[0]) # reset stored locale after all scraping is done

sys.exit()

#cleanup
count = 0
jobCount = scraperwiki.sqlite.select('count(*) FROM swdata')[0]["count(*)"]
print "Starting cleanup of ", jobCount, " rows!"
windowLength = 500
windowCount  = jobCount / windowLength
offset2       = scraperwiki.sqlite.get_var("offset2", 0)
for window in range(windowCount):
    rows = scraperwiki.sqlite.select('* from swdata LIMIT '+str(windowLength)+' OFFSET2 '+str(offset2) ) 
    for record in rows:
        count = count + 1
        if count%1000 == 0: print count, " jobs processed - up to ID: ", 1000+offset2
        try:    
            record["company"] = fix_encoding_mistakes(record["company"])
            record["company"] = re.sub("^- ", "", record["company"]).strip()
            for phrase in redundantText:
                record["company"]  = record["company"].replace(phrase, " ").strip()
        except: pass
        try:    
            record["name"]      = fix_encoding_mistakes(record["name"])
            for phrase in redundantText:
                record["name"]  = record["name"].replace(phrase, " ").strip()
        except: pass
        try:    
            record["region"]      = fix_encoding_mistakes(record["region"])
            for phrase in redundantText:
                record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
            scraperwiki.sqlite.save(["id"], record)
    
            regionList = []
            regionText = record["region"]
            if   regionText.count(',') >= 2: regionList = regionText.split(',')
    #        if "/" in regionText:            regionList = regionText.split('/')
            elif regionText.count(';') >= 2: regionList = regionText.split(';')
            elif "+" in regionText:          regionList = regionText.split('+')
            elif "+++" in regionText:        regionList = regionText.split('+++')
    #        elif "-" in regionText:          regionList = regionText.split('-')
            elif " oder " in regionText:     regionList = regionText.split(' oder ')
            elif " und " in regionText:      regionList = regionText.split(' und ')
            elif " and " in regionText:      regionList = regionText.split(' and ')
            elif " or " in regionText:       regionList = regionText.split(' or ')
            if regionList != []: 
                regionList = list(set(regionList))
    #            print regionList, regionText
    
            regionCount = 1
            orgID = record["id"]
            for region in regionList:
                regionName = region.strip()
                if len(regionName) <= 2: continue
                record["region"] = regionName
                record["id"]     = orgID + "_" + str(regionCount)
                regionCount      = regionCount +1
                scraperwiki.sqlite.save(["id"], record)
        except: pass
    offset2 = offset2 + windowLength
    scraperwiki.sqlite.save_var("offset2", offset2)
scraperwiki.sqlite.save_var("offset2", 0)
#!/usr/bin/env python

import scraperwiki
import sys
import lxml.etree
import lxml.html
from lxml.html.clean import clean_html
import urllib
import urllib2
from urlparse import urlparse
import json
import csv
#import time
import dateutil.parser
from datetime import datetime, date, time
import re
from pytz import timezone 

# start: initialize variables
countNew = 0
maxPages = 50
baseURL  = "http://jobsearch.monster.com/search/"
states=[ 'Colorado', 'Connecticut','District+of+Columbia', 'Delaware',  'Kansas','Louisiana', 'New+York','New+Jersey',  'Nebraska', 'Oregon', 'South+Carolina', 'Washington',   'Wisconsin',  'Wyoming']
degrees=[ 'High-School', 'Associate-Degree', "Bachelor's-Degree", 'Advanced-Degree']
experiences=['0','3', '5', '10','15']
careers=[  'Student-High-School',  'Student-Undergraduate-Graduate',  'Entry-Level', 'Experienced-Non-Manager', 'Manager-Manager-Supervisor-of-Staff','Executive-SVP-VP-Department-Head-etc','Senior-Executive-President-CFO-etc']
industry=['Accounting-Auditing-Services','Advertising-PR-Services','Aerospace-Defense','Agriculture-Forestry-Fishing','Architectural-Design-Services', 'Automotive-Parts-Mfg','Automotive-Sales-Repair-Services','Banking','Biotechnology-Pharmaceuticals','Broadcasting-Music-Film','Business-Services-Other','Chemicals-Petro-Chemicals','Clothing-Textile-Manufacturing','Computer-Hardware','Computer-Software','Computer-IT-Services','Construction-Industrial-Facilities-Infrastructure','Construction-Residential-&amp;-Commercial-Office','Consumer-Packaged-Goods-Manufacturing','Education','Electronics-Components-Semiconductor-Mfg','Energy-Utilities','Engineering-Services','Entertainment-Venues-Theaters','Financial-Services','Food-Beverage-Production','Government-Military','Healthcare-Services','Hotels-Lodging','Insurance','Internet-Services','Legal-Services','Management-Consulting-Services','Manufacturing-Other','Marine-Mfg-Services','Medical-Devices-Supplies','Metals-Minerals','Nonprofit-Charitable-Organizations','Other-Not-Classified','Performing-Fine-Arts','Personal-Household-Services','Printing-Publishing','Real-Estate-Property-Management','Rental-Services','Restaurant-Food-Services','Retail','Security-Surveillance','Sports-Physical-Recreation','Staffing-Employment-Agencies','Telecommunications-Services','Transport-Storage-Materials','Travel-Transportation-Tourism','Waste-Management','Wholesale-Trade-Import-Export']

class vacancy(object):
    def __init__(self, idn=None, name=None, region=None, date=None, company=None, wage=None, description=None, degree=None, exper=None, career=None, indu=None, state=None, duration=None, jobDetail=None):
        self.idn=idn
        self.name=name
        self.state=state
        self.date=date
        self.wage=wage
        self.company=company
        self.description=description
        self.degree=degree
        self.experience=exper
        self.career=career
        self.industry=indu
        self.region=region
        self.degree=degree
        self.duration=duration
        self.jobDetail=jobDetail
        
# List of text phrases to be removed from data (how to handle "(Raum "...")" ?)
redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    try:    redundantText.append(row[0].decode('utf-8'))
    except: print sys.exc_info() #pass

def fix_encoding_mistakes(unistr):
    import itertools
    l = [(0b11000010, i) for i in range(0b10100000, 0b10111111 + 1)]
    l += [(0b11000011, i) for i in range(0b10000000, 0b10111111 + 1)]
    for a, b in l:
        l1_mistake = ('%s%s' % (chr(a), chr(b))).decode('latin1')
        l9_mistake = ('%s%s' % (chr(a), chr(b))).decode('latin9')
        l1_fix = ('%s%s' % (chr(a), chr(b))).decode('utf-8')
        unistr = unistr.replace(l1_mistake, l1_fix)
        if l9_mistake != l1_mistake:
            l9_fix = ('%s%s' % (chr(a), chr(b))).decode('utf-8').encode('latin1').decode('latin9')
            unistr = unistr.replace(l9_mistake, l9_fix)
    unistr = unistr.replace(u'\xe2\x82\xac', u'\u20ac')
    return unistr

def scrapeTable(root, locale, vaclist, degree, exper, career, indu):
    
    for job in root.cssselect("div#primaryResults table tr.odd, div#primaryResults table tr.even"): 
        jobName = job.cssselect("div.jobTitleContainer a")
        try:    jobName[0]
        except: jobName = []
        idNumber                      = " ".join(jobName[0].attrib['name'].strip().split())
        saved=False
        for vac in vaclist:
            if idNumber in vac.idn:
                print "vac saved:", idNumber
                vac.industry+='/+ '+ indu
                saved=True
                break
            else:  pass 
        if saved:
            continue
        dataAlreadySaved=False 
        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where idn='"+idNumber+"'")
        silliconTime=timezone('US/Pacific')
        pst = datetime.now(silliconTime)
        duration = str(pst.strftime('%Y-%m-%d_%H-%M-%S'))
        if dataAlreadySaved: 
            print "in database"
            try:
                scraperwiki.sqlite.execute("UPDATE swdata SET duration = '%s' WHERE idn = '%s'" % (duration, idNumber))
                scraperwiki.sqlite.commit()           
                print "database updated"
            except: pass
            continue
        print "new vac", idNumber
        name            = " ".join(jobName[0].text.strip().split())
        description=""
        duration = "0"
        try:
            pageHTML              = scraperwiki.scrape(jobName[0].attrib['href'])
            pageRoot              = lxml.html.fromstring(clean_html(pageHTML))
            descrip = " ".join(pageRoot.text_content().strip().split())
            descrition=''.join(descrip.partition("#monsterAppliesPageWrapper")[2:])
            print description
            if description==[]:
                description=descrip
                
        except: print sys.exc_info() # pass
        jobDetail      = jobName[0].attrib['onclick']
        index1       = str(jobDetail).index("AVSDM") + 6
        try:    date = jobDetail[index1:index1 + 16]
        except: date = ""
        date           = dateutil.parser.parse(date)  #time.strptime(date, '%Y-%m-%d %H:%M')
        company=''
        region=''
         
        
        try:
            company = " ".join(fix_encoding_mistakes(job.cssselect("div.companyContainer a[href]")[0].text.strip()).split())
            company = re.sub("^- ", "", comapny).strip()
            for phrase in redundantText:
                company  = comapny.replace(phrase, " ").strip()
        except: pass
        region = ""
        wage=""
        try:
            region     = fix_encoding_mistakes(job.cssselect(".jobLocationSingleLine a")[0].attrib['title'])
            regionText = region
            for phrase in redundantText:
                region  = region.replace(phrase, " ").strip()
                region     = re.sub("^- ", "", region).strip()
                region     = re.sub("^, ", "", region).strip()
        except: pass
        try:
            wage    = fix_encoding_mistakes(job.cssselect(".fnt13")[0].text.strip())
            print wage
        except: pass 
        
        #save in vaclist
        vaclist.append(vacancy(idNumber, name, region, date, company, wage, description, degree, exper, career, indu, locale, duration, jobDetail))
            
    return vaclist

# recover after interruptions (e.g., CPUTimeExceededError)
firstLocale = scraperwiki.sqlite.get_var("lastLocale", states[0])
if firstLocale == None: firstLocale="Alaska"
startFound  = False
print "Start or continue from locale: ", firstLocale

def scrape(locale, degree, exper, career):
    vaclist = []
    vaclist.append(vacancy('idn', 'name', 'region', 'date', 'company', 'wage', 'description', 'degree', 'exper', 'career', 'indu', 'state'))
    for indu in industry:
        for page in range(maxPages):
            page  = page + 1
            sUrl  = baseURL + str(indu)+"_3?lv="+str(career)+"&eid="+str(degree)+"&ye="+str(exper)+"-year&pg="+str(page)+"&where="+str(locale)+"&rad=5-miles&sort=dt.rv.di" 
            print sUrl
            html  = scraperwiki.scrape(sUrl)
            root  = lxml.html.fromstring(html)
            try:
                currentPage = int(root.cssselect(".navLinks .boxWrap.selected a")[0].text.strip())
                if page != currentPage: break
            except:
                print "Problems with locale: ", locale, " - no data? ", sUrl 
                break
            record = scrapeTable(root, locale, vaclist, degree, exper, career, indu)
    return vaclist

for locale in states:
    if firstLocale == locale or startFound:
        startFound = True   
        for degree in degrees:
            print degree
            for exper in experiences:
                print exper
                for career in careers:
                    print career
                    vaclist=scrape(locale, degree, exper, career)
                    for vac in vaclist:
                        result={}
                        result["idn"]=vac.idn
                        result["name"]=vac.name
                        result["state"]=vac.state
                        result["date"]=vac.date
                        result["wage"]=vac.wage
                        result["company"]=vac.company
                        result["description"]=vac.description
                        result["experience"]=vac.experience
                        result["career"]=vac.career
                        result["industry"]=vac.industry
                        result["region"]=vac.region
                        result["degree"]=vac.degree
                        result["duration"]=vac.duration
                        result["jobDetail"]=vac.jobDetail
                        result["uploadDate"]=vac.date
                        
                        scraperwiki.sqlite.save(["idn"], result)
        scraperwiki.sqlite.save_var("lastLocale", locale) # store the last locale that was scraped
        print "Completed locale: ", locale
    else:
        print "Skipped locale: ", locale
scraperwiki.sqlite.save_var("lastLocale", states[0]) # reset stored locale after all scraping is done

sys.exit()

#cleanup
count = 0
jobCount = scraperwiki.sqlite.select('count(*) FROM swdata')[0]["count(*)"]
print "Starting cleanup of ", jobCount, " rows!"
windowLength = 500
windowCount  = jobCount / windowLength
offset2       = scraperwiki.sqlite.get_var("offset2", 0)
for window in range(windowCount):
    rows = scraperwiki.sqlite.select('* from swdata LIMIT '+str(windowLength)+' OFFSET2 '+str(offset2) ) 
    for record in rows:
        count = count + 1
        if count%1000 == 0: print count, " jobs processed - up to ID: ", 1000+offset2
        try:    
            record["company"] = fix_encoding_mistakes(record["company"])
            record["company"] = re.sub("^- ", "", record["company"]).strip()
            for phrase in redundantText:
                record["company"]  = record["company"].replace(phrase, " ").strip()
        except: pass
        try:    
            record["name"]      = fix_encoding_mistakes(record["name"])
            for phrase in redundantText:
                record["name"]  = record["name"].replace(phrase, " ").strip()
        except: pass
        try:    
            record["region"]      = fix_encoding_mistakes(record["region"])
            for phrase in redundantText:
                record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
            scraperwiki.sqlite.save(["id"], record)
    
            regionList = []
            regionText = record["region"]
            if   regionText.count(',') >= 2: regionList = regionText.split(',')
    #        if "/" in regionText:            regionList = regionText.split('/')
            elif regionText.count(';') >= 2: regionList = regionText.split(';')
            elif "+" in regionText:          regionList = regionText.split('+')
            elif "+++" in regionText:        regionList = regionText.split('+++')
    #        elif "-" in regionText:          regionList = regionText.split('-')
            elif " oder " in regionText:     regionList = regionText.split(' oder ')
            elif " und " in regionText:      regionList = regionText.split(' und ')
            elif " and " in regionText:      regionList = regionText.split(' and ')
            elif " or " in regionText:       regionList = regionText.split(' or ')
            if regionList != []: 
                regionList = list(set(regionList))
    #            print regionList, regionText
    
            regionCount = 1
            orgID = record["id"]
            for region in regionList:
                regionName = region.strip()
                if len(regionName) <= 2: continue
                record["region"] = regionName
                record["id"]     = orgID + "_" + str(regionCount)
                regionCount      = regionCount +1
                scraperwiki.sqlite.save(["id"], record)
        except: pass
    offset2 = offset2 + windowLength
    scraperwiki.sqlite.save_var("offset2", offset2)
scraperwiki.sqlite.save_var("offset2", 0)
