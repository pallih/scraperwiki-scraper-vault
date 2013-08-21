# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson
import demjson
import mechanize


html1 = scraperwiki.scrape("http://www.olb.ru//spoints/sp_detail/211462/")
html1 = html1.decode('windows-1251').encode('utf-8')

latlon = re.findall(r'new ymaps.Placemark\(\[([\d\.]+?),([\d\.]+?)\]\,\s*{balloonContent:\s*"(.+?)"}', html1, re.I|re.S|re.U)
offices= re.findall(r'<td class="name">(.+?)</td>.*?<td class="address">(.+?)</td', html1, re.I|re.S|re.U)
print latlon
print offices

exit()
# Blank Python

#init browser object
br = mechanize.Browser()

#GET HTML code of all regions
html = scraperwiki.scrape("http://www.olb.ru/bitrix/components/articul/geotar.define.new/data.php?MODE=AJAX&CACHE_TIME=15768000&REGIONS_IBLOCK_ID=44&STATES_IBLOCK_ID=45&CITIES_IBLOCK_ID=46&CACHE_ID_DATA=geotar.define.data.27094.27114.27116&REGION_ID=27094&CITY_ID=27116&STATE_ID=27114&CITY_VARIABLE_NAME=CITY_ID&STATE_VARIABLE_NAME=STATE_ID&REGION_VARIABLE_NAME=REGION_ID")

html = re.sub(r'\\"', '"', html, 0, re.I|re.U|re.S)
html = html.decode('windows-1251').encode('utf-8')

i=1
okrug_html = re.findall(r'class="city">.*?<a href="(.+?)">(.+?)</a', html, re.I|re.S|re.U)

#Iterate through Regions/Cities
for city in okrug_html:
    ids = re.findall(r'CITY_ID=(\d+?)&STATE_ID=(\d+?)&REGION_ID=(\d+?)$', city[0], re.I|re.S|re.U)
    ids = ids[0]

    region_name = re.findall(r'id="okrug'+ids[2]+'".*?okrug\-name">(.+?)</span', html, re.I|re.S|re.U)
    region_name = region_name[0] if len(region_name)>0 else ''

    state_name = re.findall(r'id="region'+ids[1]+'".*?<div>.*?<span>(.+?)</span', html, re.I|re.S|re.U)
    state_name = state_name[0] if len(state_name)>0 else ''


    #get regions
    try:
        br.open("http://www.olb.ru/spoints/" +  city[0] )
    except:
        pass

    response = br.open("http://www.olb.ru/spoints/")
    html1=response.read()
    html1 = html1.decode('windows-1251').encode('utf-8')

    latlon = re.findall(r'new ymaps.Placemark\(\[([\d\.]+?),([\d\.]+?)\]\,\s*{balloonContent:\s*"(.+?)"}', html1, re.I|re.S|re.U)
    offices= re.findall(r'<td class="name">(.+?)</td>.*?<td class="address">(.+?)</td', html1, re.I|re.S|re.U)

    # Get data of branches described in JS for yandex maps
    branch_data = []
    for l in latlon:
        branch_data.append(
            {'branch_name': l[2], \
             'lat': l[1], \
             'lon': l[0], \
             'branch_url': re.findall("href='(.+?)'", l[2])[0]})
        
    #Iterate through branches ( offices ) and add data to database, find the corresponding lat/lon if exists
    for office in offices:
        
        data = {'id':i, 'region': region_name, 'state_name': state_name, 'city_name': city[1], 'city_href':city[0], \
                'branch_name':'', 'branch_url':'', 'lat':'', 'lon':'', 'address':''}

        data['branch_name'] = office[0].strip(' \t\n\r')
        data['branch_url'] = re.findall(r'href="(.+?)"', data['branch_name'])[0]
        data['address'] = office[1].strip(' \t\n\r')

        for l in branch_data:
            if l['branch_url'] == data['branch_url']:
                data['lat'] = l['lat']
                data['lon'] = l['lon']
                break;

        #Save data to datastore
        i+=1
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")


