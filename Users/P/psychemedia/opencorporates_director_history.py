import scraperwiki, simplejson, urllib, time

dirname="MARTIN STUART SORRELL"

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
except:
    ockey=''

#----
APISTUB='http://api.opencorporates.com/v0.2'

def deslash(x): return x.strip('/')
def signed(url): return url+'?api_token='+ockey

def occStrip(ocURL):
    stripped=ocURL.replace('http://opencorporates.com/companies','')
    stripped=stripped.replace('http://opencorporates.com/officers','')
    return deslash(stripped)

def buildURL(items):
    url=APISTUB
    for i in items:
        url='/'.join([url,deslash(i)])
    return signed(url)

exclusions_d=[] 
exclusions_r=[] #['nominated director','nominated secretary']
def getOCofficerSearch(name,page=1,dnames=[]):
    durl=APISTUB+'/officers/search?q="'+name+'"&per_page=100&page='+str(page)
    ocdata=simplejson.load(urllib.urlopen(durl+'&api_token='+ockey))['results']
    optimise=0
    for officer in ocdata['officers']:
        if name==officer['officer']['name']:
            dnames.append( ( occStrip(officer['officer']['opencorporates_url']), occStrip(officer['officer']['company']['opencorporates_url']) ) )
    if page < ocdata['total_pages'] and page<pagemax:
        page=page+1
        time.sleep(1.5)
        dnames=getOCofficerSearch(name,page,dnames)
    return dnames

def getOCofficerData(ocid):
    ocurl=buildURL(['officers',ocid])
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    time.sleep(1.5)
    print ocdata
    return ocdata['results']

dnames=getOCofficerSearch(dirname)

def recorder(data,table='swdata',keys=[]):
     scraperwiki.sqlite.save(unique_keys=keys, table_name=table, data=data)

tname='dir_'+dirname.replace(' ','_').lower()
keys=['dirID']
bigtmp=[]
for dir,company in dnames:
    data=getOCofficerData(dir)

    tmp={}
    dd=data['officer']

    tmp['dirID']=dd['id']
    tmp['dirName']=dd['name']
    tmp['dirPos']=dd['position']
    tmp['start_date']=dd['start_date']
    tmp['end_date']=dd['end_date']
    tmp['inactive']=dd['inactive?']
    
    tmp['cname']=dd['company']['name']
    tmp['cjurisdiction']=dd['company']['jurisdiction_code']
    tmp['ccode']=dd['company']['company_number']

    bigtmp.append(tmp.copy())
    if len(bigtmp)>20:
        recorder(bigtmp,tname,keys)
        bigtmp=[]
recorder(bigtmp,tname,keys)
import scraperwiki, simplejson, urllib, time

dirname="MARTIN STUART SORRELL"

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
except:
    ockey=''

#----
APISTUB='http://api.opencorporates.com/v0.2'

def deslash(x): return x.strip('/')
def signed(url): return url+'?api_token='+ockey

def occStrip(ocURL):
    stripped=ocURL.replace('http://opencorporates.com/companies','')
    stripped=stripped.replace('http://opencorporates.com/officers','')
    return deslash(stripped)

def buildURL(items):
    url=APISTUB
    for i in items:
        url='/'.join([url,deslash(i)])
    return signed(url)

exclusions_d=[] 
exclusions_r=[] #['nominated director','nominated secretary']
def getOCofficerSearch(name,page=1,dnames=[]):
    durl=APISTUB+'/officers/search?q="'+name+'"&per_page=100&page='+str(page)
    ocdata=simplejson.load(urllib.urlopen(durl+'&api_token='+ockey))['results']
    optimise=0
    for officer in ocdata['officers']:
        if name==officer['officer']['name']:
            dnames.append( ( occStrip(officer['officer']['opencorporates_url']), occStrip(officer['officer']['company']['opencorporates_url']) ) )
    if page < ocdata['total_pages'] and page<pagemax:
        page=page+1
        time.sleep(1.5)
        dnames=getOCofficerSearch(name,page,dnames)
    return dnames

def getOCofficerData(ocid):
    ocurl=buildURL(['officers',ocid])
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    time.sleep(1.5)
    print ocdata
    return ocdata['results']

dnames=getOCofficerSearch(dirname)

def recorder(data,table='swdata',keys=[]):
     scraperwiki.sqlite.save(unique_keys=keys, table_name=table, data=data)

tname='dir_'+dirname.replace(' ','_').lower()
keys=['dirID']
bigtmp=[]
for dir,company in dnames:
    data=getOCofficerData(dir)

    tmp={}
    dd=data['officer']

    tmp['dirID']=dd['id']
    tmp['dirName']=dd['name']
    tmp['dirPos']=dd['position']
    tmp['start_date']=dd['start_date']
    tmp['end_date']=dd['end_date']
    tmp['inactive']=dd['inactive?']
    
    tmp['cname']=dd['company']['name']
    tmp['cjurisdiction']=dd['company']['jurisdiction_code']
    tmp['ccode']=dd['company']['company_number']

    bigtmp.append(tmp.copy())
    if len(bigtmp)>20:
        recorder(bigtmp,tname,keys)
        bigtmp=[]
recorder(bigtmp,tname,keys)
