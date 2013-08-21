import scraperwiki,simplejson,urllib,time

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    ockey=qsenv["OCKEY"]
    ykey=qsenv["YKEY"]
except:
    ockey=''




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


def getOCcompanyDetails(ocid):
    ocurl='http://api.opencorporates.com'+ocid+'?api_token='+ockey
    ocdata=simplejson.load(urllib.urlopen(ocurl))
    return ocdata

def logCompanyDetails(ocid,ocdata):
    cdata={'ocid':ocid}
    cdata['name']=ocdata['company']['name']
    cdata['address']=ocdata['company']['registered_address_in_full']
    print cdata,ocdata
    scraperwiki.sqlite.save(unique_keys=['ocid'], table_name='companydetails_'+ttarget, data=cdata)

def logOpenlyLocalData(ocid,oldata):
    cdata={'ocid':ocid}
    cdata['name']=oldata['company']['title']
    for supplyto in oldata['company']['supplying_relationships']:
        cdata['supplytoName']=supplyto['organisation']['name']
        cdata['olurl']=supplyto['organisation']['openlylocal_url']
        scraperwiki.sqlite.save(unique_keys=['olurl'], table_name='supplierdetails_'+ttarget, data=cdata)
'''
    cdata['address']=ocdata['company']['registered_address_in_full']
    print cdata,ocdata
    scraperwiki.sqlite.save(unique_keys=['ocid'], table_name='supplierdetails_'+ttarget, data=cdata)
'''

def getOpenlyLocalData(ocid):
    #http://openlylocal.com/companies/gb/01485809?format=xml
    print 'getting openlylocal data'
    olUrl='http://openlylocal.com'+ocid+'?format=json'
    try: oldata=simplejson.load(urllib.urlopen(olUrl))
    except: return None
    return oldata

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
            oldata=getOpenlyLocalData(ocid)
            if oldata!=None: logOpenlyLocalData(ocid,oldata)
            #if ocid not in directors:
            #    print 'getting directors', ocid
            #    filings=getOCfilingData(ocid)
            #    logDirectors(ocname,ocid,filings)
        else: print 'got it already'
        cci=cci+1

def ocOnOL(target=''):
    if target=='': exit(-1)
    ttarget=target.replace(' ','')
    rurl='http://opencorporates.com/reconcile/gb?query='+urllib.quote(target)
    #note - the opencorporates api also offers a search:  companies/search
    entities=simplejson.load(urllib.urlopen(rurl))

    companies=[]
    companyProcessor()
#ocOnOL('g4s')



#----UTILITY

#from: kljensen https://gist.github.com/742164
"""
fingerprint_cluster.py
Based on http://code.google.com/p/google-refine/wiki/ClusteringInDepth
Created by Kyle Jensen on 2010-12-15.
"""

#ah add
#stopwords
stoppers=set(['counc','ccl','council'])

import re
NONALPHANUMSPACE_re = re.compile(r'[^\w\s]', re.I|re.UNICODE)

latin_to_uni = {
    'a' : (u'\u00C0',u'\u00C1',u'\u00C2',u'\u00C3',u'\u00C4',u'\u00C5',u'\u00E0',u'\u00E1',u'\u00E2',
        u'\u00E3',u'\u00E4',u'\u00E5',u'\u0100',u'\u0101',u'\u0102',u'\u0103',u'\u0104',u'\u0105',),
    'c' : (u'\u00C7',u'\u00E7',u'\u0106',u'\u0107',u'\u0108',u'\u0109',u'\u010A',u'\u010B',
    u'\u010C',u'\u010D',),
    'd' : (u'\u00D0',u'\u00F0',u'\u010E',u'\u010F',u'\u0110',u'\u0111',),
    'e' : (u'\u00C8',u'\u00C9',u'\u00CA',u'\u00CB',u'\u00E8',u'\u00E9',u'\u00EA',u'\u00EB',
     u'\u0112',u'\u0113',u'\u0114',u'\u0115',u'\u0116',u'\u0117',u'\u0118',u'\u0119',u'\u011A',
     u'\u011B',),
    'g' : (u'\u011C',u'\u011D',u'\u011E',u'\u011F',u'\u0120',u'\u0121',u'\u0122',u'\u0123',),
    'h' : (u'\u0124',u'\u0125',u'\u0126',u'\u0127',),
    'i' : (u'\u00CC',u'\u00CD',u'\u00CE',u'\u00CF',u'\u00EC',u'\u00ED',u'\u00EE',u'\u00EF',
     u'\u0128',u'\u0129',u'\u012A',u'\u012B',u'\u012C',u'\u012D',u'\u012E',u'\u012F',u'\u0130',
     u'\u0131',),
    'j' : (u'\u0134',u'\u0135',),
    'k' : (u'\u0136',u'\u0137',u'\u0138',),
    'l' : (u'\u0139',u'\u013A',u'\u013B',u'\u013C',u'\u013D',u'\u013E',u'\u013F',u'\u0140',
     u'\u0141',u'\u0142',),
    'n' : (u'\u00D1',u'\u00F1',u'\u0143',u'\u0144',u'\u0145',u'\u0146',u'\u0147',u'\u0148',
     u'\u0149',u'\u014A',u'\u014B',),
    'o' : (u'\u00D2',u'\u00D3',u'\u00D4',u'\u00D5',u'\u00D6',u'\u00D8',u'\u00F2',u'\u00F3',
     u'\u00F4',u'\u00F5',u'\u00F6',u'\u00F8',u'\u014C',u'\u014D',u'\u014E',u'\u014F',u'\u0150',
     u'\u0151',),
    'r' : (u'\u0154',u'\u0155',u'\u0156',u'\u0157',u'\u0158',u'\u0159',),
    's' : (u'\u015A',u'\u015B',u'\u015C',u'\u015D',u'\u015E',u'\u015F',u'\u0160',u'\u0161',
     u'\u017F',),
    't' : (u'\u0162',u'\u0163',u'\u0164',u'\u0165',u'\u0166',u'\u0167',),
    'u' : (u'\u00D9',u'\u00DA',u'\u00DB',u'\u00DC',u'\u00F9',u'\u00FA',u'\u00FB',u'\u00FC',
     u'\u0168',u'\u0169',u'\u016A',u'\u016B',u'\u016C',u'\u016D',u'\u016E',u'\u016F',u'\u0170',
     u'\u0171',u'\u0172',u'\u0173',),
    'w' : (u'\u0174',u'\u0175',),
    'u' : (u'\u00DD',u'\u00FD',u'\u00FF',u'\u0176',u'\u0177',u'\u0178',),
    'z' : (u'\u0179',u'\u017A',u'\u017B',u'\u017C',u'\u017D',u'\u017E',),
}

uni_to_latin = dict([(u,l) for l,d in latin_to_uni.iteritems() for u in d])
def latinize(x):
    """Try to find the best latin character for any unicode characters in a string"""
    return ''.join(uni_to_latin.get(y,y) for y in x)

def fingerprint(s):
    """ The fingerprint fron Google Refine
        http://code.google.com/p/google-refine/wiki/ClusteringInDepth
    """
    f = s.strip()
    f = f.lower()
    f = NONALPHANUMSPACE_re.sub('', f)
    fs=set(f.split())
    fsd=fs.difference(stoppers)
    #fsd=f
    f = u' '.join(sorted(latinize(x) for x in fsd))
    return f

'''
def main():
    examples = [
        u'Comment ça va ? Très bien',
        u'woot hey Kyle JenseN ' + u'\u0179dd'
    ]
    for ex in examples:
        print(fingerprint(ex))


if __name__ == '__main__':
    main()
'''
#______

import lxml.html

def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass


def flatten(el):
    if el != None:
        result = [ (el.text or "") ]
        for sel in el:
            result.append(flatten(sel))
            result.append(sel.tail or "")
        return "".join(result)
    return ''


def olParsePage(oldata):
    for item in oldata['suppliers']:
        print item
        scraperwiki.sqlite.save(unique_keys=[], table_name='companyspend_'+typ.replace(' ',''), data=item)
        scraperwiki.sqlite.save(unique_keys=[], table_name='publicMesh', data=item)
    '''
    cdata={'ocid':ocid}
    cdata['name']=oldata['company']['title']
    for supplyto in oldata['company']['supplying_relationships']:
        cdata['supplytoName']=supplyto['organisation']['name']
        cdata['olurl']=supplyto['organisation']['openlylocal_url']
        scraperwiki.sqlite.save(unique_keys=['olurl'], table_name='supplierdetails_'+ttarget, data=cdata)
    '''
def ascii(s): return "".join(i for i in s if ord(i)<128)

#dropper('publicMesh')
def olSearchPage(searchterm,pagenum=1,scraper='html'):
    if scraper=='json':
        url='http://openlylocal.com/suppliers.json?name_filter=&page='+str(pagenum)
        data=simplejson.load(urllib.urlopen(url))
        print data
        return data
    else:
        data={'suppliers':[]}
        url='http://openlylocal.com/suppliers?name_filter='+urllib.quote(searchterm)+'&page='+str(pagenum)
        html = scraperwiki.scrape(url)
        print html
        root = lxml.html.fromstring(html)
        table=root.find('.//table')
        rows = table.findall('./tr')

        headers=rows[0].findall('./th')
        
        for row in rows[1:]:
            dataitem={}
            cells=row.findall('./td')
            #print flatten(headers[0]),flatten(cells[0])
            #print flatten(headers[1]),flatten(cells[1])
            #print flatten(headers[2]),flatten(cells[2])
            dataitem['supplier']=flatten(cells[0])
            r=re.match(r"(.*)\s*\(.*$",dataitem['supplier'])
            dataitem['supplier']=r.group(1)
            dataitem['normsupplier']=fingerprint(dataitem['supplier'])
            dataitem['supplyingTo']=flatten(cells[1])
            dataitem['payer']=cells[1].find('./a').get('href')
            dataitem['supplierURL']=cells[0].find('./strong/a').get('href')
            r=re.match(r"/suppliers/[0-9]*-(.*)$",dataitem['supplierURL'])
            dataitem['supplierSlug']=r.group(1)
            dataitem['supplierDetailsURL']=cells[0].find('./a').get('href')
            if dataitem['supplierDetailsURL'].startswith('/user_sub'):  dataitem['supplierDetailsURL']=''
            dataitem['normsupplyingTo']=fingerprint(dataitem['supplyingTo'])
            dataitem['total']=float(ascii(flatten(cells[2])).replace(',',''))
            data['suppliers'].append(dataitem)
        return data

def olSearchPages(searchterm):
    page=1
    data=olSearchPage(searchterm)
    olParsePage(data)
    while len(data['suppliers'])>0 and page<51:
        page=page+1
        data=olSearchPage(searchterm,page)
        olParsePage(data)
'''
typs=['town', 'district', 'county', 'borough']
for typ in typs:
    olSearchPages(typ+' council')
#town, district, county, borough - parish gives too many hits (1500 max returnable?)
'''

target='atos'
typ=target
dropper('companyspend_'+target)
olSearchPages(target)


#dropper('publicMesh_'+typ)
#olSearchPages(typ)



'''<table class="statistics" id="payer_breakdown">
<caption>Payer breakdown</caption>
<tr><th class="description">Payed By</th><th class="value">Total Spend</th><th class="value">Average Monthly Spend</th></tr>
<tr class="element" style="display:none"><td class="description"><a href="/suppliers/161244-serco-solutions-ltd" class="supplier_link">Coventry City Council (SERCO SOLUTIONS LTD)</a></td><td class="value">&pound;4,284,259</td><td class="value">&pound;535,532</td></tr>
<tr class="subtotal"><td class="description">Coventry City Council <span class='description' style='display:none'>subtotal</span></td><td class="value">&pound;4,284,259</td><td class="value">&pound;535,532</td></tr>
<tr class="element" style="display:none"><td class="description"><a href="/suppliers/167051-serco-solutions-limited" class="supplier_link">Oxfordshire County Council (Serco Solutions Limited)</a></td><td class="value">&pound;7,185</td><td class="value">&pound;3,592</td></tr>
<tr class="subtotal"><td class="description">Oxfordshire County Council <span class='description' style='display:none'>subtotal</span></td><td class="value">&pound;7,185</td><td class="value">&pound;3,592</td></tr></table>
'''
def getSpendWithCompany(target,suppID,name,payer,suppTo):
    url='http://openlylocal.com'+suppID+'.json'
    oldata=simplejson.load(urllib.urlopen(url))
    suppname=oldata['supplier']['name']
    for item in oldata['supplier']['financial_transactions']:
        dataitem={'cname':name,'suppID':suppID,'suppname':suppname,'suppTo':suppTo,'payr':payer}
        dataitem['department_name']=item['department_name']
        dataitem['description']=item['description']
        dataitem['value']=item['value']
        dataitem['service']=item['service']
        #print dataitem
        scraperwiki.sqlite.save(unique_keys=[], table_name='coSpend_'+target, data=dataitem)

#target='police'
dropper('coSpend_'+target)

supplierdata=scraperwiki.sqlite.select("* from companyspend_"+target)
print supplierdata
councils=[]
done=[]
#getSpendWithCompany(target,'/suppliers/280805-the-open-university',"Open University")
for item in supplierdata:
    if item['supplierURL'] not in done: done.append(item['supplierURL'])
    else:continue
    getSpendWithCompany(target,item['supplierURL'],item['supplier'],item['payer'],item['supplyingTo'])
