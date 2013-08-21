###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF. 
###########################################################################################

import scraperwiki
import urllib2, urllib
import lxml.etree
import lxml.html

import scraperwiki, re, HTMLParser
from BeautifulSoup import BeautifulSoup

class MLStripper(HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_fed_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    #Warning this does all including script and javascript
    x = MLStripper()
    x.feed(html)
    return x.get_fed_data()


def process_pdf( url ):
    print "PROCESSING: " , url, 
    pdfdata = urllib2.urlopen(url).read()
    print len( pdfdata ), "bytes"
    if len(pdfdata) > 50000:
        return "" #too BIG Daddio!

    str = ''
    xmldata = scraperwiki.pdftoxml(pdfdata)

    root = lxml.etree.fromstring(xmldata)
    pages = list(root)


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

    for page in pages :
        print page.attrib.get("number")
        # print the first hundred text elements from the first page
        page0 = pages[0]
        i = []
        data = []
        for el in list(page)[:1000]:
            if el.tag == "text":
                 data = {}
                 text = strip_tags( gettext_with_bi_tags(el) )
                 #data['text'] =  text
                 #data['url'] = url # The source of these words 
                 if text != '' and text != ' ':
                     #scraperwiki.sqlite.save(i, data)
                     str += " " + text
    return str                     




i = 0
base_url = "http://www.york.gov.uk/info/200601/freedom_of_information/180/freedom_of_information/5"
found_pdfs = []
html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)
els = root.cssselect("a")
for el in els:          
    link_text = el.text
    try:
        if "commencing" in link_text and "2013" in link_text:
            subpage_url = urllib.basejoin("http://www.york.gov.uk/", el.attrib['href'])
            print "Getting: " , subpage_url 
            subpage_html = scraperwiki.scrape( subpage_url )
            subpage_root = lxml.html.fromstring(subpage_html)
            subpage_els = subpage_root.cssselect("a")
            for subpage_el in subpage_els:
                url = urllib.basejoin("http://www.york.gov.uk/", subpage_el.attrib['href'])
                if "/downloads/file/" in url:
                    print "SUBPAGE: ",subpage_el.text, "    ",  url

                    final_html = scraperwiki.scrape( url )
                    final_root = lxml.html.fromstring(final_html)
                    final_els = final_root.cssselect("a")
                    for final_el in final_els:
                         
                         try:
                             if "Download Now" in final_el.text and "/download/downloads" in final_el.attrib['href']:
                                 final_url = final_el.attrib['href']
                                 if "CF2327___attachment_1.pdf" not in final_url and "/6750/" not in final_url and "/6751/" not in final_url: # scary bloody tables
                                     print "FINAL: ", final_el.text, final_url
                                     str = process_pdf( final_url )
                                     data = {'text': str, 'url': final_url}
                                     scraperwiki.sqlite.save([], data)
                                     i = i + 1
                                     #found_pdfs.append( final_url )
                         

                         except Exception, err:
                            pass
                            print "Final: " , err
                              

    except Exception, err:
        print "Main: ", err

print found_pdfs


