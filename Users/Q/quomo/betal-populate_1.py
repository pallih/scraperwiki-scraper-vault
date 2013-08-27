import scraperwiki
import requests
import csv
import StringIO
import string
import lxml.html
import re
import json
import xlrd
from requests import session

# Blank Python

class AspBrowser:
    def __init__(self):
        self.s = session()

    def get(self, url):
        print 'url:',repr(url)
        self.r=self.s.get(url)
        return self.r

    def doPostBack(self,eventtarget, eventargument):
        html = lxml.html.fromstring(self.r.text)

        html.make_links_absolute(self.r.url)
        url = html.xpath('//form[@name="aspnetForm"]')[0].attrib.get('action', self.r.url)

        inputs= html.xpath('//form[@name="aspnetForm"]//input[@type="hidden" and @value]')
        params= {i.attrib['name']: i.attrib['value'] for i in inputs}
        params.update({
                '__EVENTTARGET': eventtarget,
                '__EVENTARGUMENT': eventargument,
            })
        
        self.r= self.s.post(
            url,
            params
        )
        return self.r

def gettext(e):
    # get text associated with an element, both before and after.
    b=e.text or ''
    t=e.tail or ''
    if b and t:
        return b+'<br>'+t
    else:
        return b+t

def get(url): # this should be worked on to make it somewhat robust against 404, etc; and check whether in datastore?
    'http://www.nationalarchives.gov.uk/documents/information-management/redirection-technical-guidance-for-departments-v4.2-web-version.pdf'
    url = re.sub(':/+','://',url) # yuck!
    while True:
        print "URL: ", repr(url)
        try:
            return requests.get(url, verify=False)
        except Exception, e:
            print 'Exception', repr(e), 'on', url
            if 'URLRequired()' in repr(e):
                exit()
            raise
            

############


def bis_pub_list():
    def parseindexpage(url='https://www.dropbox.com/s/z2gh25ui8hf6v6m/bis.csv?dl=1', index=None):
        """extract data from a single CSV file"""
        r=get(url)
        raw=r.content
        r.raise_for_status()
        csvreader = csv.reader(StringIO.StringIO(raw))
        builder=[]
        for row in csvreader:
            try: # title - IGNORED
                title=row[2]
            except IndexError:
                title=None
            if row[0]: # category - IGNORED
                cat=row[0]
            if row[1]: # url
                page_req=get(row[1])
                page_raw=page_req.content
                page_stat=page_req.status_code
                builder.append({'link':row[1], 'type':index, 'html':page_raw, 'status':page_stat})
        scraperwiki.sqlite.save(table_name='raw',data=builder, unique_keys=['link'],verbose=0)
        return builder

    indexes={'news':'https://www.dropbox.com/s/o2psri903n424rq/BIS.gov.uk%20URLs%20-%20News.csv?dl=1',
             #'consult':'https://www.dropbox.com/s/2tajehnwhxqkf87/BIS.gov.uk%20URLs%20-%20Consultations.csv?dl=1',
             'pubs':'https://www.dropbox.com/s/hzsjxvzy65e8wol/BIS.gov.uk%20URLs%20-%20Publications.csv?dl=1',
             'speeches':'https://www.dropbox.com/s/qwg6qmq3bgi7nz7/BIS.gov.uk%20URLs%20-%20Speeches.csv?dl=1'}
    builder=[]
    for i in indexes:
        builder.extend(parseindexpage(indexes[i],i))
    return builder

###########

def bis_pub_server():
    def getrows(char=None, url=None):
        """returns rows on a page"""
        if not url:
            baseurl='http://bis.ecgroup.net/Search.aspx?AtoZ=%s' % char
        else:
            baseurl=url
        asp=AspBrowser()
        first=asp.get(baseurl)
        r=asp.doPostBack('ctl00$MainContent$SearchResults$lnkPageSizeAll','')
        root=lxml.html.fromstring(r.content)
        xpath=root.xpath("//table[@id='ctl00_MainContent_SearchResults_gvResults']//tr[@class='gridRow' or @class='gridRowAlternate']")
        link=['http://bis.ecgroup.net/page.aspx?urn='+x.cssselect('td')[1].text for x in xpath]
        print link
        # do more parsing
        print len(xpath)
        meta={'originurl':baseurl}
        if 'Publications' in baseurl:
            match=re.match("http://bis.ecgroup.net/Publications/(.*)/(.*).aspx", baseurl)
            if match:
                (meta['cat'], meta['subcat'])=match.groups()
            
        return [{'link':link[i], 'type':'pub_server', 'html':lxml.html.tostring(x), 'status':r.status_code, 'meta':json.dumps(meta)} for i,x in enumerate(xpath)]
    
    def saveaz(): # TODO
        builder=[]
        for a in string.uppercase:
             builder.extend(getrows(char=a))
        return builder
    
    def getcats():
        baseurl='http://bis.ecgroup.net/Browse.aspx'
        html=scraperwiki.scrape(baseurl)
        root=lxml.html.fromstring(html)
        root.make_links_absolute(baseurl)
        builder=[]
        for supercat in root.xpath("//li[@class='categoryItem']"):
            supercatname=supercat.cssselect('h2')[0].text
            for cat in supercat.cssselect('a'):
                builder.append([supercatname.partition('(')[0].strip(), cat.text.partition('(')[0].strip(), cat.attrib['href']])
        return builder
    
    def savecats():
        builder=[]
        for cat in getcats():
            print cat[1]
            builder.extend(getrows(url=cat[2]))
        return builder
    print 'az'
    scraperwiki.sqlite.save(table_name='raw',data=saveaz(), unique_keys=['link'],verbose=0)
    print 'cats'
    scraperwiki.sqlite.save(table_name='raw',data=savecats(), unique_keys=['link'], verbose=0)

def getxls(url, index, sheet=0, link=0, title=1):
    print index, sheet, url
    r=get(url)
    raw=r.content
    r.raise_for_status()
    book = xlrd.open_workbook(file_contents=raw)
    sheet = book.sheet_by_index(sheet)
    builder=[]
    for row in [sheet.row(i) for i in range(sheet.nrows)]:
        data={}
        data['link']=row[link].value
        if data['link'].strip()=='':
            continue
        data['title']=row[title].value
        page_req=get(data['link'])
        page_raw=page_req.content
        data['status']=page_req.status_code
        data['html']=page_raw
        data['html']=unicode(page_raw, 'iso-8859-1')
        data['meta']={}
        data['type']=index
        scraperwiki.sqlite.save(table_name='raw',data=data, unique_keys=['link'],verbose=0)
    return None

def getcsv(url, index, link=0, title=1, skip=[]):
    print url, index
    r=get(url)
    raw=r.content
    r.raise_for_status()
    csvreader = csv.reader(StringIO.StringIO(raw))
    builder=[]
    donelist=[x['link'] for x in scraperwiki.sqlite.select("link from raw where type=?", index)]
    for i,r in enumerate(csvreader):
        if i in skip:
            continue
        if len(r) <= link:
            continue
        if r[link].strip()=='':
            continue
        if r[link].strip() in donelist:
            continue
        print i,r
        page_req=get(r[link].strip())
        #page_raw=page_req.content
        page_raw=page_req.text
        page_stat=page_req.status_code
        page_u=unicode(page_raw) # , 'iso-8859-1'
        if title is not None:
            t=r[title]
        else:
            t=''
        data={'link':r[link].strip(), 'title':t, 'html':page_u, 'status':page_stat, 'meta':{}, 'type':index}
        builder.append(data)
        scraperwiki.sqlite.save(table_name='raw',data=data, unique_keys=['link'],verbose=0)
    return builder

def blinktrade():
    getcsv(url='https://www.dropbox.com/s/4fnq8shwf3yg2nk/International%20trade%20BLink%20analysis%20-%20Guides%20to%20scrape.csv?dl=1', link=1, title=0, index='tradeanalysis')

def blinkfarm():
    getcsv(url='https://www.dropbox.com/s/xn1tmpt1i6o3o1a/Farming%20and%20Excise%20for%20scraping%20-%20Sheet1.csv?dl=1', link=1, title=0, index='farmexcise')

def mod():
    url='https://www.dropbox.com/s/12exno8v7qmbult/MoD%20URLs%20FINAL.xls?dl=1'
    news=getxls(url, 'modnews', sheet=1, title=0, link=1)
    speeches=getxls(url, 'modspeech', sheet=2, title=0, link=1)
    consult=getxls(url, 'modconsult', sheet=3, title=0, link=1)
    pubs=getxls(url, 'modpubs', sheet=4, title=0, link=1)

def bis_consult():
    params={'pp':50,
        'start':1}
    
    baseurls=["http://www.bis.gov.uk/Consultations/category/open", "http://www.bis.gov.uk/Consultations/category/closedwithresponse", "http://www.bis.gov.uk/Consultations/category/closedawaitingresponse"]
    
    # ignoring "http://www.bis.gov.uk/Consultations/category/closingsoon",  since it has no content.
    builder=[]
    for url in baseurls:
        myparams=dict(params)
        loop=True
        while loop:
            print url, myparams['start']
            html=requests.get(url, params=myparams).content
            root=lxml.html.fromstring(html)
            root.make_links_absolute(url)
            links=root.xpath("//ul[@id='listing']/li//a")
            for item in links:
                print url
                url=item.attrib['href']
                page_req=get(url)
                page_u=page_req.text # guess
                page_stat=page_req.status_code
        
                data={'link':url, 'title':item.text, 'html':page_u, 'status':page_stat, 'meta':{}, 'type':'consult'}
                builder.append(data)
            loop=len(links)==50
            myparams['start']=myparams['start']+1
    scraperwiki.sqlite.save(table_name='raw', data=builder, unique_keys=['link'])

def fco_news():
    #url='https://www.dropbox.com/s/jtn15ub4heka055/FCO%20scraping%20instructions%20-%20News%20URLs.csv?dl=1'
    #getcsv(url=url, link=0, title=None, index='fco_news')
    url='https://www.dropbox.com/s/47c1ucc28z1evt0/FCO%20scraping%20instructions%20NEW%20-%20News%20URLs%20v2.csv?dl=1'
    getcsv(url=url, link=0, title=None, index='fco_news', skip=range(0,3333))

def fco_speech():
    pass
    #url='https://www.dropbox.com/s/37vnq4biggqvtbl/FCO%20scraping%20instructions%20-%20Speech%20URLs.csv?dl=1'
    #getcsv(url=url, link=0, title=None, index='fco_speech')


def phase2():
    urls='''https://dl.dropbox.com/s/7mp9miw6c8jx6ho/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20BIS%20Consultation%20%2816%29.csv
https://dl.dropbox.com/s/eya0sujvxi9xxcx/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20BIS%20News%20%2877%29.csv
https://dl.dropbox.com/s/cemnhmqu4m8x7ff/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20BIS%20Speech%20%2822%29.csv
https://dl.dropbox.com/s/xk0zcu5v0itg1bg/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20FCO%20News%20%28220%29.csv
https://dl.dropbox.com/s/w9twmxr9ptnd13e/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20FCO%20Speech%20%2824%29.csv
https://dl.dropbox.com/s/jiiw60ialrch2u4/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20MOD%20News%20%28674%29.csv
https://dl.dropbox.com/s/1dgqs3zuriny9gh/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20MOD%20Publications%20%28279%29.csv
https://dl.dropbox.com/s/w9bcdf6b59jcvnm/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20MOD%20Speeches%20%2827%29.csv'''
    indexes = '''2_bis_con
2_bis_news
2_bis_speech
2_fco_news
2_fco_speech
2_mod_news
2_mod_pubs
2_mod_speech'''

    pairs = zip(urls.split('\n'), indexes.split('\n'))
    for i in pairs:
        print i
        getcsv(url=i[0], link=0, title=0, index=i[1], skip=[])
    print "done"
    exit()


def man_and_mar():
    url='https://www.dropbox.com/s/hzkg8urua2aj0q7/Manufacturing%20and%20Maritime%20guides%20for%20scraping%20280812%20-%20Sheet1.csv?dl=1'
    getcsv(url=url, link=2, title=3, index='man_and_mar', skip=[0])

def transadv():
    url="https://dl.dropbox.com/s/tqi3t6uoa4gtklp/Transport%20and%20Adviser%20links%20-%20Sheet1.csv"
    getcsv(url=url, link=0, title=3, index='transadv', skip=[0])

def specialist():
    url='https://dl.dropbox.com/s/c1beyv9swa83qzz/Definitive%20specialist%20list%20-%20Missing%20specialist%20to%20scrape.csv'
    getcsv(url=url, link=1, title=2, index='specialist', skip=[0])

def dclg_news():
    getcsv(url='https://www.dropbox.com/s/jh7tqbjlpgwal6b/DCLG%20scraping%20instructions%20-%20News%20URLs.csv?dl=1', link=1, title=0, index='dclg_news')

def dclg_news2():
    getcsv(url='https://www.dropbox.com/s/fw2rw7x6in91l37/DCLG scraping instructions part 2 - News URLs.csv?dl=1', link=0, title=0, index="dclg_news2")

def dclg_news3():
    getcsv(url='https://www.dropbox.com/s/1bq4yap73xqyxjk/DCLG%20scraping%20instructions%20part%202%20-%20News%20-%20Attempt%20pt3%2C%20full%20list.csv?dl=1',
           link = 0, title = 0, index = "dclg_news3")

def dclg_data():
    getcsv(url='https://www.dropbox.com/s/dv0wgonz5gtjzh6/DCLG%20Scraping%20Instructions%20pt3%20-%20Data%20Tables%20%252B%20News%20-%20Data%20Tables.csv?dl=1', link = 0, title = 0, index = "dclg_data", skip = [0])

def dclg_speeches():
    getcsv(url='https://www.dropbox.com/s/vs3bp4tcgo3stbi/DCLG%20scraping%20instructions%20-%20Speech%20URLs.csv?dl=1', link=1, title=0, index='dclg_speech')

def dclg_speeches2():
    getcsv(url='https://www.dropbox.com/s/zb37okqrpg2z3dv/DCLG%20scraping%20instructions%20part%202%20-%20Speech%20URLs.csv?dl=1', link=1, title=1, index='dclg_speech2')

def dclg_consult():
    sess=session()
    sess.get('http://www.communities.gov.uk/corporate/publications/consultations/') # set cookies
    
    baseurl='http://www.communities.gov.uk/corporate/publications/consultations/?doPaging=true&resultsPerPage=1000&currentPageNumber=1'
    resp=sess.get(baseurl)
    html=resp.content
    root=lxml.html.fromstring(html)
    root.make_links_absolute(baseurl)
    links=root.xpath("//form[@id='frmConsultations']//a")
    linklist=[x.get('href') for x in links]
    linkstring = "('"+"','".join(linklist)+"')"
    print linkstring
    gotalready=scraperwiki.sqlite.select("link from raw where link in "+linkstring+" and type = 'dclg_consult'")
    gotlinks=[x['link'] for x in gotalready]
    print len(gotlinks)
    print len(links)
    for link in links:
        #gotalready=scraperwiki.sqlite.select ("link from raw where link = ? and type = 'dclg_consult'", link.get('href'))
        if link.get('href') in gotlinks:
            #print "Skip %r"% gotalready
            continue
                
        print 'get',link.get('href')
        page_req=get(link.get('href'))
        page_u=page_req.text # guess
        page_stat=page_req.status_code
        print page_stat

        data={'link':link.get('href'), 'title':link.text_content(), 'html':page_u, 'status':page_stat, 'meta':{}, 'type':'dclg_consult'}
        print 'save'
        scraperwiki.sqlite.save(table_name='raw', data=data, unique_keys=['link'])

def dclg_pubs(cat='communities', url=None, t='dclg_pubs'):
        if not url:
            url = 'http://www.communities.gov.uk/%s/publications/all/'%cat
        page=scraperwiki.sqlite.get_var('dclg_pub_'+cat)
        if not page:
            page=1
        print page
        bail=False
        while not bail:
            print url, page
            
            params={'viewPrevious':'true','currentPageNumber':page}
            html=requests.get(url, params=params).content
            root=lxml.html.fromstring(html)
            root.make_links_absolute(url)
            links=root.xpath("//ul[@class='searchResultList']//h4/a")
            if len(links)<20:
                print "Only %d links on page %d of %s... bailing"%(len(links), page, url)
                bail=True
                
            builder=[]
            for link in links:
                newurl=link.get('href')
                gotalready=scraperwiki.sqlite.select ("link from raw where link = ? and type = ?", [newurl, t])
                if len(gotalready)>0:
                #  print "Skip %r", gotalready
                   continue
                page_req=get(newurl)
                page_u=page_req.text # guess
                page_stat=page_req.status_code
        
                data={'link':newurl, 'title':link.text_content(), 'html':page_u, 'status':page_stat, 'meta':{'subtype':cat}, 'type':t} # TODO: META is wrong, should be json.
                builder.append(data)
            scraperwiki.sqlite.save(table_name='raw', data=builder, unique_keys=['link'])
            page=page+1
            scraperwiki.sqlite.save_var('dclg_pub_'+cat, page)
            


###########

#scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS type_index ON raw (type)')
#scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS link_index ON raw (link)')

phase2()
exit()
pairs = [['nr_pn','http://www.communities.gov.uk/newsroom/pressnotices/'],
         ['nr_iar','http://www.communities.gov.uk/newsroom/issuesandresponses/'],
         ['nr_n','http://www.communities.gov.uk/newsroom/news/'],
         ['f_nr_ns','http://www.communities.gov.uk/fire/newsroom/newsstories/'],
         ['f_nr_n','http://www.communities.gov.uk/fire/newsroom/news/'],
         ['h_nr_ns','http://www.communities.gov.uk/housing/newsroom/newsstories/'],
         ['h_nr','http://www.communities.gov.uk/housing/newsroom/'],
         ['c_nr,ns','http://www.communities.gov.uk/corporate/newsroom/newsstories/'],
         ['c_nr_n','http://www.communities.gov.uk/corporate/newsroom/news/'],
         ['r_nr_ns','http://www.communities.gov.uk/regeneration/newsroom/newsstories/'],
         ['r_nr_n','http://www.communities.gov.uk/regeneration/newsroom/news/'],
         ['cs_nr_ns','http://www.communities.gov.uk/communities/newsroom/newsstories/'],
         ['cs_nr_n','http://www.communities.gov.uk/communities/newsroom/news/'],
         ['lg_nr_ns','http://www.communities.gov.uk/localgovernment/newsroom/newsstories/'],
         ['lg_nr_n','http://www.communities.gov.uk/localgovernment/newsroom/news/']]

for i in pairs:
    print i
    dclg_pubs(i[0], i[1], 'dclg_newsscrape')

#bis_pub_list()
#bis_pub_server()
#blinktrade()
#blinkfarm()
#mod()

#bis_consult()

#dclg_consult()
#cats = ['communities', 'corporate', 'fire', 'housing', 'localgovernment',  'planningandbuilding', 'regeneration']
#cats = ['housing', 'localgovernment',  'planningandbuilding', 'regeneration']
#for cat in cats:
#    print "CAT"
#    dclg_pubs(cat)
#print "CONSULTS"
#dclg_consult()

#dclg_news2()
#dclg_news3()
dclg_data()

#print "NEWSOK"
#dclg_speeches2()

#fco_news()
#man_and_mar()
#fco_speech()
#transadv()
#specialist()
import scraperwiki
import requests
import csv
import StringIO
import string
import lxml.html
import re
import json
import xlrd
from requests import session

# Blank Python

class AspBrowser:
    def __init__(self):
        self.s = session()

    def get(self, url):
        print 'url:',repr(url)
        self.r=self.s.get(url)
        return self.r

    def doPostBack(self,eventtarget, eventargument):
        html = lxml.html.fromstring(self.r.text)

        html.make_links_absolute(self.r.url)
        url = html.xpath('//form[@name="aspnetForm"]')[0].attrib.get('action', self.r.url)

        inputs= html.xpath('//form[@name="aspnetForm"]//input[@type="hidden" and @value]')
        params= {i.attrib['name']: i.attrib['value'] for i in inputs}
        params.update({
                '__EVENTTARGET': eventtarget,
                '__EVENTARGUMENT': eventargument,
            })
        
        self.r= self.s.post(
            url,
            params
        )
        return self.r

def gettext(e):
    # get text associated with an element, both before and after.
    b=e.text or ''
    t=e.tail or ''
    if b and t:
        return b+'<br>'+t
    else:
        return b+t

def get(url): # this should be worked on to make it somewhat robust against 404, etc; and check whether in datastore?
    'http://www.nationalarchives.gov.uk/documents/information-management/redirection-technical-guidance-for-departments-v4.2-web-version.pdf'
    url = re.sub(':/+','://',url) # yuck!
    while True:
        print "URL: ", repr(url)
        try:
            return requests.get(url, verify=False)
        except Exception, e:
            print 'Exception', repr(e), 'on', url
            if 'URLRequired()' in repr(e):
                exit()
            raise
            

############


def bis_pub_list():
    def parseindexpage(url='https://www.dropbox.com/s/z2gh25ui8hf6v6m/bis.csv?dl=1', index=None):
        """extract data from a single CSV file"""
        r=get(url)
        raw=r.content
        r.raise_for_status()
        csvreader = csv.reader(StringIO.StringIO(raw))
        builder=[]
        for row in csvreader:
            try: # title - IGNORED
                title=row[2]
            except IndexError:
                title=None
            if row[0]: # category - IGNORED
                cat=row[0]
            if row[1]: # url
                page_req=get(row[1])
                page_raw=page_req.content
                page_stat=page_req.status_code
                builder.append({'link':row[1], 'type':index, 'html':page_raw, 'status':page_stat})
        scraperwiki.sqlite.save(table_name='raw',data=builder, unique_keys=['link'],verbose=0)
        return builder

    indexes={'news':'https://www.dropbox.com/s/o2psri903n424rq/BIS.gov.uk%20URLs%20-%20News.csv?dl=1',
             #'consult':'https://www.dropbox.com/s/2tajehnwhxqkf87/BIS.gov.uk%20URLs%20-%20Consultations.csv?dl=1',
             'pubs':'https://www.dropbox.com/s/hzsjxvzy65e8wol/BIS.gov.uk%20URLs%20-%20Publications.csv?dl=1',
             'speeches':'https://www.dropbox.com/s/qwg6qmq3bgi7nz7/BIS.gov.uk%20URLs%20-%20Speeches.csv?dl=1'}
    builder=[]
    for i in indexes:
        builder.extend(parseindexpage(indexes[i],i))
    return builder

###########

def bis_pub_server():
    def getrows(char=None, url=None):
        """returns rows on a page"""
        if not url:
            baseurl='http://bis.ecgroup.net/Search.aspx?AtoZ=%s' % char
        else:
            baseurl=url
        asp=AspBrowser()
        first=asp.get(baseurl)
        r=asp.doPostBack('ctl00$MainContent$SearchResults$lnkPageSizeAll','')
        root=lxml.html.fromstring(r.content)
        xpath=root.xpath("//table[@id='ctl00_MainContent_SearchResults_gvResults']//tr[@class='gridRow' or @class='gridRowAlternate']")
        link=['http://bis.ecgroup.net/page.aspx?urn='+x.cssselect('td')[1].text for x in xpath]
        print link
        # do more parsing
        print len(xpath)
        meta={'originurl':baseurl}
        if 'Publications' in baseurl:
            match=re.match("http://bis.ecgroup.net/Publications/(.*)/(.*).aspx", baseurl)
            if match:
                (meta['cat'], meta['subcat'])=match.groups()
            
        return [{'link':link[i], 'type':'pub_server', 'html':lxml.html.tostring(x), 'status':r.status_code, 'meta':json.dumps(meta)} for i,x in enumerate(xpath)]
    
    def saveaz(): # TODO
        builder=[]
        for a in string.uppercase:
             builder.extend(getrows(char=a))
        return builder
    
    def getcats():
        baseurl='http://bis.ecgroup.net/Browse.aspx'
        html=scraperwiki.scrape(baseurl)
        root=lxml.html.fromstring(html)
        root.make_links_absolute(baseurl)
        builder=[]
        for supercat in root.xpath("//li[@class='categoryItem']"):
            supercatname=supercat.cssselect('h2')[0].text
            for cat in supercat.cssselect('a'):
                builder.append([supercatname.partition('(')[0].strip(), cat.text.partition('(')[0].strip(), cat.attrib['href']])
        return builder
    
    def savecats():
        builder=[]
        for cat in getcats():
            print cat[1]
            builder.extend(getrows(url=cat[2]))
        return builder
    print 'az'
    scraperwiki.sqlite.save(table_name='raw',data=saveaz(), unique_keys=['link'],verbose=0)
    print 'cats'
    scraperwiki.sqlite.save(table_name='raw',data=savecats(), unique_keys=['link'], verbose=0)

def getxls(url, index, sheet=0, link=0, title=1):
    print index, sheet, url
    r=get(url)
    raw=r.content
    r.raise_for_status()
    book = xlrd.open_workbook(file_contents=raw)
    sheet = book.sheet_by_index(sheet)
    builder=[]
    for row in [sheet.row(i) for i in range(sheet.nrows)]:
        data={}
        data['link']=row[link].value
        if data['link'].strip()=='':
            continue
        data['title']=row[title].value
        page_req=get(data['link'])
        page_raw=page_req.content
        data['status']=page_req.status_code
        data['html']=page_raw
        data['html']=unicode(page_raw, 'iso-8859-1')
        data['meta']={}
        data['type']=index
        scraperwiki.sqlite.save(table_name='raw',data=data, unique_keys=['link'],verbose=0)
    return None

def getcsv(url, index, link=0, title=1, skip=[]):
    print url, index
    r=get(url)
    raw=r.content
    r.raise_for_status()
    csvreader = csv.reader(StringIO.StringIO(raw))
    builder=[]
    donelist=[x['link'] for x in scraperwiki.sqlite.select("link from raw where type=?", index)]
    for i,r in enumerate(csvreader):
        if i in skip:
            continue
        if len(r) <= link:
            continue
        if r[link].strip()=='':
            continue
        if r[link].strip() in donelist:
            continue
        print i,r
        page_req=get(r[link].strip())
        #page_raw=page_req.content
        page_raw=page_req.text
        page_stat=page_req.status_code
        page_u=unicode(page_raw) # , 'iso-8859-1'
        if title is not None:
            t=r[title]
        else:
            t=''
        data={'link':r[link].strip(), 'title':t, 'html':page_u, 'status':page_stat, 'meta':{}, 'type':index}
        builder.append(data)
        scraperwiki.sqlite.save(table_name='raw',data=data, unique_keys=['link'],verbose=0)
    return builder

def blinktrade():
    getcsv(url='https://www.dropbox.com/s/4fnq8shwf3yg2nk/International%20trade%20BLink%20analysis%20-%20Guides%20to%20scrape.csv?dl=1', link=1, title=0, index='tradeanalysis')

def blinkfarm():
    getcsv(url='https://www.dropbox.com/s/xn1tmpt1i6o3o1a/Farming%20and%20Excise%20for%20scraping%20-%20Sheet1.csv?dl=1', link=1, title=0, index='farmexcise')

def mod():
    url='https://www.dropbox.com/s/12exno8v7qmbult/MoD%20URLs%20FINAL.xls?dl=1'
    news=getxls(url, 'modnews', sheet=1, title=0, link=1)
    speeches=getxls(url, 'modspeech', sheet=2, title=0, link=1)
    consult=getxls(url, 'modconsult', sheet=3, title=0, link=1)
    pubs=getxls(url, 'modpubs', sheet=4, title=0, link=1)

def bis_consult():
    params={'pp':50,
        'start':1}
    
    baseurls=["http://www.bis.gov.uk/Consultations/category/open", "http://www.bis.gov.uk/Consultations/category/closedwithresponse", "http://www.bis.gov.uk/Consultations/category/closedawaitingresponse"]
    
    # ignoring "http://www.bis.gov.uk/Consultations/category/closingsoon",  since it has no content.
    builder=[]
    for url in baseurls:
        myparams=dict(params)
        loop=True
        while loop:
            print url, myparams['start']
            html=requests.get(url, params=myparams).content
            root=lxml.html.fromstring(html)
            root.make_links_absolute(url)
            links=root.xpath("//ul[@id='listing']/li//a")
            for item in links:
                print url
                url=item.attrib['href']
                page_req=get(url)
                page_u=page_req.text # guess
                page_stat=page_req.status_code
        
                data={'link':url, 'title':item.text, 'html':page_u, 'status':page_stat, 'meta':{}, 'type':'consult'}
                builder.append(data)
            loop=len(links)==50
            myparams['start']=myparams['start']+1
    scraperwiki.sqlite.save(table_name='raw', data=builder, unique_keys=['link'])

def fco_news():
    #url='https://www.dropbox.com/s/jtn15ub4heka055/FCO%20scraping%20instructions%20-%20News%20URLs.csv?dl=1'
    #getcsv(url=url, link=0, title=None, index='fco_news')
    url='https://www.dropbox.com/s/47c1ucc28z1evt0/FCO%20scraping%20instructions%20NEW%20-%20News%20URLs%20v2.csv?dl=1'
    getcsv(url=url, link=0, title=None, index='fco_news', skip=range(0,3333))

def fco_speech():
    pass
    #url='https://www.dropbox.com/s/37vnq4biggqvtbl/FCO%20scraping%20instructions%20-%20Speech%20URLs.csv?dl=1'
    #getcsv(url=url, link=0, title=None, index='fco_speech')


def phase2():
    urls='''https://dl.dropbox.com/s/7mp9miw6c8jx6ho/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20BIS%20Consultation%20%2816%29.csv
https://dl.dropbox.com/s/eya0sujvxi9xxcx/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20BIS%20News%20%2877%29.csv
https://dl.dropbox.com/s/cemnhmqu4m8x7ff/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20BIS%20Speech%20%2822%29.csv
https://dl.dropbox.com/s/xk0zcu5v0itg1bg/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20FCO%20News%20%28220%29.csv
https://dl.dropbox.com/s/w9twmxr9ptnd13e/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20FCO%20Speech%20%2824%29.csv
https://dl.dropbox.com/s/jiiw60ialrch2u4/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20MOD%20News%20%28674%29.csv
https://dl.dropbox.com/s/1dgqs3zuriny9gh/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20MOD%20Publications%20%28279%29.csv
https://dl.dropbox.com/s/w9bcdf6b59jcvnm/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20MOD%20Speeches%20%2827%29.csv'''
    indexes = '''2_bis_con
2_bis_news
2_bis_speech
2_fco_news
2_fco_speech
2_mod_news
2_mod_pubs
2_mod_speech'''

    pairs = zip(urls.split('\n'), indexes.split('\n'))
    for i in pairs:
        print i
        getcsv(url=i[0], link=0, title=0, index=i[1], skip=[])
    print "done"
    exit()


def man_and_mar():
    url='https://www.dropbox.com/s/hzkg8urua2aj0q7/Manufacturing%20and%20Maritime%20guides%20for%20scraping%20280812%20-%20Sheet1.csv?dl=1'
    getcsv(url=url, link=2, title=3, index='man_and_mar', skip=[0])

def transadv():
    url="https://dl.dropbox.com/s/tqi3t6uoa4gtklp/Transport%20and%20Adviser%20links%20-%20Sheet1.csv"
    getcsv(url=url, link=0, title=3, index='transadv', skip=[0])

def specialist():
    url='https://dl.dropbox.com/s/c1beyv9swa83qzz/Definitive%20specialist%20list%20-%20Missing%20specialist%20to%20scrape.csv'
    getcsv(url=url, link=1, title=2, index='specialist', skip=[0])

def dclg_news():
    getcsv(url='https://www.dropbox.com/s/jh7tqbjlpgwal6b/DCLG%20scraping%20instructions%20-%20News%20URLs.csv?dl=1', link=1, title=0, index='dclg_news')

def dclg_news2():
    getcsv(url='https://www.dropbox.com/s/fw2rw7x6in91l37/DCLG scraping instructions part 2 - News URLs.csv?dl=1', link=0, title=0, index="dclg_news2")

def dclg_news3():
    getcsv(url='https://www.dropbox.com/s/1bq4yap73xqyxjk/DCLG%20scraping%20instructions%20part%202%20-%20News%20-%20Attempt%20pt3%2C%20full%20list.csv?dl=1',
           link = 0, title = 0, index = "dclg_news3")

def dclg_data():
    getcsv(url='https://www.dropbox.com/s/dv0wgonz5gtjzh6/DCLG%20Scraping%20Instructions%20pt3%20-%20Data%20Tables%20%252B%20News%20-%20Data%20Tables.csv?dl=1', link = 0, title = 0, index = "dclg_data", skip = [0])

def dclg_speeches():
    getcsv(url='https://www.dropbox.com/s/vs3bp4tcgo3stbi/DCLG%20scraping%20instructions%20-%20Speech%20URLs.csv?dl=1', link=1, title=0, index='dclg_speech')

def dclg_speeches2():
    getcsv(url='https://www.dropbox.com/s/zb37okqrpg2z3dv/DCLG%20scraping%20instructions%20part%202%20-%20Speech%20URLs.csv?dl=1', link=1, title=1, index='dclg_speech2')

def dclg_consult():
    sess=session()
    sess.get('http://www.communities.gov.uk/corporate/publications/consultations/') # set cookies
    
    baseurl='http://www.communities.gov.uk/corporate/publications/consultations/?doPaging=true&resultsPerPage=1000&currentPageNumber=1'
    resp=sess.get(baseurl)
    html=resp.content
    root=lxml.html.fromstring(html)
    root.make_links_absolute(baseurl)
    links=root.xpath("//form[@id='frmConsultations']//a")
    linklist=[x.get('href') for x in links]
    linkstring = "('"+"','".join(linklist)+"')"
    print linkstring
    gotalready=scraperwiki.sqlite.select("link from raw where link in "+linkstring+" and type = 'dclg_consult'")
    gotlinks=[x['link'] for x in gotalready]
    print len(gotlinks)
    print len(links)
    for link in links:
        #gotalready=scraperwiki.sqlite.select ("link from raw where link = ? and type = 'dclg_consult'", link.get('href'))
        if link.get('href') in gotlinks:
            #print "Skip %r"% gotalready
            continue
                
        print 'get',link.get('href')
        page_req=get(link.get('href'))
        page_u=page_req.text # guess
        page_stat=page_req.status_code
        print page_stat

        data={'link':link.get('href'), 'title':link.text_content(), 'html':page_u, 'status':page_stat, 'meta':{}, 'type':'dclg_consult'}
        print 'save'
        scraperwiki.sqlite.save(table_name='raw', data=data, unique_keys=['link'])

def dclg_pubs(cat='communities', url=None, t='dclg_pubs'):
        if not url:
            url = 'http://www.communities.gov.uk/%s/publications/all/'%cat
        page=scraperwiki.sqlite.get_var('dclg_pub_'+cat)
        if not page:
            page=1
        print page
        bail=False
        while not bail:
            print url, page
            
            params={'viewPrevious':'true','currentPageNumber':page}
            html=requests.get(url, params=params).content
            root=lxml.html.fromstring(html)
            root.make_links_absolute(url)
            links=root.xpath("//ul[@class='searchResultList']//h4/a")
            if len(links)<20:
                print "Only %d links on page %d of %s... bailing"%(len(links), page, url)
                bail=True
                
            builder=[]
            for link in links:
                newurl=link.get('href')
                gotalready=scraperwiki.sqlite.select ("link from raw where link = ? and type = ?", [newurl, t])
                if len(gotalready)>0:
                #  print "Skip %r", gotalready
                   continue
                page_req=get(newurl)
                page_u=page_req.text # guess
                page_stat=page_req.status_code
        
                data={'link':newurl, 'title':link.text_content(), 'html':page_u, 'status':page_stat, 'meta':{'subtype':cat}, 'type':t} # TODO: META is wrong, should be json.
                builder.append(data)
            scraperwiki.sqlite.save(table_name='raw', data=builder, unique_keys=['link'])
            page=page+1
            scraperwiki.sqlite.save_var('dclg_pub_'+cat, page)
            


###########

#scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS type_index ON raw (type)')
#scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS link_index ON raw (link)')

phase2()
exit()
pairs = [['nr_pn','http://www.communities.gov.uk/newsroom/pressnotices/'],
         ['nr_iar','http://www.communities.gov.uk/newsroom/issuesandresponses/'],
         ['nr_n','http://www.communities.gov.uk/newsroom/news/'],
         ['f_nr_ns','http://www.communities.gov.uk/fire/newsroom/newsstories/'],
         ['f_nr_n','http://www.communities.gov.uk/fire/newsroom/news/'],
         ['h_nr_ns','http://www.communities.gov.uk/housing/newsroom/newsstories/'],
         ['h_nr','http://www.communities.gov.uk/housing/newsroom/'],
         ['c_nr,ns','http://www.communities.gov.uk/corporate/newsroom/newsstories/'],
         ['c_nr_n','http://www.communities.gov.uk/corporate/newsroom/news/'],
         ['r_nr_ns','http://www.communities.gov.uk/regeneration/newsroom/newsstories/'],
         ['r_nr_n','http://www.communities.gov.uk/regeneration/newsroom/news/'],
         ['cs_nr_ns','http://www.communities.gov.uk/communities/newsroom/newsstories/'],
         ['cs_nr_n','http://www.communities.gov.uk/communities/newsroom/news/'],
         ['lg_nr_ns','http://www.communities.gov.uk/localgovernment/newsroom/newsstories/'],
         ['lg_nr_n','http://www.communities.gov.uk/localgovernment/newsroom/news/']]

for i in pairs:
    print i
    dclg_pubs(i[0], i[1], 'dclg_newsscrape')

#bis_pub_list()
#bis_pub_server()
#blinktrade()
#blinkfarm()
#mod()

#bis_consult()

#dclg_consult()
#cats = ['communities', 'corporate', 'fire', 'housing', 'localgovernment',  'planningandbuilding', 'regeneration']
#cats = ['housing', 'localgovernment',  'planningandbuilding', 'regeneration']
#for cat in cats:
#    print "CAT"
#    dclg_pubs(cat)
#print "CONSULTS"
#dclg_consult()

#dclg_news2()
#dclg_news3()
dclg_data()

#print "NEWSOK"
#dclg_speeches2()

#fco_news()
#man_and_mar()
#fco_speech()
#transadv()
#specialist()
import scraperwiki
import requests
import csv
import StringIO
import string
import lxml.html
import re
import json
import xlrd
from requests import session

# Blank Python

class AspBrowser:
    def __init__(self):
        self.s = session()

    def get(self, url):
        print 'url:',repr(url)
        self.r=self.s.get(url)
        return self.r

    def doPostBack(self,eventtarget, eventargument):
        html = lxml.html.fromstring(self.r.text)

        html.make_links_absolute(self.r.url)
        url = html.xpath('//form[@name="aspnetForm"]')[0].attrib.get('action', self.r.url)

        inputs= html.xpath('//form[@name="aspnetForm"]//input[@type="hidden" and @value]')
        params= {i.attrib['name']: i.attrib['value'] for i in inputs}
        params.update({
                '__EVENTTARGET': eventtarget,
                '__EVENTARGUMENT': eventargument,
            })
        
        self.r= self.s.post(
            url,
            params
        )
        return self.r

def gettext(e):
    # get text associated with an element, both before and after.
    b=e.text or ''
    t=e.tail or ''
    if b and t:
        return b+'<br>'+t
    else:
        return b+t

def get(url): # this should be worked on to make it somewhat robust against 404, etc; and check whether in datastore?
    'http://www.nationalarchives.gov.uk/documents/information-management/redirection-technical-guidance-for-departments-v4.2-web-version.pdf'
    url = re.sub(':/+','://',url) # yuck!
    while True:
        print "URL: ", repr(url)
        try:
            return requests.get(url, verify=False)
        except Exception, e:
            print 'Exception', repr(e), 'on', url
            if 'URLRequired()' in repr(e):
                exit()
            raise
            

############


def bis_pub_list():
    def parseindexpage(url='https://www.dropbox.com/s/z2gh25ui8hf6v6m/bis.csv?dl=1', index=None):
        """extract data from a single CSV file"""
        r=get(url)
        raw=r.content
        r.raise_for_status()
        csvreader = csv.reader(StringIO.StringIO(raw))
        builder=[]
        for row in csvreader:
            try: # title - IGNORED
                title=row[2]
            except IndexError:
                title=None
            if row[0]: # category - IGNORED
                cat=row[0]
            if row[1]: # url
                page_req=get(row[1])
                page_raw=page_req.content
                page_stat=page_req.status_code
                builder.append({'link':row[1], 'type':index, 'html':page_raw, 'status':page_stat})
        scraperwiki.sqlite.save(table_name='raw',data=builder, unique_keys=['link'],verbose=0)
        return builder

    indexes={'news':'https://www.dropbox.com/s/o2psri903n424rq/BIS.gov.uk%20URLs%20-%20News.csv?dl=1',
             #'consult':'https://www.dropbox.com/s/2tajehnwhxqkf87/BIS.gov.uk%20URLs%20-%20Consultations.csv?dl=1',
             'pubs':'https://www.dropbox.com/s/hzsjxvzy65e8wol/BIS.gov.uk%20URLs%20-%20Publications.csv?dl=1',
             'speeches':'https://www.dropbox.com/s/qwg6qmq3bgi7nz7/BIS.gov.uk%20URLs%20-%20Speeches.csv?dl=1'}
    builder=[]
    for i in indexes:
        builder.extend(parseindexpage(indexes[i],i))
    return builder

###########

def bis_pub_server():
    def getrows(char=None, url=None):
        """returns rows on a page"""
        if not url:
            baseurl='http://bis.ecgroup.net/Search.aspx?AtoZ=%s' % char
        else:
            baseurl=url
        asp=AspBrowser()
        first=asp.get(baseurl)
        r=asp.doPostBack('ctl00$MainContent$SearchResults$lnkPageSizeAll','')
        root=lxml.html.fromstring(r.content)
        xpath=root.xpath("//table[@id='ctl00_MainContent_SearchResults_gvResults']//tr[@class='gridRow' or @class='gridRowAlternate']")
        link=['http://bis.ecgroup.net/page.aspx?urn='+x.cssselect('td')[1].text for x in xpath]
        print link
        # do more parsing
        print len(xpath)
        meta={'originurl':baseurl}
        if 'Publications' in baseurl:
            match=re.match("http://bis.ecgroup.net/Publications/(.*)/(.*).aspx", baseurl)
            if match:
                (meta['cat'], meta['subcat'])=match.groups()
            
        return [{'link':link[i], 'type':'pub_server', 'html':lxml.html.tostring(x), 'status':r.status_code, 'meta':json.dumps(meta)} for i,x in enumerate(xpath)]
    
    def saveaz(): # TODO
        builder=[]
        for a in string.uppercase:
             builder.extend(getrows(char=a))
        return builder
    
    def getcats():
        baseurl='http://bis.ecgroup.net/Browse.aspx'
        html=scraperwiki.scrape(baseurl)
        root=lxml.html.fromstring(html)
        root.make_links_absolute(baseurl)
        builder=[]
        for supercat in root.xpath("//li[@class='categoryItem']"):
            supercatname=supercat.cssselect('h2')[0].text
            for cat in supercat.cssselect('a'):
                builder.append([supercatname.partition('(')[0].strip(), cat.text.partition('(')[0].strip(), cat.attrib['href']])
        return builder
    
    def savecats():
        builder=[]
        for cat in getcats():
            print cat[1]
            builder.extend(getrows(url=cat[2]))
        return builder
    print 'az'
    scraperwiki.sqlite.save(table_name='raw',data=saveaz(), unique_keys=['link'],verbose=0)
    print 'cats'
    scraperwiki.sqlite.save(table_name='raw',data=savecats(), unique_keys=['link'], verbose=0)

def getxls(url, index, sheet=0, link=0, title=1):
    print index, sheet, url
    r=get(url)
    raw=r.content
    r.raise_for_status()
    book = xlrd.open_workbook(file_contents=raw)
    sheet = book.sheet_by_index(sheet)
    builder=[]
    for row in [sheet.row(i) for i in range(sheet.nrows)]:
        data={}
        data['link']=row[link].value
        if data['link'].strip()=='':
            continue
        data['title']=row[title].value
        page_req=get(data['link'])
        page_raw=page_req.content
        data['status']=page_req.status_code
        data['html']=page_raw
        data['html']=unicode(page_raw, 'iso-8859-1')
        data['meta']={}
        data['type']=index
        scraperwiki.sqlite.save(table_name='raw',data=data, unique_keys=['link'],verbose=0)
    return None

def getcsv(url, index, link=0, title=1, skip=[]):
    print url, index
    r=get(url)
    raw=r.content
    r.raise_for_status()
    csvreader = csv.reader(StringIO.StringIO(raw))
    builder=[]
    donelist=[x['link'] for x in scraperwiki.sqlite.select("link from raw where type=?", index)]
    for i,r in enumerate(csvreader):
        if i in skip:
            continue
        if len(r) <= link:
            continue
        if r[link].strip()=='':
            continue
        if r[link].strip() in donelist:
            continue
        print i,r
        page_req=get(r[link].strip())
        #page_raw=page_req.content
        page_raw=page_req.text
        page_stat=page_req.status_code
        page_u=unicode(page_raw) # , 'iso-8859-1'
        if title is not None:
            t=r[title]
        else:
            t=''
        data={'link':r[link].strip(), 'title':t, 'html':page_u, 'status':page_stat, 'meta':{}, 'type':index}
        builder.append(data)
        scraperwiki.sqlite.save(table_name='raw',data=data, unique_keys=['link'],verbose=0)
    return builder

def blinktrade():
    getcsv(url='https://www.dropbox.com/s/4fnq8shwf3yg2nk/International%20trade%20BLink%20analysis%20-%20Guides%20to%20scrape.csv?dl=1', link=1, title=0, index='tradeanalysis')

def blinkfarm():
    getcsv(url='https://www.dropbox.com/s/xn1tmpt1i6o3o1a/Farming%20and%20Excise%20for%20scraping%20-%20Sheet1.csv?dl=1', link=1, title=0, index='farmexcise')

def mod():
    url='https://www.dropbox.com/s/12exno8v7qmbult/MoD%20URLs%20FINAL.xls?dl=1'
    news=getxls(url, 'modnews', sheet=1, title=0, link=1)
    speeches=getxls(url, 'modspeech', sheet=2, title=0, link=1)
    consult=getxls(url, 'modconsult', sheet=3, title=0, link=1)
    pubs=getxls(url, 'modpubs', sheet=4, title=0, link=1)

def bis_consult():
    params={'pp':50,
        'start':1}
    
    baseurls=["http://www.bis.gov.uk/Consultations/category/open", "http://www.bis.gov.uk/Consultations/category/closedwithresponse", "http://www.bis.gov.uk/Consultations/category/closedawaitingresponse"]
    
    # ignoring "http://www.bis.gov.uk/Consultations/category/closingsoon",  since it has no content.
    builder=[]
    for url in baseurls:
        myparams=dict(params)
        loop=True
        while loop:
            print url, myparams['start']
            html=requests.get(url, params=myparams).content
            root=lxml.html.fromstring(html)
            root.make_links_absolute(url)
            links=root.xpath("//ul[@id='listing']/li//a")
            for item in links:
                print url
                url=item.attrib['href']
                page_req=get(url)
                page_u=page_req.text # guess
                page_stat=page_req.status_code
        
                data={'link':url, 'title':item.text, 'html':page_u, 'status':page_stat, 'meta':{}, 'type':'consult'}
                builder.append(data)
            loop=len(links)==50
            myparams['start']=myparams['start']+1
    scraperwiki.sqlite.save(table_name='raw', data=builder, unique_keys=['link'])

def fco_news():
    #url='https://www.dropbox.com/s/jtn15ub4heka055/FCO%20scraping%20instructions%20-%20News%20URLs.csv?dl=1'
    #getcsv(url=url, link=0, title=None, index='fco_news')
    url='https://www.dropbox.com/s/47c1ucc28z1evt0/FCO%20scraping%20instructions%20NEW%20-%20News%20URLs%20v2.csv?dl=1'
    getcsv(url=url, link=0, title=None, index='fco_news', skip=range(0,3333))

def fco_speech():
    pass
    #url='https://www.dropbox.com/s/37vnq4biggqvtbl/FCO%20scraping%20instructions%20-%20Speech%20URLs.csv?dl=1'
    #getcsv(url=url, link=0, title=None, index='fco_speech')


def phase2():
    urls='''https://dl.dropbox.com/s/7mp9miw6c8jx6ho/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20BIS%20Consultation%20%2816%29.csv
https://dl.dropbox.com/s/eya0sujvxi9xxcx/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20BIS%20News%20%2877%29.csv
https://dl.dropbox.com/s/cemnhmqu4m8x7ff/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20BIS%20Speech%20%2822%29.csv
https://dl.dropbox.com/s/xk0zcu5v0itg1bg/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20FCO%20News%20%28220%29.csv
https://dl.dropbox.com/s/w9twmxr9ptnd13e/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20FCO%20Speech%20%2824%29.csv
https://dl.dropbox.com/s/jiiw60ialrch2u4/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20MOD%20News%20%28674%29.csv
https://dl.dropbox.com/s/1dgqs3zuriny9gh/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20MOD%20Publications%20%28279%29.csv
https://dl.dropbox.com/s/w9bcdf6b59jcvnm/Round%202%20scraping%20for%20BIS%2C%20MOD%20and%20FCO%20-%20MOD%20Speeches%20%2827%29.csv'''
    indexes = '''2_bis_con
2_bis_news
2_bis_speech
2_fco_news
2_fco_speech
2_mod_news
2_mod_pubs
2_mod_speech'''

    pairs = zip(urls.split('\n'), indexes.split('\n'))
    for i in pairs:
        print i
        getcsv(url=i[0], link=0, title=0, index=i[1], skip=[])
    print "done"
    exit()


def man_and_mar():
    url='https://www.dropbox.com/s/hzkg8urua2aj0q7/Manufacturing%20and%20Maritime%20guides%20for%20scraping%20280812%20-%20Sheet1.csv?dl=1'
    getcsv(url=url, link=2, title=3, index='man_and_mar', skip=[0])

def transadv():
    url="https://dl.dropbox.com/s/tqi3t6uoa4gtklp/Transport%20and%20Adviser%20links%20-%20Sheet1.csv"
    getcsv(url=url, link=0, title=3, index='transadv', skip=[0])

def specialist():
    url='https://dl.dropbox.com/s/c1beyv9swa83qzz/Definitive%20specialist%20list%20-%20Missing%20specialist%20to%20scrape.csv'
    getcsv(url=url, link=1, title=2, index='specialist', skip=[0])

def dclg_news():
    getcsv(url='https://www.dropbox.com/s/jh7tqbjlpgwal6b/DCLG%20scraping%20instructions%20-%20News%20URLs.csv?dl=1', link=1, title=0, index='dclg_news')

def dclg_news2():
    getcsv(url='https://www.dropbox.com/s/fw2rw7x6in91l37/DCLG scraping instructions part 2 - News URLs.csv?dl=1', link=0, title=0, index="dclg_news2")

def dclg_news3():
    getcsv(url='https://www.dropbox.com/s/1bq4yap73xqyxjk/DCLG%20scraping%20instructions%20part%202%20-%20News%20-%20Attempt%20pt3%2C%20full%20list.csv?dl=1',
           link = 0, title = 0, index = "dclg_news3")

def dclg_data():
    getcsv(url='https://www.dropbox.com/s/dv0wgonz5gtjzh6/DCLG%20Scraping%20Instructions%20pt3%20-%20Data%20Tables%20%252B%20News%20-%20Data%20Tables.csv?dl=1', link = 0, title = 0, index = "dclg_data", skip = [0])

def dclg_speeches():
    getcsv(url='https://www.dropbox.com/s/vs3bp4tcgo3stbi/DCLG%20scraping%20instructions%20-%20Speech%20URLs.csv?dl=1', link=1, title=0, index='dclg_speech')

def dclg_speeches2():
    getcsv(url='https://www.dropbox.com/s/zb37okqrpg2z3dv/DCLG%20scraping%20instructions%20part%202%20-%20Speech%20URLs.csv?dl=1', link=1, title=1, index='dclg_speech2')

def dclg_consult():
    sess=session()
    sess.get('http://www.communities.gov.uk/corporate/publications/consultations/') # set cookies
    
    baseurl='http://www.communities.gov.uk/corporate/publications/consultations/?doPaging=true&resultsPerPage=1000&currentPageNumber=1'
    resp=sess.get(baseurl)
    html=resp.content
    root=lxml.html.fromstring(html)
    root.make_links_absolute(baseurl)
    links=root.xpath("//form[@id='frmConsultations']//a")
    linklist=[x.get('href') for x in links]
    linkstring = "('"+"','".join(linklist)+"')"
    print linkstring
    gotalready=scraperwiki.sqlite.select("link from raw where link in "+linkstring+" and type = 'dclg_consult'")
    gotlinks=[x['link'] for x in gotalready]
    print len(gotlinks)
    print len(links)
    for link in links:
        #gotalready=scraperwiki.sqlite.select ("link from raw where link = ? and type = 'dclg_consult'", link.get('href'))
        if link.get('href') in gotlinks:
            #print "Skip %r"% gotalready
            continue
                
        print 'get',link.get('href')
        page_req=get(link.get('href'))
        page_u=page_req.text # guess
        page_stat=page_req.status_code
        print page_stat

        data={'link':link.get('href'), 'title':link.text_content(), 'html':page_u, 'status':page_stat, 'meta':{}, 'type':'dclg_consult'}
        print 'save'
        scraperwiki.sqlite.save(table_name='raw', data=data, unique_keys=['link'])

def dclg_pubs(cat='communities', url=None, t='dclg_pubs'):
        if not url:
            url = 'http://www.communities.gov.uk/%s/publications/all/'%cat
        page=scraperwiki.sqlite.get_var('dclg_pub_'+cat)
        if not page:
            page=1
        print page
        bail=False
        while not bail:
            print url, page
            
            params={'viewPrevious':'true','currentPageNumber':page}
            html=requests.get(url, params=params).content
            root=lxml.html.fromstring(html)
            root.make_links_absolute(url)
            links=root.xpath("//ul[@class='searchResultList']//h4/a")
            if len(links)<20:
                print "Only %d links on page %d of %s... bailing"%(len(links), page, url)
                bail=True
                
            builder=[]
            for link in links:
                newurl=link.get('href')
                gotalready=scraperwiki.sqlite.select ("link from raw where link = ? and type = ?", [newurl, t])
                if len(gotalready)>0:
                #  print "Skip %r", gotalready
                   continue
                page_req=get(newurl)
                page_u=page_req.text # guess
                page_stat=page_req.status_code
        
                data={'link':newurl, 'title':link.text_content(), 'html':page_u, 'status':page_stat, 'meta':{'subtype':cat}, 'type':t} # TODO: META is wrong, should be json.
                builder.append(data)
            scraperwiki.sqlite.save(table_name='raw', data=builder, unique_keys=['link'])
            page=page+1
            scraperwiki.sqlite.save_var('dclg_pub_'+cat, page)
            


###########

#scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS type_index ON raw (type)')
#scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS link_index ON raw (link)')

phase2()
exit()
pairs = [['nr_pn','http://www.communities.gov.uk/newsroom/pressnotices/'],
         ['nr_iar','http://www.communities.gov.uk/newsroom/issuesandresponses/'],
         ['nr_n','http://www.communities.gov.uk/newsroom/news/'],
         ['f_nr_ns','http://www.communities.gov.uk/fire/newsroom/newsstories/'],
         ['f_nr_n','http://www.communities.gov.uk/fire/newsroom/news/'],
         ['h_nr_ns','http://www.communities.gov.uk/housing/newsroom/newsstories/'],
         ['h_nr','http://www.communities.gov.uk/housing/newsroom/'],
         ['c_nr,ns','http://www.communities.gov.uk/corporate/newsroom/newsstories/'],
         ['c_nr_n','http://www.communities.gov.uk/corporate/newsroom/news/'],
         ['r_nr_ns','http://www.communities.gov.uk/regeneration/newsroom/newsstories/'],
         ['r_nr_n','http://www.communities.gov.uk/regeneration/newsroom/news/'],
         ['cs_nr_ns','http://www.communities.gov.uk/communities/newsroom/newsstories/'],
         ['cs_nr_n','http://www.communities.gov.uk/communities/newsroom/news/'],
         ['lg_nr_ns','http://www.communities.gov.uk/localgovernment/newsroom/newsstories/'],
         ['lg_nr_n','http://www.communities.gov.uk/localgovernment/newsroom/news/']]

for i in pairs:
    print i
    dclg_pubs(i[0], i[1], 'dclg_newsscrape')

#bis_pub_list()
#bis_pub_server()
#blinktrade()
#blinkfarm()
#mod()

#bis_consult()

#dclg_consult()
#cats = ['communities', 'corporate', 'fire', 'housing', 'localgovernment',  'planningandbuilding', 'regeneration']
#cats = ['housing', 'localgovernment',  'planningandbuilding', 'regeneration']
#for cat in cats:
#    print "CAT"
#    dclg_pubs(cat)
#print "CONSULTS"
#dclg_consult()

#dclg_news2()
#dclg_news3()
dclg_data()

#print "NEWSOK"
#dclg_speeches2()

#fco_news()
#man_and_mar()
#fco_speech()
#transadv()
#specialist()
