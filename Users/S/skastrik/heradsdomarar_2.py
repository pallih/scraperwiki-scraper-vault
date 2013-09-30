import scraperwiki
import requests
import lxml.html
import datetime
import time
import base64
import re

url = 'http://domstolar.is/domaleit/?action=search'

domstolar = [{'name':'Reykjavík','id':'2'},{'name':'Reykjanes','id':'3'},{'name':'Suðurland','id':'4'},{'name':'Austurland','id':'5'},{'name':'Norðurland eystra','id':'6'},{'name':'Norðurland vestra','id':'7'},{'name':'Vestfirðir','id':'8'},{'name':'Vesturland','id':'9'}]


# 2 Reykjavík
# 3 Reykjanes
# 4 Suðurland
# 5 Austurland
# 6 Norðurland eystra
# 7 Norðurland vestra
# 8 Vestfirðir
# 9 Vesturland

def get_domstoll(domstoll):
    payload = {'Heradsdomar':domstoll,'B1':'Leita'}
    response = requests.post(url, data=payload)
    root = lxml.html.fromstring( response.text )
    domar = root.xpath('//div[@class="domadiv"]')
    print 'Fann ',len(domar), 'fyrir domstol nr. ', domstoll
    print 'Vista i _cache'
    scraperwiki.sqlite.save(table_name='__cache',data={'domstoll':domstoll,'payload':base64.b64encode(response.text.encode('iso-8859-1')),'date':datetime.datetime.now()},unique_keys=['domstoll'])
    #for dom in domar:
     #   print dom.text_content()

def process_domstoll(id,name):
    r=scraperwiki.sqlite.select("* from __cache where domstoll=?", id, verbose=0) # attempt grab from database.
    print r

    html =  base64.b64decode(r[0]['payload'])
    root = lxml.html.fromstring(html)
    batch = []
    domar = root.xpath('//div[@class="domadiv"]')
    print 'Fann ',len(domar), 'fyrir domstol ', name
    for dom in domar:
        record = {}
        record['date'] =  dom[0][0][0].text.strip()
        record['domur'] =  re.match('(.+\d+/\d+).*',dom[0][1].text.strip()).group(1)
        record['domstoll'] = name
        record['domari'] = dom[0][1][0].tail.strip()
        record['detail'] = dom[1].text_content()
        record['url'] = 'http://domstolar.is' + dom[2][0].attrib['href']
        record['domatexti'] = requests.get(record['url']).text
        batch.append(record)
    scraperwiki.sqlite.save(["domur","url","detail"],data=batch,table_name='allt')
    print ' Klaradi thetta '

for domstoll in domstolar:
    get_domstoll(domstoll['id'])

#print process_domstoll('2')

for domstoll in domstolar:
    #print domstoll['name'],domstoll['id']
    process_domstoll(domstoll['id'],domstoll['name'])
import scraperwiki
import requests
import lxml.html
import datetime
import time
import base64
import re

url = 'http://domstolar.is/domaleit/?action=search'

domstolar = [{'name':'Reykjavík','id':'2'},{'name':'Reykjanes','id':'3'},{'name':'Suðurland','id':'4'},{'name':'Austurland','id':'5'},{'name':'Norðurland eystra','id':'6'},{'name':'Norðurland vestra','id':'7'},{'name':'Vestfirðir','id':'8'},{'name':'Vesturland','id':'9'}]


# 2 Reykjavík
# 3 Reykjanes
# 4 Suðurland
# 5 Austurland
# 6 Norðurland eystra
# 7 Norðurland vestra
# 8 Vestfirðir
# 9 Vesturland

def get_domstoll(domstoll):
    payload = {'Heradsdomar':domstoll,'B1':'Leita'}
    response = requests.post(url, data=payload)
    root = lxml.html.fromstring( response.text )
    domar = root.xpath('//div[@class="domadiv"]')
    print 'Fann ',len(domar), 'fyrir domstol nr. ', domstoll
    print 'Vista i _cache'
    scraperwiki.sqlite.save(table_name='__cache',data={'domstoll':domstoll,'payload':base64.b64encode(response.text.encode('iso-8859-1')),'date':datetime.datetime.now()},unique_keys=['domstoll'])
    #for dom in domar:
     #   print dom.text_content()

def process_domstoll(id,name):
    r=scraperwiki.sqlite.select("* from __cache where domstoll=?", id, verbose=0) # attempt grab from database.
    print r

    html =  base64.b64decode(r[0]['payload'])
    root = lxml.html.fromstring(html)
    batch = []
    domar = root.xpath('//div[@class="domadiv"]')
    print 'Fann ',len(domar), 'fyrir domstol ', name
    for dom in domar:
        record = {}
        record['date'] =  dom[0][0][0].text.strip()
        record['domur'] =  re.match('(.+\d+/\d+).*',dom[0][1].text.strip()).group(1)
        record['domstoll'] = name
        record['domari'] = dom[0][1][0].tail.strip()
        record['detail'] = dom[1].text_content()
        record['url'] = 'http://domstolar.is' + dom[2][0].attrib['href']
        record['domatexti'] = requests.get(record['url']).text
        batch.append(record)
    scraperwiki.sqlite.save(["domur","url","detail"],data=batch,table_name='allt')
    print ' Klaradi thetta '

for domstoll in domstolar:
    get_domstoll(domstoll['id'])

#print process_domstoll('2')

for domstoll in domstolar:
    #print domstoll['name'],domstoll['id']
    process_domstoll(domstoll['id'],domstoll['name'])
