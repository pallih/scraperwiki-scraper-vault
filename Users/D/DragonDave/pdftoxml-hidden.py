import scraperwiki

import tempfile, os

# Blank Python
def pdftoxml(pdfdata,options=''):
    """converts pdf file to xml file"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    xmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.xml')
    tmpxml = xmlin.name # "temph.xml"
    cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes %s "%s" "%s"' % (options, pdffout.name, os.path.splitext(tmpxml)[0])
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    #xmlfin = open(tmpxml)
    xmldata = xmlin.read()
    xmlin.close()
    return xmldata

pdf='http://nrk.no/contentfile/file/1.8116520!offentligjournal02052012.pdf'
pdfdata=scraperwiki.scrape(pdf)
p1=pdftoxml(pdfdata,'-hidden')
p2=pdftoxml(pdfdata)
print p1
print p2
assert p1 != p2
import scraperwiki

import tempfile, os

# Blank Python
def pdftoxml(pdfdata,options=''):
    """converts pdf file to xml file"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    xmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.xml')
    tmpxml = xmlin.name # "temph.xml"
    cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes %s "%s" "%s"' % (options, pdffout.name, os.path.splitext(tmpxml)[0])
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    #xmlfin = open(tmpxml)
    xmldata = xmlin.read()
    xmlin.close()
    return xmldata

pdf='http://nrk.no/contentfile/file/1.8116520!offentligjournal02052012.pdf'
pdfdata=scraperwiki.scrape(pdf)
p1=pdftoxml(pdfdata,'-hidden')
p2=pdftoxml(pdfdata)
print p1
print p2
assert p1 != p2
