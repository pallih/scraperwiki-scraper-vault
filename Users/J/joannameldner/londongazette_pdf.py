import scraperwiki
import lxml.html
import urllib2
import lxml.etree
         
#scraperwiki.sqlite.attach("londongazette")
#scraperwiki.sqlite.execute("create table pdfs as select * from londongazette.pdfs order by id")

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


scraperwiki.sqlite.save_var('last_page', 0)
a=scraperwiki.sqlite.get_var('last_page')

linklist=[]
linklist = scraperwiki.sqlite.select("* from pdfs where id>="+str(a))

record = {}

for i in linklist:
#check if line has "water resources act" if so, collect & move to next line
#if line does not start with a bracket, then number(s) , then bracket -> append and move on.
#if line starts with number in brackets, append, save record, empty record, move on.

    scraperwiki.sqlite.save_var('last_page', i['id'])
    url =i['pdflink']
    pdfdata = urllib2.urlopen(url).read()

    #print "The pdf file has %d bytes" % len(pdfdata)

    xmldata = scraperwiki.pdftoxml(pdfdata,'-hidden')
    #print "After converting to xml it has %d bytes" % len(xmldata)
    #print "The first 8000 characters are: ", xmldata[:8000]

    root = lxml.etree.fromstring(xmldata)
    pages = list(root)

    #print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

    page = pages[0]
    text=''
    empty=0
    id=1
    
    for el in list(page):
        if el.tag == "text":
            #if empty==2:
                #print '----' +  text
            #    record['sourceurl']=url
            #    record['id']=id
            #    record['data']=text
                #text=text.replace('\n',' ').replace('\r',' ').replace('  ',' ')
                #record['person']=text.partition('Take notice that')[2].partition(' of ')[0]
                #record['address']=text.partition('Take notice that')[2].partition(' of ')[2].partition(' is applying')[0]
                #record['region']=text.partition('NATIONAL RIVERS AUTHORITY')[2].partition('<i>')[0]
                #record['water_source']=text.partition('abstract water from ')[2].partition(' at ')[0]
                #record['gridref']=text.partition('National Grid Reference')[2]
                ##record['town']=text.partition('National Grid Reference ')[2].partition(' at ')[2].partition('.')[0]
                #record['volume']=text.partition('rates')[2].partition('The water will be used')[0]
                #record['use']=text.partition('The water will be used')[2]
            #    scraperwiki.sqlite.save(['sourceurl','id'], record,'notices')
            #    text=''
            #    empty=0
            #    id=id+1
                 
            #if el.text is None:
            #    empty=empty+1
            #text=text + '\n' + gettext_with_bi_tags(el)
            
            ##print el.attrib, gettext_with_bi_tags(el)
            ##print empty,el.text,' |||| ', gettext_with_bi_tags(el)
            ##print gettext_with_bi_tags(el)
            ##print text
            text=gettext_with_bi_tags(el).replace('    ',' ').replace('   ',' ').replace('  ',' ').replace('\n',' ')

        #SET STARTING TRIGER
            if 'WATER RESOURCES ACT' in texp.upper():
                trigger=1

        #SET STOP TRIGER
            if 'BRACKET NUMBER BRACKET' in texp.upper():
                ^\([0-9]\)
                trigger=1


            if trigger==1:
                #concatenate text to notice_text
                notice_text = notice_text + '\n' + text
    
    ##scraperwiki.sqlite.execute("alter table notices add column info text")
    ##scraperwiki.sqlite.execute("update notices set info=data.partition('Take notice that')[2]")

import scraperwiki
import lxml.html
import urllib2
import lxml.etree
         
#scraperwiki.sqlite.attach("londongazette")
#scraperwiki.sqlite.execute("create table pdfs as select * from londongazette.pdfs order by id")

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


scraperwiki.sqlite.save_var('last_page', 0)
a=scraperwiki.sqlite.get_var('last_page')

linklist=[]
linklist = scraperwiki.sqlite.select("* from pdfs where id>="+str(a))

record = {}

for i in linklist:
#check if line has "water resources act" if so, collect & move to next line
#if line does not start with a bracket, then number(s) , then bracket -> append and move on.
#if line starts with number in brackets, append, save record, empty record, move on.

    scraperwiki.sqlite.save_var('last_page', i['id'])
    url =i['pdflink']
    pdfdata = urllib2.urlopen(url).read()

    #print "The pdf file has %d bytes" % len(pdfdata)

    xmldata = scraperwiki.pdftoxml(pdfdata,'-hidden')
    #print "After converting to xml it has %d bytes" % len(xmldata)
    #print "The first 8000 characters are: ", xmldata[:8000]

    root = lxml.etree.fromstring(xmldata)
    pages = list(root)

    #print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

    page = pages[0]
    text=''
    empty=0
    id=1
    
    for el in list(page):
        if el.tag == "text":
            #if empty==2:
                #print '----' +  text
            #    record['sourceurl']=url
            #    record['id']=id
            #    record['data']=text
                #text=text.replace('\n',' ').replace('\r',' ').replace('  ',' ')
                #record['person']=text.partition('Take notice that')[2].partition(' of ')[0]
                #record['address']=text.partition('Take notice that')[2].partition(' of ')[2].partition(' is applying')[0]
                #record['region']=text.partition('NATIONAL RIVERS AUTHORITY')[2].partition('<i>')[0]
                #record['water_source']=text.partition('abstract water from ')[2].partition(' at ')[0]
                #record['gridref']=text.partition('National Grid Reference')[2]
                ##record['town']=text.partition('National Grid Reference ')[2].partition(' at ')[2].partition('.')[0]
                #record['volume']=text.partition('rates')[2].partition('The water will be used')[0]
                #record['use']=text.partition('The water will be used')[2]
            #    scraperwiki.sqlite.save(['sourceurl','id'], record,'notices')
            #    text=''
            #    empty=0
            #    id=id+1
                 
            #if el.text is None:
            #    empty=empty+1
            #text=text + '\n' + gettext_with_bi_tags(el)
            
            ##print el.attrib, gettext_with_bi_tags(el)
            ##print empty,el.text,' |||| ', gettext_with_bi_tags(el)
            ##print gettext_with_bi_tags(el)
            ##print text
            text=gettext_with_bi_tags(el).replace('    ',' ').replace('   ',' ').replace('  ',' ').replace('\n',' ')

        #SET STARTING TRIGER
            if 'WATER RESOURCES ACT' in texp.upper():
                trigger=1

        #SET STOP TRIGER
            if 'BRACKET NUMBER BRACKET' in texp.upper():
                ^\([0-9]\)
                trigger=1


            if trigger==1:
                #concatenate text to notice_text
                notice_text = notice_text + '\n' + text
    
    ##scraperwiki.sqlite.execute("alter table notices add column info text")
    ##scraperwiki.sqlite.execute("update notices set info=data.partition('Take notice that')[2]")

