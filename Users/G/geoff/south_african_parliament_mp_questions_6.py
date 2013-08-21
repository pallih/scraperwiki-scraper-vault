import scraperwiki
import urllib2
import lxml.etree
import sys
import re, os
import lxml.html  
import json 
import dateutil.parser 
import string 

#scraperwiki.sqlite.execute("create table completed_documents (`url` string)")   
#sys.exit()

def getdocument(getfile):
    file = getfile
    pdfdata = urllib2.urlopen(file).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)
    
    try:
        root = lxml.etree.fromstring(xmldata)
    except:
        print getfile, " failed"
        return False
    pages = list(root)
    
    
    def gettext_with_bi_tags(el):
        res = [ ]
        if el.text:
            #print 'text',el.text
            res.append(el.text)
        for lel in el:
            #print 'lel:', lel.text
            res.append("<%s>" % lel.tag)
            res.append(gettext_with_bi_tags(lel))
            res.append("</%s>" % lel.tag)
            if el.tail:
                #print 'tail', el.tail
                res.append(el.tail)
        return "".join(res)
    
    #page = pages[8]
    
    #for el in list(pages[36]): #for el in list(page)[:300]:
    #    if el.tag == "text":
    #        print el.attrib, re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)
    inquestion=0
    intro=''
    question=''
    number1=''
    number2=''
    started=0
    questiontype=''
    translated=0
    document=''
    house=''
    session=''
    date=''
    questionto='' #for multi line question intros
    startintro=False
    for page in pages:
        for el in list(page): #for el in list(page)[:300]:
            if el.tag == "text":
                if re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)=='<b>SUMMARY OF QUESTIONS FOR WRITTEN REPLY NOT YET REPLIED TO </b>':
                    return True
                if page.attrib.get('number')=='1' and el.attrib['font']=='0' and date=='':
                    tmpdate=re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1).replace('<i>','').replace('</i>','').partition(',')
                    if tmpdate[2]!='':
                        tmpdate2=tmpdate[2].partition(']')
                        date=dateutil.parser.parse(tmpdate2[0]).date()
                    #print tmpdate, date
                if ((el.attrib['font']=='3' and not re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1).isdigit()) or (el.attrib['font']=='6') ) and page.attrib.get('number')=='1' and house=='':
                    house=re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1).replace('<b>','').replace('</b>','')
                    if (not 'NATIONAL ASSEMBLY' in house) and (not 'NATIONAL COUNCIL OF PROVINCES' in house):
                        house=''
                    if 'NATIONAL ASSEMBLY' in house:
                        house='NATIONAL ASSEMBLY'
                    if 'NATIONAL COUNCIL OF PROVINCES' in house:
                        house='NATIONAL COUNCIL OF PROVINCES'
                if page.attrib.get('number')=='1' and (el.attrib['top']=='122' or el.attrib['top']=='118' or el.attrib['top']=='162'):
                    session=session+re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)
                if el.attrib['font']=='2' and el.attrib['top']=='1197':
                    document=re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1).replace('&#9472;','-')
                if re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)=='<b>QUESTIONS FOR ORAL REPLY </b>':
                    started=1
                    questiontype='oral'
                if questiontype=='oral' and (el.attrib['font']=='9' or el.attrib['font']=='11'):
                    questionto=re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1).replace('<b>','').replace('</b>','')
                if re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)=='<b>QUESTIONS FOR WRITTEN REPLY </b>':
                    questiontype='written'
                    questionto=''
                    started=1
                if started==0:
                    continue
                #print re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)
                #text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)
                #print text
                if ((el.attrib['font']=='4' and not re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)=='(1) ') or el.attrib['font']=='7' or el.attrib['font']=='11') and ("ask" in re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1) or re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1).replace('<b>','').replace('</b>','').replace('.','').replace(' ','').isdigit() or startintro) or (el.attrib['font']=='15' and startintro):
                    startintro=True
                    inquestion=1
                    intro=intro+re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1).replace('<b>','').replace('</b>','').replace('&#9632;','')
                    #print 'question' , intro
                else:
                    if inquestion and re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)=='<b>&#8224;</b>':
                        translated=1 
                    #print el.attrib['height'],re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)
                    if (el.attrib['height']=='13' or el.attrib['height']=='11') and inquestion and (el.attrib['font']=='12' or el.attrib['font']=='11' or el.attrib['font']=='2' or el.attrib['font']=='13' or el.attrib['font']=='10' or el.attrib['font']=='14' or el.attrib['font']=='9') and not re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)=='<b>&#8224;</b>' and not 'INTERNAL QUESTION PAPER: NATIONAL ASSEMBLY NO' in re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1):
                        inquestion=0
                        number1=re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)
                        parts = intro.partition('.')
                        title=''
                        if not parts[1]=='.':
                            title=intro.translate(None, string.digits)
                            number2=intro.replace(title,'')
                        else:
                            number2 = parts[0]
                            title=parts[2]
                        #print number2, title
                        tmp=session.partition(']')
                        #session=tmp[2]
                        data = {'title':title, 'question':question, 'number1':number1 , 'number2':number2, 'translated':translated, 'type':questiontype, 'questionto':questionto, 'document':document, 'house':house, 'session':tmp[2],'date':date, 'source':getfile}
                        #print data
                        scraperwiki.sqlite.save(unique_keys=[], data=data)
                        #print parts[2]
                        #print question
                        #print number1 , number2, translated, questiontype
                        #print '-----'
                        question='' 
                        intro='' 
                        number = '' 
                        translated=0
                        #print 'finish'
                    else:
                        if "ask" in re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1) and not "ask" in intro and inquestion:
                            startintro=True
                            inquestion=1
                            intro=intro+re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1).replace('<b>','').replace('</b>','')
                        elif (el.attrib['font']=='0' or el.attrib['font']=='1' or el.attrib['font']=='4' or el.attrib['font']=='12') and inquestion and not re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)=='<b>&#8224;</b>' and not (el.attrib['top']=='123' and el.attrib['left']=='131'):
                            question=question+re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1)
                            #print 'answer'
                #print el.attrib, gettext_with_bi_tags(el)
                if startintro and not "ask" in re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(el)).group(1):
                    startintro=False
    return True

#direct scraping of parliament page with list of internal question papers failed due to timeouts, separate php scraper retrieves list of links

#getdocument('http://www.parliament.gov.za/live/commonrepository/Processed/20110729/218675_1.pdf')
#sys.exit()

file = urllib2.urlopen("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=south_africa_parliament_internal_question_papers&query=select%20*%20from%20%60swdata%60%20where%20date%3E'2009-04-01'%20order%20by%20date%20DESC")
urls = json.load(file)


#getdocument('http://www.parliament.gov.za/live/commonrepository/Processed/20120808/445779_1.pdf')

print "Processing ",len(urls), " documents"

count=0
for url in urls:
    count+=1
    print "Document ", count
    if url['language']=='English' and url['type']=='.pdf': # and url['house']=='National Council of Provinces'
        past=scraperwiki.sqlite.select("* from completed_documents where `url`='"+url['url']+"'")
        if len(past)==0:
            getdocument(url['url'])
            scraperwiki.sqlite.save([], {'url':url['url']},'completed_documents')
    elif url['language']=='English':
        print url['url'],' is not a pdf'