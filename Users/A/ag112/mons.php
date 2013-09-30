import lxml.html

url = "http://jobsearch.monsterindia.com/searchresult.html?fts=websphere&loc=199&loc=5&mne=6&mxe=&ind=65&jbc=22&ctp=0&day=30"
root = lxml.html.parse(url).getroot()

# alternatively you can use:
#   html = urllib2.urlopen(url).read()
#   root = lxml.html.fromstring(html)

print "The root element is:", root
print "The elements in this root element are:", list(root)
print "The elements two levels down are:", [ list(el)  for el in root ]

divs = root.cssselect("div")
print "There are %d elements with tag div in this page" % len(divs)
print "Their corresponding attributes are:", [div.attrib  for div in divs ]

crdiv = root.cssselect("div#divCopyright")[0]
print "The copyright message is: ", lxml.html.tostring(crdiv)

# Click on "Quick help" and select lxml cheat sheet for more advice

import lxml.html

url = "http://jobsearch.monsterindia.com/searchresult.html?fts=websphere&loc=199&loc=5&mne=6&mxe=&ind=65&jbc=22&ctp=0&day=30"
root = lxml.html.parse(url).getroot()

# alternatively you can use:
#   html = urllib2.urlopen(url).read()
#   root = lxml.html.fromstring(html)

print "The root element is:", root
print "The elements in this root element are:", list(root)
print "The elements two levels down are:", [ list(el)  for el in root ]

divs = root.cssselect("div")
print "There are %d elements with tag div in this page" % len(divs)
print "Their corresponding attributes are:", [div.attrib  for div in divs ]

crdiv = root.cssselect("div#divCopyright")[0]
print "The copyright message is: ", lxml.html.tostring(crdiv)

# Click on "Quick help" and select lxml cheat sheet for more advice

