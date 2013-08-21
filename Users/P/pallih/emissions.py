###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree
import re

url = "https://www.cdproject.net/CDPResults/CDP-Global-500-Climate-Change-Report-2012.pdf"
pdfdata = urllib2.urlopen(url).read()
#print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata

root = lxml.etree.fromstring(xmldata)
pages = root.xpath('//page')

pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

def Pageblock(page, index):
    ''' 
    Print each page of the PDF in turn, outputting the contents as HTML.
    '''
    result = [ ]
    assert page.tag == 'page'
    height = int(page.attrib.get('height'))
    width = int(page.attrib.get('width'))
    number = page.attrib.get('number')
    assert page.attrib.get('position') == "absolute"

    result.append('<p>Page %s index %d height=%d width=%d</p>' % (number, index, height, width))
    result.append('<div class="page" style="height:%dpx; width:%dpx">' % (height, width))
    for v in page:
        if v.tag == 'fontspec':
            continue
        assert v.tag == 'text'
        text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)
        top = int(v.attrib.get('top'))
        left = int(v.attrib.get('left'))
        width = int(v.attrib.get('width'))
        height = int(v.attrib.get('height'))
        fontid = v.attrib.get('font')
        style = 'top:%dpx; left:%dpx; height:%dpx; width:%dpx' % (top, left, height, width)
        result.append('    <div class="text fontspec-%s" style="%s">%s</div>' % (fontid, style, text))
    result.append('</div>')        
    return '\n'.join(result)

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

for index, page in enumerate(root):
        print Pageblock(page, index)

exit()

start = root.xpath('//text[text()="Appendix"]/following::text[following::text[text()="KEy TO APPENDIX "]]')
batch = []
for s in start:
    record = {}
        
    record['item'] = s.attrib, s.text
    batch.append(record)
print batch

exit()
# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"


# print the first hundred text elements from the first page
#page = pages[39]
for page in pages:
    print page.text_content()
    #elements = page.xpath('//text[text()="Appendix"]/following-sibling::text[following::text[text()="KEy TO APPENDIX "]]')
    for el in elements:
        #if el.tag == "text" and el.attrib['font'] == '5' and el.text=='Appendix':
        print el.attrib, el.tag, gettext_with_bi_tags(el)


# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/

