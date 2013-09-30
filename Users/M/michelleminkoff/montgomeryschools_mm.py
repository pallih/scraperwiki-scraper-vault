import scraperwiki
import sys
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice

html = scraperwiki.scrape("http://www.montgomeryschoolsmd.org/departments/regulatoryaccountability/glance/fy2011/fy2011.shtm")

import lxml.html           
root = lxml.html.fromstring(html)
index = 0
for table in root.cssselect("table"):
    index = index + 1
    if index == 8:
        for tr in table.cssselect("tr td"):
            if tr.text_content() != "" and tr.text_content()[-1] != "g":
                for a in tr.cssselect("a"):
                    print a.text_content()
                    if a.text_content() == 'Elementary School Summary':
                        sys.exit()
                    elif 'ES' in a.text_content():
                        schoolType = 'elementary'

                    elif 'MS' in a.text_content():
                        schoolType = 'middle'
                    elif 'HS' in a.text_content():
                        schoolType = 'high'
                    else:
                        schoolType = 'special'
                    fp = scraperwiki.scrape('http://montgomeryschoolsmd.org/' + a.attrib['href'])
                    parser = PDFParser(fp)
                    print parser
                    data = {
                          'school' : a.text_content(),
                          'schoolType': schoolType,
                          'link': a.attrib['href']
                    }
                    scraperwiki.sqlite.save(unique_keys=['school'], data=data)
        
import scraperwiki
import sys
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice

html = scraperwiki.scrape("http://www.montgomeryschoolsmd.org/departments/regulatoryaccountability/glance/fy2011/fy2011.shtm")

import lxml.html           
root = lxml.html.fromstring(html)
index = 0
for table in root.cssselect("table"):
    index = index + 1
    if index == 8:
        for tr in table.cssselect("tr td"):
            if tr.text_content() != "" and tr.text_content()[-1] != "g":
                for a in tr.cssselect("a"):
                    print a.text_content()
                    if a.text_content() == 'Elementary School Summary':
                        sys.exit()
                    elif 'ES' in a.text_content():
                        schoolType = 'elementary'

                    elif 'MS' in a.text_content():
                        schoolType = 'middle'
                    elif 'HS' in a.text_content():
                        schoolType = 'high'
                    else:
                        schoolType = 'special'
                    fp = scraperwiki.scrape('http://montgomeryschoolsmd.org/' + a.attrib['href'])
                    parser = PDFParser(fp)
                    print parser
                    data = {
                          'school' : a.text_content(),
                          'schoolType': schoolType,
                          'link': a.attrib['href']
                    }
                    scraperwiki.sqlite.save(unique_keys=['school'], data=data)
        
