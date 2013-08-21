import scraperwiki
from scraperwiki import datastore
import lxml.html

# Looks like Barnet's web site now uses the harder-to-parse CSS table layouts rather than traditional HTML tables.
# Work in progress.

# Barnet now have an entirely different web site 2012-04. Back to a table layout
#
#

html = scraperwiki.scrape('http://barnet.moderngov.co.uk/mgMemberIndex.aspx?VW=TABLE&PIC=1&FN=')
root = lxml.html.fromstring(html)

for tr in root.cssselect('table#mgTable1 tr'):
#    print lxml.html.tostring(tr)
    tds = tr.cssselect('td a')
    if tds:
     councillor_name = tds[0].text
     councillor_href = tds[0].attrib['href']

    tds = tr.cssselect('td')
    if tds:
     print lxml.html.tostring(tds[2])
     councillor_ward = tds[3].text
     councillor_party = tds[2].text
     print councillor_name, councillor_href, councillor_ward, councillor_party
     # save to datastore
     data = {    'name' : councillor_name,
                'ward' : councillor_ward,           
                'party' : councillor_party,
                'link' : councillor_href,
                }
     scraperwiki.sqlite.save(unique_keys=['name', 'ward'], data=data)


