# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson
import demjson
import HTMLParser

h = HTMLParser.HTMLParser()

# Blank Python
#
regions = [("Брестская область","http://belarusbank.by/ru/about/structure/search_filials/Brestskaya_oblast"),\
("Витебская область","http://belarusbank.by/ru/about/structure/search_filials/Vitebskaya_oblast"),\
("Гомельская область","http://belarusbank.by/ru/about/structure/search_filials/Gomelskaya_oblast"),\
("Гродненская область","http://belarusbank.by/ru/about/structure/search_filials/Grodnenskaya_oblast"),\
("Минск","http://belarusbank.by/ru/about/structure/search_filials/Minsk"),\
("Минская область","http://belarusbank.by/ru/about/structure/search_filials/Minskaya_oblast"),\
("Могилевская область","http://belarusbank.by/ru/about/structure/search_filials/Mogilevskaya_oblast")]
i=1
for region in regions:
    #print region
    region_name = region[0]
    rayon_html = scraperwiki.scrape(region[1])
    rayon_html = rayon_html.decode('windows-1251').encode('utf-8')
    #print rayon_html

    #content = re.findall(r'class="content">(.+?)</table', rayon_html, re.I|re.U|re.S)
    #print content
    columns = re.findall(r'<td>(.*?)<\/td', rayon_html, re.I|re.U|re.S)
    #print columns
    
    for col in columns:
        #print col
        #continue
        cities = re.findall(r'<a\s*?href="('+region[1]+'.+?)"\s*?>(.+?)<\/a>',col, re.I|re.U|re.S)
        if cities == []: continue
        for city in cities :
            html = scraperwiki.scrape(city[0])
            root = lxml.html.document_fromstring(html)
            branch_name = root.xpath("//table[@class='solid_table']/tr/td[2]")
            branch_address = root.xpath("//table[@class='solid_table']/tr/td[3]")
            branch_detail = root.xpath("//table[@class='solid_table']/tr/td[6]")
            
            #print branch_name , branch_address
            for j in range(len(branch_name)):
                branch_url = re.findall(r'href="(.*?)"',  lxml.etree.tostring(branch_detail[j]), re.I|re.U|re.S)
                
                address = re.findall(r'<td.*?>(.+?)</td',lxml.html.tostring(branch_address[j]), re.I|re.U|re.S)
                address = re.sub(r'\n|\r|\t','',address[0],0,re.I|re.U|re.S)

                data = {'id': i,
                        'branch_name': branch_name[j].text_content().strip(), 
                        'address': h.unescape(address), 
                        'detail_url' : branch_url[0], 
                        'region': region_name, 
                        'raion': city[1]}
                #print data
                
                scraperwiki.sqlite.save(unique_keys= ['id'], data=data, table_name='processed')
                i+=1
            #exit()

        


