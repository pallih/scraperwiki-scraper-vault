import scraperwiki
import lxml.html
import json

csd = {'City of Cambridge': '/boundaries/census-subdivisions/3530010/',
       'City of Kitchener': '/boundaries/census-subdivisions/3530013/',
       'City of Waterloo': '/boundaries/census-subdivisions/3530016/',
       'Township of North Dumfries': '/boundaries/census-subdivisions/3530004/',
       'Township of Wellesley': '/boundaries/census-subdivisions/3530027/',
       'Township of Wilmot': '/boundaries/census-subdivisions/3530020/',
       'Township of Woolwich': '/boundaries/census-subdivisions/3530035/',
       'Regional Municipality of Waterloo': '/boundaries/census-divisions/3530/'}

source_url = 'http://www.regionofwaterloo.ca/en/regionalgovernment/regionalcouncil.asp'
html = scraperwiki.scrape(source_url)
root = lxml.html.fromstring(html)

muni = None

scraperwiki.sqlite.execute('delete from swdata')
scraperwiki.sqlite.commit()

for elem in root.cssselect("h3, a[title^='20'], h2"):

    if elem.tag == 'h3':
        muni = elem.text_content()
        if muni == 'Head of Regional Council':
            muni = 'Regional Municipality of Waterloo'
    elif elem.tag == 'h2':
        muni = None
    elif muni is not None:
        
        href = elem.get('href')
        name = elem.text_content()
        isMayor = ('Mayor' in elem.tail)
        
        page = scraperwiki.scrape(href)
        pageroot = lxml.html.fromstring(page)
        
        paras = pageroot.cssselect(".contactBody p")
        office = paras[0][0].tail
        if isMayor: 
            office = 'Mayor'
        phone = paras[1][0].tail.replace(': ', '')
        fax = paras[1][-1].tail.replace(': ', '')
        email = paras[2][2].get('href').replace('mailto:', '')
        postal = ' '.join([br.tail for br in paras[0][1:]])
        
        photo = pageroot.cssselect('img[src^="http://www.regionofwaterloo.ca/en/regionalGovernment/resources/"]')[0].get('src')
        
        data = {'name': name.strip(),
                'url': href,
                'photo_url': photo,
                'source_url': source_url,
                'district_name': muni,
                'elected_office': office,
                'offices': json.dumps([{'tel': phone, 'fax': fax, 'postal': postal}]),
                'email': email,
                'boundary_url': csd[muni]
               }
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
