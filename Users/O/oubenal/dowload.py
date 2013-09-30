from urllib2 import urlopen
from lxml.html import fromstring, tostring

download = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
raw = download.read()

html = fromstring(raw)
#print tostring(html)from urllib2 import urlopen
from lxml.html import fromstring, tostring

download = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
raw = download.read()

html = fromstring(raw)
#print tostring(html)