import scraperwiki
import urllib2
import lxml.etree
# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

url = "http://www.trasporti.provincia.tn.it/binary/pat_trasporti/primo_piano/Orario_Valsugana_10.06.2012.1339493934.pdf"
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)
pages = list(root)
for el in pages[0]:
    if el.tag == 'text':
        left= el.attrib.get('left')
        right = el.attrib.get('right')
        top = el.attrib.get('top')
        bottom = el.attrib.get('bottom')
        print left
        if (left==70): # and (el.attrib.get('right') == 117):
            print "Ciao"
import scraperwiki
import urllib2
import lxml.etree
# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

url = "http://www.trasporti.provincia.tn.it/binary/pat_trasporti/primo_piano/Orario_Valsugana_10.06.2012.1339493934.pdf"
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)
pages = list(root)
for el in pages[0]:
    if el.tag == 'text':
        left= el.attrib.get('left')
        right = el.attrib.get('right')
        top = el.attrib.get('top')
        bottom = el.attrib.get('bottom')
        print left
        if (left==70): # and (el.attrib.get('right') == 117):
            print "Ciao"
