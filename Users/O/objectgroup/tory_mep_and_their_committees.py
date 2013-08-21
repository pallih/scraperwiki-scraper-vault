# Blank Python
import urllib2
import lxml.html

url = "http://www.europarl.org.uk/section/your-meps/findmep?filter7=&filter0=**ALL**&filter1=Conservative+Party&filter2=**ALL**&filter6=**ALL**&filter4=**ALL**&submit=Submit"
filein = urllib2.urlopen(url)

print "The page has been loaded (see the 'Sources' tab below)"

html = filein.read()
print "The page is %d bytes long" % len(html)

print "The first 2000 characters of the page is:", html[:2000]

url = "http://scraperwiki.com"
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

