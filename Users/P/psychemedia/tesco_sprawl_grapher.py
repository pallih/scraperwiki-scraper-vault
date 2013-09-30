import scraperwiki, simplejson,urllib,re

import networkx as nx

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
    ykey=qsenv["YKEY"]
except:
    ockey=''


target='care uk'
tabletarget=target#''

if target=='' or tabletarget=='': exit(-1)

ttarget=tabletarget.replace(' ','')
rurl='http://opencorporates.com/reconcile/gb?query='+urllib.quote(target)
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
    tmpdata=simplejson.load(urllib.urlopen(ocurl))['results'] #missing out on paged data
    ocdata=tmpdata['filings']
    print 'filings',ocid
    #print 'filings',ocid,ocdata
    #print 'filings 2',tmpdata
    while tmpdata['page']<tmpdata['total_pages']:
        page=str(tmpdata['page']+1)
        print '...another page',page,str(tmpdata["total_pages"]),str(tmpdata['page'])
        ocurl='http://api.opencorporates.com'+ocid+'/filings'+'?page='+page+'&per_page=100&api_token='+ockey
        tmpdata=simplejson.load(urllib.urlopen(ocurl))['results']
        ocdata=ocdata+tmpdata['filings']
    return ocdata

def recordDirectorChange(ocname,ocid,ffiling,director,addr=''):
    ddata={}
    ddata['ocname']=ocname
    ddata['ocid']=ocid
    ddata['fdesc']=ffiling["description"]
    ddata['fdirector']=director
    ddata['fdate']=ffiling["date"]
    ddata['fid']=ffiling["id"]
    ddata['ftyp']=ffiling["filing_type"]
    ddata['fcode']=ffiling["filing_code"]
    ddata['addr']=addr
    print 'ddata',ddata
    scraperwiki.sqlite.save(unique_keys=['fid'], table_name='directors_'+ttarget, data=ddata)

#TO DO
#Here are some more director(?) name related dealings

#IN TESTING- NEED TO CHANGE TO REGEXP director filings [{'filing': {'uid': None, 'filing_code': 'BR1-PAR', 'title': 'Filing dated 2006-10-17', 'url': None, 'description': 'BR009041 PAR APPOINTED, CLARK, ALISTAIR EWAN, SERVICE ADDRESS, NEW TESCO HOUSE, DELAMARE ROAD, CHESHUNT, HERTFORDSHIRE EN8 9SL', 'date': '2006-10-17', 'opencorporates_url': 'http://opencorporates.com/filings/81409502', 'id': 81409502, 'filing_type': None}}

#{'filing': {'uid': '1d3b59eJxjZRd2Eme0dBLnMDIwMDc0MDJzYnUS5zcwMHAMNPd1CQkJNjY2M3cSZ3YKMmlSc87PLUjMy0wt9sgvLU61sorw9XEPt7LyzE1MT4VS3qmVRCpjZWBgYARiJiBmBmIWIGYFAH0eJA0=', 'filing_code': 'BR4', 'title': 'Return by an oversea company subject to branch registration of change of directors or secretary or of their particulars', 'url': None, 'description': 'DIR APPOINTED        17/09/07, TEO, MICHAEL CHEE HONG, SERVICE ADDRESS, 1 CHURCHILL PLACE, LONDON E14 5HP', 'date': '2007-10-26', 'opencorporates_url': 'http://opencorporates.com/filings/59420474', 'id': 59420474, 'filing_type': 'Return by an oversea company subject to branch registration of change of directors or secretary or of their particulars'}}

#{'filing': {'uid': '004756eJxjZRd2YnXi4ohPyU9OSS1OBnHYQJzMFCdxfgMDgwALfwtnZ6dgYwsjIycuzvi0/KLcksqCVCdxZqcgMycu1viU5MQSJ3FGS5gpiSVASQ4jAwNLAwtDwyY15/zcgsS8zNRij/zS4lQrqwhfH/dwKyvP3MT0VCjlnVpJpDJuBgYGRiBmAmJmIGYBYlYgZgNidiDmAGJOIOYCYm4AzKo0nA==', 'filing_code': 'BR6', 'title': 'Return of change of person authorised to accept service or to represent the branch of an oversea company or any change in their particulars', 'url': None, 'description': 'TRANSACTION BR6- BR008167 PERSON AUTHORISED TO REPRESENT TERMINATED 10/07/2009 ADAM NICHOLAS JANISCH', 'date': '2009-08-11', 'opencorporates_url': 'http://opencorporates.com/filings/79898379', 'id': 79898379, 'filing_type': 'Return of change of person authorised to accept service or to represent the branch of an oversea company or any change in their particulars'}},

#{'filing': {'uid': '60eb0beJxjZRd2YnXi4ohPyU9OSS1OBnHYQJzMFCdxfgMDA5cwwyhXX58QEyMTSycuzvi0/KLcksqCVCdxNv9gxwADUycu1viU5MQSJ3FGS5hBiSVAeQ4jA0MDAwtDsyY15/zcgsS8zNRij/zS4lQrqwhfH/dwKyvP3MT0VCjlnVpJpDJuBgYGRiBmAmJmIGYBYlYgZgNidiDmAGJOIOYCYm4AolI1mw==', 'filing_code': 'OSAP05', 'title': 'Appointment by an overseas company of a person authorised to represent the company as a permanent representative in respect of a UK establishment', 'url': None, 'description': 'TRANSACTION OSAP05- BR008167 PERSON AUTHORISED TO REPRESENT APPOINTED 17/06/2010 PRIYAN SHAH  -- ADDRESS: 1 CHURCHILL PLACE, LONDON, E14 5HP', 'date': '2010-08-16', 'opencorporates_url': 'http://opencorporates.com/filings/79898371', 'id': 79898371, 'filing_type': 'Appointment by an overseas company of a person authorised to represent the company as a permanent representative in respect of a UK establishment'}}

#{'filing': {'uid': 'ff30d3eJxjZRd2YnXi4ohPyU9OSS1OBnHYQJzMFCdxfgMDA8fwQG8nf2NPEyNLYycuzvi0/KLcksqCVCdxNv/gEF8DoCBrfEpyYomTOKMlzKDEEqA8h5GBIQiaNqk55+cWJOZlphZ75JcWp1pZRfj6uIdbWXnmJqanQinv1EoilXEzMDAwAjETEDMDMQsQswIxGxCzAzEHEHMCMRcQcwMAlvo1ig==', 'filing_code': 'OSTM03', 'title': 'Termination of appointment by an overseas company of a person authorised to accept service of documents or person authorised to represent the company in respect of a UK establishment', 'url': None, 'description': 'TRANSACTION OSTM03- BR008167 PERSON AUTHORISED TO REPRESENT TERMINATED 17/05/2010 ELKE EDIS', 'date': '2010-10-15', 'opencorporates_url': 'http://opencorporates.com/filings/79898369', 'id': 79898369, 'filing_type': 'Termination of appointment by an overseas company of a person authorised to accept service of documents or person authorised to represent the company in respect of a UK establishment'}}

def logDirectors(ocname,ocid,filings,logger=True):
    #br1-par untested
    print 'director filings',filings
    for filing in filings:
        if filing["filing"]["filing_type"]=="Appointment of director" or filing["filing"]["filing_code"]=="AP01":
            desc=filing["filing"]["description"]
            director=desc.replace('DIRECTOR APPOINTED ','')
            if logger: recordDirectorChange(ocname,ocid,filing['filing'],director)
            else: print "AP01",ocid,filing['filing'],director
        elif filing["filing"]["filing_type"]=="Termination of appointment of director" or filing["filing"]["filing_code"]=="TM01":
            desc=filing["filing"]["description"]
            director=desc.replace('APPOINTMENT TERMINATED, DIRECTOR ','')
            director=director.replace('APPOINTMENT TERMINATED, ','')
            if logger: recordDirectorChange(ocname,ocid,filing['filing'],director)
            else: print "TM01",ocid,filing['filing'],director
        elif filing["filing"]["filing_code"]=="BR1-PAR":
            desc=filing["filing"]["description"]
            r=re.match(r".* APPOINTED, ([^,]*, [^,]*), SERVICE ADDRESS, (.*)$",desc)
            if r!=None and logger:
                recordDirectorChange(ocname,ocid,filing['filing'],r.group(1),r.group(2))
        elif filing["filing"]["filing_code"]=="BR4":
            desc=filing["filing"]["description"]
            r=re.match(r".* APPOINTED[^,]*, ([^,]*, [^,]*), SERVICE ADDRESS, (.*)$",desc)
            if r!=None and logger:
                recordDirectorChange(ocname,ocid,filing['filing'],r.group(1),r.group(2))
        elif filing["filing"]["filing_code"]=="BR6":
            desc=filing["filing"]["description"]
            r=re.match(r".* TERMINATED [^\s]*\s(.*)$",desc)
            if r!=None and logger:
                recordDirectorChange(ocname,ocid,filing['filing'],r.group(1))
        elif filing["filing"]["filing_code"]=="OSAP05":
            desc=filing["filing"]["description"]
            r=re.match(r".*TED [^\s]*\s(.*)\s-.*ADDRESS: (.*)$",desc)
            if r!=None and logger:
                recordDirectorChange(ocname,ocid,filing['filing'],r.group(1),r.group(2))
        elif filing["filing"]["filing_code"]=="OSTM03":
            desc=filing["filing"]["description"]
            r=re.match(r".*TED [^\s]*\s(.*)$",desc)
            if r!=None and logger:
                recordDirectorChange(ocname,ocid,filing['filing'],r.group(1))


def getOCcompanyDetails(ocid):
    ocurl='http://api.opencorporates.com'+ocid+'?api_token='+ockey
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    return ocdata['results']

def logCompanyDetails(ocid,ocdata):
    if 'error' in ocdata: return
    print ocdata,
    cdata={'ocid':ocid}
    cdata['name']=ocdata['company']['name']
    cdata['address']=ocdata['company']['registered_address_in_full']
    print cdata
    scraperwiki.sqlite.save(unique_keys=['ocid'], table_name='companydetails_'+ttarget, data=cdata)

try:
    q = '* FROM "companydetails_'+ttarget+'"'
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
    q = '* FROM "directors_'+ttarget+'"'
    qdata = scraperwiki.sqlite.select(q)
    print qdata
except:
    qdata=[]

directors=[]
for d in qdata:
    directors.append(d['ocid'])

#"result":[{"id":"/companies/gb/00445790","name":"TESCO PLC","type":[{"id":"/organization/organization","name":"Organization"}],"score":78.0,"match":false,"uri":"htt
def companyProcessor():
    ccount=len(entities['result'])
    cci = 1
    for entity in entities['result']:
        ocid=entity['id']
        ocname=entity['name']
        print 'processing',ocid, cci,'of',ccount
        if ocid not in companies:
            time.sleep(1.0)
            print 'getting company', ocid
            ocdata=getOCcompanyDetails(ocid)
            logCompanyDetails(ocid,ocdata)
            if ocid not in directors:
                print 'getting directors', ocid
                filings=getOCfilingData(ocid)
                logDirectors(ocname,ocid,filings)
        else: print 'got it already'
        cci=cci+1



def testfiling(ocid):
    filings=getOCfilingData(ocid)
    logDirectors('',ocid,filings,False)

#testfiling('/companies/gb/FC026875')

companyProcessor()

#scraperwiki.sqlite.execute('drop table "companyaddress"')import scraperwiki, simplejson,urllib,re

import networkx as nx

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
    ykey=qsenv["YKEY"]
except:
    ockey=''


target='care uk'
tabletarget=target#''

if target=='' or tabletarget=='': exit(-1)

ttarget=tabletarget.replace(' ','')
rurl='http://opencorporates.com/reconcile/gb?query='+urllib.quote(target)
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
    tmpdata=simplejson.load(urllib.urlopen(ocurl))['results'] #missing out on paged data
    ocdata=tmpdata['filings']
    print 'filings',ocid
    #print 'filings',ocid,ocdata
    #print 'filings 2',tmpdata
    while tmpdata['page']<tmpdata['total_pages']:
        page=str(tmpdata['page']+1)
        print '...another page',page,str(tmpdata["total_pages"]),str(tmpdata['page'])
        ocurl='http://api.opencorporates.com'+ocid+'/filings'+'?page='+page+'&per_page=100&api_token='+ockey
        tmpdata=simplejson.load(urllib.urlopen(ocurl))['results']
        ocdata=ocdata+tmpdata['filings']
    return ocdata

def recordDirectorChange(ocname,ocid,ffiling,director,addr=''):
    ddata={}
    ddata['ocname']=ocname
    ddata['ocid']=ocid
    ddata['fdesc']=ffiling["description"]
    ddata['fdirector']=director
    ddata['fdate']=ffiling["date"]
    ddata['fid']=ffiling["id"]
    ddata['ftyp']=ffiling["filing_type"]
    ddata['fcode']=ffiling["filing_code"]
    ddata['addr']=addr
    print 'ddata',ddata
    scraperwiki.sqlite.save(unique_keys=['fid'], table_name='directors_'+ttarget, data=ddata)

#TO DO
#Here are some more director(?) name related dealings

#IN TESTING- NEED TO CHANGE TO REGEXP director filings [{'filing': {'uid': None, 'filing_code': 'BR1-PAR', 'title': 'Filing dated 2006-10-17', 'url': None, 'description': 'BR009041 PAR APPOINTED, CLARK, ALISTAIR EWAN, SERVICE ADDRESS, NEW TESCO HOUSE, DELAMARE ROAD, CHESHUNT, HERTFORDSHIRE EN8 9SL', 'date': '2006-10-17', 'opencorporates_url': 'http://opencorporates.com/filings/81409502', 'id': 81409502, 'filing_type': None}}

#{'filing': {'uid': '1d3b59eJxjZRd2Eme0dBLnMDIwMDc0MDJzYnUS5zcwMHAMNPd1CQkJNjY2M3cSZ3YKMmlSc87PLUjMy0wt9sgvLU61sorw9XEPt7LyzE1MT4VS3qmVRCpjZWBgYARiJiBmBmIWIGYFAH0eJA0=', 'filing_code': 'BR4', 'title': 'Return by an oversea company subject to branch registration of change of directors or secretary or of their particulars', 'url': None, 'description': 'DIR APPOINTED        17/09/07, TEO, MICHAEL CHEE HONG, SERVICE ADDRESS, 1 CHURCHILL PLACE, LONDON E14 5HP', 'date': '2007-10-26', 'opencorporates_url': 'http://opencorporates.com/filings/59420474', 'id': 59420474, 'filing_type': 'Return by an oversea company subject to branch registration of change of directors or secretary or of their particulars'}}

#{'filing': {'uid': '004756eJxjZRd2YnXi4ohPyU9OSS1OBnHYQJzMFCdxfgMDgwALfwtnZ6dgYwsjIycuzvi0/KLcksqCVCdxZqcgMycu1viU5MQSJ3FGS5gpiSVASQ4jAwNLAwtDwyY15/zcgsS8zNRij/zS4lQrqwhfH/dwKyvP3MT0VCjlnVpJpDJuBgYGRiBmAmJmIGYBYlYgZgNidiDmAGJOIOYCYm4AzKo0nA==', 'filing_code': 'BR6', 'title': 'Return of change of person authorised to accept service or to represent the branch of an oversea company or any change in their particulars', 'url': None, 'description': 'TRANSACTION BR6- BR008167 PERSON AUTHORISED TO REPRESENT TERMINATED 10/07/2009 ADAM NICHOLAS JANISCH', 'date': '2009-08-11', 'opencorporates_url': 'http://opencorporates.com/filings/79898379', 'id': 79898379, 'filing_type': 'Return of change of person authorised to accept service or to represent the branch of an oversea company or any change in their particulars'}},

#{'filing': {'uid': '60eb0beJxjZRd2YnXi4ohPyU9OSS1OBnHYQJzMFCdxfgMDA5cwwyhXX58QEyMTSycuzvi0/KLcksqCVCdxNv9gxwADUycu1viU5MQSJ3FGS5hBiSVAeQ4jA0MDAwtDsyY15/zcgsS8zNRij/zS4lQrqwhfH/dwKyvP3MT0VCjlnVpJpDJuBgYGRiBmAmJmIGYBYlYgZgNidiDmAGJOIOYCYm4AolI1mw==', 'filing_code': 'OSAP05', 'title': 'Appointment by an overseas company of a person authorised to represent the company as a permanent representative in respect of a UK establishment', 'url': None, 'description': 'TRANSACTION OSAP05- BR008167 PERSON AUTHORISED TO REPRESENT APPOINTED 17/06/2010 PRIYAN SHAH  -- ADDRESS: 1 CHURCHILL PLACE, LONDON, E14 5HP', 'date': '2010-08-16', 'opencorporates_url': 'http://opencorporates.com/filings/79898371', 'id': 79898371, 'filing_type': 'Appointment by an overseas company of a person authorised to represent the company as a permanent representative in respect of a UK establishment'}}

#{'filing': {'uid': 'ff30d3eJxjZRd2YnXi4ohPyU9OSS1OBnHYQJzMFCdxfgMDA8fwQG8nf2NPEyNLYycuzvi0/KLcksqCVCdxNv/gEF8DoCBrfEpyYomTOKMlzKDEEqA8h5GBIQiaNqk55+cWJOZlphZ75JcWp1pZRfj6uIdbWXnmJqanQinv1EoilXEzMDAwAjETEDMDMQsQswIxGxCzAzEHEHMCMRcQcwMAlvo1ig==', 'filing_code': 'OSTM03', 'title': 'Termination of appointment by an overseas company of a person authorised to accept service of documents or person authorised to represent the company in respect of a UK establishment', 'url': None, 'description': 'TRANSACTION OSTM03- BR008167 PERSON AUTHORISED TO REPRESENT TERMINATED 17/05/2010 ELKE EDIS', 'date': '2010-10-15', 'opencorporates_url': 'http://opencorporates.com/filings/79898369', 'id': 79898369, 'filing_type': 'Termination of appointment by an overseas company of a person authorised to accept service of documents or person authorised to represent the company in respect of a UK establishment'}}

def logDirectors(ocname,ocid,filings,logger=True):
    #br1-par untested
    print 'director filings',filings
    for filing in filings:
        if filing["filing"]["filing_type"]=="Appointment of director" or filing["filing"]["filing_code"]=="AP01":
            desc=filing["filing"]["description"]
            director=desc.replace('DIRECTOR APPOINTED ','')
            if logger: recordDirectorChange(ocname,ocid,filing['filing'],director)
            else: print "AP01",ocid,filing['filing'],director
        elif filing["filing"]["filing_type"]=="Termination of appointment of director" or filing["filing"]["filing_code"]=="TM01":
            desc=filing["filing"]["description"]
            director=desc.replace('APPOINTMENT TERMINATED, DIRECTOR ','')
            director=director.replace('APPOINTMENT TERMINATED, ','')
            if logger: recordDirectorChange(ocname,ocid,filing['filing'],director)
            else: print "TM01",ocid,filing['filing'],director
        elif filing["filing"]["filing_code"]=="BR1-PAR":
            desc=filing["filing"]["description"]
            r=re.match(r".* APPOINTED, ([^,]*, [^,]*), SERVICE ADDRESS, (.*)$",desc)
            if r!=None and logger:
                recordDirectorChange(ocname,ocid,filing['filing'],r.group(1),r.group(2))
        elif filing["filing"]["filing_code"]=="BR4":
            desc=filing["filing"]["description"]
            r=re.match(r".* APPOINTED[^,]*, ([^,]*, [^,]*), SERVICE ADDRESS, (.*)$",desc)
            if r!=None and logger:
                recordDirectorChange(ocname,ocid,filing['filing'],r.group(1),r.group(2))
        elif filing["filing"]["filing_code"]=="BR6":
            desc=filing["filing"]["description"]
            r=re.match(r".* TERMINATED [^\s]*\s(.*)$",desc)
            if r!=None and logger:
                recordDirectorChange(ocname,ocid,filing['filing'],r.group(1))
        elif filing["filing"]["filing_code"]=="OSAP05":
            desc=filing["filing"]["description"]
            r=re.match(r".*TED [^\s]*\s(.*)\s-.*ADDRESS: (.*)$",desc)
            if r!=None and logger:
                recordDirectorChange(ocname,ocid,filing['filing'],r.group(1),r.group(2))
        elif filing["filing"]["filing_code"]=="OSTM03":
            desc=filing["filing"]["description"]
            r=re.match(r".*TED [^\s]*\s(.*)$",desc)
            if r!=None and logger:
                recordDirectorChange(ocname,ocid,filing['filing'],r.group(1))


def getOCcompanyDetails(ocid):
    ocurl='http://api.opencorporates.com'+ocid+'?api_token='+ockey
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    return ocdata['results']

def logCompanyDetails(ocid,ocdata):
    if 'error' in ocdata: return
    print ocdata,
    cdata={'ocid':ocid}
    cdata['name']=ocdata['company']['name']
    cdata['address']=ocdata['company']['registered_address_in_full']
    print cdata
    scraperwiki.sqlite.save(unique_keys=['ocid'], table_name='companydetails_'+ttarget, data=cdata)

try:
    q = '* FROM "companydetails_'+ttarget+'"'
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
    q = '* FROM "directors_'+ttarget+'"'
    qdata = scraperwiki.sqlite.select(q)
    print qdata
except:
    qdata=[]

directors=[]
for d in qdata:
    directors.append(d['ocid'])

#"result":[{"id":"/companies/gb/00445790","name":"TESCO PLC","type":[{"id":"/organization/organization","name":"Organization"}],"score":78.0,"match":false,"uri":"htt
def companyProcessor():
    ccount=len(entities['result'])
    cci = 1
    for entity in entities['result']:
        ocid=entity['id']
        ocname=entity['name']
        print 'processing',ocid, cci,'of',ccount
        if ocid not in companies:
            time.sleep(1.0)
            print 'getting company', ocid
            ocdata=getOCcompanyDetails(ocid)
            logCompanyDetails(ocid,ocdata)
            if ocid not in directors:
                print 'getting directors', ocid
                filings=getOCfilingData(ocid)
                logDirectors(ocname,ocid,filings)
        else: print 'got it already'
        cci=cci+1



def testfiling(ocid):
    filings=getOCfilingData(ocid)
    logDirectors('',ocid,filings,False)

#testfiling('/companies/gb/FC026875')

companyProcessor()

#scraperwiki.sqlite.execute('drop table "companyaddress"')