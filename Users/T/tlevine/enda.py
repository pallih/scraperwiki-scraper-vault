from scraperwiki import pdftoxml
from urllib2 import urlopen
from lxml.html import fromstring, tostring
import lxml.etree

def get_pdf_list():
    raw = urlopen('http://www.dropbox.com/sh/gpi0ejooop07x8a/bMDz4s9Ixp').read()
    html = fromstring(raw)
    
    a_elements = html.cssselect('li.browse-file.list-view-cols div.filename-col a')
    pdf_urls = [a.attrib['href'] + '?dl=1' for a in a_elements]
    return pdf_urls

test_url = 'https://www.dropbox.com/sh/gpi0ejooop07x8a/qJxWkjx8fz/ENDA-HR1858-June1997.pdf?dl=1'

raw_pdf = urlopen(test_url).read()
pdfxml = lxml.etree.fromstring(pdftoxml(raw_pdf))

rawtext = pdfxml.xpath('string()').replace('\n', ' ')
print rawtext