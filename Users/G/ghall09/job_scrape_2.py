from urllib import urlopen
from lxml import etree
from BeautifulSoup import BeautifulSoup 
import re

#open and read webpage
webpage = urlopen("https://experian.taleo.net/careersection/2/moresearch.ftl?lang=en").read()


root = etree.Element(webpage)
print(root.tag)


#locate job title
title = re.compile("api.fillList(.*)")

#search for article title
findtitle = re.findall(title, webpage)

print findtitlefrom urllib import urlopen
from lxml import etree
from BeautifulSoup import BeautifulSoup 
import re

#open and read webpage
webpage = urlopen("https://experian.taleo.net/careersection/2/moresearch.ftl?lang=en").read()


root = etree.Element(webpage)
print(root.tag)


#locate job title
title = re.compile("api.fillList(.*)")

#search for article title
findtitle = re.findall(title, webpage)

print findtitle