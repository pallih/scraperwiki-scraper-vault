import re
import lxml.html
import scraperwiki
from urlparse import urljoin

base="http://treaties.un.org/Pages/ParticipationStatus.aspx"

sigre=re.compile(r'Signature',re.I)
datere=re.compile(r'(Ratification|Accession|Succession|Acceptance)')
countryre=re.compile(r'([^0-9]*)')

def unws(txt):
    return u' '.join(txt.split())

def toText(node):
    if node is None: return ''
    return ''.join([x.strip() for x in node.xpath(".//text()") if x.strip()]).replace(u"\u00A0",' ').strip()

def getFrag(url, path, retries=5):
    try:
        html=scraperwiki.scrape(url)
    except Exception, e:
        if hasattr(e, 'code') and e.code>=400 and e.code not in [504, 502]:
            print "[!] %d %s" % (e.code, url)
        if retries>0:
            timeout=4*(6-retries)
            time.sleep(timeout)
            html=getFrag(url, path, retries-1)
        else:
            raise
    return lxml.html.fromstring(html).xpath(path)

def convertRow(cells, fields):
    res={}
    for name, i in fields:
        tmp=toText(cells[i])
        if tmp:
            if name=='Country':
                tmp=countryre.search(tmp).group(1)
            res[name]=unws(tmp)
    return res

def toObj(header):
    res=[]
    fields={ 'Country': 0}
    for i, field in list(enumerate([''.join(x.xpath('.//text()')) for x in header.xpath('.//td')]))[1:]:
        if sigre.search(field):
            fields['Signature']=i
        elif datere.search(field):
            fields['Ratification']=i
    rows=header.xpath('./following-sibling::tr')
    for row in rows:
        items=row.xpath('td')
        value=convertRow(items, fields.items())
        if value:
            res.append(value)
    return res

for chap in getFrag(base, '//table[@id="ctl00_ContentPlaceHolder1_dgChapterList"]//tr'):
    chapter=''.join(chap.xpath('.//span//text()'))
    url=urljoin(base,chap.xpath('.//a')[0].get('href'))
    #print "chapter", chapter, url
    for trty in getFrag(url, '//table[@id="ctl00_ContentPlaceHolder1_dgSubChapterList"]//tr'):
        treaty=trty.xpath('.//a/text()')[0].split('  ')[0]
        tmp=treaty.split(u"\u00A0",1)
        treaty=tmp[0].replace(u"\u00A0",' ').strip()
        if len(tmp)>1:
            city=tmp[1].replace(u"\u00A0",' ').strip()
        else:
            city=None

        url=urljoin(base,trty.xpath('.//a')[0].get('href'))
        #print url
        #i=0
        header=getFrag(url,'//table//tr[@class="tableHdr"]//*[starts-with(.,"Participant")]/ancestor::tr[1]')
        if len(header)==0:
            continue
        pdf=header[0].xpath('//img[@title="View PDF"]/..')[0].get('href')
        if pdf:
            pdf=urljoin(base,pdf)
        for obj in toObj(header[0]):
            obj['Chapter']=chapter
            obj['Treaty']=treaty
            if city:
                obj['City']=city
            if pdf:
                obj['PDF']=pdf
            scraperwiki.sqlite.save(unique_keys=['Treaty', "Country"],  data=obj)
            #i+=1
        #print i, treaty
