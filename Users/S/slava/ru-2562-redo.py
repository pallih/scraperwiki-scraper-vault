import scraperwiki
import lxml.html
import simplejson
import re
# Blank Python
libs=scraperwiki.utils.swimport('mylibs')


def get_city_branches(city_name):
    #
    b=libs.Browse()
    html=b.query("http://branches.binbank.ru/?metro_link=&metr=", { 'city':'%CC%EE%F1%EA%E2%E0', 'type0':1, 'type7':1, 'type6':1, 'type1':1, 'post_flag':'post'})
    print html
    #html=scraperwiki.scrape("http://branches.binbank.ru/?metro_link=&metr=",{ 'city':'%CC%EE%F1%EA%E2%E0', 'type0':1, 'type7':1, 'type6':1, 'type1':1, 'post_flag':'post'})
    html=html.decode('windows-1251')
    print html
    root=lxml.html.document_fromstring(html)

    print root.xpath("/html/body/table/tbody/tr[1]/td[4]/table/tbody/tr[8]/td/table/tr/td/table[2]")
    for t in root.xpath("/html/body/table/tr[1]/td[4]/table/tr[8]/td/table/tr/td//table/tr/td[2]"):
        print t.text_content()
        if 'style' in t.xpath('../td[1]')[0].attrib: 
            print "Skip" + t.xpath('../td[1]')[0].text_content()
            continue
    return ""

#scraperwiki.sqlite.execute('delete from `data`')
html=scraperwiki.scrape("http://branches.binbank.ru/?metro_link=&metr=")
html=html.decode('windows-1251')
root=lxml.html.document_fromstring(html)

for c in root.xpath("//select[@name='city']/option"):
    city_name=c.text_content()
    city_val=c.attrib['value']

    if city_val == 'any' or city_val == 'all': continue

    get_city_branches(city_val)
    exit()


#root = lxml.html.document_fromstring(html)
#trs = root.xpath("/html/body/table/tbody/tr[1]/td[4]/table/tr[8]/td/table/tr/td/table/tr/td[2]")
#trs1 = root.find_class(".adress_info")
print root
print html
print trs
print trs1
print lxml.html.tostring(root)
i=1
exit()
for tr in trs:
    data = {}
    data['branch_name'] = tr.xpath('b')[0].text_content() if tr.xpath('b') != [] else ''
    data['city_name'] = tr.xpath('p[1]/b')[0].text_content() if tr.xpath('p[1]/b') != [] else ''
    data['address'] = tr.xpath("p[@class='adress_info']")[0].text_content() if tr.xpath("p[@class='adress_info']") != [] else ''
    print data
    exit()
    scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, 'name':option.text_content(), 'address':address }, table_name='data')
    i+=1

