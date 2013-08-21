import scraperwiki
import urllib, urllib2
import lxml.etree, lxml.html
import re, os
import json

def PageSave(page, index,urn):
    '''
    Print each page of the PDF in turn, outputting the contents as HTML.
    '''
    assert page.tag == 'page'
    height = int(page.attrib.get('height'))
    width = int(page.attrib.get('width'))
    number = page.attrib.get('number')
    assert page.attrib.get('position') == "absolute"
    pagedata = []

    i = 0
    for v in page:
        if v.tag == 'fontspec':
            continue
        assert v.tag == 'text'
        text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)
        if text:
            top = int(v.attrib.get('top'))
            left = int(v.attrib.get('left'))
            width = int(v.attrib.get('width'))
            height = int(v.attrib.get('height'))
            fontid = v.attrib.get('font')
            id = "%s-%s-%s" % (urn,number,i)
            data = {'text':text,'fontid':fontid,'top':top,'left':left,'height':height,'width':width,'fontid':fontid,'urn':urn,'elementid':i,'id':id}
            pagedata.append(data)
        i=i+1      
    #print ('Page %s index %d height=%d width=%d' % (number, index, height, width))     
    return pagedata

def parseReport(pdfurl,urn):
    '''
    Take the URL of a PDF, and use scraperwiki.pdftoxml and lxml to output the contents
    as a styled HTML div.
    '''
    pdfdata = urllib2.urlopen(pdfurl).read()
    if pdfdata == '':
        return "Failed to load PDF/does not exist"
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(pdfxml)
    reportdata = []
    #print "URN %s URL %" % (pdfurl,urn)

    # Print each page of the PDF.
    for index, page in enumerate(root):
        data = PageSave(page, index,urn)
        reportdata.append(data)
        for ldata in data:
            lldata = ldata.copy()
            lldata["urm"] = urn
            scraperwiki.sqlite.save(unique_keys=ldata.keys(), data=lldata, table_name="other")
    report = {'urn':urn, 'data':reportdata}
    scraperwiki.sqlite.save(unique_keys=["urn"], data=report)
    return "Success"

def Main():
    #print welsh_schools
    #for line in json.loads(scraperwiki.scrape("http://api.scraperwiki.com/api/1.0/datastore/getdata?&name=welsh_school_finder")):
    for line in scraperwiki.datastore.getData("welsh_school_finder", offset=1291):
        if line['report']:
            if (line['id'][0] != 'T'):
                print "%s %s" % (line['name'],line['id'])
                print parseReport(str(line['report']),str(line['id']))
    #url = "http://www.estyn.gov.uk/download/publication/19792.5/inspection-reportbirchgrove-primaryeng2009/"
    #urn = "123"


Main()
