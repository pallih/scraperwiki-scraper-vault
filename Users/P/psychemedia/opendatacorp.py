import scraperwiki

import urllib,simplejson


#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
    ykey=qsenv["YKEY"]
except:
    ockey=''



companies=[]
ocOfficers=[]


def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass


def dirDetails(officer,data={}):
    data["name"]=officer["officer"]["name"]
    if "jurisdiction_code" in officer["officer"]: data["jurisdiction_code"]=officer["officer"]["jurisdiction_code"]
    else: data["jurisdiction_code"]=""
    data["position"]=officer["officer"]["position"]
    data["ocurl"]=officer["officer"]["opencorporates_url"]
    #data[""]=
    data["id"]=data["ocurl"].replace("http://opencorporates.com/officers/",'')
    print 'dirDetails', data["id"],data
    #ourl="http://api.opencorporates.com/v0.2/officers/"+data["id"]
    #odata=simplejson.load(urllib.urlopen(ourl))
    return data

def companyDetails(officer,data={}):
    data["companyName"]=officer["officer"]["company"]["name"]
    data["companyJurisdiction"]=officer["officer"]["company"]["jurisdiction_code"]
    data["companyNumber"]=officer["officer"]["company"]["company_number"]
    data["companyOCurl"]=officer["officer"]["company"]["opencorporates_url"]
    return data

def getOfficerDetails(name):
    ourl="http://api.opencorporates.com/v0.2/officers/search?q="+urllib.quote(name)+'&api_token='+ockey
    jsondata=simplejson.load(urllib.urlopen(ourl))
    print 'getOfficerDetails',jsondata
    return jsondata['results']['officers']

#url="http://api.opencorporates.com/v0.2/officers/search?q=nigel%20richard%20shadbolt"
#jsondata=simplejson.load(urllib.urlopen(url))
#officers=jsondata['results']['officers']

def handleOffices(offices,exact='',tname='test'):
    for officer in offices:
        data=dirDetails(officer)
        data=companyDetails(officer,data)
        if exact!='' and exact.lower()!=data["name"].lower():return
        if data["companyNumber"] not in companies: companies.append((data["companyNumber"],data["companyJurisdiction"]))
        if data["id"] not in ocOfficers:
            ocOfficers.append(data["id"])
            if tname!='' and data['companyJurisdiction']=='gb': scraperwiki.sqlite.save(unique_keys=["id"],table_name=tname+'x', data=data)

def getCompanies(companies,j=[],tname='test'):
    newOfficers=[]
    for (companyNumber,jurisdiction) in companies:
        if j!=[] and jurisdiction not in j: continue
        ocurl="http://api.opencorporates.com/v0.2/companies/"+jurisdiction+"/"+companyNumber+'?api_token='+ockey
        jsondata=simplejson.load(urllib.urlopen(ocurl))
        if "officers" in jsondata["results"]["company"]:
            print 'companytrawl',jsondata["results"]["company"]["officers"]
            companyName=jsondata["results"]["company"]["name"]
            for officer in jsondata["results"]["company"]["officers"]:
                data=dirDetails(officer)
                data["companyNumber"]= companyNumber
                data['companyJurisdiction']=jurisdiction
                data["companyName"]=companyName
                if data["id"] not in newOfficers:
                    print "adding"
                    ocOfficers.append(data["id"])
                    newOfficers.append(data["name"])
                    scraperwiki.sqlite.save(unique_keys=["id"],table_name=tname, data=data)
                else: print "dupe?"

    #next phase would be to look up new directors details for new companies? 
    print newOfficers

def demo1():
    name="NIGEL RICHARD SHADBOLT"
    tname=name.lower()
    tname=tname.replace(' ','')

    offices=getOfficerDetails(name)
    handleOffices(offices,name,'')

    print companies
    getCompanies(companies,tname=tname)

def demo2():
    cclurl='http://openlylocal.com/councils/298.json'
    jsondata=simplejson.load(urllib.urlopen(cclurl))

    names=[]
    members=jsondata['council']['members']
    for member in members:
        name=' '.join([member['first_name'],member['last_name']])
        names.append(name)
    print names

    tname='cclDemo'
    dropper(tname)
    dropper(tname+'x')
    for name in names:
        offices=getOfficerDetails(name)
        handleOffices(offices,name,tname)

    print companies
    getCompanies(companies,['gb'],tname)

demo2()
#for name in newOfficers:
#    offices=getOfficerDetails(name)
#    handleOffices(offices)
import scraperwiki

import urllib,simplejson


#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
    ykey=qsenv["YKEY"]
except:
    ockey=''



companies=[]
ocOfficers=[]


def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass


def dirDetails(officer,data={}):
    data["name"]=officer["officer"]["name"]
    if "jurisdiction_code" in officer["officer"]: data["jurisdiction_code"]=officer["officer"]["jurisdiction_code"]
    else: data["jurisdiction_code"]=""
    data["position"]=officer["officer"]["position"]
    data["ocurl"]=officer["officer"]["opencorporates_url"]
    #data[""]=
    data["id"]=data["ocurl"].replace("http://opencorporates.com/officers/",'')
    print 'dirDetails', data["id"],data
    #ourl="http://api.opencorporates.com/v0.2/officers/"+data["id"]
    #odata=simplejson.load(urllib.urlopen(ourl))
    return data

def companyDetails(officer,data={}):
    data["companyName"]=officer["officer"]["company"]["name"]
    data["companyJurisdiction"]=officer["officer"]["company"]["jurisdiction_code"]
    data["companyNumber"]=officer["officer"]["company"]["company_number"]
    data["companyOCurl"]=officer["officer"]["company"]["opencorporates_url"]
    return data

def getOfficerDetails(name):
    ourl="http://api.opencorporates.com/v0.2/officers/search?q="+urllib.quote(name)+'&api_token='+ockey
    jsondata=simplejson.load(urllib.urlopen(ourl))
    print 'getOfficerDetails',jsondata
    return jsondata['results']['officers']

#url="http://api.opencorporates.com/v0.2/officers/search?q=nigel%20richard%20shadbolt"
#jsondata=simplejson.load(urllib.urlopen(url))
#officers=jsondata['results']['officers']

def handleOffices(offices,exact='',tname='test'):
    for officer in offices:
        data=dirDetails(officer)
        data=companyDetails(officer,data)
        if exact!='' and exact.lower()!=data["name"].lower():return
        if data["companyNumber"] not in companies: companies.append((data["companyNumber"],data["companyJurisdiction"]))
        if data["id"] not in ocOfficers:
            ocOfficers.append(data["id"])
            if tname!='' and data['companyJurisdiction']=='gb': scraperwiki.sqlite.save(unique_keys=["id"],table_name=tname+'x', data=data)

def getCompanies(companies,j=[],tname='test'):
    newOfficers=[]
    for (companyNumber,jurisdiction) in companies:
        if j!=[] and jurisdiction not in j: continue
        ocurl="http://api.opencorporates.com/v0.2/companies/"+jurisdiction+"/"+companyNumber+'?api_token='+ockey
        jsondata=simplejson.load(urllib.urlopen(ocurl))
        if "officers" in jsondata["results"]["company"]:
            print 'companytrawl',jsondata["results"]["company"]["officers"]
            companyName=jsondata["results"]["company"]["name"]
            for officer in jsondata["results"]["company"]["officers"]:
                data=dirDetails(officer)
                data["companyNumber"]= companyNumber
                data['companyJurisdiction']=jurisdiction
                data["companyName"]=companyName
                if data["id"] not in newOfficers:
                    print "adding"
                    ocOfficers.append(data["id"])
                    newOfficers.append(data["name"])
                    scraperwiki.sqlite.save(unique_keys=["id"],table_name=tname, data=data)
                else: print "dupe?"

    #next phase would be to look up new directors details for new companies? 
    print newOfficers

def demo1():
    name="NIGEL RICHARD SHADBOLT"
    tname=name.lower()
    tname=tname.replace(' ','')

    offices=getOfficerDetails(name)
    handleOffices(offices,name,'')

    print companies
    getCompanies(companies,tname=tname)

def demo2():
    cclurl='http://openlylocal.com/councils/298.json'
    jsondata=simplejson.load(urllib.urlopen(cclurl))

    names=[]
    members=jsondata['council']['members']
    for member in members:
        name=' '.join([member['first_name'],member['last_name']])
        names.append(name)
    print names

    tname='cclDemo'
    dropper(tname)
    dropper(tname+'x')
    for name in names:
        offices=getOfficerDetails(name)
        handleOffices(offices,name,tname)

    print companies
    getCompanies(companies,['gb'],tname)

demo2()
#for name in newOfficers:
#    offices=getOfficerDetails(name)
#    handleOffices(offices)
