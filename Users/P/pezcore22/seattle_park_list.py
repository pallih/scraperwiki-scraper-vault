import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.seattleschools.org/modules/cms/pages.phtml?pageid=197023")
root = lxml.html.fromstring(html)

print html

for tr in root.cssselect("div#sps-finder-elementary"):

    tds = tr.cssselect("tr")
    
    test = tds[0].cssselect("td")[0].text
    if not "School" in test:
        school = tds[0].cssselect("td")[0].cssselect("a")[0].text
    else:
        break
    #principal = tds[1].cssselect("td")[1].cssselect("a")[0].text
    #address = tds[1].cssselect("td")[2].cssselect("a")[0].text

    data = {
       'School' : school,
      # 'Principal' : principal,
      # 'Address' : address
   }



    scraperwiki.sqlite.save(unique_keys=['School'], data=data)

# Blank Python

import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.seattleschools.org/modules/cms/pages.phtml?pageid=197023")
root = lxml.html.fromstring(html)

print html

for tr in root.cssselect("div#sps-finder-elementary"):

    tds = tr.cssselect("tr")
    
    test = tds[0].cssselect("td")[0].text
    if not "School" in test:
        school = tds[0].cssselect("td")[0].cssselect("a")[0].text
    else:
        break
    #principal = tds[1].cssselect("td")[1].cssselect("a")[0].text
    #address = tds[1].cssselect("td")[2].cssselect("a")[0].text

    data = {
       'School' : school,
      # 'Principal' : principal,
      # 'Address' : address
   }



    scraperwiki.sqlite.save(unique_keys=['School'], data=data)

# Blank Python

