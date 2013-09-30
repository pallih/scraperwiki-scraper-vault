#The aim of this scraper is to provide, in the first instance, a way of bootstrapping a search around either a company ID or a director ID
#The user should also define a tablename stub to identify the trawl.

#If one or more company IDs are specified:
#Get the company details
#??Add any names the company was previously known a list of 'previous' companies ?
#??do "morph chains" to show how company names change?
#Get the directors
#Search for directors of same name and then do an exact match filter pass
#Get the companies associated with those exact matches
#To search for only active companies, &exclude_inactive=true

#TO DO - Spot and handle rate limiting
#TO DO - populate db

#Care_UK_2,2_test gb/01668247
##Findus gb/02017367 Findus2,2_test
# ? TescoFoodSourcing2,2 bootstrap gb/07502096
##BirdsEyeFoods2,2 bootstrap gb/00341305
#TescoHoldings2,2_bootstrap  gb/00243011
# ? AssociatedBritishFoods gb/00293262
#? ABPFoods2,2_test  gb/04813576 gb/05186763
##CandDfoods_ABPbootstrap gb/05141595
##MoyPark gb/NI004842
##Greencorefoods gb/07441672 
# ? Leogroup gb/04266877
##oakfieldfoods gb/02103137
##stanlyGibson gb/03251586
#? The2Sisters Food Group gb/02826929 NorthernFOods gb/00471864
#First Practice Management gb/04699989 gb/03226910
#Whitbread plc gb/04120344
#experian gb/03720393
#sodexo gb/01986040
#premierFoods gb/05160050 gb/SC096055 gb/SC096055 premierfreshfoods gb/04052423
#compassFood gb/00420158
#butchers pet care gb/01716195
#opendatainstitute gb/08030289
#sainsburysSupermarkets gb/03261722
#morrisonSupermarket gb/07529983 gb/00358949 safeway gb/00534115
#costcutter gb/02059678
#spar gb/00634226
#co-operative group gb/IP00525R
#dragons den "THEODOROS PAPHITIS" "PETER DAVID JONES", "DEBORAH SONIA MEADEN", "DUNCAN WALKER BANNATYNE"
#brake bros gb/02035315
#blade farming gb/04976254
#haymarket
#royalShell gb/04366849 SE1 7NA
#Ringway gb/02756434 
#Island Roads gb/08169759 gb/08168976 Partners - gb/02756434 gb/08257239
#Meridiam gb/08257239
#futurelearn gb/08324083
#gallaher (JTI) gb/01501573
#Mercia Healthcare gb/03693524
#semperian holdco gb/05945929
#semperian postcode EC2V 7BX
#infrastructure investors EC2V 7EX
#interserve plc gb/00088456
#IPPR gb/2292601
#wolff olins gb/01945130
#ft gb/00227590
#facebook gb/06331310 us_wa/603092032
targetCompanies=['us_wa/603092032'] #list of OpenCorporates Company IDs with leading country code
targetDirectors=[] #list of OpenCorporates Director IDs
targetDirectorNames=[]
targetPostcode=''

targetStub='Facebook_2_2' #name of the db table stub


trawldepth=2
coverage='current' #all, current, previous **Relates to directors
status='active' #all, active, inactive **Relates to companies
DIRINTERSECT=2 #The minimum number of shared directors (current or past) to count as part of same grouping

pagemax=25 #need to address this?

#------

targetStub=targetStub.replace(' ','_')

import time
import scraperwiki, simplejson,urllib,re

import networkx as nx

#scraperwiki.sqlite.execute("drop table if exists "+targetStub)
#scraperwiki.sqlite.commit()
#exit(-1)


#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
    #ykey=qsenv["YKEY"]
except:
    ockey=''

#----
APISTUB='http://api.opencorporates.com/v0.2'

def deslash(x): return x.strip('/')
def signed(url): return url+'?api_token='+ockey

def occStrip(ocURL):
    return deslash(ocURL.replace('http://opencorporates.com/companies',''))

def getCompaniesByPostcode(targetPostcode,page=1,pcdata=[]):
    targetPostcode=targetPostcode.replace(' ','+')
    #CAVEATS ON SEARCH
    url='http://api.opencorporates.com/v0.2/companies/search?q='+targetPostcode+'&jurisdiction_code=gb&current_status=Active&per_page=50&page='+str(page)
    tmp=simplejson.load(urllib.urlopen(url))
    tmpdata=tmp['results']
    for c in tmpdata['companies']:
        pcdata.append(occStrip(c['company']['opencorporates_url']))
    page=page+1
    if tmpdata['page']<tmpdata['total_pages']:
        pcdata=getCompaniesByPostcode(targetPostcode,page,pcdata)
    return pcdata

if targetPostcode!='':
    targetCompanies=getCompaniesByPostcode(targetPostcode,1,[])
    print '..',targetCompanies

def buildURL(items):
    url=APISTUB
    for i in items:
        url='/'.join([url,deslash(i)])
    return signed(url)

def getOCcompanyData(ocid):
    time.sleep(1.5)
    ocurl=buildURL(['companies',ocid])
    try:
        ocdata=simplejson.load(urllib.urlopen(ocurl))
        #print ocurl,ocdata
        if 'results' in ocdata: return ocdata['results']
        else: return -1
    except: return -2
    return -2

def getOCofficerData(ocid):
    ocurl=buildURL(['officers',ocid])
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    time.sleep(1.5)
    return ocdata['results']


def recorder(data):
    d=[]
    for record in data['companies']:
        dd=record.copy()
        d.append(dd)
        if len(d)>100:
            scraperwiki.sqlite.save(unique_keys=['ocid'], table_name='companies_'+targetStub, data=d)
            d=[]
    scraperwiki.sqlite.save(unique_keys=['jurisdiction_code','company_number'], table_name='companies_'+targetStub, data=d)
    data['companies']=[]
    d=[]
    for record in data['directors']:
            dd=record.copy()
            d.append(dd)
            if len(d)>100:
                scraperwiki.sqlite.save(unique_keys=['ocid'], table_name='directors_'+targetStub, data=d)
                d=[]
    try:
        scraperwiki.sqlite.save(unique_keys=['id'], table_name='directors_'+targetStub, data=d)
        data['directors']=[]
    except: pass
    return data


exclusions_d=[] #['FIRST SCOTTISH SECRETARIES LIMITED','FIRST DIRECTORS LIMITED']
exclusions_r=['nominated director','nominated secretary']
def getOCofficerCompaniesSearch(name,page=1,cidnames=[]):
    durl=APISTUB+'/officers/search?q="'+name+'"&per_page=100&page='+str(page)
    jdata=simplejson.load(urllib.urlopen(durl+'&api_token='+ockey))
    if 'results' in jdata: ocdata=jdata['results']
    else: return cidnames
    optimise=0
    #?need a heuristic for results with large page count?
    #Maybe put things into secondary possibles to check against?
    for officer in ocdata['officers']:
        if (officer['officer']['name'].strip() in exclusions_d) or officer['officer']['position'] in exclusions_r:
            optimise=1
            break
        elif name==officer['officer']['name']:
            #print 'Possible new company for',name,officer['officer']['company']['name']
            #would a nominated secretary be interesting to search on? eg FIRST SECRETARIES LIMITED
            cidnames.append( ( occStrip(officer['officer']['company']['opencorporates_url']), occStrip(officer['officer']['company']['name']) ) )
    if page < ocdata['total_pages'] and page<pagemax & optimise==0:
        page=page+1
        time.sleep(1.5)
        cidnames=getOCofficerCompaniesSearch(name,page,cidnames)
    #http://api.opencorporates.com/v0.2/officers/search?q=john+smith
    return cidnames
#-----

def trawlPass(data=[],depth=1,coverage='current',status='active'):
    data['depth']=data['depth']+1
    done=1
    newTargets=[]
    for ocid in data['targetCompanies']:
        if ocid not in data['cids']:
            #bigtmp=[]
            data['cids'].append(ocid)
            cd=getOCcompanyData(ocid)
            if cd==-2:break
            if cd!=-1:
                if status=='active' and (cd['company']['inactive']): cd=-1
                elif status=='inactive' and not (cd['company']['inactive']): cd=-1
            if cd!=-1:
                cd=cd['company']
                uid=occStrip(cd['opencorporates_url'])
                dids=cd['officers']
                tmp={'ocid':uid}
                for x in ['name','jurisdiction_code','company_number','incorporation_date','dissolution_date','registered_address_in_full']:
                    tmp[x]=cd[x]
                didset=[]
                for didr in dids:
                    did=didr['officer']
                    did['name']=did['name'].strip()
                    if did['name'] not in didset:
                    #TEST - TO DO  - is None the right thing here?
                        print did['name'],did['end_date']
                        if coverage=='all':
                            didset.append(did['name'])
                        elif coverage=='current' and did['end_date'] is None:
                            didset.append(did['name'])
                        elif coverage=='previous' and did['end_date']is not None:
                            didset.append(did['name'])
                    #some additional logic for heuristically determining whether or not a company is in same grouping
                if data['depth']==1: inset=1
                else: inset=0
                print coverage,'dirset',didset
                if (len(list(set(didset) & set(data['dnames'])))) >= DIRINTERSECT : inset=1
                if cd['registered_address_in_full'] in data['addresses']: inset=1
                if (inset==1):
                    data['companies'].append(tmp.copy())
                    print 'Added',tmp
                    if cd['registered_address_in_full'] not in data['addresses']: data['addresses'].append(cd['registered_address_in_full'])
                    for didr in dids:
                        if didr['officer']['name'] in didset:
                            did=didr['officer']
                            print 'dir',did['name']
                            #print didr
                            did['ocid']=ocid#did['opencorporates_url'].replace("http://opencorporates.com/officers/","")
                            did['cname']=cd['name']
                            data['directors'].append(did.copy())
                            if did['name'] not in data['dnames']:
                                data['dnames'].append(did['name'])
                                #get matchalikes
                                cidnames=getOCofficerCompaniesSearch(did['name'],1,[])
                                bigtmp=[]
                                for (cid,cname) in cidnames:
                                    bigtmp.append({'cid':cid,'cname':cname,'dname':did['name']})
                                    if len(bigtmp)>20:
                                        try:
                                            scraperwiki.sqlite.save(unique_keys=['cid','dname'], table_name='possibles_'+targetStub, data=bigtmp)
                                            bigtmp=[]
                                        except: pass
                                    if cid not in data['targetCompanies'] and cid not in newTargets:
                                        #print 'Brand new company for dir',cid
                                                    newTargets.append(cid)
                                try:
                                    scraperwiki.sqlite.save(unique_keys=['cid','dname'], table_name='possibles_'+targetStub, data=bigtmp)
                                    bigtmp=[]
                                except: pass
                    data=recorder(data)
    data=recorder(data)
    for ocid in newTargets:
        if ocid not in data['targetCompanies']:
            data['targetCompanies'].append(ocid)
        done=0
    for director in data['targetDirectors']:
        od=getOCofficerData(ocid)['officer']
        if od==-1: continue
        ocid=occStrip(od['company']['opencorporates_url'])
        if ocid not in data['targetCompanies']:
            data['targetCompanies'].append(ocid)
            done=0
    depth=depth-1
    if (done==0) and depth>0:
        return trawlPass(data,depth,coverage,status)
    else: return data

_targetCompanies=[]
for c in targetCompanies:
    _targetCompanies.append(deslash(c))

for name in targetDirectorNames:
    dircolist=getOCofficerCompaniesSearch(name)
    for (coid,co) in dircolist:
         _targetCompanies.append(coid)

init={'depth':0,'targetCompanies':_targetCompanies,'targetDirectors':targetDirectors,'cids':[],'dnames':[],'addresses':[],'companies':[],'directors':[]}
data=trawlPass(init,trawldepth,coverage,status)
print data
#The aim of this scraper is to provide, in the first instance, a way of bootstrapping a search around either a company ID or a director ID
#The user should also define a tablename stub to identify the trawl.

#If one or more company IDs are specified:
#Get the company details
#??Add any names the company was previously known a list of 'previous' companies ?
#??do "morph chains" to show how company names change?
#Get the directors
#Search for directors of same name and then do an exact match filter pass
#Get the companies associated with those exact matches
#To search for only active companies, &exclude_inactive=true

#TO DO - Spot and handle rate limiting
#TO DO - populate db

#Care_UK_2,2_test gb/01668247
##Findus gb/02017367 Findus2,2_test
# ? TescoFoodSourcing2,2 bootstrap gb/07502096
##BirdsEyeFoods2,2 bootstrap gb/00341305
#TescoHoldings2,2_bootstrap  gb/00243011
# ? AssociatedBritishFoods gb/00293262
#? ABPFoods2,2_test  gb/04813576 gb/05186763
##CandDfoods_ABPbootstrap gb/05141595
##MoyPark gb/NI004842
##Greencorefoods gb/07441672 
# ? Leogroup gb/04266877
##oakfieldfoods gb/02103137
##stanlyGibson gb/03251586
#? The2Sisters Food Group gb/02826929 NorthernFOods gb/00471864
#First Practice Management gb/04699989 gb/03226910
#Whitbread plc gb/04120344
#experian gb/03720393
#sodexo gb/01986040
#premierFoods gb/05160050 gb/SC096055 gb/SC096055 premierfreshfoods gb/04052423
#compassFood gb/00420158
#butchers pet care gb/01716195
#opendatainstitute gb/08030289
#sainsburysSupermarkets gb/03261722
#morrisonSupermarket gb/07529983 gb/00358949 safeway gb/00534115
#costcutter gb/02059678
#spar gb/00634226
#co-operative group gb/IP00525R
#dragons den "THEODOROS PAPHITIS" "PETER DAVID JONES", "DEBORAH SONIA MEADEN", "DUNCAN WALKER BANNATYNE"
#brake bros gb/02035315
#blade farming gb/04976254
#haymarket
#royalShell gb/04366849 SE1 7NA
#Ringway gb/02756434 
#Island Roads gb/08169759 gb/08168976 Partners - gb/02756434 gb/08257239
#Meridiam gb/08257239
#futurelearn gb/08324083
#gallaher (JTI) gb/01501573
#Mercia Healthcare gb/03693524
#semperian holdco gb/05945929
#semperian postcode EC2V 7BX
#infrastructure investors EC2V 7EX
#interserve plc gb/00088456
#IPPR gb/2292601
#wolff olins gb/01945130
#ft gb/00227590
#facebook gb/06331310 us_wa/603092032
targetCompanies=['us_wa/603092032'] #list of OpenCorporates Company IDs with leading country code
targetDirectors=[] #list of OpenCorporates Director IDs
targetDirectorNames=[]
targetPostcode=''

targetStub='Facebook_2_2' #name of the db table stub


trawldepth=2
coverage='current' #all, current, previous **Relates to directors
status='active' #all, active, inactive **Relates to companies
DIRINTERSECT=2 #The minimum number of shared directors (current or past) to count as part of same grouping

pagemax=25 #need to address this?

#------

targetStub=targetStub.replace(' ','_')

import time
import scraperwiki, simplejson,urllib,re

import networkx as nx

#scraperwiki.sqlite.execute("drop table if exists "+targetStub)
#scraperwiki.sqlite.commit()
#exit(-1)


#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
    #ykey=qsenv["YKEY"]
except:
    ockey=''

#----
APISTUB='http://api.opencorporates.com/v0.2'

def deslash(x): return x.strip('/')
def signed(url): return url+'?api_token='+ockey

def occStrip(ocURL):
    return deslash(ocURL.replace('http://opencorporates.com/companies',''))

def getCompaniesByPostcode(targetPostcode,page=1,pcdata=[]):
    targetPostcode=targetPostcode.replace(' ','+')
    #CAVEATS ON SEARCH
    url='http://api.opencorporates.com/v0.2/companies/search?q='+targetPostcode+'&jurisdiction_code=gb&current_status=Active&per_page=50&page='+str(page)
    tmp=simplejson.load(urllib.urlopen(url))
    tmpdata=tmp['results']
    for c in tmpdata['companies']:
        pcdata.append(occStrip(c['company']['opencorporates_url']))
    page=page+1
    if tmpdata['page']<tmpdata['total_pages']:
        pcdata=getCompaniesByPostcode(targetPostcode,page,pcdata)
    return pcdata

if targetPostcode!='':
    targetCompanies=getCompaniesByPostcode(targetPostcode,1,[])
    print '..',targetCompanies

def buildURL(items):
    url=APISTUB
    for i in items:
        url='/'.join([url,deslash(i)])
    return signed(url)

def getOCcompanyData(ocid):
    time.sleep(1.5)
    ocurl=buildURL(['companies',ocid])
    try:
        ocdata=simplejson.load(urllib.urlopen(ocurl))
        #print ocurl,ocdata
        if 'results' in ocdata: return ocdata['results']
        else: return -1
    except: return -2
    return -2

def getOCofficerData(ocid):
    ocurl=buildURL(['officers',ocid])
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    time.sleep(1.5)
    return ocdata['results']


def recorder(data):
    d=[]
    for record in data['companies']:
        dd=record.copy()
        d.append(dd)
        if len(d)>100:
            scraperwiki.sqlite.save(unique_keys=['ocid'], table_name='companies_'+targetStub, data=d)
            d=[]
    scraperwiki.sqlite.save(unique_keys=['jurisdiction_code','company_number'], table_name='companies_'+targetStub, data=d)
    data['companies']=[]
    d=[]
    for record in data['directors']:
            dd=record.copy()
            d.append(dd)
            if len(d)>100:
                scraperwiki.sqlite.save(unique_keys=['ocid'], table_name='directors_'+targetStub, data=d)
                d=[]
    try:
        scraperwiki.sqlite.save(unique_keys=['id'], table_name='directors_'+targetStub, data=d)
        data['directors']=[]
    except: pass
    return data


exclusions_d=[] #['FIRST SCOTTISH SECRETARIES LIMITED','FIRST DIRECTORS LIMITED']
exclusions_r=['nominated director','nominated secretary']
def getOCofficerCompaniesSearch(name,page=1,cidnames=[]):
    durl=APISTUB+'/officers/search?q="'+name+'"&per_page=100&page='+str(page)
    jdata=simplejson.load(urllib.urlopen(durl+'&api_token='+ockey))
    if 'results' in jdata: ocdata=jdata['results']
    else: return cidnames
    optimise=0
    #?need a heuristic for results with large page count?
    #Maybe put things into secondary possibles to check against?
    for officer in ocdata['officers']:
        if (officer['officer']['name'].strip() in exclusions_d) or officer['officer']['position'] in exclusions_r:
            optimise=1
            break
        elif name==officer['officer']['name']:
            #print 'Possible new company for',name,officer['officer']['company']['name']
            #would a nominated secretary be interesting to search on? eg FIRST SECRETARIES LIMITED
            cidnames.append( ( occStrip(officer['officer']['company']['opencorporates_url']), occStrip(officer['officer']['company']['name']) ) )
    if page < ocdata['total_pages'] and page<pagemax & optimise==0:
        page=page+1
        time.sleep(1.5)
        cidnames=getOCofficerCompaniesSearch(name,page,cidnames)
    #http://api.opencorporates.com/v0.2/officers/search?q=john+smith
    return cidnames
#-----

def trawlPass(data=[],depth=1,coverage='current',status='active'):
    data['depth']=data['depth']+1
    done=1
    newTargets=[]
    for ocid in data['targetCompanies']:
        if ocid not in data['cids']:
            #bigtmp=[]
            data['cids'].append(ocid)
            cd=getOCcompanyData(ocid)
            if cd==-2:break
            if cd!=-1:
                if status=='active' and (cd['company']['inactive']): cd=-1
                elif status=='inactive' and not (cd['company']['inactive']): cd=-1
            if cd!=-1:
                cd=cd['company']
                uid=occStrip(cd['opencorporates_url'])
                dids=cd['officers']
                tmp={'ocid':uid}
                for x in ['name','jurisdiction_code','company_number','incorporation_date','dissolution_date','registered_address_in_full']:
                    tmp[x]=cd[x]
                didset=[]
                for didr in dids:
                    did=didr['officer']
                    did['name']=did['name'].strip()
                    if did['name'] not in didset:
                    #TEST - TO DO  - is None the right thing here?
                        print did['name'],did['end_date']
                        if coverage=='all':
                            didset.append(did['name'])
                        elif coverage=='current' and did['end_date'] is None:
                            didset.append(did['name'])
                        elif coverage=='previous' and did['end_date']is not None:
                            didset.append(did['name'])
                    #some additional logic for heuristically determining whether or not a company is in same grouping
                if data['depth']==1: inset=1
                else: inset=0
                print coverage,'dirset',didset
                if (len(list(set(didset) & set(data['dnames'])))) >= DIRINTERSECT : inset=1
                if cd['registered_address_in_full'] in data['addresses']: inset=1
                if (inset==1):
                    data['companies'].append(tmp.copy())
                    print 'Added',tmp
                    if cd['registered_address_in_full'] not in data['addresses']: data['addresses'].append(cd['registered_address_in_full'])
                    for didr in dids:
                        if didr['officer']['name'] in didset:
                            did=didr['officer']
                            print 'dir',did['name']
                            #print didr
                            did['ocid']=ocid#did['opencorporates_url'].replace("http://opencorporates.com/officers/","")
                            did['cname']=cd['name']
                            data['directors'].append(did.copy())
                            if did['name'] not in data['dnames']:
                                data['dnames'].append(did['name'])
                                #get matchalikes
                                cidnames=getOCofficerCompaniesSearch(did['name'],1,[])
                                bigtmp=[]
                                for (cid,cname) in cidnames:
                                    bigtmp.append({'cid':cid,'cname':cname,'dname':did['name']})
                                    if len(bigtmp)>20:
                                        try:
                                            scraperwiki.sqlite.save(unique_keys=['cid','dname'], table_name='possibles_'+targetStub, data=bigtmp)
                                            bigtmp=[]
                                        except: pass
                                    if cid not in data['targetCompanies'] and cid not in newTargets:
                                        #print 'Brand new company for dir',cid
                                                    newTargets.append(cid)
                                try:
                                    scraperwiki.sqlite.save(unique_keys=['cid','dname'], table_name='possibles_'+targetStub, data=bigtmp)
                                    bigtmp=[]
                                except: pass
                    data=recorder(data)
    data=recorder(data)
    for ocid in newTargets:
        if ocid not in data['targetCompanies']:
            data['targetCompanies'].append(ocid)
        done=0
    for director in data['targetDirectors']:
        od=getOCofficerData(ocid)['officer']
        if od==-1: continue
        ocid=occStrip(od['company']['opencorporates_url'])
        if ocid not in data['targetCompanies']:
            data['targetCompanies'].append(ocid)
            done=0
    depth=depth-1
    if (done==0) and depth>0:
        return trawlPass(data,depth,coverage,status)
    else: return data

_targetCompanies=[]
for c in targetCompanies:
    _targetCompanies.append(deslash(c))

for name in targetDirectorNames:
    dircolist=getOCofficerCompaniesSearch(name)
    for (coid,co) in dircolist:
         _targetCompanies.append(coid)

init={'depth':0,'targetCompanies':_targetCompanies,'targetDirectors':targetDirectors,'cids':[],'dnames':[],'addresses':[],'companies':[],'directors':[]}
data=trawlPass(init,trawldepth,coverage,status)
print data
