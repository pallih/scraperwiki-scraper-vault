"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.irishstatutebook.ie/2010/statutory.html"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

for lk, no, title in sinos:
    url = "http://www.irishstatutebook.ie"+lk
    page = scraperwiki.scrape(url)
    #print page
    mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    if mdate:
        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    else:
        print "No date on", url
        date = None
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None
    
    data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata}
    scraperwiki.datastore.save(['url'], data)   
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.irishstatutebook.ie/2010/statutory.html"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

for lk, no, title in sinos:
    url = "http://www.irishstatutebook.ie"+lk
    page = scraperwiki.scrape(url)
    #print page
    mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    if mdate:
        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    else:
        print "No date on", url
        date = None
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None
    
    data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata}
    scraperwiki.datastore.save(['url'], data)   
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.irishstatutebook.ie/2010/statutory.html"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

for lk, no, title in sinos:
    url = "http://www.irishstatutebook.ie"+lk
    page = scraperwiki.scrape(url)
    #print page
    mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    if mdate:
        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    else:
        print "No date on", url
        date = None
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None
    
    data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata}
    scraperwiki.datastore.save(['url'], data)   
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.irishstatutebook.ie/2010/statutory.html"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

for lk, no, title in sinos:
    url = "http://www.irishstatutebook.ie"+lk
    page = scraperwiki.scrape(url)
    #print page
    mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    if mdate:
        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    else:
        print "No date on", url
        date = None
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None
    
    data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata}
    scraperwiki.datastore.save(['url'], data)   
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.irishstatutebook.ie/2010/statutory.html"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

for lk, no, title in sinos:
    url = "http://www.irishstatutebook.ie"+lk
    page = scraperwiki.scrape(url)
    #print page
    mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    if mdate:
        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    else:
        print "No date on", url
        date = None
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None
    
    data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata}
    scraperwiki.datastore.save(['url'], data)   
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.irishstatutebook.ie/2010/statutory.html"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

for lk, no, title in sinos:
    url = "http://www.irishstatutebook.ie"+lk
    page = scraperwiki.scrape(url)
    #print page
    mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    if mdate:
        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    else:
        print "No date on", url
        date = None
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None
    
    data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata}
    scraperwiki.datastore.save(['url'], data)   
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.irishstatutebook.ie/2010/statutory.html"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

for lk, no, title in sinos:
    url = "http://www.irishstatutebook.ie"+lk
    page = scraperwiki.scrape(url)
    #print page
    mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    if mdate:
        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    else:
        print "No date on", url
        date = None
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None
    
    data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata}
    scraperwiki.datastore.save(['url'], data)   
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.irishstatutebook.ie/2010/statutory.html"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

for lk, no, title in sinos:
    url = "http://www.irishstatutebook.ie"+lk
    page = scraperwiki.scrape(url)
    #print page
    mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    if mdate:
        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    else:
        print "No date on", url
        date = None
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None
    
    data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata}
    scraperwiki.datastore.save(['url'], data)   
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.irishstatutebook.ie/2010/statutory.html"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

for lk, no, title in sinos:
    url = "http://www.irishstatutebook.ie"+lk
    page = scraperwiki.scrape(url)
    #print page
    mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    if mdate:
        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    else:
        print "No date on", url
        date = None
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None
    
    data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata}
    scraperwiki.datastore.save(['url'], data)   
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.irishstatutebook.ie/2010/statutory.html"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

for lk, no, title in sinos:
    url = "http://www.irishstatutebook.ie"+lk
    page = scraperwiki.scrape(url)
    #print page
    mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    if mdate:
        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    else:
        print "No date on", url
        date = None
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None
    
    data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata}
    scraperwiki.datastore.save(['url'], data)   
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.irishstatutebook.ie/2010/statutory.html"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

for lk, no, title in sinos:
    url = "http://www.irishstatutebook.ie"+lk
    page = scraperwiki.scrape(url)
    #print page
    mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    if mdate:
        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    else:
        print "No date on", url
        date = None
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None
    
    data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata}
    scraperwiki.datastore.save(['url'], data)   
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.irishstatutebook.ie/2010/statutory.html"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

for lk, no, title in sinos:
    url = "http://www.irishstatutebook.ie"+lk
    page = scraperwiki.scrape(url)
    #print page
    mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    if mdate:
        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    else:
        print "No date on", url
        date = None
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None
    
    data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata}
    scraperwiki.datastore.save(['url'], data)   
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.irishstatutebook.ie/2010/statutory.html"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

for lk, no, title in sinos:
    url = "http://www.irishstatutebook.ie"+lk
    page = scraperwiki.scrape(url)
    #print page
    mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    if mdate:
        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    else:
        print "No date on", url
        date = None
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None
    
    data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata}
    scraperwiki.datastore.save(['url'], data)   
