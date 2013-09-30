import scraperwiki,simplejson,urllib
import time

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
    ykey=qsenv["YKEY"]
except:
    ockey=''


def getOCcompanyData(ocid):
    ocurl='http://api.opencorporates.com/companies/'+ocid+'/data'+'?api_token='+ockey
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    return ocdata

def getOCtmData(ocid,octmid):
    octmurl='http://api.opencorporates.com/data/'+str(octmid)+'?api_token='+ockey
    data=simplejson.load(urllib.urlopen(octmurl))
    octmdata=data['results']['datum']['attributes']
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
    #if an image tradmarked, we can work out its URL on the WIPO site...
    print octmdata['mark_image_type']
    if tmdata['imgtype']=='JPG' or tmdata['imgtype']=='GIF':
        tmdata['imgurl']='http://www.wipo.int/romarin/images/' + tmdata['regnum'][0:2] +'/' + tmdata['regnum'][2:4] + '/' + tmdata['regnum'] + '.'+ tmdata['imgtype'].lower()
    else: tmdata['imgurl']='' 
    print tmdata
    scraperwiki.sqlite.save(unique_keys=['regnum'], table_name='trademarks', data=tmdata)
    time.sleep(1.5)
    return octmdata

def grabOCTrademarks(ocid,ocdata):
    for tm in ocdata['results']['data']:
        if tm['datum']['data_type']=='WipoTrademark':
            octmid=tm['datum']['id']
            if octmid not in cachetms:
                octmdata=getOCtmData(ocid,octmid)

scraperwiki.sqlite.attach('opencorporates_trawler')
q="* from opencorporates_trawler.`companies_sodexo2_2`"
data = scraperwiki.sqlite.select(q)

try:
    q='* from trademarks'
    cachedata= scraperwiki.sqlite.select(q)
except:cachedata=[]
cachetms=[]
for row in cachedata:
    cachetms.append(row['octmid'])

print data
for row in data:
    ocid=row['ocid']
    print ocid
    ocdata=getOCcompanyData(ocid)
    time.sleep(1.5)
    print ocdata
    octmdata=grabOCTrademarks(ocid,ocdata)

import scraperwiki,simplejson,urllib
import time

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
    ykey=qsenv["YKEY"]
except:
    ockey=''


def getOCcompanyData(ocid):
    ocurl='http://api.opencorporates.com/companies/'+ocid+'/data'+'?api_token='+ockey
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    return ocdata

def getOCtmData(ocid,octmid):
    octmurl='http://api.opencorporates.com/data/'+str(octmid)+'?api_token='+ockey
    data=simplejson.load(urllib.urlopen(octmurl))
    octmdata=data['results']['datum']['attributes']
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
    #if an image tradmarked, we can work out its URL on the WIPO site...
    print octmdata['mark_image_type']
    if tmdata['imgtype']=='JPG' or tmdata['imgtype']=='GIF':
        tmdata['imgurl']='http://www.wipo.int/romarin/images/' + tmdata['regnum'][0:2] +'/' + tmdata['regnum'][2:4] + '/' + tmdata['regnum'] + '.'+ tmdata['imgtype'].lower()
    else: tmdata['imgurl']='' 
    print tmdata
    scraperwiki.sqlite.save(unique_keys=['regnum'], table_name='trademarks', data=tmdata)
    time.sleep(1.5)
    return octmdata

def grabOCTrademarks(ocid,ocdata):
    for tm in ocdata['results']['data']:
        if tm['datum']['data_type']=='WipoTrademark':
            octmid=tm['datum']['id']
            if octmid not in cachetms:
                octmdata=getOCtmData(ocid,octmid)

scraperwiki.sqlite.attach('opencorporates_trawler')
q="* from opencorporates_trawler.`companies_sodexo2_2`"
data = scraperwiki.sqlite.select(q)

try:
    q='* from trademarks'
    cachedata= scraperwiki.sqlite.select(q)
except:cachedata=[]
cachetms=[]
for row in cachedata:
    cachetms.append(row['octmid'])

print data
for row in data:
    ocid=row['ocid']
    print ocid
    ocdata=getOCcompanyData(ocid)
    time.sleep(1.5)
    print ocdata
    octmdata=grabOCTrademarks(ocid,ocdata)

