import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import mechanize

#Read the pdf from the url given and prints the total length bytes of the pdf 
url = "http://www.stoke.gov.uk/ccm/cms-service/download/asset/?asset_id=402535"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

#Convert the pdf dat into xmland prints the total length bytes of the xml
xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)

root = lxml.etree.fromstring(xmldata)
example=[]
example=xmldata
print example

#Read the number of pages
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
        print res
    return "".join(res)
row=[]
x=[]

for i in range(100):
    x.append(i+1)
print x

# print the first hundred text elements from the first page
#page0 = pages[0]

i=0
print "page"
print lxml.html.tostring(page)
#lxml.html.tostring(el)

i=1
count=1
for page in list(pages):    
    l_c=0
    for el in list(page):
        if el.tag == "text":
            if ((count<=240 and count>=1)or count==1):# and count!=11 and count!=14:
                count+=1
                continue            
            if l_c<20:
                row.append(gettext_with_bi_tags(el))
                l_c+=1
            else:
                row.append(gettext_with_bi_tags(el))
                l_c=0
                print row
    
                scraperwiki.sqlite.save(unique_keys=["slno"],data={"slno":i,"1":row[0],"2":row[1],"3":row[2],"4":row[3],"5":row[4],"6":row[5],"7":row[6],"8":row[7],"9":row[8],"10":row[9],"11":row[10],"12":row[11],"13":row[12],"14":row[13],"16":row[15],"14":row[13]})
                i+=1
                row=[]
            count+=1
    count=1
    print count
print "Completed"
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import mechanize

#Read the pdf from the url given and prints the total length bytes of the pdf 
url = "http://www.stoke.gov.uk/ccm/cms-service/download/asset/?asset_id=402535"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

#Convert the pdf dat into xmland prints the total length bytes of the xml
xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)

root = lxml.etree.fromstring(xmldata)
example=[]
example=xmldata
print example

#Read the number of pages
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
        print res
    return "".join(res)
row=[]
x=[]

for i in range(100):
    x.append(i+1)
print x

# print the first hundred text elements from the first page
#page0 = pages[0]

i=0
print "page"
print lxml.html.tostring(page)
#lxml.html.tostring(el)

i=1
count=1
for page in list(pages):    
    l_c=0
    for el in list(page):
        if el.tag == "text":
            if ((count<=240 and count>=1)or count==1):# and count!=11 and count!=14:
                count+=1
                continue            
            if l_c<20:
                row.append(gettext_with_bi_tags(el))
                l_c+=1
            else:
                row.append(gettext_with_bi_tags(el))
                l_c=0
                print row
    
                scraperwiki.sqlite.save(unique_keys=["slno"],data={"slno":i,"1":row[0],"2":row[1],"3":row[2],"4":row[3],"5":row[4],"6":row[5],"7":row[6],"8":row[7],"9":row[8],"10":row[9],"11":row[10],"12":row[11],"13":row[12],"14":row[13],"16":row[15],"14":row[13]})
                i+=1
                row=[]
            count+=1
    count=1
    print count
print "Completed"
