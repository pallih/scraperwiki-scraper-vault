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
    appendix = ''
    nopupils = False
    noteachers = False
    teachers = []
    pupils = []
    fsm = False
    extra = []
    noexcluded = ''
    excluded = False
    aveclasssize = ''
    classsize = False
    text1 = ''
    text2 = ''
    for v in page:
        if v.tag == 'fontspec':
            continue
        assert v.tag == 'text'
        text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)
        if re.match('^.*Appendix.*$',text):
            appendix = text[11:-4].strip()
        if appendix:
            #print "%s --%s--" % (appendix,lxml.etree.tostring(v))
            if fsm and text.strip() != '':
                extra.append(text.strip())
                fsm = False
            elif excluded and text.strip() != '':
                extra.append(text.strip())
            elif excluded and text.strip() == '' or re.match('^.*Appendix.*$',text):
                excluded = False
            elif classsize and text.strip() != '':
                aveclasssize = text.strip()
                classsize = False
            if nopupils and text.strip() != '':
                pupils.append(text.strip())
            elif nopupils and text.strip() =='':
                nopupils = False
            elif noteachers and text.strip() != '':
                teachers.append(text.strip())
            elif noteachers and text.strip() =='':
                noteachers = False
            elif re.match('^.*entitled to free.*$',text):
                fsm = True
            elif re.match('^.*pupils excluded.*$',text):
                excluded = True
            if re.match('^.*umber of pupils$',text.strip()):
            #if text.strip() == 'Number of pupils':
                nopupils = True
            elif re.match('^.*umber of teachers\s+$',text):
            #elif text.strip() == 'Number of teachers':
                noteachers = True
            if (text2.strip() == 'Number' and text1.strip() == 'of' and text.strip() == 'pupils') or (text1.strip() == 'Number of' and text.strip() == 'pupils'):
                nopupils = True
            if (text2.strip() == 'Number' and text1.strip() == 'of' and text.strip() == 'teachers') or (text1.strip() == 'Number of' and text.strip() == 'teachers'):
                noteachers = True
            id = "%s-%s-%s" % (urn,number,i)
            data = {'text':text.strip(),'urn':urn,'elementid':i,'id':id}
            pagedata.append(data)
        i=i+1
        text2 = text1
        text1 = text      
    #print ('Page %s index %d height=%d width=%d' % (number, index, height, width))   
    if len(pupils) > 0:    
        print "pupils",pupils[1:]
    if len(teachers) > 0:
        print "teachers",teachers[1:] 
    if extra:    
        print extra
    #id = "%s-%s-%s" % (urn,number,i)
    #data = {'extra': extra,'urn':urn,'elementid':i,'id':id}
    #pagedata.append(data)
    return pagedata

def parseReport(pdfurl,urn):
    '''
    Take the URL of a PDF, and use scraperwiki.pdftoxml and lxml to output the contents
    as a styled HTML div.
    '''
    try:
        pdfdata = urllib2.urlopen(pdfurl).read()
        if pdfdata == '':
            return "Failed to load/PDF does not exist"
        pdfxml = scraperwiki.pdftoxml(pdfdata)
        root = lxml.etree.fromstring(pdfxml)
        reportdata = []
        #print "URN %s URL %" % (pdfurl,urn)
    
        # Print each page of the PDF.
        for index, page in enumerate(root):
            data = PageSave(page, index,urn)
            reportdata.append(data)
            for ldata in data:
                #print data
                lldata = ldata.copy()
                lldata["urm"] = urn
                scraperwiki.sqlite.save(unique_keys=ldata.keys(), data=lldata, table_name="other")
        #print reportdata
        report = {'urn':urn, 'data':reportdata}
        print report
        scraperwiki.sqlite.save(unique_keys=["urn"], data=report)
        return "Success"
    except Exception, e:
        return "Error %s" % e

def Main():
    #print welsh_schools
    #for line in json.loads(scraperwiki.scrape("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=welsh_school_finder&query=select%20*%20from%20%60swdata%60%20limit%20")):
    #for line in scraperwiki.datastore.getData("welsh_school_finder", offset=1291):
    scraperwiki.sqlite.attach("welsh_school_finder", "src")
    for line in scraperwiki.sqlite.select("* from src.swdata where id='6752000'"):
        if line['report']:
            if (line['id'][0] != 'T'):
                print "%s %s" % (line['name'],line['id'])
                print parseReport(str(line['report']),str(line['id']))
    #url = "http://www.estyn.gov.uk/download/publication/19792.5/inspection-reportbirchgrove-primaryeng2009/"
    #urn = "123"


Main()
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
    appendix = ''
    nopupils = False
    noteachers = False
    teachers = []
    pupils = []
    fsm = False
    extra = []
    noexcluded = ''
    excluded = False
    aveclasssize = ''
    classsize = False
    text1 = ''
    text2 = ''
    for v in page:
        if v.tag == 'fontspec':
            continue
        assert v.tag == 'text'
        text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)
        if re.match('^.*Appendix.*$',text):
            appendix = text[11:-4].strip()
        if appendix:
            #print "%s --%s--" % (appendix,lxml.etree.tostring(v))
            if fsm and text.strip() != '':
                extra.append(text.strip())
                fsm = False
            elif excluded and text.strip() != '':
                extra.append(text.strip())
            elif excluded and text.strip() == '' or re.match('^.*Appendix.*$',text):
                excluded = False
            elif classsize and text.strip() != '':
                aveclasssize = text.strip()
                classsize = False
            if nopupils and text.strip() != '':
                pupils.append(text.strip())
            elif nopupils and text.strip() =='':
                nopupils = False
            elif noteachers and text.strip() != '':
                teachers.append(text.strip())
            elif noteachers and text.strip() =='':
                noteachers = False
            elif re.match('^.*entitled to free.*$',text):
                fsm = True
            elif re.match('^.*pupils excluded.*$',text):
                excluded = True
            if re.match('^.*umber of pupils$',text.strip()):
            #if text.strip() == 'Number of pupils':
                nopupils = True
            elif re.match('^.*umber of teachers\s+$',text):
            #elif text.strip() == 'Number of teachers':
                noteachers = True
            if (text2.strip() == 'Number' and text1.strip() == 'of' and text.strip() == 'pupils') or (text1.strip() == 'Number of' and text.strip() == 'pupils'):
                nopupils = True
            if (text2.strip() == 'Number' and text1.strip() == 'of' and text.strip() == 'teachers') or (text1.strip() == 'Number of' and text.strip() == 'teachers'):
                noteachers = True
            id = "%s-%s-%s" % (urn,number,i)
            data = {'text':text.strip(),'urn':urn,'elementid':i,'id':id}
            pagedata.append(data)
        i=i+1
        text2 = text1
        text1 = text      
    #print ('Page %s index %d height=%d width=%d' % (number, index, height, width))   
    if len(pupils) > 0:    
        print "pupils",pupils[1:]
    if len(teachers) > 0:
        print "teachers",teachers[1:] 
    if extra:    
        print extra
    #id = "%s-%s-%s" % (urn,number,i)
    #data = {'extra': extra,'urn':urn,'elementid':i,'id':id}
    #pagedata.append(data)
    return pagedata

def parseReport(pdfurl,urn):
    '''
    Take the URL of a PDF, and use scraperwiki.pdftoxml and lxml to output the contents
    as a styled HTML div.
    '''
    try:
        pdfdata = urllib2.urlopen(pdfurl).read()
        if pdfdata == '':
            return "Failed to load/PDF does not exist"
        pdfxml = scraperwiki.pdftoxml(pdfdata)
        root = lxml.etree.fromstring(pdfxml)
        reportdata = []
        #print "URN %s URL %" % (pdfurl,urn)
    
        # Print each page of the PDF.
        for index, page in enumerate(root):
            data = PageSave(page, index,urn)
            reportdata.append(data)
            for ldata in data:
                #print data
                lldata = ldata.copy()
                lldata["urm"] = urn
                scraperwiki.sqlite.save(unique_keys=ldata.keys(), data=lldata, table_name="other")
        #print reportdata
        report = {'urn':urn, 'data':reportdata}
        print report
        scraperwiki.sqlite.save(unique_keys=["urn"], data=report)
        return "Success"
    except Exception, e:
        return "Error %s" % e

def Main():
    #print welsh_schools
    #for line in json.loads(scraperwiki.scrape("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=welsh_school_finder&query=select%20*%20from%20%60swdata%60%20limit%20")):
    #for line in scraperwiki.datastore.getData("welsh_school_finder", offset=1291):
    scraperwiki.sqlite.attach("welsh_school_finder", "src")
    for line in scraperwiki.sqlite.select("* from src.swdata where id='6752000'"):
        if line['report']:
            if (line['id'][0] != 'T'):
                print "%s %s" % (line['name'],line['id'])
                print parseReport(str(line['report']),str(line['id']))
    #url = "http://www.estyn.gov.uk/download/publication/19792.5/inspection-reportbirchgrove-primaryeng2009/"
    #urn = "123"


Main()
