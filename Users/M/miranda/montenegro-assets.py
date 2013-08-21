# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

scraperwiki.metadata.save("private_columns", ["Matični_broj"])

def scrapesingle(url):
    root = lxml.html.parse(url).getroot()
    root1 = root
    r = 0
    while root1 is not None:
        break
        print "*** root ***", r
        FindContentsRecurse(root1)
        root1 = root1.getnext()
        r += 1

    # place your cssselection case here and extract the values
    table = None
    for tr in root.cssselect('html body table td table tr td table tr td table'):
        if re.search("Mati&#269;ni broj", lxml.etree.tostring(tr)):
            table = tr
            break
    if not table:
        print "missing number:", url[-5:]
        return
    rows = [ ]
    for tr in table:
        row = [ ]
        for td in tr:
            row.append(td[0][0].text)
        rows.append(row)
    data = dict(zip(rows[0], rows[1]))
    data["url"] = url
    scraperwiki.datastore.save(unique_keys=["url"], data=data)
    

for l in range(1, 100):
    url = "http://www.nekretnine.co.me/kp.php?type=ln&srez=15&ko=81&list=%d" % l
    scrapesingle(url)
        

                        

