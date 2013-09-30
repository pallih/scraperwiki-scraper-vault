import scraperwiki
import lxml.html

# Blank Python
user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"

#scraperwiki.sqlite.execute("delete from data")
html=scraperwiki.scrape("http://en.wikipedia.org/wiki/List_of_cities_in_Tunisia", None, user_agent )
html=html.replace("<html ", '<html xmlns="http://www.w3.org/1999/xhtml" ')
html=html.replace('<meta charset="UTF-8" />', '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
root=lxml.html.document_fromstring(html.decode('utf-8'))
print html
def get_dms(url):
    if url == "" or url == None: 
        return {'lat': '', 'lon': ''}

    try:
        html=scraperwiki.scrape("http://en.wikipedia.org" + url, None, user_agent)

    except:
        return {'lat': '', 'lon': ''}
        pass

    #html=html.replace("<html ", '<html xmlns="http://www.w3.org/1999/xhtml" ')
    html=html.replace('<meta charset="UTF-8" />', '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
    root=lxml.html.document_fromstring(html)
    dms = root.xpath("//span[@class='geo-dms']")
    if dms != []:
        dms = dms[0].xpath('span')
        return {'lat': dms[0].text_content(), 'lon': dms[1].text_content()}
    else:
        return {'lat': '', 'lon': ''}
    

lst = root.xpath("//div[@id='mw-content-text']/*[name()='h3' or name()='ul']")
i=1
for l in lst:
    
    if l.tag =='h3':
        guvernorate =l.xpath('span[2]/a')
        guvernorate_link = guvernorate[0].attrib['href']
        guvernorate = guvernorate[0].text_content()
    if l.tag == 'ul':
        ville = l.xpath('li/a')
        for v in ville:
            ville = v.text_content()
            ville_link = v.attrib['href']
            dms = get_dms(ville_link)
            data={ 'id': i, \
                'guvernorate': guvernorate, \
                'guvernorate_link': 'http://en.wikipedia.org' + guvernorate_link, \
                'ville': ville, \
                'ville_link': 'http://en.wikipedia.org' + ville_link, \
                'lat': dms['lat'], \
                'lon': dms['lon']}

            scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='data')
            #exit()
            i+=1
                
                


import scraperwiki
import lxml.html

# Blank Python
user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"

#scraperwiki.sqlite.execute("delete from data")
html=scraperwiki.scrape("http://en.wikipedia.org/wiki/List_of_cities_in_Tunisia", None, user_agent )
html=html.replace("<html ", '<html xmlns="http://www.w3.org/1999/xhtml" ')
html=html.replace('<meta charset="UTF-8" />', '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
root=lxml.html.document_fromstring(html.decode('utf-8'))
print html
def get_dms(url):
    if url == "" or url == None: 
        return {'lat': '', 'lon': ''}

    try:
        html=scraperwiki.scrape("http://en.wikipedia.org" + url, None, user_agent)

    except:
        return {'lat': '', 'lon': ''}
        pass

    #html=html.replace("<html ", '<html xmlns="http://www.w3.org/1999/xhtml" ')
    html=html.replace('<meta charset="UTF-8" />', '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
    root=lxml.html.document_fromstring(html)
    dms = root.xpath("//span[@class='geo-dms']")
    if dms != []:
        dms = dms[0].xpath('span')
        return {'lat': dms[0].text_content(), 'lon': dms[1].text_content()}
    else:
        return {'lat': '', 'lon': ''}
    

lst = root.xpath("//div[@id='mw-content-text']/*[name()='h3' or name()='ul']")
i=1
for l in lst:
    
    if l.tag =='h3':
        guvernorate =l.xpath('span[2]/a')
        guvernorate_link = guvernorate[0].attrib['href']
        guvernorate = guvernorate[0].text_content()
    if l.tag == 'ul':
        ville = l.xpath('li/a')
        for v in ville:
            ville = v.text_content()
            ville_link = v.attrib['href']
            dms = get_dms(ville_link)
            data={ 'id': i, \
                'guvernorate': guvernorate, \
                'guvernorate_link': 'http://en.wikipedia.org' + guvernorate_link, \
                'ville': ville, \
                'ville_link': 'http://en.wikipedia.org' + ville_link, \
                'lat': dms['lat'], \
                'lon': dms['lon']}

            scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='data')
            #exit()
            i+=1
                
                


