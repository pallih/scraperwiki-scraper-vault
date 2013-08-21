import scraperwiki
import lxml.html

url = "http://scraperwikiviews.com/run/python_lxml_cheat_sheet/"

root = lxml.html.parse(url).getroot()
print lxml.html.tostring(root)

# all paragraphs with class="kkk"
paras = root.cssselect("p.kkk")

print paras
for p in paras:
    print (p.tag, p.attrib.get("id"), p.text)

# For more, click on Quick help and select lxml cheat sheet

import scraperwiki
import lxml.html

url = "http://scraperwikiviews.com/run/python_lxml_cheat_sheet/"

root = lxml.html.parse(url).getroot()
print lxml.html.tostring(root)

# all paragraphs with class="kkk"
paras = root.cssselect("p.kkk")

print paras
for p in paras:
    print (p.tag, p.attrib.get("id"), p.text)

# For more, click on Quick help and select lxml cheat sheet

import scraperwiki
import lxml.html

url = "http://scraperwikiviews.com/run/python_lxml_cheat_sheet/"

root = lxml.html.parse(url).getroot()
print lxml.html.tostring(root)

# all paragraphs with class="kkk"
paras = root.cssselect("p.kkk")

print paras
for p in paras:
    print (p.tag, p.attrib.get("id"), p.text)

# For more, click on Quick help and select lxml cheat sheet

import scraperwiki
import lxml.html

url = "http://scraperwikiviews.com/run/python_lxml_cheat_sheet/"

root = lxml.html.parse(url).getroot()
print lxml.html.tostring(root)

# all paragraphs with class="kkk"
paras = root.cssselect("p.kkk")

print paras
for p in paras:
    print (p.tag, p.attrib.get("id"), p.text)

# For more, click on Quick help and select lxml cheat sheet

import scraperwiki
import lxml.html

url = "http://scraperwikiviews.com/run/python_lxml_cheat_sheet/"

root = lxml.html.parse(url).getroot()
print lxml.html.tostring(root)

# all paragraphs with class="kkk"
paras = root.cssselect("p.kkk")

print paras
for p in paras:
    print (p.tag, p.attrib.get("id"), p.text)

# For more, click on Quick help and select lxml cheat sheet

