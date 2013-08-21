# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson
import demjson
# Blank Python


def get_xpath_el_text(obj, xpath, i=0, def_val='',attrib=''):
    el=obj.xpath(xpath)
    if el!=[]:
        return el[i].text_content()
    else:
        return def_val

    

def get_regions():
    id=1
    #scraperwiki.sqlite.execute('delete from regions')
    json_raw=scraperwiki.scrape("http://www.express-bank.ru/cities.json")
    json_data=simplejson.loads(json_raw)
    for e in json_data:
        okrug=json_data[e]['name']
        data=[]
        print okrug
        for o in json_data[e]['regions']:
            oblasty=json_data[e]['regions'][o]['name']
            print oblasty
            for c in json_data[e]['regions'][o]['cities']:
                
                try:
                    c=json_data[e]['regions'][o]['cities'][c]
                except TypeError:
                    pass

                city=c['name']
                url=c['synonym']

                data.append({'id':id,'okrug':okrug, 'oblasty':oblasty, 'city':city, 'city_url': url})
                id+=1
        print data
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='regions')




def get_branch_data(url=''):
    html=scraperwiki.scrape(url)
    r=lxml.html.document_fromstring(html)

    title=get_xpath_el_text(r,"//h1[@id='title']")
    address=get_xpath_el_text(r, "//div[@class='field field-type-text field-field-address']/div/div")
    address_junk=get_xpath_el_text(r, "//div[@class='field field-type-text field-field-address']")
    latlon = re.findall(r"showYaMap\(([\d\.]+?),\s*?([\d\.]+?),\s*?'(.+?)'",html, re.I|re.U)

    
    if latlon != []: 
        lat = latlon[0][0]
        lon = latlon[0][1]
        address2=latlon[0][2]
    else:
        lat = ''
        lon = ''
        address2=''

    return {'lat':lat,'lon':lon, 'branch_name':title, 'address': address, 'address_js':address2, 'address_junk':address_junk }


# get HTML code of the page

i=1
regions=scraperwiki.sqlite.select("* from regions")
start=0
for r in regions:
    if start==0:
        if r['city']==u'Промышленная' and r['oblasty']==u'Кемеровская область':
            start=1
            i=369
        else:
            continue

    city_url="http://www.express-bank.ru/" + r['city_url'].encode('utf-8')+"/offices"
    html = scraperwiki.scrape(city_url)
    root=lxml.html.document_fromstring(html)

    #IF there is no branch found, skip to next region/city
    #if len(addresses) ==0: continue
    data=[]
    for a in root.xpath("//div[@class='view-content']/table/tbody/tr/td[@class='views-field views-field-field-address-value']/a"):
        branch_url=a.attrib['href']
        branch_address=a.text_content()

        bdata=get_branch_data("http://www.express-bank.ru" + branch_url)

        data.append({'id':i, 'url': city_url , 'region': r['oblasty'], 
                'city': r['city'], 
                'okrug':r['okrug'], 
                'branch_url': "http://www.express-bank.ru" + branch_url,
                'title':bdata['branch_name'],
                'address1': bdata['address'],
                'address_js': bdata['address_js'],
                'address_junk': bdata['address_junk'],
                 'lat':bdata['lat'],
                'lon':bdata['lon']})
        i+=1

    scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="branch_data")
    #exit()



