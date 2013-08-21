import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

pdfurl = "http://www.epa.ie/downloads/pubs/other/corporate/oee/web%20list%20of%20files%20Dublin%20oct2010.pdf"



def psave(pagenumber , mrow):
    data = {'reg':mrow.group(1), 'name':mrow.group(2), 'page':pagenumber}
    eurl = 'http://www.epa.ie/downloads/pubs/other/corporate/oee/web%2520list%2520of%2520files%2520Dublin%2520oct2010.pdf'
    data['url'] = 'http://scraperwiki.com/cropper/u/page_%d/?url=%s' % (pagenumber, pdfurl)
    scraperwiki.datastore.save(unique_keys=['reg'], data=data)

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
#print pdfxml


for page in root:
    assert page.tag == 'page'
    pagenumber = int(page.attrib.get('number'))

    pline = ""
    for line in page:
        if line.tag == 'fontspec':
            #fontspecs[line.attrib.get('id')] = line
            continue

        # throw away right hand column and titles
        if line.attrib.get('font') != '2':
            continue
        assert line.tag == 'text'

        # join multiple lines
        mrow = re.match('([\d\-]+)\s+(.*)$', line.text)
        if mrow:
            if pline:
                mrowp = re.match('([\d\-]+)\s+(.*)$', pline)
                psave(pagenumber , mrowp)
                pline = ""
            psave(pagenumber , mrow)
        else:
            pline = ('%s %s' % (pline, line.text)).strip()

        #print lxml.etree.tostring(v)
        #print mrow.groups()

    
    
    
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

pdfurl = "http://www.epa.ie/downloads/pubs/other/corporate/oee/web%20list%20of%20files%20Dublin%20oct2010.pdf"



def psave(pagenumber , mrow):
    data = {'reg':mrow.group(1), 'name':mrow.group(2), 'page':pagenumber}
    eurl = 'http://www.epa.ie/downloads/pubs/other/corporate/oee/web%2520list%2520of%2520files%2520Dublin%2520oct2010.pdf'
    data['url'] = 'http://scraperwiki.com/cropper/u/page_%d/?url=%s' % (pagenumber, pdfurl)
    scraperwiki.datastore.save(unique_keys=['reg'], data=data)

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
#print pdfxml


for page in root:
    assert page.tag == 'page'
    pagenumber = int(page.attrib.get('number'))

    pline = ""
    for line in page:
        if line.tag == 'fontspec':
            #fontspecs[line.attrib.get('id')] = line
            continue

        # throw away right hand column and titles
        if line.attrib.get('font') != '2':
            continue
        assert line.tag == 'text'

        # join multiple lines
        mrow = re.match('([\d\-]+)\s+(.*)$', line.text)
        if mrow:
            if pline:
                mrowp = re.match('([\d\-]+)\s+(.*)$', pline)
                psave(pagenumber , mrowp)
                pline = ""
            psave(pagenumber , mrow)
        else:
            pline = ('%s %s' % (pline, line.text)).strip()

        #print lxml.etree.tostring(v)
        #print mrow.groups()

    
    
    
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

pdfurl = "http://www.epa.ie/downloads/pubs/other/corporate/oee/web%20list%20of%20files%20Dublin%20oct2010.pdf"



def psave(pagenumber , mrow):
    data = {'reg':mrow.group(1), 'name':mrow.group(2), 'page':pagenumber}
    eurl = 'http://www.epa.ie/downloads/pubs/other/corporate/oee/web%2520list%2520of%2520files%2520Dublin%2520oct2010.pdf'
    data['url'] = 'http://scraperwiki.com/cropper/u/page_%d/?url=%s' % (pagenumber, pdfurl)
    scraperwiki.datastore.save(unique_keys=['reg'], data=data)

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
#print pdfxml


for page in root:
    assert page.tag == 'page'
    pagenumber = int(page.attrib.get('number'))

    pline = ""
    for line in page:
        if line.tag == 'fontspec':
            #fontspecs[line.attrib.get('id')] = line
            continue

        # throw away right hand column and titles
        if line.attrib.get('font') != '2':
            continue
        assert line.tag == 'text'

        # join multiple lines
        mrow = re.match('([\d\-]+)\s+(.*)$', line.text)
        if mrow:
            if pline:
                mrowp = re.match('([\d\-]+)\s+(.*)$', pline)
                psave(pagenumber , mrowp)
                pline = ""
            psave(pagenumber , mrow)
        else:
            pline = ('%s %s' % (pline, line.text)).strip()

        #print lxml.etree.tostring(v)
        #print mrow.groups()

    
    
    
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

pdfurl = "http://www.epa.ie/downloads/pubs/other/corporate/oee/web%20list%20of%20files%20Dublin%20oct2010.pdf"



def psave(pagenumber , mrow):
    data = {'reg':mrow.group(1), 'name':mrow.group(2), 'page':pagenumber}
    eurl = 'http://www.epa.ie/downloads/pubs/other/corporate/oee/web%2520list%2520of%2520files%2520Dublin%2520oct2010.pdf'
    data['url'] = 'http://scraperwiki.com/cropper/u/page_%d/?url=%s' % (pagenumber, pdfurl)
    scraperwiki.datastore.save(unique_keys=['reg'], data=data)

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
#print pdfxml


for page in root:
    assert page.tag == 'page'
    pagenumber = int(page.attrib.get('number'))

    pline = ""
    for line in page:
        if line.tag == 'fontspec':
            #fontspecs[line.attrib.get('id')] = line
            continue

        # throw away right hand column and titles
        if line.attrib.get('font') != '2':
            continue
        assert line.tag == 'text'

        # join multiple lines
        mrow = re.match('([\d\-]+)\s+(.*)$', line.text)
        if mrow:
            if pline:
                mrowp = re.match('([\d\-]+)\s+(.*)$', pline)
                psave(pagenumber , mrowp)
                pline = ""
            psave(pagenumber , mrow)
        else:
            pline = ('%s %s' % (pline, line.text)).strip()

        #print lxml.etree.tostring(v)
        #print mrow.groups()

    
    
    
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

pdfurl = "http://www.epa.ie/downloads/pubs/other/corporate/oee/web%20list%20of%20files%20Dublin%20oct2010.pdf"



def psave(pagenumber , mrow):
    data = {'reg':mrow.group(1), 'name':mrow.group(2), 'page':pagenumber}
    eurl = 'http://www.epa.ie/downloads/pubs/other/corporate/oee/web%2520list%2520of%2520files%2520Dublin%2520oct2010.pdf'
    data['url'] = 'http://scraperwiki.com/cropper/u/page_%d/?url=%s' % (pagenumber, pdfurl)
    scraperwiki.datastore.save(unique_keys=['reg'], data=data)

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
#print pdfxml


for page in root:
    assert page.tag == 'page'
    pagenumber = int(page.attrib.get('number'))

    pline = ""
    for line in page:
        if line.tag == 'fontspec':
            #fontspecs[line.attrib.get('id')] = line
            continue

        # throw away right hand column and titles
        if line.attrib.get('font') != '2':
            continue
        assert line.tag == 'text'

        # join multiple lines
        mrow = re.match('([\d\-]+)\s+(.*)$', line.text)
        if mrow:
            if pline:
                mrowp = re.match('([\d\-]+)\s+(.*)$', pline)
                psave(pagenumber , mrowp)
                pline = ""
            psave(pagenumber , mrow)
        else:
            pline = ('%s %s' % (pline, line.text)).strip()

        #print lxml.etree.tostring(v)
        #print mrow.groups()

    
    
    
