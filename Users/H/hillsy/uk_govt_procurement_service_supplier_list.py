import scraperwiki
import lxml.html
import re
import urlparse

base_url = "http://www.buyingsolutions.gov.uk/suppliers/index.html"

def scrapeSupps(url):
    """Get a list of suppliers on each page"""

    # match supplier ID
    # /suppliers/details/supplier-2471/
    supp_re = r"""/suppliers/details/supplier-(\d+)/$"""

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    ldata = [ ]
    for a in root.cssselect("ol#suppliers li a"):
        href = a.attrib.get("href")
        supp_name = a.text_content()
        msupp_id = re.match(supp_re, href)
        assert msupp_id, href    
        data={"supp_id": msupp_id.group(1), "href": urlparse.urljoin(base_url, href), "supp_name": supp_name}
        ldata.append(data)
    scraperwiki.sqlite.save(unique_keys=["supp_id", "supp_name"], data = ldata)
    return root

def ScrapeByLetter():
    srch_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
    for srch_letter in srch_letters:
        full_url = "%s?start=%s" % (base_url, srch_letter)
        root = scrapeSupps(full_url)
        
        scount = root.cssselect("span.count")[0].text
        mpage = re.search("\(page (\d+) of (\d+)\)", scount)
        if not mpage:
            assert srch_letter >= 'O'
            continue
    
        npage = int(mpage.group(2))
        for i in range(2, npage+1):
            nurl = "%s&page_number=%s" % (full_url, i)
            nhtml = scrapeSupps(nurl)

#ScrapeByLetter()


import scraperwiki
import lxml.html
import re
import urlparse

base_url = "http://www.buyingsolutions.gov.uk/suppliers/index.html"

def scrapeSupps(url):
    """Get a list of suppliers on each page"""

    # match supplier ID
    # /suppliers/details/supplier-2471/
    supp_re = r"""/suppliers/details/supplier-(\d+)/$"""

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    ldata = [ ]
    for a in root.cssselect("ol#suppliers li a"):
        href = a.attrib.get("href")
        supp_name = a.text_content()
        msupp_id = re.match(supp_re, href)
        assert msupp_id, href    
        data={"supp_id": msupp_id.group(1), "href": urlparse.urljoin(base_url, href), "supp_name": supp_name}
        ldata.append(data)
    scraperwiki.sqlite.save(unique_keys=["supp_id", "supp_name"], data = ldata)
    return root

def ScrapeByLetter():
    srch_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
    for srch_letter in srch_letters:
        full_url = "%s?start=%s" % (base_url, srch_letter)
        root = scrapeSupps(full_url)
        
        scount = root.cssselect("span.count")[0].text
        mpage = re.search("\(page (\d+) of (\d+)\)", scount)
        if not mpage:
            assert srch_letter >= 'O'
            continue
    
        npage = int(mpage.group(2))
        for i in range(2, npage+1):
            nurl = "%s&page_number=%s" % (full_url, i)
            nhtml = scrapeSupps(nurl)

#ScrapeByLetter()


