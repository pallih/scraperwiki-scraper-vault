from urllib2 import urlopen
from scraperwiki import pdftoxml
from scraperwiki.sqlite import save_var, get_var
from lxml.etree import fromstring, tostring
from unidecode import unidecode

#pdfxml = pdftoxml(urlopen('http://www.hydepark.org/schools/HPKCC%20Youth%20Programs%20Database-%20Version%203.pdf').read())
#save_var('pdfxml', unidecode(pdfxml))

pdfxml = get_var('pdfxml')
x = fromstring(pdfxml)
for page in x.xpath('//page'):
    bs = page.xpath('descendant::b/text()')
    if len(bs) == 10 and bs[0] == 'HPKCC Youth Programs Database':
        del(bs[0])

    if len(bs) != 9:
        raise ValueError('Wrong number of bold text boxes')
    elif bs[0:7] != ['Program Name', 'Program Desc.', 'Program Website', 'Program Address', 'Contact Name', 'Contact Number', 'Contact Email']:
        raise ValueError('Wrong table keys')

    updated, pagenumber = bs[7:9]

    lefts = map(int, list(set(page.xpath('text/@left'))))
    lefts.sort()
    for left in lefts:
        print [t.xpath('string()') for t in page.xpath('text[@left = "%d"]' % left)]

    # tops = map(int, list(set(page.xpath('text/@top'))))
    # tops.sort()
    # print len(tops)