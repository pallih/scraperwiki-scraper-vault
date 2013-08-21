# -*- coding: utf-8 -*-

# Iceland - political contributions - WORK IN PROGRESS

import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

pdfurl = "http://www.rikisendurskodun.is/utgefid-efni/fjarmal-stjornmalastarfsemi/utdrattur-ur-uppgjorum-stjornmalasamtaka/?eID=dam_frontend_push&docID=1170"


# (harder example to work on: http://www.nihe.gov.uk/schemes_accepted_010109_to_310309.pdf )
pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)


print "The pdf file has %d bytes" % len(pdfdata)


print "After converting to xml it has %d bytes" % len(pdfxml)
print "The XML: ", pdfxml

pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]




fontspecs = { }
pagetexts = [ ]
for page in root:
    assert page.tag == 'page'
   
    pagelines = { }
    for v in page:
        if v.tag == 'fontspec':
            fontspecs[v.attrib.get('id')] = v
        else:
            assert v.tag == 'text'
            text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)   # there has to be a better way here to get the contents
            top = int(v.attrib.get('left'))
            if top not in pagelines:
                pagelines[top] = [ ]
            pagelines[top].append((int(v.attrib.get('left')), text))
    lpagelines = pagelines.items()
    lpagelines.sort()
    for top, line in lpagelines[:20]:
        line.sort()
        print top, line
    pagetexts.append(pagelines)
    
    
    

