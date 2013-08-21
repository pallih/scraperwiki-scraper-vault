import scraperwiki
import lxml.html
import traceback
import logging
import json
import dateutil.parser
import re
import urlparse
import stdnum.isbn
import chardet

html2text=scraperwiki.swimport('html2text')

def makeidentifier(s):
    import string
    s=s.strip().replace(' ','_')
    valid_chars = "_%s%s" % (string.ascii_letters, string.digits)
    out=''.join(c for c in s if c in valid_chars)
    if len(out)==0:
        return '_'
    else:
        return out

emptyish = lxml.html.fromstring('<none></none>')

class logger():
    def __init__(self):
        subscribers.append(self.reciever)
        self.log=[]

    def reciever(self, msg):
        self.log.append(msg)

    def read(self):
        return self.log        

def dateparse(d):
    if not d:
        return d
    try:
        return dateutil.parser.parse(d, dayfirst=True).date().isoformat()
    except:
        return d

def gettext(e):
    # get text associated with an element, both before and after.
    b=e.text or ''
    t=e.tail or ''
    if b and t:
        return b+'<br>'+t
    else:
        return b+t

def warner(d):
    formats={'onecss':'looked for "{d[selector]}" in tag "{d[tag]}", found {d[count]}!',
             'oneattrib':'no attribute "{d[attr]}" on tag "{d[tag]}".',
             'onexpath':'looked for "{d[xpath]}" in tag "{d[tag]}", found {d[count]}!',
             'oneid':'no id "{d[id]}" found.'}
    template=formats[d['source']]
    msg=template.format(d=d)
    #logging.warn(msg)

subscribers=[warner]

def __notify(self,msg=None):
    """Send a message to all subscribers."""
    try:
        subs=subscribers
    except NameError:
        return None
    for sub in subs:
        sub(msg)
    
lxml.html.HtmlElement.notify=__notify

def __onecss(self, selector, silent=False):
    """Do or be mildly irked: get the first CSSSelector match"""
    x=self.cssselect(selector)
    if len(x) != 1 and not silent:
        #self.notify('looked for "%s" in tag "%s", found %d!'%(selector, self.tag, len(x)))
        self.notify({'source':'onecss', 'selector':selector, 'tag':self.tag, 'count':len(x)})
    if len(x)==0:
        return emptyish
    else:
        return x[0]

lxml.html.HtmlElement.onecss=__onecss

def __oneattrib(self,attr,silent=False):
    """Do or be mildly irked: get HTML attribute"""
    try:
        return self.attrib[attr]
    except KeyError:
        #self.notify('no attribute "%s" on tag "%s".'%(attr, self.tag))
        if not silent: self.notify({'source':'oneattrib', 'attr':attr, 'tag': self.tag})
        return None

lxml.html.HtmlElement.oneattrib=__oneattrib

def __oneid(self,id,silent=False):
    """Do or be mildly irked: get_element_by_id"""
    try:
        return self.get_element_by_id(id)
    except KeyError:
        if not silent: self.notify({'source':'oneid', 'id':id})
        return emptyish

lxml.html.HtmlElement.oneid=__oneid

def __onexpath(self, xpath, silent=False):
    """Do or be mildly irked: get xpath item"""
    try:
        x=self.xpath(xpath)
    except SyntaxError:
        x=''
    if len(x) != 1 and not silent:
        self.notify({'source':'onexpath', 'xpath':xpath, 'tag': self.tag, 'count':len(x)})
    if len(x) == 0:
        # guess at correct type, string or element
        if xpath[-2:]=='()' or re.search('@[^/\[\]]*$', xpath): # this will break :(
            return ''
        else:
            return emptyish
    else:
        return x[0]

lxml.html.HtmlElement.onexpath=__onexpath

# =========================== END OF LXML.HTML OVERRIDES ============================================

expected={'pubs': ['html', 'title', 'markdown', 'crumbs'],
          'news': ['html', 'title', 'markdown', 'crumbs', 'date', 'abstract'],
          'speeches': ['html', 'title', 'markdown', 'crumbs', 'date', 'location', 'orator', 'orator-url', 'image'],
          'consult': ['html', 'title', 'markdown', 'crumbs', 'opendate', 'closedate', 'responsedate'],
          'pub_server': ['title', 'summary', 'date', 'urn',  'attachment', 'filename',
                         'language', 'meta', 'format', 'pages', 'originurl', 'cat', 'subcat'],
          'tradeanalysis': ['markdown','help','title','rawmarkdown','externals','rawhtml'],
          'farmexcise': ['markdown','help','title','rawmarkdown','externals','rawhtml'],
          'modconsult': ['title', 'html', 'markdown', 'ref', 'assoc_org', 'attachments', 'person', 'address', 'email', 'fax', 'open_date','close_date'],
          'modnews': ['title','summary','html','markdown','images','assoc_org','pub_date'],
          'modspeech': ['title', 'summary', 'person', 'date', 'published', 'html', 'markdown'],
          'modpubs': ['title', 'html', 'markdown', 'links', 'crumbs','isbn'],
          'dclg_consult': ['title', 'html', 'markdown', 'crumbs', 'attachments', 'person' 'email', 'addr'],
          'dclg_pubs': ['title', 'html', 'markdown', 'crumbs', 'attachments']}

def check(doctype, data):
    err=[]
    for row in data:
        if doctype not in expected:
            #print "No expected fields for %s!"%doctype
            err=None
            return err
        for item in expected[doctype]:
            if item not in row:
                err.append ('No '+item)
                continue
            if row[item] == None:
                err.append (item+' = None')
                continue
            try:
                l = len(row[item])
            except Exception, e:
                if type(row[item]) not in [int]:
                    print repr(e)
                    print "Can't len() a "+str(type(row[item]))
            else:
                if l == 0:
                    err.append ('Zero length '+item)
    if err==[]:
        err=None
    return err


# =========================== END OF DESCRIPTION OF EXPECTED DATA ===================================

def GetLinks(body, parsearg, meta):
    """body is a lxml.HTMLElement"""
    attrs=['href','cite','src','data']
    builder=[]
    for path in body.xpath('//div[@id="mainColumn"]//*'):
        try:
            c=path.attrib['class']
        except KeyError:
            c=None
        for attr in attrs:
            if attr in path.attrib:
                if path.attrib[attr]:
                    builder.append({'url':path.attrib[attr], 'class':c, 'attr':attr, 'tag': path.tag})
    return builder

def BISCore(html, parsearg, meta):
    print meta
    data={'crumbs':[]}
    root=lxml.html.fromstring(html)
    root.make_links_absolute(meta['__link'])
    try: # remove this
        body=root.get_element_by_id('mainColumn')
    except:
        return (data, ['FATAL'], None)
    data['title']=body.cssselect('h1')[0].text # unchecked

    details=body.cssselect('div[class="itemDetails"]') or body.cssselect('div[class="itemDetails withImage"]')
    # TODO: handle this better where there are no details
    if details:
        details=details[0]
        details.drop_tree()
    
    #chunk=lxml.html.tostring(body) # a bit raw
    try:
        body.get_element_by_id('pageOptions').drop_tree()
    except:
        pass
    for h1 in body.cssselect('h1'):
        if h1.getnext().oneattrib('class', silent=True)=='hr':
            h1.getnext().drop_tree()
        h1.drop_tree()
    
    data['links']=GetLinks(body, parsearg, meta)
    data['html']=lxml.html.tostring(body)
    data['markdown']=html2text.HTML2Text().handle(data=data['html'])
    
    #crumbs handling
    crumbs=root.get_element_by_id('breadcrumb').cssselect('li[class="crumb"]')
    if len(crumbs)==0: err.append('crumb')
    for i,crumb in enumerate(crumbs):
        a=crumb.cssselect('a')
        if a:
            crumburl=a[0].attrib['href']
        else:
            crumburl=None
        data['crumbs'].append({'name':crumb.text_content(), 'crumburl':crumburl})

    
    return (data, details)

def PARSEnews(html,parsearg, meta):
    (data, details)=BISCore(html, parsearg, meta)
    root=lxml.html.fromstring(html)
    root.make_links_absolute(meta['__link'])
    if details:
        data['abstract']=details.text_content()
    image=root.onexpath("//div[@id='mainColumn']/div[@class='itemDetails withImage']/img")
    data['image_url']=image.oneattrib('src')
    data['image_alt']=image.oneattrib('alt')
    print data['image_url'], data['image_alt']

    for h1 in root.cssselect('h1'):
        maybedate=h1.getnext()
        if maybedate.tag=='p':
            data['date']=dateparse(maybedate.text)
    return [data]

def PARSEpubs(html,parsearg, meta):
    (data, details)=BISCore(html, parsearg, meta)
    return [data]

def PARSEspeeches(html,parsearg, meta):
    (data, details)=BISCore(html, parsearg, meta)
    assert details
    
    # remove 'checked against delivery'
    h=lxml.html.fromstring(data['html'])
    for path in h.xpath('//*'):
        if path.text and 'against delivery' in path.text:
            print path.text
            if 'hecked' in path.text:
                data['checked']='True'
            else:
                data['checked']='False'
            path.drop_tree()
    if 'checked' not in data:
        data['checked']=''
    data['html']=lxml.html.tostring(h)
    data['markdown']=html2text.HTML2Text().handle(data=data['html'])
    
    try:
        data['image']=details.cssselect('img')[0].attrib['src']
    except IndexError:
        pass
    dateline=details.cssselect('p[class="detail alternate"]')[0].text
    (date,zz,data['location']) = dateline.partition(', ')
    data['date']=dateparse(date)

    for a in details.cssselect('a'):
        if a.text:
            data['orator']=a.text
            data['orator-url']=a.attrib['href']
        else:
            data['orator']=''
            data['orator-url']=''
    return [data]

def PARSEconsult(html, parsearg, meta):
    (data, details)=BISCore(html, parsearg, meta)
    root=lxml.html.fromstring(html)
    root.make_links_absolute(meta['__link'])
    body=root.get_element_by_id('mainColumn')
    
    consultlist = {'Open date:':'opendate','Closing date:':'closedate','Response date:':'responsedate'}
    for p in details.cssselect('p'):
        try:
            t=p.cssselect('strong')[0]
        except:
            data['abstract']=p.text
        else:
            for item in consultlist:
                if item in t.text:
                    t.drop_tree()
                    data[consultlist[item]]=dateparse(p.text_content())

    # attachments
    attachments = body.cssselect('a[rel="dc:hasPart"]')
    data['attachments']=[{'link':att.oneattrib('href'), 'name':att.text_content()} for att in attachments]
                    
    #crumbs handling
    crumbs=root.get_element_by_id('breadcrumb').cssselect('li[class="crumb"]')
    assert crumbs
    for i,crumb in enumerate(crumbs):
        a=crumb.cssselect('a')
        if a:
            crumburl=a[0].attrib['href']
        else:
            crumburl=None
        data['crumbs'].append({'name':crumb.text_content(), 'crumburl':crumburl})

    # now extract person responsible
    rhand=root.get_element_by_id('rightColumn').onecss('div[class="itemDetails"]', silent=False)
    if rhand.tag != 'none':
        data['person']=rhand.onecss("span[property='v:fn']").text
        data['assoc_org']=rhand.onecss("div[typeof='foaf:Organization']").text
        addr=rhand.onecss("div[rel='v:adr']")
        for br in addr.cssselect('br'):
            br.tail='\n'
            br.drop_tag()
        data['addr']=addr.text_content()
        data['resp_form']=[]
        data['resp_online']=[]
        data['resp_email']=[]
        data['resp_other']=[]
        for a in rhand.cssselect('a'):
            if a.oneattrib('rel')=='argot:replyByEmail':
                assert 'mailto:' in a.oneattrib('href')
                data['resp_email'].append(a.oneattrib('href').partition(':')[2])
                continue
            if a.oneattrib('rel')=='argot:replyOnline':
                data['resp_online'].append(a.oneattrib('href'))
                continue
            if '/assets/' in a.oneattrib('href'):
                data['resp_form'].append(a.oneattrib('href'))
                continue
            data['resp_other'].append(a.oneattrib('href'))
            logging.warn("resp_other used.")

    return [data]

def PARSEbroken(html, parsearg, meta):
    return [{}]

def PARSEpub_server(html, parsearg, meta):
    row = lxml.html.fromstring(html)
    try:
        data={}
        for item in meta: # is this general, in fact?
            data[item]=meta[item]
        boxes=row.cssselect('td')

        try:
            assert boxes[0].cssselect('a')
            data['attachment']=boxes[0].cssselect('a')[0].attrib['href']
            data['title']=boxes[0].cssselect('strong')[0].text.replace(' (PDF)','').strip()
            for x in boxes[0].cssselect('span'):
                if not x.oneattrib('id', True) and not x.oneattrib('class', True):
                    #print lxml.html.tostring(x)
                    data['type']=x.text
                    #print data['type'] 
            try:
                data['language']=boxes[0].cssselect('a')[0].attrib['lang']
            except:
                pass
        except AssertionError: # not downloadable, I presume.
            data['attachment']=None
            data['title']=boxes[0].cssselect('span[class="fauxLink"]')[0].text.strip()
            try:
                data['language']=boxes[0].cssselect('span[class="fauxLink"]')[0].attrib['lang']
            except:
                pass
    
        try:
            data['meta']=boxes[0].cssselect('span[class="boldText"]')[0].text.strip()
                #print data['price']
        except IndexError:
            data['price']='' 
        else:
            if u'\xa3' in data['meta']: # \xa3 == £
                data['price']=data['meta'].partition(u'\xa3')[2]
            else:
                data['price']=''
            
        data['filename']=data['title']
        data['summary']='\n\n'.join([gettext(br) for br in boxes[0].cssselect('br')]).strip()
        data['body']=''
        data['urn']=boxes[1].text.strip()
        data['isbn']=''
        data['date']=dateparse(boxes[2].text.strip())
        data['format']=boxes[3].text.strip()
        try:
            pgs=boxes[3].cssselect('br')[0].tail.strip()
        except:
            pass # some things just don't have them
        else:
            data['pages']=int(pgs.split(' ')[0])
        data['action']=boxes[4].text_content().strip()
        if data['action']:
            data['orderurl']='http://bis.ecgroup.net/page.aspx?urn=%s'%data['urn']
        else:
            data['orderurl']=''
        assert data['action'] or data['attachment'] or data['meta']=='Discontinued'
    except:
        print lxml.html.tostring(row)
        raise
    #print data
    return [data]

def PARSEtradeanalysis(html, parsearg, meta):
    # get lxml chunks
    root=lxml.html.fromstring(html)
    root.make_links_absolute(meta['__link'])
    data={}
    maincontent=root.get_element_by_id('maincontent')
    try:
        addcontent=root.get_element_by_id('additionalContent')
    except:
        addcontent=lxml.html.fromstring('<none></none')
    # parse maincontent
    h1=maincontent.cssselect('h1')[0]
    data['title']=h1.text
    h1.drop_tree()
    for x in maincontent.xpath('//hr'):
        x.drop_tree()
    for x in maincontent.xpath('//strong'):
        x.drop_tag()
        
    data['rawhtml']=lxml.html.tostring(maincontent)
    data['rawmarkdown']=html2text.html2text(data['rawhtml'])
    #parse additionalContent
    # http://stackoverflow.com/questions/8050929/select-divs-between-html-comments-in-lxml
    help=root.xpath("//*[preceding-sibling::comment()[. = ' Helplines '] and following-sibling::comment()[. = ' Internal Links']]")
    data['help']=[]
    h3=None
    contents=None
    for item in help:
        if item.tag=='h3':
            if h3:
                data['help'].append({'name':h3, 'phone':contents})
            h3=item.text
            contents=[]
        elif item.tag=='p':
            contents.append(item.text)
        else:
            assert False
    if h3:
        data['help'].append({'name':h3, 'phone':contents})
    
    external=root.xpath("//p[preceding-sibling::comment()[. = ' External Links ']]")
    data['externals']=[]
    for item in external:
        b=item.cssselect('b')[0]
        name=b.text
        b.drop_tree()
        data['externals'].append ({'name': name, 'url': item.text_content()})
    
    # rebuild markdown
    externalmd='\n\n'.join(['[%s](%s)'%(i['name'],i['url']) for i in data['externals']])
    buildhelp=[]
    for i in data['help']:
        buildhelp.append( '### %s\n%s'%(i['name'], ', '.join(i['phone'])))
    helpmd='\n\n'.join(buildhelp)
    
    #data['markdown']='\n\n'.join(['## Introduction', data['rawmarkdown'], '* * *', '\n## Further information', helpmd, externalmd])
    data['markdown']='\n\n'.join(['## Introduction', data['rawmarkdown'], '\n## Further information', helpmd, externalmd])
    return [data]

def PARSEfarmexcise(html, parsearg, meta):
    return PARSEtradeanalysis(html, parsearg, meta)

def PARSEman_and_mar(html, parsearg, meta):
    return PARSEtradeanalysis(html, parsearg, meta)

def PARSEtransadv(html, parsearg, meta):
    return PARSEtradeanalysis(html, parsearg, meta)

def PARSEspecialist(html, parsearg, meta):
    return PARSEtradeanalysis(html, parsearg, meta)

def PARSEmodpubs(html, parsearg, meta):
    #root=lxml.html.fromstring(html.encode('ISO 8859-1').decode('UTF-8'))
    root=lxml.html.fromstring(html)
    root.make_links_absolute(meta['__link'])
    #print meta['__link']
    data={}
    data['title']=root.onexpath("//h1[@class='small-header1']").text_content()
    data['html']=lxml.html.tostring(root.onexpath("//div[@class='profilecontent']"))
    data['markdown']=html2text.HTML2Text().handle(data=data['html'])
    links=root.xpath("//div[@id='left-column']//li/a")
    data['links']=[]
    for l in links:
        d={}
        d['attach']=l.attrib.get('href')
        d['attach_title']=l.text
        data['links'].append(d)

    crumbs = urlparse.urlparse(meta['__link']).path.strip('/').split('/')
    namedcrumbs = [re.sub('([A-Z])', ' \\1', c).strip() for c in crumbs]
    crumburls=[]
    for i in range(1,len(crumbs)+1):
        crumburls.append('http://www.mod.uk/'+'/'.join(crumbs[:i]))
    data['crumbs']=[{'name':z[0], 'crumburl':z[1]} for z in zip(namedcrumbs, crumburls)]

    # FOI
    if 'FOI Publication Scheme' in html:
        headings=root.xpath("//div[@class='content-area']/strong")
        assert len(headings)>0
        hdict={h.text:h.tail for h in headings}
        data['author']=hdict.get('Author:')
        data['pubdate']=dateparse(hdict.get('Date released proactively:'))
        data['price']=hdict.get('Charge:')

    for isbn_org, isbn in re.findall("(ISBN[\s:]*([\d\s\-]+))(?i)", root.text_content()):
        isbn = re.sub("[^\d]", "", isbn)
        data['isbnorg']=isbn_org
        if stdnum.isbn.is_valid(isbn):
            data['isbn']=isbn

    return [data]

def PARSEmodspeech(html, parsearg, meta):
    root=lxml.html.fromstring(html)
    root.make_links_absolute(meta['__link'])
    data={}
    data['title']=root.oneid('Pageheading1_Headline', silent=True).text_content()
    
    data['summary']=root.oneid('Pagesummary1_Summary', silent=True).text_content()
    if data['summary']:
        try:
            m=re.search('\sby\s(.*)\s(?:at|in|to)\s(.*)\son\s(.*)\.', data['summary'], re.DOTALL)
            data['person'], data['location'], d = m.groups()
            data['date']=dateparse(d)
            data['published']=dateparse(d)
        except:
            print data['summary']
            print meta['__link']
            raise

    data['html']='\n\n\n'.join([lxml.html.tostring(x) for x in root.xpath("//div[@id='left-column']/div[not(@class)]/p[1]/..")])
    data['markdown']=html2text.HTML2Text().handle(data=data['html']) # this line and above 1 from modnews.

    return [data]

    

def PARSEmodnews(html, parsearg, meta):
    root=lxml.html.fromstring(html)
    root.make_links_absolute(meta['__link'])
    data={}
    data['title']=root.oneid('DefenceHeadlineStyle').text_content()
    data['summary']=root.oneid('AboutDefenceSummary_Summary').text_content()
    data['html']='\n\n\n'.join([lxml.html.tostring(x) for x in root.xpath("//div[@id='left-column']/div[not(@class)]/p[1]/..")])
    data['markdown']=html2text.HTML2Text().handle(data=data['html'])
    images=root.xpath("//div[@id='left-column']/div[@class='image']")
    data['images']=[]
    for image in images:
        d={}
        d['imgurl']=image.onexpath("descendant-or-self::img/@src")
        d['imgalt']=image.onexpath("descendant-or-self::img/@alt")
        d['imgcap']=lxml.html.tostring(image.onexpath("descendant-or-self::p[@class='caption']")) # TODO: Broken.
        d['imgcapmd']=html2text.HTML2Text().handle(data=d['imgcap'])
        data['images'].append(d)
    data['assoc_org']='MoD'
    data['pub_date']=root.oneid('htmDate').text_content()
    if not data['pub_date']:
        data['pub_date']=root.oneid('other-content').onecss('span[class="date"]').text_content()
    return [data]
   
def PARSEmodconsult(html, parsearg, meta):
    print meta['__link']
    root=lxml.html.fromstring(html)
    root.make_links_absolute(meta['__link'])
    
    data={}
    data['title']=root.cssselect('h1')[0].text
    try:
        data['body']=lxml.html.tostring(root.xpath("//div[@class='consultationcontent'][2]")[0])
        data['markdown']=html2text.HTML2Text().handle(data=data['html'])
    except:
        pass
    data['ref'] = root.onexpath("//div[@property='dc:identifier']/text()")
    data['assoc_org']='MoD'
    
    data['attachments']=[]
    for attachment in root.xpath("//a[@rel='DC:haspart']"):
        url=attachment.attrib['href']
        name=attachment.text
        data['attachments'].append([name, url])
    
    data['person']=root.onexpath("//span[@property='v:fn']/text()")
    data['address']='\n'.join((root.onexpath("//span[@property='v:adr']/text()").strip(),
                               root.onexpath("//span[@property='v:street-address']/text()").strip(),
                               root.onexpath("//span[@property='v:locality']/text()").strip(),
                               root.onexpath("//span[@property='v:postal-code']/text()").strip())).strip()
    data['email']=root.onexpath("//span[@property='argot:replyByEmail v:email']/a/@href").replace('mailto:','').strip()
    data['fax']=root.onexpath("//span[@property='v:fax']/text()")
    
    profilecontent={'Open Date':'open_date', 'Close Date':'close_date'}
    datexml=root.xpath("//div[@class='profilecontent']/div[@class='profilecontent']")
    for i in datexml:
        matchtext=i.xpath("strong/text()")[0]
        datetext=i.xpath("text()")[0]
        for content in profilecontent:
            if content in matchtext:
                data[profilecontent[content]]=dateparse(datetext)
                break
        else:
            print "profilecontent not found: '%s'"%matchtext

    return [data]    

def dclg_core(html,parsearg,meta):
    #print meta['__link']
    #html=html.encode('latin-1')
    root=lxml.html.fromstring(html)
    root.make_links_absolute(meta['__link'])
    data={}
    
    # metadata
    metadata_heads=root.xpath("//div[@id='centerColumn']//table[1]//tr/th")
    metadata_data=root.xpath("//div[@id='centerColumn']//table[1]//tr/td")
    data=dict(zip([m.text_content().strip() for m in metadata_heads], [m.text_content().strip() for m in metadata_data]))

    # breadcrumbs
    breadcrumbs=root.xpath("id('Breadcrumbs')//a")
    for crumb in breadcrumbs:
        assert crumb.attrib['href'] in breadcrumbs[-1].attrib['href']
    data['crumbs']=[{'name':crumb.text, 'crumburl':crumb.get('href')} for crumb in breadcrumbs]
    
    
    if 'speech' not in meta:
        try:
            data['title']=root.get_element_by_id('Page').onecss('h2').text.strip() # not speeches
            if data['title']=='Archived content':
                data['title']=root.get_element_by_id('Page').cssselect('h2')[1].text.strip()
        except AttributeError:
            pass
    #print data
    
    return data,root


def PARSEdclg_consult(html, parsearg, meta):
    data,root=dclg_core(html, parsearg, meta)
    attachments=root.xpath("//ul[@class='downloadList']//a") # pubs / consult only.
    data['attachments']=[{'link':att.get('href'), 'name':att.text_content()} for att in attachments]
    
    summary=[]
    maybe_summary=root.xpath("//div[@id='Page']/h3[text()='Summary']/following-sibling::*")
    try:
        summary.append(root.xpath("//div[@id='Page']/h3[text()='Summary']")[0].tail)
    except:
        pass
    for i in maybe_summary:
        if i.tag=='h3' and i.text=='Order': break
        #print i.text
        summary.append(lxml.html.tostring(i))
    data['html']=''.join(summary)
    data['markdown']=html2text.HTML2Text().handle(data=data['html'])

    data['person']=root.onexpath('//span[@property="v:fn"]/text()', silent=True)
    data['email']=root.onexpath('//a[@rel="argot:replyByEmail v:email"]/@href', silent=True)
    data['addr']='\n'.join(root.xpath('//address/span[@property != "v:fn"]/text()', silent=True))
    return [data]
    
def PARSEdclg_pubs(html, parsearg, meta):
    return PARSEdclg_consult(html, parsearg, meta)

def PARSEdclg_news(html, parsearg, meta):
    #print meta['__link']
    data,root=dclg_core(html, parsearg, meta)
    data['html']=''.join([lxml.html.tostring(x) for x in root.xpath("//div[@id='Page']/*[name() != 'h2' and name() != 'table']")])
    for item in root.xpath("//div[@id='Page']/table[1]//tr"):
        data['t_'+makeidentifier(item.onecss('th').text_content())]=item.onecss('td').text_content()
    imgs= root.xpath("//div[@id='Page']//img")
    data['images']=[{'url':i.get('src'), 'alt':i.get('alt')} for i in imgs]
    md =html2text.HTML2Text()
    md.parse_weird_links=True # turn off images?
    data['markdown']=md.handle(data=data['html']) # there's at least one.
    return [data]

def PARSEdclg_data(html, parsearg, meta):
    return PARSEdclg_consult(html, parsearg, meta)
   
def PARSEdclg_speech(html, parsearg, meta):
    meta['speech']=True
    data,root=dclg_core(html, parsearg, meta)
    for item in root.xpath("//div[@id='Page']/table[1]//tr"):
        data['t_'+makeidentifier(item.onecss('th').text_content())]=item.onecss('td').text_content()
    #print lxml.html.tostring(root)
    #root=lxml.html.fromstring(html)
    title_element=root.onexpath('//*[@id="Page"]/h3')
    data['title']=title_element.text.strip()    
    title_element.drop_tree() 
    data['html']=''.join([lxml.html.tostring(x) for x in root.xpath("//div[@id='Page']/*[(@class!='ministerIntro' or not(@class)) and name() != 'table']")])
    assert data['html']
    md =html2text.HTML2Text()
    md.parse_weird_links=True
    data['markdown']=md.handle(data=data['html']) # there's at least one.

    data['author_name']=root.onexpath("//div[@class='ministerIntro']/h3/text()").strip()
    data['author_title']=root.onexpath("//div[@class='ministerIntro']/h4/text()").strip()
    data['author_desc']=''.join(root.xpath("//div[@class='ministerIntro']/text()")).strip()
    data['author_profile']=root.onexpath("//div[@class='ministerIntro']//li[1]/a/@href")
    
    return [data]

def PARSEdclg_news2(html, parsearg, meta):
    return PARSEdclg_news(html, parsearg, meta)
def PARSEdclg_news3(html, parsearg, meta):
    return PARSEdclg_news(html, parsearg, meta)

def PARSEdclg_speech2(html, parsearg, meta):
    return PARSEdclg_speech(html,parsearg,meta)

def PARSEfco_news(html, parsearg, meta):
    print meta['__link']
    #html=html.encode('latin-1') # undo my horrid unicode mangling
    root=lxml.html.fromstring(html)
    root.make_links_absolute(meta['__link'])
    data={}
    
    if 'speech' in meta:
        for row in root.xpath("//table[@class='SpeachDetails']//tr"):
            [rowname, rowtext]=[x.text_content().strip() for x in row.cssselect('td')]
            data['table!'+rowname[:-1]]=rowtext

    #data['speaker']=root.onexpath("//span[@class='SpeachDetailsSpan']/text()")

    title_element=root.onexpath('//div[@id="Main"]/h1')
    try:
        data['title']=title_element.text.strip()
        title_element.drop_tree()
    except:
        print "FAIL"
        return [data] 
    date_element=root.onexpath('//div[@id="Main"]/div[@class="NewsHeader"]/p[@class="Smaller"]')
    data['date']=date_element.text.strip()
    data['date_clean']=dateparse(data['date'])
    date_element.drop_tree()
    
    summary_element=root.onexpath('//div[@id="Main"]/div[@class="NewsHeader"]')
    data['summary']=summary_element.text.strip()
    summary_element.drop_tree()

    data['updated_raw']=root.onexpath("//div[@id='Content']/div[@id='SmallerDate']/text()").strip()
    data['updated']=data['updated_raw'].replace('Last updated at ','').replace(' (UK time)','')
    data['updated_clean']=dateparse(data['updated'])

    # remove pinterest
    for i in root.xpath("//div[@id='Main']//a[contains(@href,'javascript:')]"):
        i.drop_tree()

    data['images']=[]
    img_elements=root.xpath('//div[@id="Main"]//img')
    for i in img_elements:
        data['images'].append({'link':i.get('src'), 'text':i.get('title')})
        i.drop_tree()
    
    bodychunks=[]
    if bodychunks==[]:
        bodychunks=root.xpath("//div[@id='Main']/h2[text()='Search the news archive']/preceding-sibling::*")
    if bodychunks==[]:
        bodychunks=root.xpath("//div[@id='Main']/h3[text()='Further information']/preceding-sibling::*")
    if bodychunks==[]:
        bodychunks=root.xpath("//div[@id='Main']/h3[text()='More information']/preceding-sibling::*")
    if bodychunks==[]:
        bodychunks=root.xpath("//div[@id='Main']/*")
    data['html']='\n\n'.join([lxml.html.tostring(x) for x in bodychunks])
    mdparser=html2text.HTML2Text()
    mdparser.parse_weird_links=True
    data['markdown'] = mdparser.handle(data=data['html'])
    
    #print data
    return [data]
   
def PARSEfco_speech(html, parsearg, meta):
    meta['speech']=True
    if meta['__link']=='http://www.fco.gov.uk/en/news/latest-news/?view=Speech&id=553024182':
        return []
    # note speaker in fco_news
    #print  meta['__link']
    [data]=PARSEfco_news(html, parsearg, meta)
    return [data]

def PARSE2_fco_speech(*args, **kwargs):
    meta['__link']=re.sub(r':/(?=[^/])','://',meta['__link'])
    return PARSEfco_speech(*args, **kwargs)

def PARSE2_fco_news(*args, **kwargs):
    meta['__link']=re.sub(r':/(?=[^/])','://',meta['__link'])
    return PARSEfco_news(*args, **kwargs)

def PARSE2_bis_news(*args, **kwargs):
    meta['__link']=re.sub(r':/(?=[^/])','://',meta['__link'])
    return PARSEnews(*args, **kwargs)

def PARSE2_bis_speech(*args,**kwargs):
    meta['__link']=re.sub(r':/(?=[^/])','://',meta['__link'])
    return PARSEspeeches(*args, **kwargs)

def PARSE2_bis_con(*args, **kwargs):
    meta['__link']=re.sub(r':/(?=[^/])','://',meta['__link'])
    return PARSEconsult(*args, **kwargs)

def PARSE2_mod_news(*args, **kwargs):
    meta['__link']=re.sub(r':/(?=[^/])','://',meta['__link'])
    return PARSEmodnews(*args, **kwargs)

def PARSE2_mod_speech(*args, **kwargs):
    meta['__link']=re.sub(r':/(?=[^/])','://',meta['__link'])
    return PARSEmodspeech(*args, **kwargs)

def PARSE2_mod_pubs(*args, **kwargs):
    meta['__link']=re.sub(r':/(?=[^/])','://',meta['__link'])
    return PARSEmodpubs(*args, **kwargs)


# ==========================end of parser functions ===================================== 

scraperwiki.sqlite.execute('create table if not exists output (link primary key, data, err)')
scraperwiki.sqlite.attach('betal-populate', 'populate')
scraperwiki.sqlite.attach('betal-override', 'override')

#qselect = ["raw.link AS link", "COALESCE(override.type, raw.type) AS ctype", "raw.html AS html", "override.parsearg AS parsearg", "raw.meta as meta" ] 
qselect = ["raw.link AS link", "raw.type ctype", "raw.html AS html", "'' AS parsearg", "raw.meta as meta" ] 
qselect.append('"" as otype, raw.type as rtype')
qfrom = ["FROM raw"]
qfrom.append("LEFT JOIN todo ON raw.link=todo.link") 
qfrom.append("LEFT JOIN output ON raw.link=output.link")
#qfrom.append("LEFT JOIN override ON raw.link=override.link")
#qwhere = ['WHERE todo.link IS NOT NULL']  # fetch the filters from another variable that has been saved by the UI
qwhere = ['where ctype is "2_fco_speech"']
qlimit = "limit 2000 offset 0"
query = "%s %s %s %s" % (", ".join(qselect), " ".join(qfrom), " ".join(qwhere), qlimit)
print query
rows = scraperwiki.sqlite.select(query)
print len(rows)

print "Done query."
for i, row in enumerate(rows):
    l=logger()
    #print row['link']
    
    if 'meta' in row and row['meta']:
        try:
            meta=json.loads(row['meta'])
        except TypeError:
            print row['meta']
            raise
        except ValueError:
            # ugly hack
            meta={}
                
    else:
        meta={}
    meta['__link']=row['link']
    try:
        pdata = globals()['PARSE'+row['ctype']](row['html'], row["parsearg"], meta) # run function with name of row['type']
    except Exception, e:
        print repr(e)
        raise

    err=check(row['ctype'], pdata) # 

    for item in pdata:
        item["link"] = row["link"]

    jdata=json.dumps(pdata, indent=4)
    if err:
        jerr=json.dumps(err)
    else:
        jerr=None
    
    sql={'link': row["link"],
         'err': jerr,
         'data': jdata}

    if l.log: print meta['__link'], l.log # TODO: make this save to datastore or something... work it out!
    if l.log: scraperwiki.sqlite.save(unique_keys=['link'], data= {'link':meta['__link'], 'log':l.log}, table_name="hmmm")
    scraperwiki.sqlite.save(unique_keys=["link"], data=sql, table_name="output", verbose=0)
    if i%20 == 0: print i, len(rows)


print "DONE"
