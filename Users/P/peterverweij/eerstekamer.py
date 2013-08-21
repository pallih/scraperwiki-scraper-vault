import scraperwiki
import urllib2 
import lxml.etree
url = "http://www.eerstekamer.nl/id/vi8hbyhqdcwy/document_extern/ledenlijst/f=/vjamkorfbwnn.pdf"
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)
lines = root.findall(".//text/b")
print lines
for el in lines:
    if el.tag =="text":
        print el.text, el.attrib
       # if el.attrib=='font'
        #print el.attrib
       


#print lxml.etree.tostring(root, pretty_print=True)

#pages = list(root)
#print len(pages)
#   for el in page:
 #       if el.tag == "text":
  #          print el.text, el.attrib
   #         if el.attrib == "['font': '2']":
    #            print el.text
       


import scraperwiki
import urllib2 
import lxml.etree
url = "http://www.eerstekamer.nl/id/vi8hbyhqdcwy/document_extern/ledenlijst/f=/vjamkorfbwnn.pdf"
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)
lines = root.findall(".//text/b")
print lines
for el in lines:
    if el.tag =="text":
        print el.text, el.attrib
       # if el.attrib=='font'
        #print el.attrib
       


#print lxml.etree.tostring(root, pretty_print=True)

#pages = list(root)
#print len(pages)
#   for el in page:
 #       if el.tag == "text":
  #          print el.text, el.attrib
   #         if el.attrib == "['font': '2']":
    #            print el.text
       


