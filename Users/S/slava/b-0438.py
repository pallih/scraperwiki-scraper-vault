import scraperwiki
import lxml, lxml.html
import pprint
# Blank Python


html = scraperwiki.scrape("http://www.kamkombank.ru/contacts/")
root = lxml.html.fromstring(html)

for tr in root.cssselect('td[id=maincol] div[class=padd_left] *'):
    print tr.tag
    #if tr.attrib.get('class') != 'thead':
    #    data = {'address':'', 'branch_name': ''}
    #    for td in tr.cssselect("td"):
#
#            a = td.cssselect("div a.address-link")
#            if len(a) > 0:
#                data['address'] = a[0].text_content()
#
#            a = td.cssselect("a")
#            for i in a:
#                if i.attrib.get('href').find("http://www.ubrr.ru/about/offices/office") !=-1:
#                    data['branch_name']=i.text_content()
#            scraperwiki.sqlite.save(unique_keys=['address'], data=data)
#            print data
            
