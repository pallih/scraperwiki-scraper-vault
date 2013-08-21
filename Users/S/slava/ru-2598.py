import scraperwiki
import lxml.html
import simplejson
import re
# Blank Python

#scraperwiki.sqlite.execute('delete from `data`')


def get_element(el, strXpath,index=0):
    r = el.xpath(strXpath)
    if r != [] and len(r)>index:
        return r[index].text_content()
    else:
        return ''
    

def process_links(links,i):
    for l in links :
        html = scraperwiki.scrape("http://www.zapad.ru" + l.attrib['href'] )
        r = lxml.html.document_fromstring(html)

        sub_links = l.xpath("ul/li/a")
        if sub_links != []:
            i = process_links(sub_links,i)

        data = {}
        data['branch_name'] = get_element(r,"//div[@class='article-content']/h1/span")
        data['address'] = get_element(r,"//div[@class='article-content']/p[1]")
        data['script'] = get_element(r,"//div[@class='article-content']/script")
        print data['script']
        data['script'] = re.findall(r'createObject\("Placemark", new YMaps\.GeoPoint\(([\d\.]+?),\s*([\d\.]+?)\)',data['script'], re.I|re.U|re.S)
        print data['script']
        print data
        #exit()
        #scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, 'name':option.text_content(), 'address':address }, table_name='data')
        #i+=1
    return i

html = scraperwiki.scrape("http://www.zapad.ru/branches")
root = lxml.html.document_fromstring(html)
links = root.xpath("//ul[@id='menu-left']/li/a")
#print links
#exit()
process_links(links,1)
    

