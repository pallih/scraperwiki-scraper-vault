import scraperwiki, urllib,csv
import lxml.html


dataUrl='https://docs.google.com/spreadsheet/pub?key=0AirrQecc6H_vdGRPTUdxSUxCSTBDbVBzVHZGaU05UlE&output=csv'
data=csv.DictReader(urllib.urlopen(dataUrl))



# A function I usually bring in with lxml that strips tags and just give you text contained in an XML substree
## via http://stackoverflow.com/questions/5757201/help-or-advice-me-get-started-with-lxml/5899005#5899005
def flatten(el):           
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)


def brregLookup(coname):
    urlstub='http://w2.brreg.no/enhet/sok/treffliste.jsp?navn='
    url=urlstub+urllib.quote(coname)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    guessID=[]
    if root.xpath('.//b[starts-with(text(),"Orgnr")]')==[]: return []
    intable=root.xpath('.//b[starts-with(text(),"Orgnr")]/../../../.')[0]

    if intable!=[]: 
        for row in intable.xpath('tr')[1:]:
            cells=row.xpath('td')
            #print flatten(cells[0]).strip(),flatten(cells[1]).strip()
            guessID.append( (flatten(cells[0]).strip(),flatten(cells[1]).strip()) )
    return guessID

#brregLookup('A/S Norske Shell')
#brregLookup('ALTINEX OIL NORWAY AS')

def directors(root,company="",cid=''):
    bigdirs=[]
    dirsBlock=root.xpath("//div[@id='companyDirectors']")
    items= dirsBlock[0].xpath("div[@class='boxContent']/div")
    for i in items[:-2]:
        if len(i.xpath("div")):
            dirs={}
            #print flatten(i.xpath("div")[1]), flatten(i.xpath("div")[0])
            dirs['name']= flatten(i.xpath("div")[1])
            dirs['role']= flatten(i.xpath("div")[0]) 
            dirs['did']=i.xpath('div/a/@href')[0]
            dirs['company']=company
            dirs['cid']=cid
            bigdirs.append(dirs.copy())
    if bigdirs!={}:
        scraperwiki.sqlite.save(unique_keys=[], table_name='directors_', data=bigdirs)
    print bigdirs

def printCos(b):
    items= b.xpath("div[@class='boxContent']/div")
    cos=[]
    for i in items[1:-1]:
        #print flatten(i)
        #print flatten(i.xpath("label")[0]), i.xpath("div/text()")[0].strip('%')
        if len(i.xpath('label/a'))>0:
            #print i.xpath('label/a/@href')[0]
            cUrl=i.xpath('label/a/@href')[0]
        else: cUrl=''
        cos.append( {'co':flatten(i.xpath("label")[0]), 'amount':i.xpath("div/text()")[0].strip('%'), 'cUrl':cUrl } )
    return cos

def getCompanies(root,sel):
    cos=[]
    blocks=root.xpath("//div[@id='companyOwnership']")
    if sel=='other':
        if len(blocks)>1:
            cos=printCos(blocks[0])
        #print 'b',b.xpath("div[@class='boxHeader']/text()")
    else:
        if len(blocks)>1:
            cos=printCos(blocks[1])
        else:            
            cos=printCos(blocks[0])
    return cos

def patch(costmp,company="",cid=''):
    cos=[]
    for co in costmp:
        co['company']=company
        co['cid']=cid
        cos.append(co.copy())
    return cos

def shareholders(root,company="",cid=''):
    #print '..shareholders'
    costmp=getCompanies(root,'shareholders')
    cos=patch(costmp,company,cid)
    print 'shareholder',cos
    if cos!=[]:
        scraperwiki.sqlite.save(unique_keys=[], table_name='shareholders_', data=cos)

def otherCompanies(root,company="",cid=''):
    #print '..other'
    costmp=getCompanies(root,'other')
    cos=patch(costmp,company,cid)
    print 'other',cos
    if cos!=[]:
        scraperwiki.sqlite.save(unique_keys=[], table_name='othercos_', data=cos)
    
def getPureHelp_cScrape(cid):
    url='http://www.purehelp.no/company/details/'+str(cid)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    return root

#url='http://www.purehelp.no/company/details/914807077'
#root=getPureHelp_cScrape('914807077')
#otherCompanies(root)
#print '...'
#exit(-1)
#shareholders(root)
#print '...'
#directors(root)

done=[]
for d in data:
    cname=d['navn'].strip()
    cnames=brregLookup(cname)
    if cnames==[]:
        print 'pass',cname
        continue
    lookupId,lookupName=cnames[0]
    if lookupId in done: continue
    else: done.append(lookupId)

    if lookupName.lower()==cname.lower():
        print 'ok',cname,cnames[0]
    else:
        print 'ish?',cname,cnames[0]
    #lookupId='914807077'
    root=getPureHelp_cScrape(lookupId)
    shareholders(root,lookupName,lookupId)
    otherCompanies(root,lookupName,lookupId)
    directors(root,lookupName,lookupId)

import scraperwiki, urllib,csv
import lxml.html


dataUrl='https://docs.google.com/spreadsheet/pub?key=0AirrQecc6H_vdGRPTUdxSUxCSTBDbVBzVHZGaU05UlE&output=csv'
data=csv.DictReader(urllib.urlopen(dataUrl))



# A function I usually bring in with lxml that strips tags and just give you text contained in an XML substree
## via http://stackoverflow.com/questions/5757201/help-or-advice-me-get-started-with-lxml/5899005#5899005
def flatten(el):           
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)


def brregLookup(coname):
    urlstub='http://w2.brreg.no/enhet/sok/treffliste.jsp?navn='
    url=urlstub+urllib.quote(coname)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    guessID=[]
    if root.xpath('.//b[starts-with(text(),"Orgnr")]')==[]: return []
    intable=root.xpath('.//b[starts-with(text(),"Orgnr")]/../../../.')[0]

    if intable!=[]: 
        for row in intable.xpath('tr')[1:]:
            cells=row.xpath('td')
            #print flatten(cells[0]).strip(),flatten(cells[1]).strip()
            guessID.append( (flatten(cells[0]).strip(),flatten(cells[1]).strip()) )
    return guessID

#brregLookup('A/S Norske Shell')
#brregLookup('ALTINEX OIL NORWAY AS')

def directors(root,company="",cid=''):
    bigdirs=[]
    dirsBlock=root.xpath("//div[@id='companyDirectors']")
    items= dirsBlock[0].xpath("div[@class='boxContent']/div")
    for i in items[:-2]:
        if len(i.xpath("div")):
            dirs={}
            #print flatten(i.xpath("div")[1]), flatten(i.xpath("div")[0])
            dirs['name']= flatten(i.xpath("div")[1])
            dirs['role']= flatten(i.xpath("div")[0]) 
            dirs['did']=i.xpath('div/a/@href')[0]
            dirs['company']=company
            dirs['cid']=cid
            bigdirs.append(dirs.copy())
    if bigdirs!={}:
        scraperwiki.sqlite.save(unique_keys=[], table_name='directors_', data=bigdirs)
    print bigdirs

def printCos(b):
    items= b.xpath("div[@class='boxContent']/div")
    cos=[]
    for i in items[1:-1]:
        #print flatten(i)
        #print flatten(i.xpath("label")[0]), i.xpath("div/text()")[0].strip('%')
        if len(i.xpath('label/a'))>0:
            #print i.xpath('label/a/@href')[0]
            cUrl=i.xpath('label/a/@href')[0]
        else: cUrl=''
        cos.append( {'co':flatten(i.xpath("label")[0]), 'amount':i.xpath("div/text()")[0].strip('%'), 'cUrl':cUrl } )
    return cos

def getCompanies(root,sel):
    cos=[]
    blocks=root.xpath("//div[@id='companyOwnership']")
    if sel=='other':
        if len(blocks)>1:
            cos=printCos(blocks[0])
        #print 'b',b.xpath("div[@class='boxHeader']/text()")
    else:
        if len(blocks)>1:
            cos=printCos(blocks[1])
        else:            
            cos=printCos(blocks[0])
    return cos

def patch(costmp,company="",cid=''):
    cos=[]
    for co in costmp:
        co['company']=company
        co['cid']=cid
        cos.append(co.copy())
    return cos

def shareholders(root,company="",cid=''):
    #print '..shareholders'
    costmp=getCompanies(root,'shareholders')
    cos=patch(costmp,company,cid)
    print 'shareholder',cos
    if cos!=[]:
        scraperwiki.sqlite.save(unique_keys=[], table_name='shareholders_', data=cos)

def otherCompanies(root,company="",cid=''):
    #print '..other'
    costmp=getCompanies(root,'other')
    cos=patch(costmp,company,cid)
    print 'other',cos
    if cos!=[]:
        scraperwiki.sqlite.save(unique_keys=[], table_name='othercos_', data=cos)
    
def getPureHelp_cScrape(cid):
    url='http://www.purehelp.no/company/details/'+str(cid)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    return root

#url='http://www.purehelp.no/company/details/914807077'
#root=getPureHelp_cScrape('914807077')
#otherCompanies(root)
#print '...'
#exit(-1)
#shareholders(root)
#print '...'
#directors(root)

done=[]
for d in data:
    cname=d['navn'].strip()
    cnames=brregLookup(cname)
    if cnames==[]:
        print 'pass',cname
        continue
    lookupId,lookupName=cnames[0]
    if lookupId in done: continue
    else: done.append(lookupId)

    if lookupName.lower()==cname.lower():
        print 'ok',cname,cnames[0]
    else:
        print 'ish?',cname,cnames[0]
    #lookupId='914807077'
    root=getPureHelp_cScrape(lookupId)
    shareholders(root,lookupName,lookupId)
    otherCompanies(root,lookupName,lookupId)
    directors(root,lookupName,lookupId)

