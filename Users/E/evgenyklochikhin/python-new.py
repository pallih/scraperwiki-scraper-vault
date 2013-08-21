import scraperwiki
import sys, httplib2, urllib, re, random, mechanize
from lxml import etree
import lxml.html
from StringIO import StringIO
from BeautifulSoup import BeautifulSoup

url = "http://www.manchester.ac.uk/research/directory/staffprofiles/"
url2 = "http://www.manchester.ac.uk/research/directory/staffprofiles/?index=Z"
br = mechanize.Browser()
br.set_handle_robots(False)  # bypass robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Firefox')]  # Some websites demand a user-agent that isn't a robot

#response2 = br.open(url2)     # to scrape only Z-index researcher names since function scrape(response) does not allow to do that...
#links6 = list(br.links(url_regex=".*/research/.*\."))
def scrape(response2):
        for link6 in links6:
            resp3 = br.follow_link(link6)
            resp4 = resp3.get_data()
            doc = lxml.html.document_fromstring(resp4)
            records = doc.cssselect('div.vcard')
            str999 = re.compile('^[\W_]+|[\W_]+$|\n|\t|\r|\f')
            for r in records:
                data = {}
                data['key'] = random.random()
                for ite1 in r.cssselect('span.fn'):     #name
                    data['name'] = ite1.text
                for ite2 in r.cssselect('span.title'):    #position
                    data['title'] = ite2.text
                for ite3 in r.xpath('//*[@class="url"]/text()'):              #website which is normally name of department
                    depart = re.search(r'.*choo.*|.*acul.*|.*epart.*|.*cien.*|.*entr.*|.*enter.*', ite3)   
                    if depart is not None:      #check whether it is department name of personal website
                        SEP = ', '
                        data['department'] = SEP.join([ite3 for ite3 in r.xpath('//*[@class="url"]/text()')])                        
                for num in range(4,10):
                    for ite4 in r.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[1]/h3' % (num)):     #anything within the section with substantive info, usually biography, teaching, qualifications, etc.
                        ite5 = ite4.text_content().strip()
                        str_go = re.compile(',.*|;.*|:.*|"|&.?quot;', re.DOTALL)
                        ite5 = str_go.sub('', ite5)
                        ite5 = ite5.encode('ascii', 'ignore') # to ensure there are no frictions in parsing name of column
                        str_h1 = re.search(r'.*iograph.*', ite5)    #check for usual suspects: Biography, Teaching, Research
                        str_h2 = re.search(r'.*esearc.*', ite5)
                        str_h3 = re.search(r'.*eachin.*', ite5)
                        if str_h1:
                            for item_h1 in r.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[2]' % (num)):
                                item_h12 = item_h1.text_content().strip()
                                item_h12 = str999.sub('', item_h12)
                                data['biography'] = item_h12
                        if str_h2:
                            for item_h2 in r.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[2]' % (num)):
                                item_h22 = item_h2.text_content().strip()
                                item_h22 = str999.sub('', item_h22)
                                data['research_brief'] = item_h22
                        if str_h3:
                            for item_h3 in r.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[2]' % (num)):
                                item_h32 = item_h3.text_content().strip()
                                item_h32 = str999.sub('', item_h32)
                                data['teaching_brief'] = item_h32
                        else:
                             for item_h4 in r.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[2]' % (num)):
                                item_h42 = item_h4.text_content().strip()
                                item_h42 = str999.sub('', item_h42)
                                data[ite5] = item_h42     # BUG: have to put item5 in brackets to start populating sqlite and once there is at least one line stop to delete brackets and use as variable, otherwise does not run
                for link7 in list(br.links(url_regex=link6.url)):
                    str_link3 = re.search('.*ersona.*', link7.url)
                    if str_link3 is None:
                        resp3 = br.follow_link(link7)
                        resp4 = resp3.get_data()
                        doc2 = lxml.html.document_fromstring(resp4)
                        records2 = doc2.cssselect('div.vcard')
                        for r2 in records2:
                            for num2 in range(3,10):
                                for rec1 in r2.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[1]/h3' % (num2)):
                                    rec2 = rec1.text_content().strip()
                                    str_goe = re.compile(',|:|;|"|&.?quot;', re.DOTALL)
                                    rec2 = str_goe.sub('', rec2)
                                    rec2 = rec2.encode('ascii', 'ignore')
                                    for rec_h1 in r2.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[2]' % (num2)):    
                                        rec_h12 = rec_h1.text_content().strip()
                                        rec_h12 = str999.sub('', rec_h12)
                                        data[rec2] = rec_h12     # same problem as with item5 above
                        br.back()
                
                
                scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database
                #print r.cssselect('span.title')
            br.back()

#scrape(response2)



response = br.open(url)
links = list(br.links(url_regex=".*index=.*[K-Z]"))

def scrape(response):    #to scrape all the rest records excluding Z-names
    for link in links:
        links2 = list(br.links(url_regex=".*/research/.*\."))
        br.follow_link(link)
        for link2 in links2:
            resp = br.follow_link(link2)
            resp2 = resp.get_data()
            doc = lxml.html.document_fromstring(resp2)
            records = doc.cssselect('div.vcard')
            str555 = re.compile('^[\W_]+|[\W_]+$|\n|\t|\r|\f')
            for r in records:
                data = {}
                data['key'] = random.random()
                for item1 in r.cssselect('span.fn'):     #name
                    data['name'] = item1.text
                for item2 in r.cssselect('span.title'):    #position
                    data['title'] = item2.text
                for item3 in r.xpath('//*[@class="url"]/text()'):              #website which is normally name of department
                    depart = re.search(r'.*choo.*|.*acul.*|.*epart.*|.*cien.*|.*entr.*|.*enter.*', item3)   
                    if depart is not None:      #check whether it is department name of personal website
                        SEP = ', '
                        data['department'] = SEP.join([item3 for item3 in r.xpath('//*[@class="url"]/text()')])                        
                for num in range(4,10):
                    for item4 in r.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[1]/h3' % (num)):     #anything within the section with substantive info, usually biography, teaching, qualifications, etc.
                        item5 = item4.text_content().strip()
                        str_go = re.compile(',|:.*|;.*|\+|\-|"|\.|\(|\)|\*|\?|\!|\'', re.DOTALL)
                        item5 = str_go.sub('', item5)
                        item5 = item5.encode('ascii', 'ignore')
                        str_h1 = re.search(r'.*iograph.*', item5)    #check for usual suspects: Biography, Teaching, Research
                        str_h2 = re.search(r'.*esearc.*', item5)
                        str_h3 = re.search(r'.*eachin.*', item5)
                        if str_h1:
                            for item_h1 in r.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[2]' % (num)):
                                item_h12 = item_h1.text_content().strip()
                                item_h12 = str555.sub('', item_h12)
                                data['biography'] = item_h12
                        if str_h2:
                            for item_h2 in r.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[2]' % (num)):
                                item_h22 = item_h2.text_content().strip()
                                item_h22 = str555.sub('', item_h22)
                                data['research_brief'] = item_h22
                        if str_h3:
                            for item_h3 in r.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[2]' % (num)):
                                item_h32 = item_h3.text_content().strip()
                                item_h32 = str555.sub('', item_h32)
                                data['teaching_brief'] = item_h32
                        else:
                             for item_h4 in r.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[2]' % (num)):
                                item_h42 = item_h4.text_content().strip()
                                item_h42 = str555.sub('', item_h42)
                                data[item5] = item_h42     # BUG: have to put item5 in brackets to start populating sqlite and once there is at least one line stop to delete brackets and use as variable, otherwise does not run
                for link3 in list(br.links(url_regex=link2.url)):
                    str_link3 = re.search('.*ersona.*', link3.url)
                    if str_link3 is None:
                        resp3 = br.follow_link(link3)
                        resp4 = resp3.get_data()
                        doc2 = lxml.html.document_fromstring(resp4)
                        records2 = doc2.cssselect('div.vcard')
                        for r2 in records2:
                            for num2 in range(3,10):
                                for rec1 in r2.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[1]/h3' % (num2)):
                                    rec2 = rec1.text_content().strip()
                                    str_goe = re.compile(',|:.*|;.*|\+|\-|"|\.|\(|\)|\*|\!|\?|\'', re.DOTALL)
                                    rec2 = str_goe.sub('', rec2)
                                    rec2 = rec2.encode('ascii', 'ignore')
                                    for rec_h1 in r2.xpath('//*[@id="researchstaffprofile"]/div[%d]/div[2]' % (num2)):    
                                        rec_h12 = rec_h1.text_content().strip()
                                        rec_h12 = str555.sub('', rec_h12)
                                        data[rec2] = rec_h12     # same problem as with item5 above
                        br.back()
                
                
                scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database
                #print r.cssselect('span.title')
            br.back()
            

scrape(response)
