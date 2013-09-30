import scraperwiki
import urllib2
import lxml.etree

url = "http://www.bl.uk/reshelp/atyourdesk/docsupply/help/replycodes/dirlibcodes/Aug%202011.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

print 'Converting to xml....'
xmldata = scraperwiki.pdftoxml(pdfdata)
print '....done'

print 'parsing tree....'
root = lxml.etree.fromstring(xmldata)
print '...done'
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

frame=[]
recordset=[]
#page=pages[0]:
#in testing, should just use one page...
for page in pages:
    for el in list(page):
        if el.tag == "text":
            txt=gettext_with_bi_tags(el)
            #print el.attrib, txt
            frame.append(txt)
            if (txt=='Policy:'):
                tmpframe=frame[:-3]
                frame=frame[-3:]
                #print 'Record:',tmpframe, 'Next',frame
                ##recordset.append(tmpframe)
                #print tmpframe
                
                if len(tmpframe)>0:
                    if len(tmpframe[0])>3: policy=''
                    else: policy=tmpframe[0]
                    scraperwiki.sqlite.save(unique_keys=['code'], data={'code':tmpframe[1],'library':tmpframe[-1],'policy':policy,'misc':'::'.join(tmpframe[2:-1])})
            else:
                #print 'else:',frame,'...',txt
                pass

'''
for record in recordset:
    print record
    #scraperwiki.sqlite.save(unique_keys=['code'], data={'code':record[1],'policy':record[0],'misc':'::'.join(record[2:])})
'''import scraperwiki
import urllib2
import lxml.etree

url = "http://www.bl.uk/reshelp/atyourdesk/docsupply/help/replycodes/dirlibcodes/Aug%202011.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

print 'Converting to xml....'
xmldata = scraperwiki.pdftoxml(pdfdata)
print '....done'

print 'parsing tree....'
root = lxml.etree.fromstring(xmldata)
print '...done'
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

frame=[]
recordset=[]
#page=pages[0]:
#in testing, should just use one page...
for page in pages:
    for el in list(page):
        if el.tag == "text":
            txt=gettext_with_bi_tags(el)
            #print el.attrib, txt
            frame.append(txt)
            if (txt=='Policy:'):
                tmpframe=frame[:-3]
                frame=frame[-3:]
                #print 'Record:',tmpframe, 'Next',frame
                ##recordset.append(tmpframe)
                #print tmpframe
                
                if len(tmpframe)>0:
                    if len(tmpframe[0])>3: policy=''
                    else: policy=tmpframe[0]
                    scraperwiki.sqlite.save(unique_keys=['code'], data={'code':tmpframe[1],'library':tmpframe[-1],'policy':policy,'misc':'::'.join(tmpframe[2:-1])})
            else:
                #print 'else:',frame,'...',txt
                pass

'''
for record in recordset:
    print record
    #scraperwiki.sqlite.save(unique_keys=['code'], data={'code':record[1],'policy':record[0],'misc':'::'.join(record[2:])})
'''