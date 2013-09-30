#Scrape sit reports
#Reshape data from original format - dates are facet values, and as such row vals not column vals
#Dates are given in all manner of formats in the oroginal col headings; I've made a start on parsing them but there's still work to be done
#Need to build a table that contains scraped sheets so we don't scrape them again

#TO DO - I chose some really bad column names - to, from, table; need to change these really?

#import xlrd library - documentation at https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html
import xlrd

import md5

import time
from time import mktime
from datetime import datetime

import scraperwiki
import lxml.html

#UTILITY FUNCTION TO DROP TABLES
def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass


#---
#http://stackoverflow.com/a/1112664/454773
import datetime

def minimalist_xldate_as_datetime(xldate, datemode):
    # datemode: 0 for 1900-based, 1 for 1904-based
    return (
        datetime.datetime(1899, 12, 30)
        + datetime.timedelta(days=xldate + 1462 * datemode)
        )
#----

#Start of with a fudge - can we assume spreadsheets are templated, same each week?
def init():
    templateURL='https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Pub-file-WE-11-11-123.xls'
    xlbin = scraperwiki.scrape(templateURL)
    #use the open_workbook function on that new variable to create another, 'book'
    book = xlrd.open_workbook(file_contents=xlbin)
    #Create a table that acts as a table directory
    sheetnum=0
    for sheetname in book.sheet_names():
        sid='id_'+str(sheetnum)
        data={'id':sid,'name':sheetname}
        scraperwiki.sqlite.save(["id", "name"], data)
        sheetnum=sheetnum+1

#init()
#exit(-1)

def tablePatch(bd):
    bd2=[]
    for r in bd:
        if 'tid' not in r:
            r['tid']= tableLookup[r['tableName']]
            bd2.append(r.copy())
        elif r['tid']=='':
            r['tid']= tableLookup[r['tableName']]
            bd2.append(r.copy())
    return bd2

def maintenanceHack1():
    tables=scraperwiki.sqlite.select("* from swdata")
    fulltable=scraperwiki.sqlite.select("* from fulltable")
    bigdata=[]
    tid={}
    for t in tables:
        tid[t['name']]=t['id']
    for r in fulltable:
        if 'tid' not in r:
            r['tid']=tid[r['tableName']]
            bigdata.append(r.copy())
        elif r['tid']=='':
            r['tid']=tid[r['tableName']]
            bigdata.append(r.copy())
        if len(bigdata)>1000:
            scraperwiki.sqlite.save(unique_keys=['id'],table_name='fulltable', data=bigdata,verbose = 0)
            bigdata=[]
    scraperwiki.sqlite.save(unique_keys=['id'],table_name='fulltable', data=bigdata,verbose = 0)

#maintenanceHack1()

def init2():
    tables=scraperwiki.sqlite.select("* from swdata")
    for t in tables:
        dropper(t['id'])
    dropper('fulltable')
    #dropper('swdata')
    #exit(-1)

#init2()
#exit(-1)

try:
    tables=scraperwiki.sqlite.select("* from swdata")
except:
    tables=[]
print tables
tableLookup={}
for t in tables:
    tableLookup[t['name']]=t['id']

scrapedAlready=[]
try:
    scrapedtables=scraperwiki.sqlite.select("* from scraped")
    for t in scrapedtables:
        scrapedAlready.append(t['url'])
except: pass

def simplifiedKey(key):
    key=key.replace('/','.')
    #still got bad key? ???in Cancelled operations ???
    #replaced to and still broken:
    # 16 18.11.2012
    return key


dateLookup={}

def dateNormalise(d):
    #This is a bit of a hack - each time we find new date formats for the cols, we'll need to extend this
    #For pattern matching strings, see http://www.tutorialspoint.com/python/time_strptime.htm
    for trials in ["%d %b %y","%d %b%y",'%d-%b-%y','%d-%b-%Y','%d/%m/%Y','%d/%m/%y','%d %b %Y','%d-%m-%Y','%d/%m%Y']:
        try:
            d=d.strip()
            dtf =datetime.datetime.fromtimestamp(mktime(time.strptime(d, trials)))
            break
        except:
             dtf=d
    if type(dtf) is datetime.datetime:
        dtf=dtf.strftime("%Y-%m-%d")
    return dtf

def patchDate(f,t):
    tt=t.split('-')
    ff=f.split('-')
    f=int(ff[0])
    #how to cope with month rollover
    if int(tt[2])<int(f):
        #so we have a month change
        tt[1]=int(tt[1])-1
        #There may ne an issue at year rollover but we have to see how that is represented...
        if int(tt[1])==0:
            print 'weekend rollover at year end - how have they represented the dates?'
            tt[0]=int(tt[0])-1
            tt[1]=12
            #exit(-1)
    fromdate='-'.join( [ str(tt[0]),str(tt[1]),str(f) ])
    dtf=datetime.datetime.fromtimestamp(mktime(time.strptime(fromdate, "%Y-%m-%d")))
    if type(dtf) is datetime.datetime:
        fromdate=dtf.strftime("%Y-%m-%d")
    else:
        print dtf
        exit(-1)
    return fromdate

def dateRangeParse(daterange):

    #----
    #HORRIBLE HACK to cope with 02/122012
    #-->handle in the trials parse pattern
    #=daterange.replace('122012','12/2012')
    #----

    dd=daterange.split(' to ')

    if len(dd)<2:
        dd2=daterange.split(' - ')
        if len(dd2)<2:
            fromdate=daterange
            todate=daterange
        else:
            fromdate=dd2[0]
            todate=dd2[1]
    else:
        fromdate=dd[0]
        todate=dd[1]

    todate=dateNormalise(todate)
    #I think we'll require another fudge here, eg if date is given as '6 to 8 Nov 2012' we'll need to finesse '6' to '6 Nov 2012'
    fromdate=dateNormalise(fromdate)
    #if len(fromdate)<3:
    try:
        datetime.datetime.fromtimestamp(mktime(time.strptime(fromdate, "%Y-%m-%d")))
    except:
        fromdate=patchDate(fromdate,todate)
    return (fromdate,todate)

def scrapesheets3(XLS):
    xlbin = scraperwiki.scrape(XLS)
    book = xlrd.open_workbook(file_contents=xlbin)

    print book.sheet_names()

    for sheetname in book.sheet_names():
        bigdata=[]
        if sheetname in tableLookup:
            tt=tableLookup[sheetname]
            #If we want to clear the tables...
            #dropper(tt)
        else:
            l=len(tableLookup)
            sid='id_'+str(l)
            tableLookup[sheetname]=sid
            scraperwiki.sqlite.save(["id", "name"], {'id':sid,'name':sheetname} )
            tt=tableLookup[sheetname]
            #exit(-1) #crash out for now...
        print 'Tablename:',tt
        sheet = book.sheet_by_name(sheetname)
        sheetwidth=len(sheet.row_values(17))
        print sheetname,sheetwidth,sheet.nrows

        keys={}
        facetAkeys={}
        tokeys={}
        fromkeys={}
        facetBkeys={}
        for col in range(1,4):
            keys[col]=sheet.row_values(14)[col]

        lastfacetAkey=-1

        if sheet.row_values(13)[5]!='' or sheet.row_values(13)[4]!='':
            for col in range (4,sheetwidth):
                if sheet.row_values(13)[col]!='':
                    try:
                        facetAkeys[col]=minimalist_xldate_as_datetime(sheet.row_values(13)[col],book.datemode).date().strftime("%Y-%m-%d")
                    except:
                        facetAkeys[col]=sheet.row_values(13)[col]
                    lastfacetAkey=facetAkeys[col]
                else:
                    facetAkeys[col]=lastfacetAkey
                if facetAkeys[col] not in dateLookup:
                    (fromkeys[col],tokeys[col])=dateRangeParse(facetAkeys[col])
                    dateLookup[facetAkeys[col]]=(fromkeys[col],tokeys[col])
                else:
                    (fromkeys[col],tokeys[col])=dateLookup[facetAkeys[col]]
                facetBkeys[col]=sheet.row_values(14)[col]
        else:
            for col in range (4,sheetwidth):
                try:
                    facetAkeys[col]=minimalist_xldate_as_datetime(sheet.row_values(14)[col],book.datemode).date().strftime("%Y-%m-%d")
                    #It may make more sense to save this as a proper date - in which case just drop the strftime bit
                    #facetAkeys[col]=minimalist_xldate_as_datetime(sheet.row_values(14)[col],book.datemode).date()
                    #As query in https://scraperwiki.com/views/ou_bbc_co-pro_on_iplayer_-_bootstrap/ shows, we can do time based SQLite queries?
                    #TO DO? Some of the facetAkeys are date ranges, so maybe bettwe to split as facetAkeysFrom and facetAkeysTo?
                    ##If it's not a range, set from and to as the same.
                except:
                    facetAkeys[col]=sheet.row_values(14)[col]
                if facetAkeys[col] not in dateLookup:
                    (fromkeys[col],tokeys[col])=dateRangeParse(facetAkeys[col])
                    dateLookup[facetAkeys[col]]=(fromkeys[col],tokeys[col])
                else:
                    (fromkeys[col],tokeys[col])=dateLookup[facetAkeys[col]]
                facetBkeys[col]=''
        #print fromkeys
        

        for row in range(17, sheet.nrows):
            data={}
            #hack fudge error trap
            if sheet.row_values(row)[2]=='':continue
            for col in range(1,4):
                #these are typically ['SHA','Code','Name',]
                data[keys[col]]=sheet.row_values(row)[col]
            for col in range (4,sheetwidth):
                #TO DO - change colhead to tableName
                #data['table']=sheetname
                data['tableName']=sheetname
                data['facetA']=facetAkeys[col]
                #TO DO - change colhead to fromDateStr
                #data['from']=fromkeys[col]
                data['fromDateStr']=fromkeys[col]
                #TO DO - change colhead to toDateStr
                #data['to']=tokeys[col]
                data['toDateStr']=tokeys[col]
                data['facetB']=facetBkeys[col]
                data["value"]=sheet.row_values(row)[col]
                data['id']=md5.new(''.join([ data['tableName'],data['Code'],data['fromDateStr'],data['facetB'] ])).hexdigest()
                #scraperwiki.sqlite.save(unique_keys=['id'],table_name=tt, data=data)
                #If we get properly unique keys - uniqid - eg as in hash idea above but also adding tt into hash mix, we can do a fulltable?
                #scraperwiki.sqlite.save(unique_keys=['id'],table_name='fulltable', data=data,verbose = 0)
                
                #If data variable persists, the pass by reference append of the data dict breaks bigdata; so force append by value instead 
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=['id'],table_name=tt, data=bigdata,verbose = 0)
                    #scraperwiki.sqlite.save(unique_keys=['id'],table_name='fulltable', data=tablePatch(bigdata),verbose = 0)
                    bigdata=[]
        #Tidy up by saving any data that's left outstanding
        scraperwiki.sqlite.save(unique_keys=['id'],table_name=tt, data=bigdata,verbose = 0)
        #scraperwiki.sqlite.save(unique_keys=['id'],table_name='fulltable', data=tablePatch(bigdata),verbose = 0)
        bigdata=[]
    scraperwiki.sqlite.save(unique_keys=['url'],table_name='scraped', data={'url':XLS})

#TESTING
#scrapesheets2('https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Web-file-WE-18-11-12.xls')
#scrapesheets3('https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Web-file-WE-18-11-12.xls')



#From a scraper by paulbradshaw

#define our URL - this links to all the spreadsheets
#URL = 'http://transparency.dh.gov.uk/2012/10/26/winter-pressures-daily-situation-reports-2012-13/'
URL='http://www.dh.gov.uk/en/Publicationsandstatistics/Statistics/Performancedataandstatistics/DailySituationReports/index.htm'

#HTML to grab is:
#<p><strong>November 2012</strong><br />
#<a href="https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Web-file-WE-18-11-12.xls">DailySR &#8211; week ending 18 Nov 12.xls (492KB).</a><br />
#<a href="https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Pub-file-WE-11-11-123.xls">DailySR &#8211; 6 Nov 12 to 11 Nov 12.xls (446KB)</a>.</p>

#HTML to avoid that generates an error is:
#<p>Data for this collection is available back to November 2010.<br />
#For previous years’ data <a #href="http://www.dh.gov.uk/en/Publicationsandstatistics/Statistics/Performancedataandstatistics/DailySituationReports/index.htm">click here</a>.</p>

#Create a new function which takes one parameter and names it 'URL'
def grabexcellinks(URL):
    #Use Scraperwiki's scrape function on 'URL', put results in new variable 'html'
    html = scraperwiki.scrape(URL)
    #and show it us
    print html
    #Use lxml.html's fromstring function on 'html', put results in new variable 'root'
    root = lxml.html.fromstring(html)
    #use cssselect method on 'root' to grab all <a> tags within a <p> tag - and put in a new list variable 'links'
    links = root.cssselect('p a')
    #for each item in that list variable, from the first to the second last [0:-1], put it in the variable 'link'
    '''
    for link in links[0:-1]:
        #and print the text_content of that (after the string "link text:")
        print "link text:", link.text_content()
        #use the attrib.get method on 'link' to grab the href= attribute of the HTML, and put in new 'linkurl' variable
        linkurl = link.attrib.get('href')
        #print it
        print linkurl
        #run the function scrapesheets, using that variable as the parameter
        scrapesheets(linkurl)
    '''
    urls=[]
    for link in links[0:-1]: urls.append(link.attrib.get('href'))
    return urls

#grabexcellinks(URL)
#--

#urls= grabexcellinks(URL)
#I'm starting to think - is the first sheet all the data to date?
#In which case, we probably need to avoid scraping this one if we're doing weekly updates
urls=[]
for url in urls[1:]:
    if url not in scrapedAlready:
        print url
        scrapesheets3(url)
    else: print "Ignoring",url

scrapesheets3('http://www.dh.gov.uk/prod_consum_dh/groups/dh_digitalassets/@dh/@en/@ps/@sta/@perf/documents/digitalasset/dh_132988.xls')
#Scrape sit reports
#Reshape data from original format - dates are facet values, and as such row vals not column vals
#Dates are given in all manner of formats in the oroginal col headings; I've made a start on parsing them but there's still work to be done
#Need to build a table that contains scraped sheets so we don't scrape them again

#TO DO - I chose some really bad column names - to, from, table; need to change these really?

#import xlrd library - documentation at https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html
import xlrd

import md5

import time
from time import mktime
from datetime import datetime

import scraperwiki
import lxml.html

#UTILITY FUNCTION TO DROP TABLES
def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass


#---
#http://stackoverflow.com/a/1112664/454773
import datetime

def minimalist_xldate_as_datetime(xldate, datemode):
    # datemode: 0 for 1900-based, 1 for 1904-based
    return (
        datetime.datetime(1899, 12, 30)
        + datetime.timedelta(days=xldate + 1462 * datemode)
        )
#----

#Start of with a fudge - can we assume spreadsheets are templated, same each week?
def init():
    templateURL='https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Pub-file-WE-11-11-123.xls'
    xlbin = scraperwiki.scrape(templateURL)
    #use the open_workbook function on that new variable to create another, 'book'
    book = xlrd.open_workbook(file_contents=xlbin)
    #Create a table that acts as a table directory
    sheetnum=0
    for sheetname in book.sheet_names():
        sid='id_'+str(sheetnum)
        data={'id':sid,'name':sheetname}
        scraperwiki.sqlite.save(["id", "name"], data)
        sheetnum=sheetnum+1

#init()
#exit(-1)

def tablePatch(bd):
    bd2=[]
    for r in bd:
        if 'tid' not in r:
            r['tid']= tableLookup[r['tableName']]
            bd2.append(r.copy())
        elif r['tid']=='':
            r['tid']= tableLookup[r['tableName']]
            bd2.append(r.copy())
    return bd2

def maintenanceHack1():
    tables=scraperwiki.sqlite.select("* from swdata")
    fulltable=scraperwiki.sqlite.select("* from fulltable")
    bigdata=[]
    tid={}
    for t in tables:
        tid[t['name']]=t['id']
    for r in fulltable:
        if 'tid' not in r:
            r['tid']=tid[r['tableName']]
            bigdata.append(r.copy())
        elif r['tid']=='':
            r['tid']=tid[r['tableName']]
            bigdata.append(r.copy())
        if len(bigdata)>1000:
            scraperwiki.sqlite.save(unique_keys=['id'],table_name='fulltable', data=bigdata,verbose = 0)
            bigdata=[]
    scraperwiki.sqlite.save(unique_keys=['id'],table_name='fulltable', data=bigdata,verbose = 0)

#maintenanceHack1()

def init2():
    tables=scraperwiki.sqlite.select("* from swdata")
    for t in tables:
        dropper(t['id'])
    dropper('fulltable')
    #dropper('swdata')
    #exit(-1)

#init2()
#exit(-1)

try:
    tables=scraperwiki.sqlite.select("* from swdata")
except:
    tables=[]
print tables
tableLookup={}
for t in tables:
    tableLookup[t['name']]=t['id']

scrapedAlready=[]
try:
    scrapedtables=scraperwiki.sqlite.select("* from scraped")
    for t in scrapedtables:
        scrapedAlready.append(t['url'])
except: pass

def simplifiedKey(key):
    key=key.replace('/','.')
    #still got bad key? ???in Cancelled operations ???
    #replaced to and still broken:
    # 16 18.11.2012
    return key


dateLookup={}

def dateNormalise(d):
    #This is a bit of a hack - each time we find new date formats for the cols, we'll need to extend this
    #For pattern matching strings, see http://www.tutorialspoint.com/python/time_strptime.htm
    for trials in ["%d %b %y","%d %b%y",'%d-%b-%y','%d-%b-%Y','%d/%m/%Y','%d/%m/%y','%d %b %Y','%d-%m-%Y','%d/%m%Y']:
        try:
            d=d.strip()
            dtf =datetime.datetime.fromtimestamp(mktime(time.strptime(d, trials)))
            break
        except:
             dtf=d
    if type(dtf) is datetime.datetime:
        dtf=dtf.strftime("%Y-%m-%d")
    return dtf

def patchDate(f,t):
    tt=t.split('-')
    ff=f.split('-')
    f=int(ff[0])
    #how to cope with month rollover
    if int(tt[2])<int(f):
        #so we have a month change
        tt[1]=int(tt[1])-1
        #There may ne an issue at year rollover but we have to see how that is represented...
        if int(tt[1])==0:
            print 'weekend rollover at year end - how have they represented the dates?'
            tt[0]=int(tt[0])-1
            tt[1]=12
            #exit(-1)
    fromdate='-'.join( [ str(tt[0]),str(tt[1]),str(f) ])
    dtf=datetime.datetime.fromtimestamp(mktime(time.strptime(fromdate, "%Y-%m-%d")))
    if type(dtf) is datetime.datetime:
        fromdate=dtf.strftime("%Y-%m-%d")
    else:
        print dtf
        exit(-1)
    return fromdate

def dateRangeParse(daterange):

    #----
    #HORRIBLE HACK to cope with 02/122012
    #-->handle in the trials parse pattern
    #=daterange.replace('122012','12/2012')
    #----

    dd=daterange.split(' to ')

    if len(dd)<2:
        dd2=daterange.split(' - ')
        if len(dd2)<2:
            fromdate=daterange
            todate=daterange
        else:
            fromdate=dd2[0]
            todate=dd2[1]
    else:
        fromdate=dd[0]
        todate=dd[1]

    todate=dateNormalise(todate)
    #I think we'll require another fudge here, eg if date is given as '6 to 8 Nov 2012' we'll need to finesse '6' to '6 Nov 2012'
    fromdate=dateNormalise(fromdate)
    #if len(fromdate)<3:
    try:
        datetime.datetime.fromtimestamp(mktime(time.strptime(fromdate, "%Y-%m-%d")))
    except:
        fromdate=patchDate(fromdate,todate)
    return (fromdate,todate)

def scrapesheets3(XLS):
    xlbin = scraperwiki.scrape(XLS)
    book = xlrd.open_workbook(file_contents=xlbin)

    print book.sheet_names()

    for sheetname in book.sheet_names():
        bigdata=[]
        if sheetname in tableLookup:
            tt=tableLookup[sheetname]
            #If we want to clear the tables...
            #dropper(tt)
        else:
            l=len(tableLookup)
            sid='id_'+str(l)
            tableLookup[sheetname]=sid
            scraperwiki.sqlite.save(["id", "name"], {'id':sid,'name':sheetname} )
            tt=tableLookup[sheetname]
            #exit(-1) #crash out for now...
        print 'Tablename:',tt
        sheet = book.sheet_by_name(sheetname)
        sheetwidth=len(sheet.row_values(17))
        print sheetname,sheetwidth,sheet.nrows

        keys={}
        facetAkeys={}
        tokeys={}
        fromkeys={}
        facetBkeys={}
        for col in range(1,4):
            keys[col]=sheet.row_values(14)[col]

        lastfacetAkey=-1

        if sheet.row_values(13)[5]!='' or sheet.row_values(13)[4]!='':
            for col in range (4,sheetwidth):
                if sheet.row_values(13)[col]!='':
                    try:
                        facetAkeys[col]=minimalist_xldate_as_datetime(sheet.row_values(13)[col],book.datemode).date().strftime("%Y-%m-%d")
                    except:
                        facetAkeys[col]=sheet.row_values(13)[col]
                    lastfacetAkey=facetAkeys[col]
                else:
                    facetAkeys[col]=lastfacetAkey
                if facetAkeys[col] not in dateLookup:
                    (fromkeys[col],tokeys[col])=dateRangeParse(facetAkeys[col])
                    dateLookup[facetAkeys[col]]=(fromkeys[col],tokeys[col])
                else:
                    (fromkeys[col],tokeys[col])=dateLookup[facetAkeys[col]]
                facetBkeys[col]=sheet.row_values(14)[col]
        else:
            for col in range (4,sheetwidth):
                try:
                    facetAkeys[col]=minimalist_xldate_as_datetime(sheet.row_values(14)[col],book.datemode).date().strftime("%Y-%m-%d")
                    #It may make more sense to save this as a proper date - in which case just drop the strftime bit
                    #facetAkeys[col]=minimalist_xldate_as_datetime(sheet.row_values(14)[col],book.datemode).date()
                    #As query in https://scraperwiki.com/views/ou_bbc_co-pro_on_iplayer_-_bootstrap/ shows, we can do time based SQLite queries?
                    #TO DO? Some of the facetAkeys are date ranges, so maybe bettwe to split as facetAkeysFrom and facetAkeysTo?
                    ##If it's not a range, set from and to as the same.
                except:
                    facetAkeys[col]=sheet.row_values(14)[col]
                if facetAkeys[col] not in dateLookup:
                    (fromkeys[col],tokeys[col])=dateRangeParse(facetAkeys[col])
                    dateLookup[facetAkeys[col]]=(fromkeys[col],tokeys[col])
                else:
                    (fromkeys[col],tokeys[col])=dateLookup[facetAkeys[col]]
                facetBkeys[col]=''
        #print fromkeys
        

        for row in range(17, sheet.nrows):
            data={}
            #hack fudge error trap
            if sheet.row_values(row)[2]=='':continue
            for col in range(1,4):
                #these are typically ['SHA','Code','Name',]
                data[keys[col]]=sheet.row_values(row)[col]
            for col in range (4,sheetwidth):
                #TO DO - change colhead to tableName
                #data['table']=sheetname
                data['tableName']=sheetname
                data['facetA']=facetAkeys[col]
                #TO DO - change colhead to fromDateStr
                #data['from']=fromkeys[col]
                data['fromDateStr']=fromkeys[col]
                #TO DO - change colhead to toDateStr
                #data['to']=tokeys[col]
                data['toDateStr']=tokeys[col]
                data['facetB']=facetBkeys[col]
                data["value"]=sheet.row_values(row)[col]
                data['id']=md5.new(''.join([ data['tableName'],data['Code'],data['fromDateStr'],data['facetB'] ])).hexdigest()
                #scraperwiki.sqlite.save(unique_keys=['id'],table_name=tt, data=data)
                #If we get properly unique keys - uniqid - eg as in hash idea above but also adding tt into hash mix, we can do a fulltable?
                #scraperwiki.sqlite.save(unique_keys=['id'],table_name='fulltable', data=data,verbose = 0)
                
                #If data variable persists, the pass by reference append of the data dict breaks bigdata; so force append by value instead 
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=['id'],table_name=tt, data=bigdata,verbose = 0)
                    #scraperwiki.sqlite.save(unique_keys=['id'],table_name='fulltable', data=tablePatch(bigdata),verbose = 0)
                    bigdata=[]
        #Tidy up by saving any data that's left outstanding
        scraperwiki.sqlite.save(unique_keys=['id'],table_name=tt, data=bigdata,verbose = 0)
        #scraperwiki.sqlite.save(unique_keys=['id'],table_name='fulltable', data=tablePatch(bigdata),verbose = 0)
        bigdata=[]
    scraperwiki.sqlite.save(unique_keys=['url'],table_name='scraped', data={'url':XLS})

#TESTING
#scrapesheets2('https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Web-file-WE-18-11-12.xls')
#scrapesheets3('https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Web-file-WE-18-11-12.xls')



#From a scraper by paulbradshaw

#define our URL - this links to all the spreadsheets
#URL = 'http://transparency.dh.gov.uk/2012/10/26/winter-pressures-daily-situation-reports-2012-13/'
URL='http://www.dh.gov.uk/en/Publicationsandstatistics/Statistics/Performancedataandstatistics/DailySituationReports/index.htm'

#HTML to grab is:
#<p><strong>November 2012</strong><br />
#<a href="https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Web-file-WE-18-11-12.xls">DailySR &#8211; week ending 18 Nov 12.xls (492KB).</a><br />
#<a href="https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Pub-file-WE-11-11-123.xls">DailySR &#8211; 6 Nov 12 to 11 Nov 12.xls (446KB)</a>.</p>

#HTML to avoid that generates an error is:
#<p>Data for this collection is available back to November 2010.<br />
#For previous years’ data <a #href="http://www.dh.gov.uk/en/Publicationsandstatistics/Statistics/Performancedataandstatistics/DailySituationReports/index.htm">click here</a>.</p>

#Create a new function which takes one parameter and names it 'URL'
def grabexcellinks(URL):
    #Use Scraperwiki's scrape function on 'URL', put results in new variable 'html'
    html = scraperwiki.scrape(URL)
    #and show it us
    print html
    #Use lxml.html's fromstring function on 'html', put results in new variable 'root'
    root = lxml.html.fromstring(html)
    #use cssselect method on 'root' to grab all <a> tags within a <p> tag - and put in a new list variable 'links'
    links = root.cssselect('p a')
    #for each item in that list variable, from the first to the second last [0:-1], put it in the variable 'link'
    '''
    for link in links[0:-1]:
        #and print the text_content of that (after the string "link text:")
        print "link text:", link.text_content()
        #use the attrib.get method on 'link' to grab the href= attribute of the HTML, and put in new 'linkurl' variable
        linkurl = link.attrib.get('href')
        #print it
        print linkurl
        #run the function scrapesheets, using that variable as the parameter
        scrapesheets(linkurl)
    '''
    urls=[]
    for link in links[0:-1]: urls.append(link.attrib.get('href'))
    return urls

#grabexcellinks(URL)
#--

#urls= grabexcellinks(URL)
#I'm starting to think - is the first sheet all the data to date?
#In which case, we probably need to avoid scraping this one if we're doing weekly updates
urls=[]
for url in urls[1:]:
    if url not in scrapedAlready:
        print url
        scrapesheets3(url)
    else: print "Ignoring",url

scrapesheets3('http://www.dh.gov.uk/prod_consum_dh/groups/dh_digitalassets/@dh/@en/@ps/@sta/@perf/documents/digitalasset/dh_132988.xls')
