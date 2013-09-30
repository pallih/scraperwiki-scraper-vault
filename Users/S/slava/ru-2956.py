import scraperwiki
import re
import lxml.html
# Blank Python

html=scraperwiki.scrape("http://www.mteb.ru/about.asp?c_no=8141")
root=lxml.html.document_fromstring(html)
el=root.xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/p/table/tbody/tr/td//a")
print el
i=1
for e in root.xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/p/table/tbody/tr/td//a"):
    link=a.attrib['href']
    name=a.text_content()

    html=scraperwiki.scrape(link)
    root1=lxml.html.document_fromstring(html)
    s=root1.xpath("/html/body/table/tbody/tr/td/table[3]/tbody/tr/td[4]/p[@class='MsoNormal'][1]/span[1]")[0]
    address=s.text_content()
    map_link=s.attrib['href']
    print name, link, address, map_link
    html=scraperwiki.scrape(map_link)
    ll=re.findall(r'/\?ll=([\d\.]+?),([\d\.]+?)&amp', html, re.I|re.U|re.S)
    if ll==[] or (ll!=[] and len(ll[0])!=2): ll=['','']
    ll=ll[0]

    scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, 'name':name, 'link':link, 'address':address, 'lat':ll[1], 'lon':ll[0]}, table_name="data")
    i+=1
    exit()


import scraperwiki
import re
import lxml.html
# Blank Python

html=scraperwiki.scrape("http://www.mteb.ru/about.asp?c_no=8141")
root=lxml.html.document_fromstring(html)
el=root.xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/p/table/tbody/tr/td//a")
print el
i=1
for e in root.xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/p/table/tbody/tr/td//a"):
    link=a.attrib['href']
    name=a.text_content()

    html=scraperwiki.scrape(link)
    root1=lxml.html.document_fromstring(html)
    s=root1.xpath("/html/body/table/tbody/tr/td/table[3]/tbody/tr/td[4]/p[@class='MsoNormal'][1]/span[1]")[0]
    address=s.text_content()
    map_link=s.attrib['href']
    print name, link, address, map_link
    html=scraperwiki.scrape(map_link)
    ll=re.findall(r'/\?ll=([\d\.]+?),([\d\.]+?)&amp', html, re.I|re.U|re.S)
    if ll==[] or (ll!=[] and len(ll[0])!=2): ll=['','']
    ll=ll[0]

    scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, 'name':name, 'link':link, 'address':address, 'lat':ll[1], 'lon':ll[0]}, table_name="data")
    i+=1
    exit()


