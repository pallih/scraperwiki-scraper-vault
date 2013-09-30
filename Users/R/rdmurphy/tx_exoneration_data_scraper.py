import scraperwiki
import lxml.html

SITE_URL = "http://www.law.umich.edu/special/exoneration/Pages/browse.aspx?SortField=State&SortDir=Asc&FilterField1=State&FilterValue1=Texas"

html = scraperwiki.scrape(SITE_URL)
root = lxml.html.fromstring(html)
rows = root.cssselect("table")[8][2:]

count = 0

for row in rows:
    print count
    blocks = row.cssselect("td")
    l_name = blocks[0].cssselect("td")[0].text_content()
    f_name = blocks[1].cssselect("td")[0].text_content()
    i_url = blocks[0].cssselect("a")[0].get("href")[-4:]
    print l_name, f_name, i_url
    count += 1

print count

import scraperwiki
import lxml.html

SITE_URL = "http://www.law.umich.edu/special/exoneration/Pages/browse.aspx?SortField=State&SortDir=Asc&FilterField1=State&FilterValue1=Texas"

html = scraperwiki.scrape(SITE_URL)
root = lxml.html.fromstring(html)
rows = root.cssselect("table")[8][2:]

count = 0

for row in rows:
    print count
    blocks = row.cssselect("td")
    l_name = blocks[0].cssselect("td")[0].text_content()
    f_name = blocks[1].cssselect("td")[0].text_content()
    i_url = blocks[0].cssselect("a")[0].get("href")[-4:]
    print l_name, f_name, i_url
    count += 1

print count

