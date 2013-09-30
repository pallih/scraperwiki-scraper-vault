import scraperwiki
import lxml.html
import lxml.etree

def fetch():
    root = lxml.html.parse('http://www.cba.gov.ar/registro-oficial-de-proveedores/').getroot()
    links = root.cssselect('a')
    result = ''
    for link in links:
        href = link.get('href')
        if 'pdf' in href and 'requis_inscrip_tramite' not in href:
            result = href
            break

    return result

def getpages(href):
    pdfdata = scraperwiki.scrape(href)
    xml = scraperwiki.pdftoxml(pdfdata)
    dom = lxml.etree.fromstring(xml)
    pages = list(dom)
    print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]
    return pages


href = fetch()
pages = getpages(href)
print pages


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

# print the first hundred text elements from the first page
page0 = pages[0]
for el in list(page0)[:100]:
    if el.tag == "text":
        print el.attrib
        print el.text
        # print gettext_with_bi_tags(el)


# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/
import scraperwiki
import lxml.html
import lxml.etree

def fetch():
    root = lxml.html.parse('http://www.cba.gov.ar/registro-oficial-de-proveedores/').getroot()
    links = root.cssselect('a')
    result = ''
    for link in links:
        href = link.get('href')
        if 'pdf' in href and 'requis_inscrip_tramite' not in href:
            result = href
            break

    return result

def getpages(href):
    pdfdata = scraperwiki.scrape(href)
    xml = scraperwiki.pdftoxml(pdfdata)
    dom = lxml.etree.fromstring(xml)
    pages = list(dom)
    print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]
    return pages


href = fetch()
pages = getpages(href)
print pages


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

# print the first hundred text elements from the first page
page0 = pages[0]
for el in list(page0)[:100]:
    if el.tag == "text":
        print el.attrib
        print el.text
        # print gettext_with_bi_tags(el)


# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/
