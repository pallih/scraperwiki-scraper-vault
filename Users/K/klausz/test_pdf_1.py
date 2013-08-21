# Blank Python
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

pdfurl = "http://grff.in/out.pdf"

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
#        regex = "\(\d+, '(\d+)'\), \(\d+, '(\d+)'\), \(\d+, '(.+?)'\), \(\d+, '(\w+)'\), \(\d+, '(.+?)'\)"
#        r = re.search("^\[\(\d+, '(\d+)'\), \(\d+, '(\d+)'\), \(\d+, '(.+?)'\), \(\d+, '(\w+)'\), \(\d+, '(.+?)'\)", line).group
#        print r
        r = re.search('[a-z]+',r)        
        print line
        #key = page.attrib.get('number') + ':' + str(top)
        #scraperwiki.sqlite.save(unique_keys=[ 'key' ], data={ 'key' : key, 'line' : line })