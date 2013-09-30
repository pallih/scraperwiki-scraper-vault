# -*- coding: utf-8 -*-
import scraperwiki
import urllib2, lxml.etree

url='http://www.jma.go.jp/jma/kishou/know/amedas/ame_master.pdf'

pdfdata = urllib2.urlopen(url).read()

xmldata = scraperwiki.pdftoxml(pdfdata)

root = lxml.etree.fromstring(xmldata)
pages = list(root)

#print xmldata
for page in pages[4:]:
    i = 0
    typeidx = []
    for el in page:
        if el.text == u'四' or el.text == u'三' or el.text == u'官' or el.text == u'雨' or el.text == u'雪':
            typeidx.append(i)
        i=i+1
    for ti in typeidx:
        if len(page[ti-1].text) == 5:
            lonlat=page[ti+4].text.split()+page[ti+5].text.split()+page[ti+6].text.split()
#            print lonlat
            latitude=float(lonlat[0])+float(lonlat[1])/60.0
            longitude=float(lonlat[2])+float(lonlat[3])/60.0
            data = {'code':int(page[ti-1].text),'name':page[ti+1].text.encode('utf-8'),'longitude':longitude,'latitude':latitude}
            scraperwiki.sqlite.save(unique_keys=['code'], data=data)
# -*- coding: utf-8 -*-
import scraperwiki
import urllib2, lxml.etree

url='http://www.jma.go.jp/jma/kishou/know/amedas/ame_master.pdf'

pdfdata = urllib2.urlopen(url).read()

xmldata = scraperwiki.pdftoxml(pdfdata)

root = lxml.etree.fromstring(xmldata)
pages = list(root)

#print xmldata
for page in pages[4:]:
    i = 0
    typeidx = []
    for el in page:
        if el.text == u'四' or el.text == u'三' or el.text == u'官' or el.text == u'雨' or el.text == u'雪':
            typeidx.append(i)
        i=i+1
    for ti in typeidx:
        if len(page[ti-1].text) == 5:
            lonlat=page[ti+4].text.split()+page[ti+5].text.split()+page[ti+6].text.split()
#            print lonlat
            latitude=float(lonlat[0])+float(lonlat[1])/60.0
            longitude=float(lonlat[2])+float(lonlat[3])/60.0
            data = {'code':int(page[ti-1].text),'name':page[ti+1].text.encode('utf-8'),'longitude':longitude,'latitude':latitude}
            scraperwiki.sqlite.save(unique_keys=['code'], data=data)
