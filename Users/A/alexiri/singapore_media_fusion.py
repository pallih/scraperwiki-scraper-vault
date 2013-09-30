# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://www.smf.sg/MediaDirectory/Pages/OrganizationProfileList.aspx?showAllFlag=true&param=pubProfile&link=All&currentPageNumber=1000")

count = 0
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[class='popup_content']"):
    tds = tr.cssselect("p")
    
    data = {
      'Name'     : tds[0].text_content().replace("Org Name", ""),
      'Address'  : tds[3].text_content().replace("Address", ""),
      'Email'    : tds[6].text_content().replace("Email", ""),
      'Website'  : tds[7].text_content().replace("Website", ""),
      'Phone'    : tds[4].text_content().replace("Telephone", ""),
      'Fax'      : tds[5].text_content().replace("Fax", ""),
      'Description' : tds[2].text_content().replace("Description", ""),
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['Name'], data=data)
    count += 1

print 'Total count: %d' % count

# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://www.smf.sg/MediaDirectory/Pages/OrganizationProfileList.aspx?showAllFlag=true&param=pubProfile&link=All&currentPageNumber=1000")

count = 0
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[class='popup_content']"):
    tds = tr.cssselect("p")
    
    data = {
      'Name'     : tds[0].text_content().replace("Org Name", ""),
      'Address'  : tds[3].text_content().replace("Address", ""),
      'Email'    : tds[6].text_content().replace("Email", ""),
      'Website'  : tds[7].text_content().replace("Website", ""),
      'Phone'    : tds[4].text_content().replace("Telephone", ""),
      'Fax'      : tds[5].text_content().replace("Fax", ""),
      'Description' : tds[2].text_content().replace("Description", ""),
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['Name'], data=data)
    count += 1

print 'Total count: %d' % count

