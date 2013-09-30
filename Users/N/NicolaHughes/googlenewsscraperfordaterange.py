import urllib2
from xml.dom.minidom import parseString

obj = parseString( urllib2.urlopen('http://news.google.com/news?q=obama+rice&hl=en&output=rss').read() )

pubdate = obj.getElementsByTagName('pubDate')[2:]

print pubdate

import urllib2
from xml.dom.minidom import parseString

obj = parseString( urllib2.urlopen('http://news.google.com/news?q=obama+rice&hl=en&output=rss').read() )

pubdate = obj.getElementsByTagName('pubDate')[2:]

print pubdate

