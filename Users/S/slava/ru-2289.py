import scraperwiki
import lxml.html
import simplejson
import re
# Blank Python

html = scraperwiki.scrape("http://www.rsb.ru/location/")
root = lxml.html.document_fromstring(html)
options = root.xpath("//select[@name='user_city_list']/option")
scraperwiki.sqlite.execute('delete from `data`')

i=1
for option in options:
    #print option

    if option.attrib['value'] != '' and option.attrib['value']!= '0':
        html = scraperwiki.scrape("http://www.rsb.ru/" + option.attrib['value'] + "/about/branch/")
        root = lxml.html.document_fromstring(html)
        coords = re.findall(r'items: \[(.+?)\]', html, re.I|re.U|re.S|re.M)
        #print html
        #print coords

        if coords !=[]:
            coords = coords[0].replace("id: ", " 'id': ") \
                .replace("longitude: ", " 'longitude': ") \
                .replace("latitude: ", " 'latitude': ") \
                .replace("zoom: ", " 'zoom': ") \
                .replace("filter: ", " 'filter': ")
            #print coords
            coords = coords.replace(', , ,', ',0,0,')
            items = eval('[' + coords + ']')
            

            #exit()
            #print branches
            for item in items:
                cols = root.xpath("//tr[@id='point_"+item['id']+"']/td")
                data = {'id':i, \
                        'city': option.text_content(), \
                        'city_id': option.attrib['value'], \
                        'name':'', \
                        'link':'', \
                        'address':'', \
                        'lat':item['latitude'], \
                        'lng':item['longitude'], \
                        'internal_id':item['id']}
                for c in cols:
                    if c.attrib['class'] == 'point_name':
                        d = c.xpath('a')
                        data['name'] = d[0].text_content()
                        data['link'] = d[0].attrib['href']
                    elif c.attrib['class'] == 'point_address':
                            d = c.xpath("span[@class='street']/span")
                            if d==[]: 
                                d = c.xpath("span[@class='street']")
                            data['address'] = d[0].text_content()

                #print data
                scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='data')
                i+=1
        #exit()

        
