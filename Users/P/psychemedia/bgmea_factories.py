import scraperwiki
import lxml.html
import urllib2, lxml.etree

# Blank Python
#http://www.bgmea.com.bd/member/memberlist/2920

def flatten(el):           
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)

#This function scrapes data from a company page. At the moment I don't scrape all of it, but maybe we should?
def detailPageLookup(url,cid):
    fhtml = scraperwiki.scrape(url)
    froot = lxml.html.fromstring(fhtml)
    data={}

    #This scrapes the factory address - maybe we should also scrape the registration address - this might help colocate owners of multiple factoreis?
    #THe scraping technique is to search into a unique cell in the row we're interested in, then backtrack and walk to the result we actually want
    addr= flatten(froot.xpath('.//td[starts-with(text(),"Factory Address")]/.././td')[1] ) #address data
    typ=flatten(froot.xpath('.//td[starts-with(text(),"Priority")]/../../tr')[1].xpath('./td')[0] ) #garment type
    siz=flatten(froot.xpath('.//td[starts-with(text()," No of Machines")]/.././td')[1] ) #number of machines

    data={'address':addr.strip(), 'type':typ.strip(),'cid':cid.strip(),'size':siz}
    scraperwiki.sqlite.save(unique_keys=['cid'], table_name='factoryData', data=data)

#This function looks up each results page and scrapes data relating to company and a link to it's compnay page
def resPageLookup(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    t=root.xpath('.//table')[4]
    #bigdirs collects the data from the search results page into a list so we can just write to the results db table once per results page
    bigdirs=[]
    for row in t.xpath('tr')[1:]:
        cells=row.xpath('td')
        print flatten(cells[0]).strip(),flatten(cells[2]).strip(),cells[5].xpath('a/@href')[0]
        cid=cells[5].xpath('a/@href')[0]
        try:
            email=flatten(cells[4]).strip().split('@')[1]
        except:email=''
        bigdirs.append({'cname':flatten(cells[0]).strip(),'contact':flatten(cells[2]).strip(),'email':email,'cid':cid })
        #When we've got the link to the compnay page, we can scrape that page
        detailPageLookup( cells[5].xpath('a/@href')[0], cid )
    if bigdirs!={}:
        scraperwiki.sqlite.save(unique_keys=['cid'], table_name='indexData', data=bigdirs)


#This is a fudge for now, based on an observation of how many results pages there are
#Note that each results page sghows 20 items but the paging links assume 10 results per page
#Really should calculate number of page loads from total number of results
#Note = scraper seemed to fail at end - maybe a fence post error somewhere? 


BGMEA=0

if BGMEA==1:
    for pi in range(0,146):
    #for pi in range(0,3):
        url='http://www.bgmea.com.bd/member/memberlist/'+str(20*pi)
        resPageLookup(url)


#------PUMA

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
    return "".join(res).strip()


puma=0
if puma==1:
    url='http://about.puma.com/wp-content/themes/aboutPUMA_theme/media/pdf/2013/250413_Factory%20List.pdf'
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    
    bigdata=[]
    
    print pages
    for page in pages:
        data={}
        for el in page:
            if el.tag == "text":
                #print el
                val=gettext_with_bi_tags(el)
                print val,el.attrib
                if int(el.attrib['left'])<250:
                    data={}
                    data['company']=gettext_with_bi_tags(el)
                elif int(el.attrib['left'])<400: data['country']=gettext_with_bi_tags(el)
                else:
                    data['city']=gettext_with_bi_tags(el)
                    bigdata.append(data.copy())
                #if el.attrib['top']=='1220': pass
                #else:
                    #HorribleHack - there must be a better way of dealing with this?
                    #val=gettext_with_bi_tags(el).encode('utf8').replace('\xc2\xa0',' ')
                    #val=gettext_with_bi_tags(el)
                    #if val in headings:
                        #print '..',headings[val],
                        #keyval=headings[val]
                        #data[ keyval ]=''
                    #elif data!={}: 
                        #print val
                        #data[ keyval ] = ' '.join( [ data[ keyval ], val ] )
            #bigdata.append(data.copy())
    
    for data in bigdata[1:-1]:
        print data
        scraperwiki.sqlite.save(unique_keys=[], table_name='puma', data=data)


#---Adidas
def handleMultiLine(d,el):
    e=gettext_with_bi_tags(el)
    if d=='': return e
    else: return ' '.join([ d, e ])\

adidas=0
if adidas==1:
    url='http://www.adidas-group.com/en/sustainability/assets/factory_list/2012_Jan_Global_Factory_List.pdf'
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    
    bigdata=[]
    
    print pages
    started=0
    for page in pages:
        data={}
        for el in page:
            if el.tag == "text" and int(el.attrib['left'])<70: started=1
            if el.tag == "text" and started:
                #print el
                val=gettext_with_bi_tags(el)
                #print val,el.attrib
                if int(el.attrib['left'])<70:
                    print data
                    #improve speed by saving data to db at page level
                    if data!={}: scraperwiki.sqlite.save(unique_keys=[], table_name='adidas', data=data)
                    data={'country':'','factoryname':'','address1':'','address2':'','address3':'','city':'','province':''}
                elif int(el.attrib['left'])<100:
                    data['country']=handleMultiLine(data['country'],el)
                    data['country']=data['country'].replace('<b>','').replace('</b>','')
                elif int(el.attrib['left'])<250: data['factoryname']=handleMultiLine(data['factoryname'],el)
                elif int(el.attrib['left'])<500: data['address1']=handleMultiLine(data['address1'],el)
                elif int(el.attrib['left'])<750: data['address2']=handleMultiLine(data['address2'],el)
                elif int(el.attrib['left'])<900: data['address3']=handleMultiLine(data['address3'],el)
                elif int(el.attrib['left'])<1000: data['city']=handleMultiLine(data['city'],el)
                else: data['province']=handleMultiLine(data['province'],el)

                #else:
                    #data['city']=gettext_with_bi_tags(el)
                    #bigdata.append(data.copy())


#------Fab Varn
fabvarn=0
if fabvarn==1:
    skiplist=['COUNTRY','FACTORY NAME','ADDRESS','CITY','REGION']
    url='http://cdn.varner.eu/cdn-1ce36b6442a6146/Global/Varner/CSR/Downloads_CSR/Fabrikklister_VarnerGruppen_2013.pdf'
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    
    bigdata=[]
    for page in pages[1:]:
        data={}
        for el in page:
            if el.tag == "text":
                val=gettext_with_bi_tags(el)
                #print val,el.attrib
                if val not in skiplist:
                    if int(el.attrib['left'])<100: data['Country']=gettext_with_bi_tags(el)
                    elif int(el.attrib['left'])<100: data['Factory name']=gettext_with_bi_tags(el)
                    elif int(el.attrib['left'])<250: data['Address']=gettext_with_bi_tags(el)
                    elif int(el.attrib['left'])<500: data['City']=gettext_with_bi_tags(el)
                    elif int(el.attrib['left'])<1000:
                        data['Region']=gettext_with_bi_tags(el)
                        bigdata.append(data.copy())
        print bigdata
        scraperwiki.sqlite.save(unique_keys=[], table_name='fabvarn', data=bigdata)
        bigdata=[]import scraperwiki
import lxml.html
import urllib2, lxml.etree

# Blank Python
#http://www.bgmea.com.bd/member/memberlist/2920

def flatten(el):           
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)

#This function scrapes data from a company page. At the moment I don't scrape all of it, but maybe we should?
def detailPageLookup(url,cid):
    fhtml = scraperwiki.scrape(url)
    froot = lxml.html.fromstring(fhtml)
    data={}

    #This scrapes the factory address - maybe we should also scrape the registration address - this might help colocate owners of multiple factoreis?
    #THe scraping technique is to search into a unique cell in the row we're interested in, then backtrack and walk to the result we actually want
    addr= flatten(froot.xpath('.//td[starts-with(text(),"Factory Address")]/.././td')[1] ) #address data
    typ=flatten(froot.xpath('.//td[starts-with(text(),"Priority")]/../../tr')[1].xpath('./td')[0] ) #garment type
    siz=flatten(froot.xpath('.//td[starts-with(text()," No of Machines")]/.././td')[1] ) #number of machines

    data={'address':addr.strip(), 'type':typ.strip(),'cid':cid.strip(),'size':siz}
    scraperwiki.sqlite.save(unique_keys=['cid'], table_name='factoryData', data=data)

#This function looks up each results page and scrapes data relating to company and a link to it's compnay page
def resPageLookup(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    t=root.xpath('.//table')[4]
    #bigdirs collects the data from the search results page into a list so we can just write to the results db table once per results page
    bigdirs=[]
    for row in t.xpath('tr')[1:]:
        cells=row.xpath('td')
        print flatten(cells[0]).strip(),flatten(cells[2]).strip(),cells[5].xpath('a/@href')[0]
        cid=cells[5].xpath('a/@href')[0]
        try:
            email=flatten(cells[4]).strip().split('@')[1]
        except:email=''
        bigdirs.append({'cname':flatten(cells[0]).strip(),'contact':flatten(cells[2]).strip(),'email':email,'cid':cid })
        #When we've got the link to the compnay page, we can scrape that page
        detailPageLookup( cells[5].xpath('a/@href')[0], cid )
    if bigdirs!={}:
        scraperwiki.sqlite.save(unique_keys=['cid'], table_name='indexData', data=bigdirs)


#This is a fudge for now, based on an observation of how many results pages there are
#Note that each results page sghows 20 items but the paging links assume 10 results per page
#Really should calculate number of page loads from total number of results
#Note = scraper seemed to fail at end - maybe a fence post error somewhere? 


BGMEA=0

if BGMEA==1:
    for pi in range(0,146):
    #for pi in range(0,3):
        url='http://www.bgmea.com.bd/member/memberlist/'+str(20*pi)
        resPageLookup(url)


#------PUMA

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
    return "".join(res).strip()


puma=0
if puma==1:
    url='http://about.puma.com/wp-content/themes/aboutPUMA_theme/media/pdf/2013/250413_Factory%20List.pdf'
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    
    bigdata=[]
    
    print pages
    for page in pages:
        data={}
        for el in page:
            if el.tag == "text":
                #print el
                val=gettext_with_bi_tags(el)
                print val,el.attrib
                if int(el.attrib['left'])<250:
                    data={}
                    data['company']=gettext_with_bi_tags(el)
                elif int(el.attrib['left'])<400: data['country']=gettext_with_bi_tags(el)
                else:
                    data['city']=gettext_with_bi_tags(el)
                    bigdata.append(data.copy())
                #if el.attrib['top']=='1220': pass
                #else:
                    #HorribleHack - there must be a better way of dealing with this?
                    #val=gettext_with_bi_tags(el).encode('utf8').replace('\xc2\xa0',' ')
                    #val=gettext_with_bi_tags(el)
                    #if val in headings:
                        #print '..',headings[val],
                        #keyval=headings[val]
                        #data[ keyval ]=''
                    #elif data!={}: 
                        #print val
                        #data[ keyval ] = ' '.join( [ data[ keyval ], val ] )
            #bigdata.append(data.copy())
    
    for data in bigdata[1:-1]:
        print data
        scraperwiki.sqlite.save(unique_keys=[], table_name='puma', data=data)


#---Adidas
def handleMultiLine(d,el):
    e=gettext_with_bi_tags(el)
    if d=='': return e
    else: return ' '.join([ d, e ])\

adidas=0
if adidas==1:
    url='http://www.adidas-group.com/en/sustainability/assets/factory_list/2012_Jan_Global_Factory_List.pdf'
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    
    bigdata=[]
    
    print pages
    started=0
    for page in pages:
        data={}
        for el in page:
            if el.tag == "text" and int(el.attrib['left'])<70: started=1
            if el.tag == "text" and started:
                #print el
                val=gettext_with_bi_tags(el)
                #print val,el.attrib
                if int(el.attrib['left'])<70:
                    print data
                    #improve speed by saving data to db at page level
                    if data!={}: scraperwiki.sqlite.save(unique_keys=[], table_name='adidas', data=data)
                    data={'country':'','factoryname':'','address1':'','address2':'','address3':'','city':'','province':''}
                elif int(el.attrib['left'])<100:
                    data['country']=handleMultiLine(data['country'],el)
                    data['country']=data['country'].replace('<b>','').replace('</b>','')
                elif int(el.attrib['left'])<250: data['factoryname']=handleMultiLine(data['factoryname'],el)
                elif int(el.attrib['left'])<500: data['address1']=handleMultiLine(data['address1'],el)
                elif int(el.attrib['left'])<750: data['address2']=handleMultiLine(data['address2'],el)
                elif int(el.attrib['left'])<900: data['address3']=handleMultiLine(data['address3'],el)
                elif int(el.attrib['left'])<1000: data['city']=handleMultiLine(data['city'],el)
                else: data['province']=handleMultiLine(data['province'],el)

                #else:
                    #data['city']=gettext_with_bi_tags(el)
                    #bigdata.append(data.copy())


#------Fab Varn
fabvarn=0
if fabvarn==1:
    skiplist=['COUNTRY','FACTORY NAME','ADDRESS','CITY','REGION']
    url='http://cdn.varner.eu/cdn-1ce36b6442a6146/Global/Varner/CSR/Downloads_CSR/Fabrikklister_VarnerGruppen_2013.pdf'
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    
    bigdata=[]
    for page in pages[1:]:
        data={}
        for el in page:
            if el.tag == "text":
                val=gettext_with_bi_tags(el)
                #print val,el.attrib
                if val not in skiplist:
                    if int(el.attrib['left'])<100: data['Country']=gettext_with_bi_tags(el)
                    elif int(el.attrib['left'])<100: data['Factory name']=gettext_with_bi_tags(el)
                    elif int(el.attrib['left'])<250: data['Address']=gettext_with_bi_tags(el)
                    elif int(el.attrib['left'])<500: data['City']=gettext_with_bi_tags(el)
                    elif int(el.attrib['left'])<1000:
                        data['Region']=gettext_with_bi_tags(el)
                        bigdata.append(data.copy())
        print bigdata
        scraperwiki.sqlite.save(unique_keys=[], table_name='fabvarn', data=bigdata)
        bigdata=[]