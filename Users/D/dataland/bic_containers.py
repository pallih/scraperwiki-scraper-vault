import scraperwiki
import lxml.html
import urllib2
import datetime
import json
import string
import random
from BeautifulSoup import BeautifulSoup
import random

# Build array of lowercase letters (a:z)
let_list = map(chr, range(97, 123))
page_list = [0,400]
good_list = []

def urlfortoken(token,pagenum):
    return 'http://www.bic-code.org/glossary-bic-codes-{token}-{pagenum}-400-asc.html'.format(token=token,pagenum=pagenum)

try:
    curr_index = scraperwiki.sqlite.get_var("index_next_run",0)
    if curr_index == 26:
        curr_index = 0
except NameError:
    curr_index = 0

for n in page_list:
    url = urlfortoken(let_list[curr_index],n)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for count, tr in enumerate(root.cssselect('tr')):
        row = [(td.text_content()) for td in tr.cssselect('td')]
        for ahref in tr.cssselect('a'):
            detailink = ahref.attrib['href']
            text = urllib2.urlopen(detailink).read()
            soup = BeautifulSoup(text)
            data2 = soup.findAll('div',attrs={'class':'nocode'})
            if len(data2)==0:
                
                owner= ""
                code= ""
                addr1 = ""
                addr2 = ""
                zipcode= ""
                city = ""
                country = ""
                telephone = ""
                fax = ""
                email = ""
                web = ""
                owner = soup.find('h4').text
                data2 = soup.findAll('li',attrs={'class':'impair'})
                for r in data2:
                    o = r.text
                    if o.upper()[:5]=="CODES":
                        code = o[5:]
                    elif o.upper()[:8]=="ZIP CODE":
                        zipcode = o[8:]
                    elif o.upper()[:7]=="COUNTRY":
                        country = o[7:]
                    elif o.upper()[:3]=="FAX":
                        fax = o[3:]
                    elif o.upper()[:3]=="WEB":
                        web = o[3:]
                data3 = soup.findAll('li',attrs={'class':'pair'})
                for s in data3:
                    p = s.text
                    x = str(s)
                    if p.upper()[:7]=="ADDRESS":
                        # Two line address
                        if x.find("<br />")!= -1:
                            addr1st = x.index("droite")+8
                            addr1fn = x.index("<br />")
                            addr1 = x[addr1st:addr1fn]
                            addr2st = x.index("br />")+5
                            addr2fn = x.index("</span></li>")
                            addr2 = x[addr2st:addr2fn]
                        else:
                            addr1st = x.index("droite")+8
                            addr1fn = x.index("</span></li>")
                            addr1 = addr1 = x[addr1st:addr1fn]
                            addr2 = ""
                    elif p.upper()[:4]=="CITY":
                        city = p[4:]
                    elif p.upper()[:9]=="TELEPHONE":
                        telephone = p[9:]
                    elif p.upper()[:6]=="E-MAIL":
                        email = p[6:]
                now = datetime.datetime.now()
                data = {"tmsp_scraped":str(now), "owner":owner, "code":code, "addr1":addr1, "addr2":addr2, "zipcode":zipcode, "city":city, "country":country, "telephone":telephone, "fax":fax, "email":email, "web":web, "index_page":url, "detail_page":detailink}
                scraperwiki.sqlite.save(unique_keys=["index_page","detail_page"], data=data, table_name="s_bic")

if curr_index < 26:
    next_index = curr_index + 1
else:
    next_index = 0
scraperwiki.sqlite.save_var("index_next_run",next_index)

if next_index != 0:
    print "Index Value for Next Run: "+str(let_list[next_index].upper())
else:
    print "Index Value for Next Run: 0"

import scraperwiki
import lxml.html
import urllib2
import datetime
import json
import string
import random
from BeautifulSoup import BeautifulSoup
import random

# Build array of lowercase letters (a:z)
let_list = map(chr, range(97, 123))
page_list = [0,400]
good_list = []

def urlfortoken(token,pagenum):
    return 'http://www.bic-code.org/glossary-bic-codes-{token}-{pagenum}-400-asc.html'.format(token=token,pagenum=pagenum)

try:
    curr_index = scraperwiki.sqlite.get_var("index_next_run",0)
    if curr_index == 26:
        curr_index = 0
except NameError:
    curr_index = 0

for n in page_list:
    url = urlfortoken(let_list[curr_index],n)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for count, tr in enumerate(root.cssselect('tr')):
        row = [(td.text_content()) for td in tr.cssselect('td')]
        for ahref in tr.cssselect('a'):
            detailink = ahref.attrib['href']
            text = urllib2.urlopen(detailink).read()
            soup = BeautifulSoup(text)
            data2 = soup.findAll('div',attrs={'class':'nocode'})
            if len(data2)==0:
                
                owner= ""
                code= ""
                addr1 = ""
                addr2 = ""
                zipcode= ""
                city = ""
                country = ""
                telephone = ""
                fax = ""
                email = ""
                web = ""
                owner = soup.find('h4').text
                data2 = soup.findAll('li',attrs={'class':'impair'})
                for r in data2:
                    o = r.text
                    if o.upper()[:5]=="CODES":
                        code = o[5:]
                    elif o.upper()[:8]=="ZIP CODE":
                        zipcode = o[8:]
                    elif o.upper()[:7]=="COUNTRY":
                        country = o[7:]
                    elif o.upper()[:3]=="FAX":
                        fax = o[3:]
                    elif o.upper()[:3]=="WEB":
                        web = o[3:]
                data3 = soup.findAll('li',attrs={'class':'pair'})
                for s in data3:
                    p = s.text
                    x = str(s)
                    if p.upper()[:7]=="ADDRESS":
                        # Two line address
                        if x.find("<br />")!= -1:
                            addr1st = x.index("droite")+8
                            addr1fn = x.index("<br />")
                            addr1 = x[addr1st:addr1fn]
                            addr2st = x.index("br />")+5
                            addr2fn = x.index("</span></li>")
                            addr2 = x[addr2st:addr2fn]
                        else:
                            addr1st = x.index("droite")+8
                            addr1fn = x.index("</span></li>")
                            addr1 = addr1 = x[addr1st:addr1fn]
                            addr2 = ""
                    elif p.upper()[:4]=="CITY":
                        city = p[4:]
                    elif p.upper()[:9]=="TELEPHONE":
                        telephone = p[9:]
                    elif p.upper()[:6]=="E-MAIL":
                        email = p[6:]
                now = datetime.datetime.now()
                data = {"tmsp_scraped":str(now), "owner":owner, "code":code, "addr1":addr1, "addr2":addr2, "zipcode":zipcode, "city":city, "country":country, "telephone":telephone, "fax":fax, "email":email, "web":web, "index_page":url, "detail_page":detailink}
                scraperwiki.sqlite.save(unique_keys=["index_page","detail_page"], data=data, table_name="s_bic")

if curr_index < 26:
    next_index = curr_index + 1
else:
    next_index = 0
scraperwiki.sqlite.save_var("index_next_run",next_index)

if next_index != 0:
    print "Index Value for Next Run: "+str(let_list[next_index].upper())
else:
    print "Index Value for Next Run: 0"

