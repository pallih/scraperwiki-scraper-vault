# Blank Python
# copied from
# https://github.com/tlpinney/foodscrape

import httplib2
from glob import glob
from lxml.html import parse
from BeautifulSoup import BeautifulSoup
import re
import sys
import string

import scraperwiki



h = httplib2.Http()




nums = [ str(i) for i in range(10) ]
strs = [ i for i in string.uppercase ]

all = nums + strs

re_inspect = re.compile(".+inspectionID=([0-9]+)&.+")

re_risk = re.compile('([0-9]) <span class="checkboxRed" style="height:5px;width:5px;background-color:#FF0000;">&nbsp;</span>&nbsp;')

ignore = ['15','2159','7907','9104','3955']

for part in all:
    resp, content = h.request("http://washington.dc.gegov.com/webadmin/dhd_431/web/?a=inspections&alpha=%s" % part)
    soup = BeautifulSoup(content) 
    for link in soup.findAll( 'a', attrs={ 'href' : re.compile('^../lib/mod/inspection/paper/_paper_food_inspection_report.cfm')}):
        line = "http://washington.dc.gegov.com/webadmin/dhd_431" + link['href'][2:]
        line = line.strip()
        m = re_inspect.match(line)
        fname = m.group(1)
        resp, content = h.request(line)
    
        html = content
        iid = line.split('?')[1].split('&')[0].split('=')[-1]      
        if iid in ignore:
            continue
        soup = BeautifulSoup(html)
        tds = soup.findAll("td", attrs={'colspan':'2'})
        name = tds[0].text.split('&nbsp;')[1]
        
        phone_number = ''
        phone_number = tds[2].text.split('&nbsp;')[1].replace('(','').replace(')','').replace('-','').replace(' ','')

        addr = tds[1].text

        street = addr.split("&nbsp;")[1].split("City/State/Zip Code")[0]

        city = addr.split("&nbsp;")[2].split(",")[0].upper()

        state, zipcode = addr.split("&nbsp;")[2].split(",")[1].strip().split(" ")

        date =  soup.findAll("td", attrs={'colspan': '2'})[3].text.split("&nbsp;")
        date = "".join(date[1:4])

        m = re_risk.search(html)
        if m == None:
            continue
        #yelp_resp, yelp_content = h.request("http://washington.dc.gegov.com/webadmin/dhd_431/web/?a=inspections&alpha=%s" % part)
        risk = m.group(1)
        data = {
                'iid':iid,
                'phone_number':phone_number,              
                'risk': risk,
                'date':date,
                'name':name,
                'street':street,
                'city':city,
                'state':state,
                'zipcode':zipcode
                }
        scraperwiki.datastore.save(['iid'], data)
# Blank Python
# copied from
# https://github.com/tlpinney/foodscrape

import httplib2
from glob import glob
from lxml.html import parse
from BeautifulSoup import BeautifulSoup
import re
import sys
import string

import scraperwiki



h = httplib2.Http()




nums = [ str(i) for i in range(10) ]
strs = [ i for i in string.uppercase ]

all = nums + strs

re_inspect = re.compile(".+inspectionID=([0-9]+)&.+")

re_risk = re.compile('([0-9]) <span class="checkboxRed" style="height:5px;width:5px;background-color:#FF0000;">&nbsp;</span>&nbsp;')

ignore = ['15','2159','7907','9104','3955']

for part in all:
    resp, content = h.request("http://washington.dc.gegov.com/webadmin/dhd_431/web/?a=inspections&alpha=%s" % part)
    soup = BeautifulSoup(content) 
    for link in soup.findAll( 'a', attrs={ 'href' : re.compile('^../lib/mod/inspection/paper/_paper_food_inspection_report.cfm')}):
        line = "http://washington.dc.gegov.com/webadmin/dhd_431" + link['href'][2:]
        line = line.strip()
        m = re_inspect.match(line)
        fname = m.group(1)
        resp, content = h.request(line)
    
        html = content
        iid = line.split('?')[1].split('&')[0].split('=')[-1]      
        if iid in ignore:
            continue
        soup = BeautifulSoup(html)
        tds = soup.findAll("td", attrs={'colspan':'2'})
        name = tds[0].text.split('&nbsp;')[1]
        
        phone_number = ''
        phone_number = tds[2].text.split('&nbsp;')[1].replace('(','').replace(')','').replace('-','').replace(' ','')

        addr = tds[1].text

        street = addr.split("&nbsp;")[1].split("City/State/Zip Code")[0]

        city = addr.split("&nbsp;")[2].split(",")[0].upper()

        state, zipcode = addr.split("&nbsp;")[2].split(",")[1].strip().split(" ")

        date =  soup.findAll("td", attrs={'colspan': '2'})[3].text.split("&nbsp;")
        date = "".join(date[1:4])

        m = re_risk.search(html)
        if m == None:
            continue
        #yelp_resp, yelp_content = h.request("http://washington.dc.gegov.com/webadmin/dhd_431/web/?a=inspections&alpha=%s" % part)
        risk = m.group(1)
        data = {
                'iid':iid,
                'phone_number':phone_number,              
                'risk': risk,
                'date':date,
                'name':name,
                'street':street,
                'city':city,
                'state':state,
                'zipcode':zipcode
                }
        scraperwiki.datastore.save(['iid'], data)
