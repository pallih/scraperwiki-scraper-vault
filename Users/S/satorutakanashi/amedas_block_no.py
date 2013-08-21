# -*- coding: utf-8 -*-
import scraperwiki
import lxml.html
import re

url='http://www.data.jma.go.jp/obd/stats/etrn/select/prefecture00.php'

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
data={}
for el in root.cssselect("map[name='point'] area"):
    burl = 'http://www.data.jma.go.jp/obd/stats/etrn/select/' + el.attrib['href']
    broot = lxml.html.fromstring(scraperwiki.scrape(burl))
    m = re.search(r'prec_no=(\d{2})', el.attrib['href'])
    if m != None:
        prec_no = int(m.group(1))
        for bel in broot.cssselect("map[name='point'] area"):
            if 'onmouseover' in bel.attrib:
                m = re.search(r'javascript:viewPoint\((.+)\);', bel.attrib['onmouseover'])
            if m != None:
                args = [s.strip("'") for s in m.group(1).split(',')]
                typecode = args[0]
                block_no = int(args[1])
                if block_no > 0:
                    name = args[2]
                    kananame = args[3]
                    latitude = float(args[4])+float(args[5])/60.0
                    longitude = float(args[6])+float(args[7])/60.0
                    altitude = float(args[8])
                    obscode = int(args[9])*2**4+int(args[10])*2**3+int(args[11])*2**2+int(args[12])*2+int(args[13])
                    data[name] = {'prec_no':prec_no,'block_no':block_no,'name':name,'kananame':kananame,'latitude':latitude,'longitude':longitude,'altitude':altitude,'type':typecode,'obs':obscode}

scraperwiki.sqlite.save(unique_keys=['name'], data=[v for v in data.values()])