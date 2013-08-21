import scraperwiki
import lxml.html
import re
import urlparse

base_url = "http://www.buyingsolutions.gov.uk/frameworks/full.html"

def scrapeFrameworks(url):
    """Get a list of frameworks on each page"""

    # match supplier ID
    # /frameworks/contract_details.html?contract_id=1185
    framework_re = r"""/frameworks/contract_details.html\?contract_id=(\d+)"""

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    ldata = [ ]
    for a in root.cssselect("div#framework_details h4 a"):
        href = a.attrib.get("href")
        framework_name = a.text_content()
        framework_id = re.match(framework_re, href)
        assert framework_id, href    
        data={"framework_id": framework_id.group(1), "href": urlparse.urljoin(base_url, href), "framework_name": framework_name}
        ldata.append(data)
    scraperwiki.sqlite.save(unique_keys=["framework_id", "framework_name"], data = ldata)
    return root

def ScrapeByLetter():
    srch_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
    for srch_letter in srch_letters:
        full_url = "%s?start=%s" % (base_url, srch_letter)
        root = scrapeFrameworks(full_url)
        
        scount = root.cssselect("span.count")[0].text
        mpage = re.search("\(page (\d+) of (\d+)\)", scount)
        if not mpage:
            assert srch_letter >= 'D'
            continue
    
        npage = int(mpage.group(2))
        for i in range(2, npage+1):
            nurl = "%s&page_number=%s" % (full_url, i)
            nhtml = scrapeFrameworks(nurl)

ScrapeByLetter()


