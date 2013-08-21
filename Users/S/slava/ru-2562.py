import scraperwiki
import lxml.html
import simplejson
import re
# Blank Python

#scraperwiki.sqlite.execute('delete from `data`')

html = scraperwiki.scrape("http://dl.dropbox.com/u/14865435/test.txt").strip()
root = lxml.html.document_fromstring(html)
trs = root.xpath("/html/body/table/tbody/tr[1]/td[4]/table/tr[8]/td/table/tr/td/table/tr/td[2]")
trs1 = root.find_class(".adress_info")
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

