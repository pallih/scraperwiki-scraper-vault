# Blank Python
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re
# -*- coding: latin1 -*-
# import string

# have a look at pdfminer, pdftotext, pdftoipe, pyPdf

#pdfurl = "http://grff.in/out.pdf"
#pdfurl = "http://www.obairs.com/11.pdf"
#pdfurl = "http://www.vdi-nachrichten.com/_library/content/download/obj1382_Tabelle_N.pdf"
pdfurl = "http://www.bad-schussenried.de/publishNews/redirect.php?id2=13015&id=2210-1305524807-0.pdf" #Gemeindeblatt Schussenkaff
pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)

for page in root:
    assert page.tag == 'page'
    #print "page details", page.attrib
    pagelines = { }
    for v in page:
        if v.tag == 'text':
            text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)   # there has to be a better way here to get the contents
            top = int(v.attrib.get('top'))
            if (top - 1) in pagelines:
                top = top - 1
            elif (top + 1) in pagelines:
                top = top + 1
            elif top not in pagelines:
                pagelines[top] = [ ]
            pagelines[top].append((int(v.attrib.get('left')), text))
    lpagelines = pagelines.items()
    lpagelines.sort()
    for top, line in lpagelines:
        line.sort()
        convertedToString = str(line) #convert to String
        print convertedToString
#        afterRegularExpressionOnString = re.findall('[A-Z][A-Za-z]*',convertedToString) #it's a good start :-)
#        print afterRegularExpressionOnString[:200]
        #key = page.attrib.get('number') + ':' + str(top)
        #scraperwiki.sqlite.save(unique_keys=[ 'key' ], data={ 'key' : key, 'line' : line })