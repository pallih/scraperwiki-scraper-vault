import cgi           
import os
import requests
import chardet
import scraperwiki
import sys
get = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
url=get.get('url')
name=get.get('name')
if not name: 
    name='csv'

if not url: print "No url specified."
try:
    text=requests.get(url, verify=False).content
except Exception, e:
    print "URL Error: ", e
if not text: print "No text found."

#print 'A', repr(text[:1000])
newtext=text.decode('utf-8')
#newtext = u'\x93'
# \x93 instead of ", for example at this stage
#print 'B', repr(newtext[:1000])
newtext=newtext.replace(u'\u200b',u' ')
newtext=newtext.encode('latin-1')
print 'C', repr(newtext[:1000])
newtext=newtext.decode('cp1252')
print 'D', repr(newtext[:1000])
print sys.stdout.__class__
print newtext[:1000].encode('ascii')
exit()
# but it's secretely actually CP1252
scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")
scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment;filename=%s.csv" % name)
print newtext[:1000]