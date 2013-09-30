import scraperwiki, simplejson,urllib

import networkx as nx

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
    ykey=qsenv["YKEY"]
except:
    ockey=''


target='unilever'
rurl='http://opencorporates.com/reconcile/gb?query='+target
#note - the opencorporates api also offers a search:  companies/search
entities=simplejson.load(urllib.urlopen(rurl))


def getOCcompanyData(ocid):
    ocurl='http://api.opencorporates.com'+ocid+'/data'+'?api_token='+ockey
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    return ocdata

#need to find a way of playing nice with the api, and not keep retrawling

def getOCfilingData(ocid):
    ocurl='http://api.opencorporates.com'+ocid+'/filings'+'?per_page=100&api_token='+ockey
    print ocurl
    tmpdata=simplejson.load(urllib.urlopen(ocurl))
    ocdata=tmpdata['filings']
    print 'filings',ocid
    #print 'filings',ocid,ocdata
    #print 'filings 2',tmpdata
    while tmpdata['page']<tmpdata['total_pages']:
        page=str(tmpdata['page']+1)
        print '...another page',page,str(tmpdata["total_pages"]),str(tmpdata['page'])
        ocurl='http://api.opencorporates.com'+ocid+'/filings'+'?page='+page+'&per_page=100&api_token='+ockey
        tmpdata=simplejson.load(urllib.urlopen(ocurl))
        ocdata=ocdata+tmpdata['filings']
    return ocdata

def recordDirectorChange(ocname,ocid,ffiling,director):
    ddata={}
    ddata['ocname']=ocname
    ddata['ocid']=ocid
    ddata['fdesc']=ffiling["description"]
    ddata['fdirector']=director
    ddata['fdate']=ffiling["date"]
    ddata['fid']=ffiling["id"]
    ddata['ftyp']=ffiling["filing_type"]
    ddata['fcode']=ffiling["filing_code"]
    print 'ddata',ddata
    scraperwiki.sqlite.save(unique_keys=['fid'], table_name='directors_'+target, data=ddata)

#TO DO
#Here are some more director(?) name related dealings
#director filings [{'filing': {'uid': None, 'filing_code': 'BR1-PAR', 'title': 'Filing dated 2006-10-17', 'url': None, 'description': 'BR009041 PAR APPOINTED, CLARK, ALISTAIR EWAN, SERVICE ADDRESS, NEW TESCO HOUSE, DELAMARE ROAD, CHESHUNT, HERTFORDSHIRE EN8 9SL', 'date': '2006-10-17', 'opencorporates_url': 'http://opencorporates.com/filings/81409502', 'id': 81409502, 'filing_type': None}}


def logDirectors(ocname,ocid,filings):
    print 'director filings',filings
    for filing in filings:
        if filing["filing"]["filing_type"]=="Appointment of director" or filing["filing"]["filing_code"]=="AP01":
            desc=filing["filing"]["description"]
            director=desc.replace('DIRECTOR APPOINTED ','')
            recordDirectorChange(ocname,ocid,filing['filing'],director)
        elif filing["filing"]["filing_type"]=="Termination of appointment of director" or filing["filing"]["filing_code"]=="TM01":
            desc=filing["filing"]["description"]
            director=desc.replace('APPOINTMENT TERMINATED, DIRECTOR ','')
            director=director.replace('APPOINTMENT TERMINATED, ','')
            recordDirectorChange(ocname,ocid,filing['filing'],director)

def getOCcompanyDetails(ocid):
    ocurl='http://api.opencorporates.com'+ocid+'?api_token='+ockey
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    return ocdata

def logCompanyDetails(ocid,ocdata):
    cdata={'ocid':ocid}
    cdata['name']=ocdata['company']['name']
    cdata['address']=ocdata['company']['registered_address_in_full']
    print cdata,ocdata
    scraperwiki.sqlite.save(unique_keys=['ocid'], table_name='companydetails_'+target, data=cdata)

try:
    q = '* FROM "companydetails_'+target+'"'
    qdata = scraperwiki.sqlite.select(q)
    print qdata
except:
    qdata=[]

companies=[]
for c in qdata:
    companies.append(c['ocid'])

import time

from geopy import geocoders  
def addrgeocoder(qdata):
    q = '* FROM "geotable"'
    gdata = scraperwiki.sqlite.select(q)
    gcompanies=[]
    for gd in gdata:
        gcompanies.append(c['ocid'])
    print qdata
    for c in qdata:
        if c['ocid'] not in gcompanies:
            #g = geocoders.Google()
            time.sleep(2.0)
            g=geocoders.Yahoo(ykey) 
            place, (lat, lng) = g.geocode(c['address'])
            c['place']=place
            c['lat']=lat
            c['lng']=lng
            c['latlng']=','.join([str(lat),str(lng)])
            scraperwiki.sqlite.save(unique_keys=['ocid'], table_name='geotable', data=c)
try:
    addrgeocoder(qdata)
except:
    print 'geocoding oops'


try:
    q = '* FROM "directors_'+target+'"'
    qdata = scraperwiki.sqlite.select(q)
    print qdata
except:
    qdata=[]

directors=[]
for d in qdata:
    directors.append(d['ocid'])

#"result":[{"id":"/companies/gb/00445790","name":"TESCO PLC","type":[{"id":"/organization/organization","name":"Organization"}],"score":78.0,"match":false,"uri":"htt
def companyProcessor():
    for entity in entities['result']:
        ocid=entity['id']
        ocname=entity['name']
        if ocid not in directors:
            print 'getting directors', ocid
            filings=getOCfilingData(ocid)
            logDirectors(ocname,ocid,filings)
        if ocid not in companies:
            print 'getting company', ocid
            ocdata=getOCcompanyDetails(ocid)
            logCompanyDetails(ocid,ocdata)

companyProcessor()



#scraperwiki.sqlite.execute('drop table "companyaddress"')import scraperwiki, simplejson,urllib

import networkx as nx

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
    ykey=qsenv["YKEY"]
except:
    ockey=''


target='unilever'
rurl='http://opencorporates.com/reconcile/gb?query='+target
#note - the opencorporates api also offers a search:  companies/search
entities=simplejson.load(urllib.urlopen(rurl))


def getOCcompanyData(ocid):
    ocurl='http://api.opencorporates.com'+ocid+'/data'+'?api_token='+ockey
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    return ocdata

#need to find a way of playing nice with the api, and not keep retrawling

def getOCfilingData(ocid):
    ocurl='http://api.opencorporates.com'+ocid+'/filings'+'?per_page=100&api_token='+ockey
    print ocurl
    tmpdata=simplejson.load(urllib.urlopen(ocurl))
    ocdata=tmpdata['filings']
    print 'filings',ocid
    #print 'filings',ocid,ocdata
    #print 'filings 2',tmpdata
    while tmpdata['page']<tmpdata['total_pages']:
        page=str(tmpdata['page']+1)
        print '...another page',page,str(tmpdata["total_pages"]),str(tmpdata['page'])
        ocurl='http://api.opencorporates.com'+ocid+'/filings'+'?page='+page+'&per_page=100&api_token='+ockey
        tmpdata=simplejson.load(urllib.urlopen(ocurl))
        ocdata=ocdata+tmpdata['filings']
    return ocdata

def recordDirectorChange(ocname,ocid,ffiling,director):
    ddata={}
    ddata['ocname']=ocname
    ddata['ocid']=ocid
    ddata['fdesc']=ffiling["description"]
    ddata['fdirector']=director
    ddata['fdate']=ffiling["date"]
    ddata['fid']=ffiling["id"]
    ddata['ftyp']=ffiling["filing_type"]
    ddata['fcode']=ffiling["filing_code"]
    print 'ddata',ddata
    scraperwiki.sqlite.save(unique_keys=['fid'], table_name='directors_'+target, data=ddata)

#TO DO
#Here are some more director(?) name related dealings
#director filings [{'filing': {'uid': None, 'filing_code': 'BR1-PAR', 'title': 'Filing dated 2006-10-17', 'url': None, 'description': 'BR009041 PAR APPOINTED, CLARK, ALISTAIR EWAN, SERVICE ADDRESS, NEW TESCO HOUSE, DELAMARE ROAD, CHESHUNT, HERTFORDSHIRE EN8 9SL', 'date': '2006-10-17', 'opencorporates_url': 'http://opencorporates.com/filings/81409502', 'id': 81409502, 'filing_type': None}}


def logDirectors(ocname,ocid,filings):
    print 'director filings',filings
    for filing in filings:
        if filing["filing"]["filing_type"]=="Appointment of director" or filing["filing"]["filing_code"]=="AP01":
            desc=filing["filing"]["description"]
            director=desc.replace('DIRECTOR APPOINTED ','')
            recordDirectorChange(ocname,ocid,filing['filing'],director)
        elif filing["filing"]["filing_type"]=="Termination of appointment of director" or filing["filing"]["filing_code"]=="TM01":
            desc=filing["filing"]["description"]
            director=desc.replace('APPOINTMENT TERMINATED, DIRECTOR ','')
            director=director.replace('APPOINTMENT TERMINATED, ','')
            recordDirectorChange(ocname,ocid,filing['filing'],director)

def getOCcompanyDetails(ocid):
    ocurl='http://api.opencorporates.com'+ocid+'?api_token='+ockey
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    return ocdata

def logCompanyDetails(ocid,ocdata):
    cdata={'ocid':ocid}
    cdata['name']=ocdata['company']['name']
    cdata['address']=ocdata['company']['registered_address_in_full']
    print cdata,ocdata
    scraperwiki.sqlite.save(unique_keys=['ocid'], table_name='companydetails_'+target, data=cdata)

try:
    q = '* FROM "companydetails_'+target+'"'
    qdata = scraperwiki.sqlite.select(q)
    print qdata
except:
    qdata=[]

companies=[]
for c in qdata:
    companies.append(c['ocid'])

import time

from geopy import geocoders  
def addrgeocoder(qdata):
    q = '* FROM "geotable"'
    gdata = scraperwiki.sqlite.select(q)
    gcompanies=[]
    for gd in gdata:
        gcompanies.append(c['ocid'])
    print qdata
    for c in qdata:
        if c['ocid'] not in gcompanies:
            #g = geocoders.Google()
            time.sleep(2.0)
            g=geocoders.Yahoo(ykey) 
            place, (lat, lng) = g.geocode(c['address'])
            c['place']=place
            c['lat']=lat
            c['lng']=lng
            c['latlng']=','.join([str(lat),str(lng)])
            scraperwiki.sqlite.save(unique_keys=['ocid'], table_name='geotable', data=c)
try:
    addrgeocoder(qdata)
except:
    print 'geocoding oops'


try:
    q = '* FROM "directors_'+target+'"'
    qdata = scraperwiki.sqlite.select(q)
    print qdata
except:
    qdata=[]

directors=[]
for d in qdata:
    directors.append(d['ocid'])

#"result":[{"id":"/companies/gb/00445790","name":"TESCO PLC","type":[{"id":"/organization/organization","name":"Organization"}],"score":78.0,"match":false,"uri":"htt
def companyProcessor():
    for entity in entities['result']:
        ocid=entity['id']
        ocname=entity['name']
        if ocid not in directors:
            print 'getting directors', ocid
            filings=getOCfilingData(ocid)
            logDirectors(ocname,ocid,filings)
        if ocid not in companies:
            print 'getting company', ocid
            ocdata=getOCcompanyDetails(ocid)
            logCompanyDetails(ocid,ocdata)

companyProcessor()



#scraperwiki.sqlite.execute('drop table "companyaddress"')