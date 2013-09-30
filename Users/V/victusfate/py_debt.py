import scraperwiki
html = scraperwiki.scrape("http://www.treasurydirect.gov/NP/BPDLogin?application=np")
print html

import lxml.html
root = lxml.html.fromstring(html)
for td in root.cssselect('td'):
    print lxml.html.tostring(td)

import datetime
now = datetime.datetime.now()
print now


#for td in root.cssselect('td'):
#    data = {'table_cell': td.text} # save data in dictionary
#    data["date"] = now
    # Choose unique keyname
#    scraperwiki.datastore.save(unique_keys=['table_cell'], data=data)



import scraperwiki
html = scraperwiki.scrape("http://www.treasurydirect.gov/NP/BPDLogin?application=np")
print html

import lxml.html
root = lxml.html.fromstring(html)
for td in root.cssselect('td'):
    print lxml.html.tostring(td)

import datetime
now = datetime.datetime.now()
print now


#for td in root.cssselect('td'):
#    data = {'table_cell': td.text} # save data in dictionary
#    data["date"] = now
    # Choose unique keyname
#    scraperwiki.datastore.save(unique_keys=['table_cell'], data=data)



