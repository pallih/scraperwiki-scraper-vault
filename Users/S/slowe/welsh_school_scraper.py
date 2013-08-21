import scraperwiki
import urllib, urllib2
import lxml.etree, lxml.html
import re, os


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


def Main(pdfurl):
    '''
    Take the URL of a PDF, and use scraperwiki.pdftoxml and lxml to output the contents
    as a styled HTML div.
    '''
    pdfdata = urllib2.urlopen(pdfurl).read()
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(pdfxml)




    # Print each page of the PDF.
    for index, page in enumerate(root):
        print Pageblock(page, index)
url = "http://www.estyn.gov.uk/download/publication/12694.5/inspection-reportabercerdin-primary-schooleng2008/"
Main(url)

