import scraperwiki
import lxml.html
import re
import urllib2
import lxml.etree

#scraperwiki.sqlite.attach("londongazette_pdf")

#scraperwiki.sqlite.execute("CREATE TABLE `pdflist` (`id` integer, `sourceurl` text, `issue_no` text, `page_no` text)")

#linklist=[]
#record={}
#linklist = scraperwiki.sqlite.select("id, pdflink from londongazette_pdf.pdfs order by pdflink desc")

#for l in linklist:
#    record['id']=l['id']
#    record['sourceurl']=l['pdflink']
#    record['issue_no']=l['pdflink'].partition('issues/')[2].partition('/')[0]
#    record['page_no']=l['pdflink'].partition('issues/')[2].partition('/')[2].partition('/')[2].partition('/')[0]
#    scraperwiki.sqlite.save(['sourceurl','id'], record,'pdflist')


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

def find_begining(text):
    t=text.replace('\n',' ').upper()
    #RE = re.compile("(NOTICE OF APPLICATION|Application for Licence to abstract water|NOTIFICATION OF APPLICATION TO VARY A LICENCE TO ABSTRACT WATER|Notice that)", re.I | re.DOTALL)
    RE = re.compile("((APPLICATION FOR (A )*LICENCE TO ABSTRACT WATER)|NOTICE IS HEREBY GIVEN|NIOITICE IS HEREBY GIVEN)", re.I | re.DOTALL)
    r= RE.search(t)
    if (r!= None): b=r.start()
    else: b=None
    return b
def find_end(text, b):
    t=text.upper()
    RE = re.compile("((\n)\s*\\(([0-9]{3,4}))", re.I | re.DOTALL)
    r= RE.search(t,b)
    if (r!= None): e=r.start()
    else: e=None
    return e

urllist=[]
urllist = scraperwiki.sqlite.select("* from pdflist order by id asc")

for l in urllist:
    id=l['id']
#only do a set number or pdfs
    if id>6 : break
    text=''
    url=l['sourceurl']
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata,'-hidden')
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    page = pages[0]    
    
    for el in list(page):
        if el.tag == "text":
            record={}
            text=text + '\n' + gettext_with_bi_tags(el)
    text=text.replace('<i>For any late Notices see Contents list on last page</i>','')

    while len(text)>300:
        b=find_begining(text)
        if b==None: 
            print 'could not find begining - ',text
            break
        else:
             if 'Order under section' not in text[b:].replace('\n',' '):
                e=find_end(text,b)
                if e==None:
                    print 'cound not find end - ',text
                    break
                else:
                    #print b,e, text
                    notice=text[b:e]
                    #if 'Order under section' not in notice.replace('\n',' '): 
                    print 'NOTICE: ',notice
                    #remove idenfittied description & move on
                    text=text[e:]

print 'stop'
import scraperwiki
import lxml.html
import re
import urllib2
import lxml.etree

#scraperwiki.sqlite.attach("londongazette_pdf")

#scraperwiki.sqlite.execute("CREATE TABLE `pdflist` (`id` integer, `sourceurl` text, `issue_no` text, `page_no` text)")

#linklist=[]
#record={}
#linklist = scraperwiki.sqlite.select("id, pdflink from londongazette_pdf.pdfs order by pdflink desc")

#for l in linklist:
#    record['id']=l['id']
#    record['sourceurl']=l['pdflink']
#    record['issue_no']=l['pdflink'].partition('issues/')[2].partition('/')[0]
#    record['page_no']=l['pdflink'].partition('issues/')[2].partition('/')[2].partition('/')[2].partition('/')[0]
#    scraperwiki.sqlite.save(['sourceurl','id'], record,'pdflist')


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

def find_begining(text):
    t=text.replace('\n',' ').upper()
    #RE = re.compile("(NOTICE OF APPLICATION|Application for Licence to abstract water|NOTIFICATION OF APPLICATION TO VARY A LICENCE TO ABSTRACT WATER|Notice that)", re.I | re.DOTALL)
    RE = re.compile("((APPLICATION FOR (A )*LICENCE TO ABSTRACT WATER)|NOTICE IS HEREBY GIVEN|NIOITICE IS HEREBY GIVEN)", re.I | re.DOTALL)
    r= RE.search(t)
    if (r!= None): b=r.start()
    else: b=None
    return b
def find_end(text, b):
    t=text.upper()
    RE = re.compile("((\n)\s*\\(([0-9]{3,4}))", re.I | re.DOTALL)
    r= RE.search(t,b)
    if (r!= None): e=r.start()
    else: e=None
    return e

urllist=[]
urllist = scraperwiki.sqlite.select("* from pdflist order by id asc")

for l in urllist:
    id=l['id']
#only do a set number or pdfs
    if id>6 : break
    text=''
    url=l['sourceurl']
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata,'-hidden')
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    page = pages[0]    
    
    for el in list(page):
        if el.tag == "text":
            record={}
            text=text + '\n' + gettext_with_bi_tags(el)
    text=text.replace('<i>For any late Notices see Contents list on last page</i>','')

    while len(text)>300:
        b=find_begining(text)
        if b==None: 
            print 'could not find begining - ',text
            break
        else:
             if 'Order under section' not in text[b:].replace('\n',' '):
                e=find_end(text,b)
                if e==None:
                    print 'cound not find end - ',text
                    break
                else:
                    #print b,e, text
                    notice=text[b:e]
                    #if 'Order under section' not in notice.replace('\n',' '): 
                    print 'NOTICE: ',notice
                    #remove idenfittied description & move on
                    text=text[e:]

print 'stop'
