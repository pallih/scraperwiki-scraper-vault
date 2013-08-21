# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html
import urllib2



html = urllib2.urlopen("http://9gag.com/").read()
soup = lxml.html.fromstring(html)

demo_name = soup.cssselect("span.comment")



print 'name: ' + demo_name[0].text

print 'name: ' + demo_name[1].text

print 'name: ' + demo_name[2].text

print 'name: ' + demo_name[3].text

print 'name: ' + demo_name[4].text

print 'name: ' + demo_name[5].text

print 'name: ' + demo_name[6].text





