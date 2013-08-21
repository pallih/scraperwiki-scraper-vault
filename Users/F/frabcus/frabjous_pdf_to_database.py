import scraperwiki
import urllib2
import lxml.etree
import hashlib
import os

pdfurls = [
("2011-01-25", "http://www.eastsussex.gov.uk/NR/rdonlyres/90D1BB09-CC56-489C-AB32-9B9A54BD1470/25962/C25Jan2011Item7BudgetMonitoring.pdf"),
("2011-03-08", "http://www.eastsussex.gov.uk/NR/rdonlyres/B58200AD-C313-4F4F-92AF-A32FDB80F228/26310/C8Mar2011Item11BM.pdf"),
]

def ctext(el):
    result = [ ]
    if el.text:
        result.append(el.text)
    for sel in el:
        assert sel.tag in ["b", "i"]
        result.append("<"+sel.tag+">")
        result.append(ctext(sel))
        result.append("</"+sel.tag+">")
        if sel.tail:
            result.append(sel.tail)
    return "".join(result)

def ConvertPDFtoSqlite(docname, pdfurl):
    print "converting", docname, pdfurl
    pdfdata = urllib2.urlopen(pdfurl).read()
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    try:
        root = lxml.etree.fromstring(pdfxml)
    except lxml.etree.XMLSyntaxError, e:
        print "Bad xml file", str(e)
        print pdfxml[:19000]
        return

    fontdescs = [ ]
    for fontspec in root.xpath('page/fontspec'):
        fontid = fontspec.attrib.get('id')
        fontdescs.append({"fontid":fontid, 'size':int(fontspec.attrib.get('size')), 'family':fontspec.attrib.get('family'),
                          'color':fontspec.attrib.get('color'), "pdfurl":pdfurl, "docname":docname})
    scraperwiki.sqlite.save(unique_keys=["pdfurl", "fontid"], data=fontdescs, table_name="fonts")


    for index, page in enumerate(root):
        assert page.tag == 'page'
        number = int(page.attrib.get('number'))
        pagedata = {"pdfurl":pdfurl, "number":number, "height":int(page.attrib.get('height')),
                    "width":int(page.attrib.get('width')), "docname":docname }
        assert page.attrib.get('position') == "absolute"
        scraperwiki.sqlite.save(unique_keys=["pdfurl", "number"], data=pagedata, table_name="pages")

        ldata = [ ]
        for v in page:
            if v.tag == 'fontspec':
                continue
            assert v.tag == 'text'
            text = ctext(v)
            data = {"top":int(v.attrib.get('top')), "left":int(v.attrib.get('left')),
                    "width":int(v.attrib.get('width')), "height":int(v.attrib.get('height')),
                    "fontid":v.attrib.get('font'), "text":ctext(v),
                    "pdfurl":pdfurl, "page":number, "docname":docname}
            data["hid"] = hashlib.sha224("%s %d %d %d" % (pdfurl, number, data["top"], data["left"])).hexdigest()
            ldata.append(data)
            #print lxml.etree.tostring(v)
        scraperwiki.sqlite.save(unique_keys=["pdfurl", "page", "top", "left"], data=ldata, table_name="line")
        #break

for docname, pdfurl in pdfurls:
    ConvertPDFtoSqlite(docname, pdfurl)
    



