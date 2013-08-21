#from lxml import etree
#from StringIO import StringIO
#import urllib2
 
#url = "http://www.team-cymru.org/News/secnews.rss"

#link = urllib2.urlopen(url)
#xml = link.read()

#context = etree.iterparse(StringIO(xml))
#print context
#for action, elem in context:
#    if not elem.text:
#        text = "None"
#    else:
#        text = elem.text
#    print action, elem.tag + " => " + text
 
