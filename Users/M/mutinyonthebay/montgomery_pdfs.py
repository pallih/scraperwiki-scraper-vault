import scraperwiki as sw
from lxml.html import fromstring

def grab_elementary_pdfs(url):
    root = fromstring(sw.scrape(url))
    
    ele_table = root.cssselect("table[width=588]")[1]
    ele_atags = ele_table.cssselect("tr")[1].cssselect("a")

    hrefs = ["http://montgomeryschoolsmd.org"+e.get("href") for e in ele_atags]
    
    for href in hrefs:
        sw.sqlite.save([], {'pdfurl':href})



grab_elementary_pdfs("http://montgomeryschoolsmd.org/departments/regulatoryaccountability/glance/fy2011/fy2011.shtm")