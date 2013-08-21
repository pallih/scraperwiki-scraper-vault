import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

url = 'http://www.tiobe.com/index.php/content/paperinfo/tpci/index.html'




# unfortunately does not work as Tiobe requires javascript enabled in browser!
def Main():
    root = lxml.html.parse(url).getroot()
    trs = root.cssselect('#Table2')[0].cssselect('tr')
    headings = trs[0]
    for trow in trs[1:]:
        tds = tablerow.cssselect('td')
        print dict(zip(headings, tds))
        # scraperwiki.datastore.save(['code'], {'code': code, 'name': country_name})
        
Main()
