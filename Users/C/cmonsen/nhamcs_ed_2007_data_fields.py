import scraperwiki
import urllib2
import lxml.etree

url = "http://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHAMCS/doc07.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

data = []
count = 1
for page in pages[32:73]:
    for el in list(page):
#        if count > 200:
#        print el.attrib
#        if el.text is not None:
#            print el.text
        if el.tag == "text" and (int(el.get("left"))==72 or int(el.get("left"))==70):
            if el.text is not None:
                if el.text.strip().isdigit():
                    itemn = el.text.strip()
                    length = el.getnext().text.strip()
                    range = el.getnext().getnext().text.strip()
                    label = el.getnext().getnext().getnext().text.strip().split(" ")[0].replace("[","").replace("]","")
                    point = {"id":itemn,"length":length,"range":range,"label":label}
                    data.append(point)
                    print "Multiline: " + str(point)
                    count += 1
                else:
                    splitel = el.text.strip().split(" ")
                    if splitel[0].isdigit() and int(splitel[0]) < 500:
                        point = {"id":splitel[0],"length":splitel[1],"range":splitel[3],"label":splitel[4].replace("[","").replace("]","")}
                        data.append(point)
                        print "Oneline: " + str(point)
                        count += 1

scraperwiki.sqlite.save(["id"], data)

# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/

import scraperwiki
import urllib2
import lxml.etree

url = "http://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHAMCS/doc07.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

data = []
count = 1
for page in pages[32:73]:
    for el in list(page):
#        if count > 200:
#        print el.attrib
#        if el.text is not None:
#            print el.text
        if el.tag == "text" and (int(el.get("left"))==72 or int(el.get("left"))==70):
            if el.text is not None:
                if el.text.strip().isdigit():
                    itemn = el.text.strip()
                    length = el.getnext().text.strip()
                    range = el.getnext().getnext().text.strip()
                    label = el.getnext().getnext().getnext().text.strip().split(" ")[0].replace("[","").replace("]","")
                    point = {"id":itemn,"length":length,"range":range,"label":label}
                    data.append(point)
                    print "Multiline: " + str(point)
                    count += 1
                else:
                    splitel = el.text.strip().split(" ")
                    if splitel[0].isdigit() and int(splitel[0]) < 500:
                        point = {"id":splitel[0],"length":splitel[1],"range":splitel[3],"label":splitel[4].replace("[","").replace("]","")}
                        data.append(point)
                        print "Oneline: " + str(point)
                        count += 1

scraperwiki.sqlite.save(["id"], data)

# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/

