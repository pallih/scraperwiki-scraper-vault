import scraperwiki
import urlparse
import lxml.html
import re
from BeautifulSoup import BeautifulSoup

# Scrape A-Z journals name, issn and dates, if available

starturl = 'http://sfx.hul.harvard.edu/sfx_local/az/?&param_current_view_save=table'
starthtml = scraperwiki.scrape(starturl)
startroot = lxml.html.fromstring(starthtml)

i = 0
t = 0

# Grab A-Z list URLs
for az in startroot.cssselect("tr.Block a.ABC"): 
    azurl = urlparse.urljoin(starturl, az.attrib['href'])
    azhtml = scraperwiki.scrape(azurl)
    azroot = lxml.html.fromstring(azhtml)

# Grab the page number for looping
    aztd = azroot.cssselect("td.LabelBold")[4].text.split( )[4]
    aznum = int(aztd)

# Loop by page number, replace in URL
    for i in range(aznum):
        repstr = 'param_jumpToPage_value='
        repstr += str(i+1)
        repstr += '&'
        azurlminus = azurl.replace('param_jumpToPage_value=&', repstr)

# Start grabbing the A-Z table w/ name and issn
        aztablehtml = scraperwiki.scrape(azurlminus)
        aztableroot = lxml.html.fromstring(aztablehtml)

        c = 0
        data = {}

# Loop through rows/titles and add to db
        for aztable in aztableroot.cssselect("table.table_563 tr td.TableRow"):
            azinhtml = lxml.html.tostring(aztable)

            # Remove HTML
            unhtmlaz = re.sub('<[^>]*>', '', azinhtml)
            name_issn = BeautifulSoup(unhtmlaz, convertEntities=BeautifulSoup.HTML_ENTITIES)
    
            # Check whether name or issn
            if c == 0 :
                data['name'] = name_issn
            if c == 1 :
                data['issn'] = name_issn

            if c < 4 :
                c += 1
            if c == 3 :
                t += 1
                data['id'] = t
                # Add to db
                scraperwiki.sqlite.save(["id"], data)
                c = 0



