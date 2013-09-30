import scraperwiki
import urllib
import re
import mechanize
import lxml.html
import urlparse

url = 'http://armstrade.sipri.org/armstrade/html/export_toplist.php'

data = {}

data['count'] = '122'
data['import_or_export'] = 'export'
data['calc_previous'] = '1'
data['low_year'] = '1950'
data['high_year'] = '2010'                            
data['filetype'] = 'html'                                
data['Action'] = 'Download'                            
                
param = urllib.urlencode(data)
#print param      
html = urllib.urlopen(url, param).read()
root = lxml.html.fromstring(html)

titles = root.cssselect("table[class='csvtable'] tr")[10][2:-1]
titles = [' ' + t.text_content() for t in titles]

for tr in root.cssselect("table[class='csvtable'] tr")[11:123]:
    row = [r.text_content().replace('&nbsp','') for r in tr[2:-1]]
    data = dict(zip( titles, row ) )
    #print data
    scraperwiki.sqlite.save(unique_keys=[' Supplier'], data=data)
         
    


import scraperwiki
import urllib
import re
import mechanize
import lxml.html
import urlparse

url = 'http://armstrade.sipri.org/armstrade/html/export_toplist.php'

data = {}

data['count'] = '122'
data['import_or_export'] = 'export'
data['calc_previous'] = '1'
data['low_year'] = '1950'
data['high_year'] = '2010'                            
data['filetype'] = 'html'                                
data['Action'] = 'Download'                            
                
param = urllib.urlencode(data)
#print param      
html = urllib.urlopen(url, param).read()
root = lxml.html.fromstring(html)

titles = root.cssselect("table[class='csvtable'] tr")[10][2:-1]
titles = [' ' + t.text_content() for t in titles]

for tr in root.cssselect("table[class='csvtable'] tr")[11:123]:
    row = [r.text_content().replace('&nbsp','') for r in tr[2:-1]]
    data = dict(zip( titles, row ) )
    #print data
    scraperwiki.sqlite.save(unique_keys=[' Supplier'], data=data)
         
    


