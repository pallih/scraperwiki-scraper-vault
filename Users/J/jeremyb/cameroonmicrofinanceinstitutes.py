#Scraper for Cameroon microfinance data from pdf file. Based on Scraperwiki's PDF example.
# Position visualizer is here: http://scraperwikiviews.com/run/pdf-to-html-preview-1/

import scraperwiki
import os
import tempfile
import sys
import re
import lxml.html

#lineparser = re.compile(r'^(?:\s{0,2}(?P<rownum>\d{0,5}))(?:$|\s(?P<name>.{77}.*?)(?:$|\s{5,}(?P<type>.{17}.*?)\s(?P<address>.*)))\s*$')

def pdftohtml(pdfdata):
    """converts pdf file to text"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    htmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.html')
    tmphtml = htmlin.name
    cmd = '/usr/bin/pdftohtml -c -enc UTF-8 "%s" "%s" >/dev/null' % (pdffout.name, tmphtml) # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    htmlin.close()
    with file('%s-2.html' % htmlin.name.rstrip('.html')) as htmlhandle:
        html = htmlhandle.read()
    return html

pdfurl = "http://www.dgtcfm.net/images/blogs/d033e22ae348aeb5660fc2140aec35850c4da99744f683a84163b3523afe57c2e008bc8c/LISTE%20DES%20EMF%20AGREES%20EN%20ACTIVITE%20AU%20CAMEROUN05%281%29.2010.pdf"
pdfbin = scraperwiki.scrape(pdfurl)
htmlsource= pdftohtml(pdfbin)
html = lxml.html.document_fromstring(htmlsource)

lastLine = None
out = []
headers = {}

#print html
print lxml.html.tostring(html,pretty_print=True,encoding='utf-8')
divs = html.cssselect('body div div')
#for div in divs[:4]:
#    print repr(lxml.html.tostring(div,pretty_print=True,encoding='utf-8'))
#    print repr(div.text_content())
#    print ";".join((div.text_content(),lxml.html.tostring(div,pretty_print=True,encoding='utf-8').decode('utf-8'))).encode('utf-8')
print "\n".join(map(lambda x:";".join((x.text_content(),lxml.html.tostring(x,pretty_print=True,encoding='utf-8').decode('utf-8'))).rstrip().encode('utf-8'),divs))
#print "\n".join(map(lambda x: x.text_content(),divs))

#for line in rawtext.splitlines():
#    if not line.strip():
#        continue
#    lv = dict((k,v.strip()) for k,v in lineparser.search('%-200s' % line.rstrip()).groupdict().items())
#    #print(repr(dict((k,v.strip()) for k,v in lineparser.search('%-200s' % line.rstrip()).groupdict().items())))
#    print repr(lv)
#
#    if not headers:
#        if "adresse" in lv['address'].lower():
#             headers = lv
#        continue

#    if lv['rownum']:
#        if lastLine:
#            out.append(lastLine)
#            print repr(lastLine)
#        lastLine = lv
#    else:
#        for k in lastLine.keys():
#            lastLine[k] = ' '.join((lastLine[k],lv[k]))
        
    #data = args2dict(lv)
    #print repr(data)

#out.append(lastLine)
#print repr(lastLine)

#print repr(out)
#Dump data out to scraperwiki store
#scraperwiki.sqlite.save(unique_keys=['rownum'], data=out)#Scraper for Cameroon microfinance data from pdf file. Based on Scraperwiki's PDF example.
# Position visualizer is here: http://scraperwikiviews.com/run/pdf-to-html-preview-1/

import scraperwiki
import os
import tempfile
import sys
import re
import lxml.html

#lineparser = re.compile(r'^(?:\s{0,2}(?P<rownum>\d{0,5}))(?:$|\s(?P<name>.{77}.*?)(?:$|\s{5,}(?P<type>.{17}.*?)\s(?P<address>.*)))\s*$')

def pdftohtml(pdfdata):
    """converts pdf file to text"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    htmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.html')
    tmphtml = htmlin.name
    cmd = '/usr/bin/pdftohtml -c -enc UTF-8 "%s" "%s" >/dev/null' % (pdffout.name, tmphtml) # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    htmlin.close()
    with file('%s-2.html' % htmlin.name.rstrip('.html')) as htmlhandle:
        html = htmlhandle.read()
    return html

pdfurl = "http://www.dgtcfm.net/images/blogs/d033e22ae348aeb5660fc2140aec35850c4da99744f683a84163b3523afe57c2e008bc8c/LISTE%20DES%20EMF%20AGREES%20EN%20ACTIVITE%20AU%20CAMEROUN05%281%29.2010.pdf"
pdfbin = scraperwiki.scrape(pdfurl)
htmlsource= pdftohtml(pdfbin)
html = lxml.html.document_fromstring(htmlsource)

lastLine = None
out = []
headers = {}

#print html
print lxml.html.tostring(html,pretty_print=True,encoding='utf-8')
divs = html.cssselect('body div div')
#for div in divs[:4]:
#    print repr(lxml.html.tostring(div,pretty_print=True,encoding='utf-8'))
#    print repr(div.text_content())
#    print ";".join((div.text_content(),lxml.html.tostring(div,pretty_print=True,encoding='utf-8').decode('utf-8'))).encode('utf-8')
print "\n".join(map(lambda x:";".join((x.text_content(),lxml.html.tostring(x,pretty_print=True,encoding='utf-8').decode('utf-8'))).rstrip().encode('utf-8'),divs))
#print "\n".join(map(lambda x: x.text_content(),divs))

#for line in rawtext.splitlines():
#    if not line.strip():
#        continue
#    lv = dict((k,v.strip()) for k,v in lineparser.search('%-200s' % line.rstrip()).groupdict().items())
#    #print(repr(dict((k,v.strip()) for k,v in lineparser.search('%-200s' % line.rstrip()).groupdict().items())))
#    print repr(lv)
#
#    if not headers:
#        if "adresse" in lv['address'].lower():
#             headers = lv
#        continue

#    if lv['rownum']:
#        if lastLine:
#            out.append(lastLine)
#            print repr(lastLine)
#        lastLine = lv
#    else:
#        for k in lastLine.keys():
#            lastLine[k] = ' '.join((lastLine[k],lv[k]))
        
    #data = args2dict(lv)
    #print repr(data)

#out.append(lastLine)
#print repr(lastLine)

#print repr(out)
#Dump data out to scraperwiki store
#scraperwiki.sqlite.save(unique_keys=['rownum'], data=out)