import scraperwiki
import lxml.html, lxml.cssselect

# constants
baseurl="http://ckan.net"

# source
htmlurl="http://ckan.net/tag/finance"

# load
root = lxml.html.parse(htmlurl).getroot()

# parse
for main in root.cssselect('div[id="main"]'):
  for elem in main.cssselect('div[class="header"] > span > a'):
    # parse title and href
    title=elem.text
    href=elem.attrib.get('href')
    # new record
    record = {}
    record['title'] = title
    record['href'] = baseurl+href
    print record, '------------'
    scraperwiki.datastore.save(unique_keys=['title'], data=record)
import scraperwiki
import lxml.html, lxml.cssselect

# constants
baseurl="http://ckan.net"

# source
htmlurl="http://ckan.net/tag/finance"

# load
root = lxml.html.parse(htmlurl).getroot()

# parse
for main in root.cssselect('div[id="main"]'):
  for elem in main.cssselect('div[class="header"] > span > a'):
    # parse title and href
    title=elem.text
    href=elem.attrib.get('href')
    # new record
    record = {}
    record['title'] = title
    record['href'] = baseurl+href
    print record, '------------'
    scraperwiki.datastore.save(unique_keys=['title'], data=record)
