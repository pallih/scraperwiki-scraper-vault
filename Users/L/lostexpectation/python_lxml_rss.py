import scraperwiki
import urllib

xml = urllib.urlopen('http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml')
import lxml.etree as ET
doc = ET.fromstring(xml)
for item in doc.xpath('//item'):
    for elt in item.xpath('descendant::*'):
        print(ET.tostring(elt))

import scraperwiki
import urllib

xml = urllib.urlopen('http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml')
import lxml.etree as ET
doc = ET.fromstring(xml)
for item in doc.xpath('//item'):
    for elt in item.xpath('descendant::*'):
        print(ET.tostring(elt))

import scraperwiki
import urllib

xml = urllib.urlopen('http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml')
import lxml.etree as ET
doc = ET.fromstring(xml)
for item in doc.xpath('//item'):
    for elt in item.xpath('descendant::*'):
        print(ET.tostring(elt))

