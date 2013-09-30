import scraperwiki,simplejson,urllib

import time

#opencorporates company id
ocids=['gb/00041424','gb/00102498','gb/00519500'] 

target='virgin'
rurl='http://opencorporates.com/reconcile/gb?query='+urllib.quote(target)
#note - the opencorporates api also offers a search:  companies/search
entities=simplejson.load(urllib.urlopen(rurl))
ocids=[]
for entity in entities['result']:
    ocids.append(entity['id'].lstrip('/companies/'))

print ocids
#exit(-1)

trademarksDone=[]
q = 'octmid FROM "trademarks"'
try:
    tmp = scraperwiki.sqlite.select(q)
    for item in tmp:
        if item['octmid'] != None:
            trademarksDone.append(int(item['octmid']))
except: pass
print trademarksDone

#ocnames={}
#for ocid in ocids:
#    ocnurl=ocurl='http://api.opencorporates.com/companies/'+ocid
#    ocndata=simplejson.load(urllib.urlopen(ocnurl))
#    ocnames[ocid]=ocndata['company']['name']

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
except:
    ockey=''

def getOCcompanyData(ocid):
    ocurl='http://api.opencorporates.com/companies/'+ocid+'/data'+'?api_token='+ockey
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    return ocdata

def getOCtmData(ocid,octmid):
    octmurl='http://api.opencorporates.com/data/'+str(octmid)+'?api_token='+ockey
    data=simplejson.load(urllib.urlopen(octmurl))
    octmdata=data['datum']['attributes']
    print 'tm data',octmdata
    categories=[]
    for category in octmdata['goods_and_services_classifications']:
        if 'en' in octmdata['goods_and_services_classifications'][category]:
            categories.append(octmdata['goods_and_services_classifications'][category]['en']+'('+category+')')
    tmdata={}
    tmdata['ocid']=ocid
    tmdata['octmid']=octmid
    tmdata['ocname']=octmdata['holder_name']
    #tmdata['ocname']=ocnames[ocid]
    tmdata['categories']=" :: ".join(categories)
    tmdata['imgtype']=octmdata['mark_image_type']
    tmdata['marktext']=octmdata['mark_text']
    tmdata['repaddr']=octmdata['representative_address_lines']
    tmdata['repname']=octmdata['representative_name_lines']
    tmdata['regnum']=octmdata['international_registration_number']
    if tmdata['imgtype']=='JPG' or tmdata['imgtype']=='GIF':
        tmdata['imgurl']='http://www.wipo.int/romarin/images/' + tmdata['regnum'][0:2] +'/' + tmdata['regnum'][2:4] + '/' + tmdata['regnum'] + '.'+ tmdata['imgtype'].lower()
    else: tmdata['imgurl']='' 
    print tmdata
    scraperwiki.sqlite.save(unique_keys=['regnum'], table_name='trademarks', data=tmdata)

    return octmdata

def grabOCTrademarks(ocid,ocdata):
    for tm in ocdata['data']:
        #play nice
        time.sleep(0.5)
        if tm['datum']['data_type']=='WipoTrademark':
            octmid=tm['datum']['id']
            if octmid not in trademarksDone:
                octmdata=getOCtmData(ocid,octmid)
                trademarksDone.append(octmid)
            else: print 'got it already'

for ocid in ocids:
    print 'company data',str(ocid)
    ocdata=getOCcompanyData(ocid)
    octmdata=grabOCTrademarks(ocid,ocdata)
import scraperwiki,simplejson,urllib

import time

#opencorporates company id
ocids=['gb/00041424','gb/00102498','gb/00519500'] 

target='virgin'
rurl='http://opencorporates.com/reconcile/gb?query='+urllib.quote(target)
#note - the opencorporates api also offers a search:  companies/search
entities=simplejson.load(urllib.urlopen(rurl))
ocids=[]
for entity in entities['result']:
    ocids.append(entity['id'].lstrip('/companies/'))

print ocids
#exit(-1)

trademarksDone=[]
q = 'octmid FROM "trademarks"'
try:
    tmp = scraperwiki.sqlite.select(q)
    for item in tmp:
        if item['octmid'] != None:
            trademarksDone.append(int(item['octmid']))
except: pass
print trademarksDone

#ocnames={}
#for ocid in ocids:
#    ocnurl=ocurl='http://api.opencorporates.com/companies/'+ocid
#    ocndata=simplejson.load(urllib.urlopen(ocnurl))
#    ocnames[ocid]=ocndata['company']['name']

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
except:
    ockey=''

def getOCcompanyData(ocid):
    ocurl='http://api.opencorporates.com/companies/'+ocid+'/data'+'?api_token='+ockey
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    return ocdata

def getOCtmData(ocid,octmid):
    octmurl='http://api.opencorporates.com/data/'+str(octmid)+'?api_token='+ockey
    data=simplejson.load(urllib.urlopen(octmurl))
    octmdata=data['datum']['attributes']
    print 'tm data',octmdata
    categories=[]
    for category in octmdata['goods_and_services_classifications']:
        if 'en' in octmdata['goods_and_services_classifications'][category]:
            categories.append(octmdata['goods_and_services_classifications'][category]['en']+'('+category+')')
    tmdata={}
    tmdata['ocid']=ocid
    tmdata['octmid']=octmid
    tmdata['ocname']=octmdata['holder_name']
    #tmdata['ocname']=ocnames[ocid]
    tmdata['categories']=" :: ".join(categories)
    tmdata['imgtype']=octmdata['mark_image_type']
    tmdata['marktext']=octmdata['mark_text']
    tmdata['repaddr']=octmdata['representative_address_lines']
    tmdata['repname']=octmdata['representative_name_lines']
    tmdata['regnum']=octmdata['international_registration_number']
    if tmdata['imgtype']=='JPG' or tmdata['imgtype']=='GIF':
        tmdata['imgurl']='http://www.wipo.int/romarin/images/' + tmdata['regnum'][0:2] +'/' + tmdata['regnum'][2:4] + '/' + tmdata['regnum'] + '.'+ tmdata['imgtype'].lower()
    else: tmdata['imgurl']='' 
    print tmdata
    scraperwiki.sqlite.save(unique_keys=['regnum'], table_name='trademarks', data=tmdata)

    return octmdata

def grabOCTrademarks(ocid,ocdata):
    for tm in ocdata['data']:
        #play nice
        time.sleep(0.5)
        if tm['datum']['data_type']=='WipoTrademark':
            octmid=tm['datum']['id']
            if octmid not in trademarksDone:
                octmdata=getOCtmData(ocid,octmid)
                trademarksDone.append(octmid)
            else: print 'got it already'

for ocid in ocids:
    print 'company data',str(ocid)
    ocdata=getOCcompanyData(ocid)
    octmdata=grabOCTrademarks(ocid,ocdata)
