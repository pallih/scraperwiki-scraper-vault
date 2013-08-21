import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime


def ConvertDate(data, key):
    if data.get(key):
        mdate = re.match('(\d+)/(\d+)/(\d+)$', data[key])
        data[key] = datetime.datetime(int(mdate.group(3)), int(mdate.group(1)), int(mdate.group(2)))


def parsepage(id):
    url = "http://www.ni-environment.gov.uk/content-databases-buildview?id=%d" % id
    root = None
    for i in range(3):
        try:
            root = lxml.html.parse(url).getroot()
            break
        except IOError:
            pass
    
    if root is None:
        print "No scrape", id
        return

    data = { }
    for s in root.cssselect('form#frmMain strong'):
        span = list(s.getparent())[-1]
        assert span.tag == 'span', lxml.etree.tostring(s.getparent())
        data[s.text.strip(': ')] = span.text

    for h4 in root.cssselect('form#frmMain h4'):
        span = h4.getnext().getnext()
        if span.tag == 'p':
            v = ''
        else:
            assert span.tag == 'span', lxml.etree.tostring(span)
            v = span.text
        data[h4.text.strip(': ')] = v  

    data['id'] = id
    data['url'] = url

    #print id, data.get('Address')

    ConvertDate(data, 'Date of Listing')
    ConvertDate(data, 'Date of De-listing')

    scraperwiki.datastore.save(unique_keys=['id'], data=data, date=data.get('Date of Listing'))


for id in range(4072, 4900):
    parsepage(id)

                        

