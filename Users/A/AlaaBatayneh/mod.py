import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=3fc5e794-0cb4-4c10-be10-557f169c4c92&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200&ctlPaging_page=1")

root = lxml.html.fromstring(html)
for tr in root.cssselect("table#searchcontractresults-table tbody tr"):
    tds = tr.cssselect("td")
    data = {
        'contract' : tds[0].text_content(),
        'location' : tds[1].text_content(),
        'date' : tds[2].text_content(),
        'value' : tds[3].text_content(),
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['contract'], data=data)

import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=3fc5e794-0cb4-4c10-be10-557f169c4c92&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200&ctlPaging_page=1")

root = lxml.html.fromstring(html)
for tr in root.cssselect("table#searchcontractresults-table tbody tr"):
    tds = tr.cssselect("td")
    data = {
        'contract' : tds[0].text_content(),
        'location' : tds[1].text_content(),
        'date' : tds[2].text_content(),
        'value' : tds[3].text_content(),
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['contract'], data=data)

