import scraperwiki
import string
import requests
import lxml.html
import re
import itertools
import time

searchurl = 'http://www.dyraaudkenni.is/dyr_leita.jsp'
regex = re.compile(".*dyr_numer=(\d*)")


#scraperwiki.sqlite.execute("delete from dyr where dyrakyn='***villa***'")
#scraperwiki.sqlite.commit()
#exit()

alphabet = string.ascii_lowercase 
digits = string.digits
punctuation = string.punctuation
uppercase = string.ascii_uppercase
tento500 = []
for x in range(166,501):
    tento500.append(x)


searchlist = digits + punctuation +alphabet


builder=[]

def process(d):
    params = params = {
    'ormerki':'', 
    'eyrnamerki':'*'+ d +'*',
    'request':'GetFeature',
    'leita':'Leita',
    'leita':'1'
    }
    print params
    r = requests.post(searchurl,data=params)
    content = r.content
    root = lxml.html.fromstring(content)
    results = root.xpath('//table[@id="dyr_leita_tafla"]/tbody/tr')

    for r in results:
        record = {}
        record['detail_url'] = r[0][0].attrib['href']
        record['nafn'] =  r[0][0].text
        record['tegund'] =  r[1].text
        record['ar'] =  r[2].text
        record['litur'] =  r[3].text
        record['a_lifi'] =  r[4].text
        record['eyrnamerki'] =  r[5].text
        record['ormerki'] =  r[6].text
        record['eigandi'] =  r[7].text
        builder.append(record)

    scraperwiki.sqlite.save(table_name='dyr', data=builder, unique_keys=['eyrnamerki'],verbose=1)



def generator(choices, length):
    for a in choices:
        if length > 1:
            for g in generator(choices, length-1):
                yield a + g
        else:
            yield a


#print punctuation
two = []
for a in generator(alphabet, 2):
     two.append( a)

#for d in two:
#    print 'processing: ', d
#    process( str(d) )

donenumbers = scraperwiki.sqlite.select("id from dyr")

#donenumbers=[]
#for d in done:
    #print d['detail_url']
#    donenumbers.append(regex.findall(d['detail_url'])[0])

allnumbers = range(1,45683)

print 'donenumbers: ', len(donenumbers)
print 'allnumbers original: ', len(allnumbers)
print


for x in donenumbers:
    try:
        allnumbers.remove(int(x['id']))
    except:
        pass

print 'allnumbers left: ', len(allnumbers)

builder = []
counter = 0
for m in allnumbers:
     
    url = 'http://www.dyraaudkenni.is/'
    url2 = 'dyr_nanar.jsp?dyr_numer='+str(m)
    url3 = url + url2
    r = requests.get(url3)
    xpath = '//td[1]/div/div[1]/div'
    content = r.content
    root = lxml.html.fromstring(content)
    results = root.xpath(xpath)
    record = {}
    record['id'] = m
    #record['detail_url'] = url2
    try:
        record['nafn'] =  results[1][0].tail
    except Exception, error:
        record['nafn'] =  error
    try:
        record['tegund'] =  results[2][0].tail
    except Exception, error:
        record['tegund'] =  error
    try:
        record['dyrakyn'] =  results[3][0].tail
    except Exception, error:
        record['dyrakyn'] =  error
    try:
        record['ar'] =  results[4][0].tail
    except Exception, error:
        record['ar'] =  error
    try:
        record['kyn'] =  results[5][0].tail
    except Exception, error:
        record['kyn'] =  error
    try:
        record['gelt'] =  results[6][0].tail
    except Exception, error:
        record['gelt'] =  error
    try:
        record['litur'] =  results[8][0].tail
    except Exception, error:
        record['litur'] =  error
    try:
        record['a_lifi'] = results[7][0].tail
    except Exception, error:
        record['a_lifi'] =  error
    try:
        record['eyrnamerki'] =  results[10][0].tail
    except Exception, error:
        record['eyrnamerki'] =  error
    try:
        record['feldur'] =  results[9][0].tail.strip()
    except Exception, error:
        record['feldur'] =  error

    builder.append( record )
    counter = counter +1
    if counter % 100 == 0:
        scraperwiki.sqlite.save(table_name='dyr', data=builder, unique_keys=['id'],verbose=1)
        builder = []
        print 'Saved!'
        time.sleep(5)

import scraperwiki
import string
import requests
import lxml.html
import re
import itertools
import time

searchurl = 'http://www.dyraaudkenni.is/dyr_leita.jsp'
regex = re.compile(".*dyr_numer=(\d*)")


#scraperwiki.sqlite.execute("delete from dyr where dyrakyn='***villa***'")
#scraperwiki.sqlite.commit()
#exit()

alphabet = string.ascii_lowercase 
digits = string.digits
punctuation = string.punctuation
uppercase = string.ascii_uppercase
tento500 = []
for x in range(166,501):
    tento500.append(x)


searchlist = digits + punctuation +alphabet


builder=[]

def process(d):
    params = params = {
    'ormerki':'', 
    'eyrnamerki':'*'+ d +'*',
    'request':'GetFeature',
    'leita':'Leita',
    'leita':'1'
    }
    print params
    r = requests.post(searchurl,data=params)
    content = r.content
    root = lxml.html.fromstring(content)
    results = root.xpath('//table[@id="dyr_leita_tafla"]/tbody/tr')

    for r in results:
        record = {}
        record['detail_url'] = r[0][0].attrib['href']
        record['nafn'] =  r[0][0].text
        record['tegund'] =  r[1].text
        record['ar'] =  r[2].text
        record['litur'] =  r[3].text
        record['a_lifi'] =  r[4].text
        record['eyrnamerki'] =  r[5].text
        record['ormerki'] =  r[6].text
        record['eigandi'] =  r[7].text
        builder.append(record)

    scraperwiki.sqlite.save(table_name='dyr', data=builder, unique_keys=['eyrnamerki'],verbose=1)



def generator(choices, length):
    for a in choices:
        if length > 1:
            for g in generator(choices, length-1):
                yield a + g
        else:
            yield a


#print punctuation
two = []
for a in generator(alphabet, 2):
     two.append( a)

#for d in two:
#    print 'processing: ', d
#    process( str(d) )

donenumbers = scraperwiki.sqlite.select("id from dyr")

#donenumbers=[]
#for d in done:
    #print d['detail_url']
#    donenumbers.append(regex.findall(d['detail_url'])[0])

allnumbers = range(1,45683)

print 'donenumbers: ', len(donenumbers)
print 'allnumbers original: ', len(allnumbers)
print


for x in donenumbers:
    try:
        allnumbers.remove(int(x['id']))
    except:
        pass

print 'allnumbers left: ', len(allnumbers)

builder = []
counter = 0
for m in allnumbers:
     
    url = 'http://www.dyraaudkenni.is/'
    url2 = 'dyr_nanar.jsp?dyr_numer='+str(m)
    url3 = url + url2
    r = requests.get(url3)
    xpath = '//td[1]/div/div[1]/div'
    content = r.content
    root = lxml.html.fromstring(content)
    results = root.xpath(xpath)
    record = {}
    record['id'] = m
    #record['detail_url'] = url2
    try:
        record['nafn'] =  results[1][0].tail
    except Exception, error:
        record['nafn'] =  error
    try:
        record['tegund'] =  results[2][0].tail
    except Exception, error:
        record['tegund'] =  error
    try:
        record['dyrakyn'] =  results[3][0].tail
    except Exception, error:
        record['dyrakyn'] =  error
    try:
        record['ar'] =  results[4][0].tail
    except Exception, error:
        record['ar'] =  error
    try:
        record['kyn'] =  results[5][0].tail
    except Exception, error:
        record['kyn'] =  error
    try:
        record['gelt'] =  results[6][0].tail
    except Exception, error:
        record['gelt'] =  error
    try:
        record['litur'] =  results[8][0].tail
    except Exception, error:
        record['litur'] =  error
    try:
        record['a_lifi'] = results[7][0].tail
    except Exception, error:
        record['a_lifi'] =  error
    try:
        record['eyrnamerki'] =  results[10][0].tail
    except Exception, error:
        record['eyrnamerki'] =  error
    try:
        record['feldur'] =  results[9][0].tail.strip()
    except Exception, error:
        record['feldur'] =  error

    builder.append( record )
    counter = counter +1
    if counter % 100 == 0:
        scraperwiki.sqlite.save(table_name='dyr', data=builder, unique_keys=['id'],verbose=1)
        builder = []
        print 'Saved!'
        time.sleep(5)

