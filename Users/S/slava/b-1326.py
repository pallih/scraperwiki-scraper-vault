# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson
import demjson
# Blank Python

#
#urls = """http://www.alfabank.ru/russia/moscow/"""
urls = """/arhangelsk/
/astrakhan/
/barnaul/
/biysk/
/belgorod/
/vladivostok/
/nakhodka/
/vladimir/
/volgograd/
/volzhsky/
/vologda/
/voronezh/
/ekaterinburg/
/kamensk-uralsky/
/nizhny_tagil/
/pervouralsk/
/ivanovo/
/izhevsk/
/glazov/
/irkutsk/
/angarsk/
/usolye-sibirskoe/
/kazan/
/almetyevsk/
/nabchelny/
/kaliningrad/
/kaluga/
/kemerovo/
/novokuznetsk/
/yurga/
/krasnodar/
/novorossiisk/
/sochi/
/tuapse/
/krasnoyarsk/
/abakan/
/zheleznogorsk/
/kurgan/
/kursk/
/lipetsk/
/moscow/
/balashiha/
/korolev/
/odintsovo/
/khimki/
/murmansk/
/nizhnevartovsk/
/megion/
/raduzhniy/
/surgut/
/nizhninovgorod/
/novosibirsk/
/omsk/
/orenburg/
/buzuluk/
/novotroitsk/
/orsk/
/penza/
/perm/
/rostov/
/ryazan/
/samara/
/tolyatti/
/peterburg/
/saratov/
/stavropol/
/syktyvkar/
/tambov/
/tomsk/
/tula/
/tyumen/
/new_urengoy/
/ulyanovsk/
/ufa/
/sterlitamak/
/khabarovsk/
/komsomolsk_na_amure/
/yakutsk/
/cheboksary/
/chelyabinsk/
/magnitogorsk/
/yuzhnosakhalinsk/
/yaroslavl/"""


branches_re = re.compile("""pointsList = {(.+?)\};""", re.I | re.U | re.S)


def fix_json(text):
    text = text.replace("\n","").replace("\t","").replace("  "," ")
    text = re.sub("'(\d+)': {", r' "\1":{', text, 0,  re.I | re.U | re.S)
    text = re.sub("\s*(\w+)\s*:", r"'\1':", text, 0,  re.I | re.U | re.S)
    #text = re.sub(":\s*'(.+?)'\s*(,|})\s*", r': "\1"\2', text,0,  re.I | re.U | re.S)
    return text

def get_field(regexp, text):
    r = re.findall(regexp,text)
    if len(r)>0:
        r = r[0]
    else:
        r = ''
    return r

def get_branch_data(html=''):
    city_name = get_field(r'docTitle">Отделения города (.+?)<',html)
    branch_name = get_field(r'branch-title".*?>(.+?)<',html)
    address = get_field(r'ratingAddress".*?>(.+?)<',html)

    if address == "":
        address = get_field(r'plhAddress".*?>(.+?)<',html)

    lat = get_field(r"iLat\s*=\s*'(.+?)'",html)
    lon = get_field(r"iLon\s*=\s*'(.+?)'",html)
    return {'lat':lat,'lon':lon, 'city_name':city_name, 'branch_name':branch_name , 'address': address }


i=0
for url1 in urls.split("\n"):

    url1 = "http://www.alfabank.ru/russia" + url1
    try:   
        html = scraperwiki.scrape(url1)
    except Exception, e:
        print "URL: " + url1
        print e
        continue

    html = html.decode('WINDOWS-1251').encode('utf-8')

    data = {'url': '', 'id':-1, 'lat':'','lon':'', 'city':'', 'branch_url': '', 'branch_name':'' , 'address':'', 'address2': '' }

    branches = branches_re.findall(html);
    if len(branches)>0:
        obj = demjson.decode("{" + branches[0] + "}");
    
        for d in obj:
            html1 = scraperwiki.scrape("http://www.alfabank.ru"+obj[d]['href']).decode('WINDOWS-1251').encode('utf-8')
            data = get_branch_data(html1 )
            i+=1
            data = {'url': url1, 'id':i, 'lat':obj[d]['lat'],'lon':obj[d]['lon'], 'city':data['city_name'], \
                    'branch_url': "http://www.alfabank.ru"+ obj[d]['href'], 'branch_name':obj[d]['title'] , \
                    'address':obj[d]['address'], 'address2': data['address'] }
            #print data
            scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")
    else:
        data = get_branch_data(html)
        i+=1
        data = {'url': url1, 'id':i, 'lat':data['lat'], 'lon':data['lon'], 'city':data['city_name'], \
                'branch_url': url1, 'branch_name': data['branch_name'] , 'address':data['address'], 'address2':'' }
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")


# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson
import demjson
# Blank Python

#
#urls = """http://www.alfabank.ru/russia/moscow/"""
urls = """/arhangelsk/
/astrakhan/
/barnaul/
/biysk/
/belgorod/
/vladivostok/
/nakhodka/
/vladimir/
/volgograd/
/volzhsky/
/vologda/
/voronezh/
/ekaterinburg/
/kamensk-uralsky/
/nizhny_tagil/
/pervouralsk/
/ivanovo/
/izhevsk/
/glazov/
/irkutsk/
/angarsk/
/usolye-sibirskoe/
/kazan/
/almetyevsk/
/nabchelny/
/kaliningrad/
/kaluga/
/kemerovo/
/novokuznetsk/
/yurga/
/krasnodar/
/novorossiisk/
/sochi/
/tuapse/
/krasnoyarsk/
/abakan/
/zheleznogorsk/
/kurgan/
/kursk/
/lipetsk/
/moscow/
/balashiha/
/korolev/
/odintsovo/
/khimki/
/murmansk/
/nizhnevartovsk/
/megion/
/raduzhniy/
/surgut/
/nizhninovgorod/
/novosibirsk/
/omsk/
/orenburg/
/buzuluk/
/novotroitsk/
/orsk/
/penza/
/perm/
/rostov/
/ryazan/
/samara/
/tolyatti/
/peterburg/
/saratov/
/stavropol/
/syktyvkar/
/tambov/
/tomsk/
/tula/
/tyumen/
/new_urengoy/
/ulyanovsk/
/ufa/
/sterlitamak/
/khabarovsk/
/komsomolsk_na_amure/
/yakutsk/
/cheboksary/
/chelyabinsk/
/magnitogorsk/
/yuzhnosakhalinsk/
/yaroslavl/"""


branches_re = re.compile("""pointsList = {(.+?)\};""", re.I | re.U | re.S)


def fix_json(text):
    text = text.replace("\n","").replace("\t","").replace("  "," ")
    text = re.sub("'(\d+)': {", r' "\1":{', text, 0,  re.I | re.U | re.S)
    text = re.sub("\s*(\w+)\s*:", r"'\1':", text, 0,  re.I | re.U | re.S)
    #text = re.sub(":\s*'(.+?)'\s*(,|})\s*", r': "\1"\2', text,0,  re.I | re.U | re.S)
    return text

def get_field(regexp, text):
    r = re.findall(regexp,text)
    if len(r)>0:
        r = r[0]
    else:
        r = ''
    return r

def get_branch_data(html=''):
    city_name = get_field(r'docTitle">Отделения города (.+?)<',html)
    branch_name = get_field(r'branch-title".*?>(.+?)<',html)
    address = get_field(r'ratingAddress".*?>(.+?)<',html)

    if address == "":
        address = get_field(r'plhAddress".*?>(.+?)<',html)

    lat = get_field(r"iLat\s*=\s*'(.+?)'",html)
    lon = get_field(r"iLon\s*=\s*'(.+?)'",html)
    return {'lat':lat,'lon':lon, 'city_name':city_name, 'branch_name':branch_name , 'address': address }


i=0
for url1 in urls.split("\n"):

    url1 = "http://www.alfabank.ru/russia" + url1
    try:   
        html = scraperwiki.scrape(url1)
    except Exception, e:
        print "URL: " + url1
        print e
        continue

    html = html.decode('WINDOWS-1251').encode('utf-8')

    data = {'url': '', 'id':-1, 'lat':'','lon':'', 'city':'', 'branch_url': '', 'branch_name':'' , 'address':'', 'address2': '' }

    branches = branches_re.findall(html);
    if len(branches)>0:
        obj = demjson.decode("{" + branches[0] + "}");
    
        for d in obj:
            html1 = scraperwiki.scrape("http://www.alfabank.ru"+obj[d]['href']).decode('WINDOWS-1251').encode('utf-8')
            data = get_branch_data(html1 )
            i+=1
            data = {'url': url1, 'id':i, 'lat':obj[d]['lat'],'lon':obj[d]['lon'], 'city':data['city_name'], \
                    'branch_url': "http://www.alfabank.ru"+ obj[d]['href'], 'branch_name':obj[d]['title'] , \
                    'address':obj[d]['address'], 'address2': data['address'] }
            #print data
            scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")
    else:
        data = get_branch_data(html)
        i+=1
        data = {'url': url1, 'id':i, 'lat':data['lat'], 'lon':data['lon'], 'city':data['city_name'], \
                'branch_url': url1, 'branch_name': data['branch_name'] , 'address':data['address'], 'address2':'' }
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")


