import scraperwiki
import lxml.html
import urllib
import re
import time
from httplib import BadStatusLine

def get_regions():
    scraperwiki.sqlite.execute('delete from regions')
    html = scraperwiki.scrape("http://www.sbrf.ru/adygea/ru/about/branch/list_branch/")
    root = lxml.html.document_fromstring(html)
    id=1
    for r in root.xpath('//*[@id="rid"]/option'):
    
        region_name = r.text_content() 
        region_id = r.attrib['value']
    
        if region_id == '' or region_id == 0 or region_id == '0' : continue
    
        print "Processing region: '" + region_name + "'"
        
        request_data = {'data':'cid', 'par': region_id.encode('utf-8'), 'ajax':1, 'nochache':0}
    
        locality_url = "http://www.sbrf.ru/adygea/ru/about/branch/list_branch/index.php?"+urllib.urlencode(request_data)
        html = scraperwiki.scrape(locality_url)
        html = html.decode('windows-1251')
        #print html
    
        root1 = lxml.html.fromstring(html)
    
    
        for loc in root1.xpath('//select/option'):
            locality_name = loc.text_content() 
            locality_id = loc.attrib['value']
    
            if locality_id == '' or locality_id == 0 or locality_id == '0' : continue

            data={'id': id,
                    'region_id':region_id,
                    'region_name':region_name, 
                    'locality_id': locality_id, 
                    'locality_name':locality_name}

            scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="regions")
            id+=1




class Branch:

    def __init__(self, new_id=1):
        self.row_id=new_id
        #scraperwiki.sqlite.execute('delete from branch_data')
        #scraperwiki.sqlite.execute('delete from branch_data_1')

    def processBranches(self, rid, region, location=''):
        pages=self.processBranch(rid, region, location)
        print pages
        if pages>1:
            for i in range(2,pages+1):
                print "Get page " + str(i)
                self.processBranch(rid, region, location,i)


    def doScrape(self, url, params):
        try:
            html = scraperwiki.scrape(url, params)
        except BadStatusLine:
            print "Wait 10 seconds"
            time.sleep(10)
            html = self.doScrape(url, params)

        return html
        

    def processBranch(self, rid, region, location, page='undefined'):

        request_data = {'rid115': region.encode('utf-8'),
            'cid115': location.encode('utf-8') if location != '' else '',
            'clt115':0,
            'street115':'',
            'name115':'',
            'action115':'Искать',
            'charset':'utf8',
            'page': page }

        #html = scraperwiki.scrape("http://www.sbrf.ru/adygea/ru/about/branch/list_branch/index.php", request_data)
        html = self.doScrape("http://www.sberbank.ru/ru/about/branch/list_branch/index.php", request_data)
                                   
        html = html.decode('windows-1251')
        root2 = lxml.html.fromstring(html)
        #print html
        #Extract number of pages
        pages = root2.xpath("//table/tr/td/span/a")
        #print pages 
        max_page=1
        for p in pages:
            if p.text_content() != '...' and int(p.text_content()) > max_page: max_page=int(p.text_content())
    
        #Process list of branches
        for b in root2.xpath("//div[@class='cbord2']"):
            bdata_brief = b.xpath('div[1]')[0].text_content()
            bdata_detail = b.xpath('div[2]')[0].text_content()
    
            #Find coordinates
            coords = {'lat':'', 'lon':''}
            map_link = b.xpath("a[@target='ya_map_iframe']")
            if map_link != [] and map_link[0].attrib['onclick'] != '':
                latlon=re.findall(r"viewPointOnMap\('([\d\.]+?)',.*?'([\d\.]+?)',", map_link[0].attrib['onclick'], re.I|re.U)[0]
                coords['lat']=latlon[1]
                coords['lon']=latlon[0]
                
    
            #Try to split the branch name and address
            bdata=re.findall(r'^(.+?)\r\n(.+?)\r\n', bdata_brief, re.I |re.S)
            branch_address=''
            branch_name=''
    
            if len(bdata) > 0:
                if len(bdata[0]) > 0:
                    branch_name = bdata[0][0]
    
                if len(bdata[0])==2:
                    branch_address=bdata[0][1]
    
    
            data={'id': self.row_id,
                'rid'  : rid,
                'region'     : region,
                'locality'   : location,
                'brief_info' : bdata_brief,
                'detail_info': bdata_detail,
                'short_name' : branch_name,
                'address'    : branch_address,
                'lat': coords['lat'],
                'lon': coords['lon']}
            scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='branch_data_27_dec')
            self.row_id+=1
    
        return max_page



#html = scraperwiki.scrape("http://www.sbrf.ru/adygea/ru/about/branch/list_branch/")
#root = lxml.html.document_fromstring(html)
#scraperwiki.sqlite.execute('delete from data')

#data = scraperwiki.sqlite.select("distinct region_id from regions as t1")


html1=scraperwiki.scrape("http://www.sbrf.ru/moscow/ru/about/branch/list_branch/")
root=lxml.html.document_fromstring(html1)



b=Branch(1)
i=1
#for r in data:
for r in root.xpath("//select[@id='rid']/option/@value"):

    if r==0 or r=='0': continue
    #if int(r['id']) <= 8737: continue
    #print scraperwiki.sqlite.select("id from regions where region_id='" + r['region_id'] + "' limit 1")
    #b.processBranches(1, r['region_id'])
    b.processBranches(1, r)
    #exit()
    #time.sleep(1)



import scraperwiki
import lxml.html
import urllib
import re
import time
from httplib import BadStatusLine

def get_regions():
    scraperwiki.sqlite.execute('delete from regions')
    html = scraperwiki.scrape("http://www.sbrf.ru/adygea/ru/about/branch/list_branch/")
    root = lxml.html.document_fromstring(html)
    id=1
    for r in root.xpath('//*[@id="rid"]/option'):
    
        region_name = r.text_content() 
        region_id = r.attrib['value']
    
        if region_id == '' or region_id == 0 or region_id == '0' : continue
    
        print "Processing region: '" + region_name + "'"
        
        request_data = {'data':'cid', 'par': region_id.encode('utf-8'), 'ajax':1, 'nochache':0}
    
        locality_url = "http://www.sbrf.ru/adygea/ru/about/branch/list_branch/index.php?"+urllib.urlencode(request_data)
        html = scraperwiki.scrape(locality_url)
        html = html.decode('windows-1251')
        #print html
    
        root1 = lxml.html.fromstring(html)
    
    
        for loc in root1.xpath('//select/option'):
            locality_name = loc.text_content() 
            locality_id = loc.attrib['value']
    
            if locality_id == '' or locality_id == 0 or locality_id == '0' : continue

            data={'id': id,
                    'region_id':region_id,
                    'region_name':region_name, 
                    'locality_id': locality_id, 
                    'locality_name':locality_name}

            scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="regions")
            id+=1




class Branch:

    def __init__(self, new_id=1):
        self.row_id=new_id
        #scraperwiki.sqlite.execute('delete from branch_data')
        #scraperwiki.sqlite.execute('delete from branch_data_1')

    def processBranches(self, rid, region, location=''):
        pages=self.processBranch(rid, region, location)
        print pages
        if pages>1:
            for i in range(2,pages+1):
                print "Get page " + str(i)
                self.processBranch(rid, region, location,i)


    def doScrape(self, url, params):
        try:
            html = scraperwiki.scrape(url, params)
        except BadStatusLine:
            print "Wait 10 seconds"
            time.sleep(10)
            html = self.doScrape(url, params)

        return html
        

    def processBranch(self, rid, region, location, page='undefined'):

        request_data = {'rid115': region.encode('utf-8'),
            'cid115': location.encode('utf-8') if location != '' else '',
            'clt115':0,
            'street115':'',
            'name115':'',
            'action115':'Искать',
            'charset':'utf8',
            'page': page }

        #html = scraperwiki.scrape("http://www.sbrf.ru/adygea/ru/about/branch/list_branch/index.php", request_data)
        html = self.doScrape("http://www.sberbank.ru/ru/about/branch/list_branch/index.php", request_data)
                                   
        html = html.decode('windows-1251')
        root2 = lxml.html.fromstring(html)
        #print html
        #Extract number of pages
        pages = root2.xpath("//table/tr/td/span/a")
        #print pages 
        max_page=1
        for p in pages:
            if p.text_content() != '...' and int(p.text_content()) > max_page: max_page=int(p.text_content())
    
        #Process list of branches
        for b in root2.xpath("//div[@class='cbord2']"):
            bdata_brief = b.xpath('div[1]')[0].text_content()
            bdata_detail = b.xpath('div[2]')[0].text_content()
    
            #Find coordinates
            coords = {'lat':'', 'lon':''}
            map_link = b.xpath("a[@target='ya_map_iframe']")
            if map_link != [] and map_link[0].attrib['onclick'] != '':
                latlon=re.findall(r"viewPointOnMap\('([\d\.]+?)',.*?'([\d\.]+?)',", map_link[0].attrib['onclick'], re.I|re.U)[0]
                coords['lat']=latlon[1]
                coords['lon']=latlon[0]
                
    
            #Try to split the branch name and address
            bdata=re.findall(r'^(.+?)\r\n(.+?)\r\n', bdata_brief, re.I |re.S)
            branch_address=''
            branch_name=''
    
            if len(bdata) > 0:
                if len(bdata[0]) > 0:
                    branch_name = bdata[0][0]
    
                if len(bdata[0])==2:
                    branch_address=bdata[0][1]
    
    
            data={'id': self.row_id,
                'rid'  : rid,
                'region'     : region,
                'locality'   : location,
                'brief_info' : bdata_brief,
                'detail_info': bdata_detail,
                'short_name' : branch_name,
                'address'    : branch_address,
                'lat': coords['lat'],
                'lon': coords['lon']}
            scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='branch_data_27_dec')
            self.row_id+=1
    
        return max_page



#html = scraperwiki.scrape("http://www.sbrf.ru/adygea/ru/about/branch/list_branch/")
#root = lxml.html.document_fromstring(html)
#scraperwiki.sqlite.execute('delete from data')

#data = scraperwiki.sqlite.select("distinct region_id from regions as t1")


html1=scraperwiki.scrape("http://www.sbrf.ru/moscow/ru/about/branch/list_branch/")
root=lxml.html.document_fromstring(html1)



b=Branch(1)
i=1
#for r in data:
for r in root.xpath("//select[@id='rid']/option/@value"):

    if r==0 or r=='0': continue
    #if int(r['id']) <= 8737: continue
    #print scraperwiki.sqlite.select("id from regions where region_id='" + r['region_id'] + "' limit 1")
    #b.processBranches(1, r['region_id'])
    b.processBranches(1, r)
    #exit()
    #time.sleep(1)



