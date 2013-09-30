import scraperwiki
import lxml.html
import re
import time

# Blank Python

scraperwiki.sqlite.execute('delete from data')
html=scraperwiki.scrape("http://abakan.homecredit.ru/offices.php")
root=lxml.html.document_fromstring(html)

def get_xpath_el_text(obj, xpath, i=0, def_val=''):
    el=obj.xpath(xpath)
    if el!=[]:
        return el[i].text_content()
    else:
        return def_val

def grab(url):
    try:
        html=scraperwiki.scrape(url)
    except:
        time.sleep(5)
        html=grab(url)
    return html


i=1
start=0
for u in root.xpath("//*[@id='office_city']/div[2]/select/option"):

    region_id=u.attrib['value']
    region_name=u.text_content()

    #if start==0:
    #    if int(region_id) == 436:
    #        start=1
    #    else:
    #        continue

    print region_name, region_id

    html=grab("http://kazan.homecredit.ru/offices.php?tid="+region_id)
    root=lxml.html.document_fromstring(html)

    for t in root.xpath("//div/div[@class='bankomat_item']/div/div/div/table"):

        title=get_xpath_el_text(t,"tr[1]/td[1]/b/span")
        title1=get_xpath_el_text(t,"tr[1]/td[1]/span")
        office_type=get_xpath_el_text(t,"tr[2]/td/div[1]/span[2]")
        address=get_xpath_el_text(t,"tr[2]/td/div[3]/div/span[3]")

        lat=get_xpath_el_text(t, "../div[@itemprop='geo']/span[@itemprop='latitude']")
        lon=get_xpath_el_text(t, "../div[@itemprop='geo']/span[@itemprop='longitude']")
        data={'id':i,
            'region_name':region_name,
            'region_id':region_id,
            'title':title,
            'title1':title1,
            'office_type': office_type,
            'address':address,
            'lat':lat, 'lon':lon}
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="data")
        i+=1
        

import scraperwiki
import lxml.html
import re
import time

# Blank Python

scraperwiki.sqlite.execute('delete from data')
html=scraperwiki.scrape("http://abakan.homecredit.ru/offices.php")
root=lxml.html.document_fromstring(html)

def get_xpath_el_text(obj, xpath, i=0, def_val=''):
    el=obj.xpath(xpath)
    if el!=[]:
        return el[i].text_content()
    else:
        return def_val

def grab(url):
    try:
        html=scraperwiki.scrape(url)
    except:
        time.sleep(5)
        html=grab(url)
    return html


i=1
start=0
for u in root.xpath("//*[@id='office_city']/div[2]/select/option"):

    region_id=u.attrib['value']
    region_name=u.text_content()

    #if start==0:
    #    if int(region_id) == 436:
    #        start=1
    #    else:
    #        continue

    print region_name, region_id

    html=grab("http://kazan.homecredit.ru/offices.php?tid="+region_id)
    root=lxml.html.document_fromstring(html)

    for t in root.xpath("//div/div[@class='bankomat_item']/div/div/div/table"):

        title=get_xpath_el_text(t,"tr[1]/td[1]/b/span")
        title1=get_xpath_el_text(t,"tr[1]/td[1]/span")
        office_type=get_xpath_el_text(t,"tr[2]/td/div[1]/span[2]")
        address=get_xpath_el_text(t,"tr[2]/td/div[3]/div/span[3]")

        lat=get_xpath_el_text(t, "../div[@itemprop='geo']/span[@itemprop='latitude']")
        lon=get_xpath_el_text(t, "../div[@itemprop='geo']/span[@itemprop='longitude']")
        data={'id':i,
            'region_name':region_name,
            'region_id':region_id,
            'title':title,
            'title1':title1,
            'office_type': office_type,
            'address':address,
            'lat':lat, 'lon':lon}
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="data")
        i+=1
        

