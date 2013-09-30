import scraperwiki
import mechanize 
import re
import lxml.html
import sys
import requests
from bs4 import BeautifulSoup

def select(var):
    br.select_form("Form1")
    br.set_all_readonly(False)
    d=dict()
    for control in br.form.controls:
        d[control.name]=br[control.name]
    br["__EVENTTARGET"]=d['__EVENTTARGET']
    br["__EVENTARGUMENT"]=d['__EVENTARGUMENT']
    br["__LASTFOCUS"]=d['__LASTFOCUS']
    br["__VIEWSTATE"]=d['__VIEWSTATE']
    br["__EVENTVALIDATION"]=d['__EVENTVALIDATION']
    
def getFinal(StateCode):
    response = br.open(url)
    VAR1 = response.read()
    ##############    Select State Radio Button
    select(VAR1)
    br['rdbIndiaState']=['rdbState']
    response = br.submit()
    var=response.read()
    #############     Select State Dropdown
    select(var)
    br['rdbIndiaState']=['rdbState']
    br["drpState"]=['19']
    response = br.submit()
    var=response.read()
    ############      Select District Radio Button
    select(var)
    br['rdbIndiaState']=['rdbState']
    br["drpState"]=StateCode
    br['rdbIndiaState']=['rdbDistrict']
    response = br.submit()
    var=response.read()
    return var
 
def createStateList():
    for i in range(1,36):
        l=[]
        if i <10:
            st='0'+str(i)
            l.append(st)
        else:
            st=str(i)
            l.append(st)
        state_list.append(l)

def scrape(var,sl_no):
    root=lxml.html.fromstring(var)
    flag=True
    row=[]
    count=0
    for el in root.cssselect("table#DG_District tr"):
        #print 'here'
        for el2 in el.cssselect("tr.GridAlternativeRows td"):
            #print 'here'
            text=el2.text_content().replace('\r\n','')
            text=text.replace('\t','')
            text=text.replace(',','')
            if count<6:
                count+=1
                row.append(text)
                #data_pts.append(text)
            if count==6:
                sl_no+=1
                count=0
                scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"District":row[1],"TRU":row[2],"Persons":row[3],"Males":row[4],"Females":row[5]})
                row=[]
        count=0
        for el2 in el.cssselect("tr.GridRows td"):
            text=el2.text_content().replace('\r\n','')
            text=text.replace('\t','')
            text=text.replace(',','')
            if count<6:
                count+=1
                row.append(text)
                #data_pts.append(text)
            if count==6:
                sl_no+=1
                count=0
                scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"District":row[1],"TRU":row[2],"Persons":row[3],"Males":row[4],"Females":row[5]})
                row=[]
        #print dat
    return sl_no

url="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Economic_Data/Total_Worker.aspx"
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
state_list=[]
createStateList()
dat=dict()
data_pts=[]
flag=True
sl_no=0
for i in state_list:
    var=getFinal(i)
    #print var
    print i
    sl_no=scrape(var,sl_no)
    #print varimport scraperwiki
import mechanize 
import re
import lxml.html
import sys
import requests
from bs4 import BeautifulSoup

def select(var):
    br.select_form("Form1")
    br.set_all_readonly(False)
    d=dict()
    for control in br.form.controls:
        d[control.name]=br[control.name]
    br["__EVENTTARGET"]=d['__EVENTTARGET']
    br["__EVENTARGUMENT"]=d['__EVENTARGUMENT']
    br["__LASTFOCUS"]=d['__LASTFOCUS']
    br["__VIEWSTATE"]=d['__VIEWSTATE']
    br["__EVENTVALIDATION"]=d['__EVENTVALIDATION']
    
def getFinal(StateCode):
    response = br.open(url)
    VAR1 = response.read()
    ##############    Select State Radio Button
    select(VAR1)
    br['rdbIndiaState']=['rdbState']
    response = br.submit()
    var=response.read()
    #############     Select State Dropdown
    select(var)
    br['rdbIndiaState']=['rdbState']
    br["drpState"]=['19']
    response = br.submit()
    var=response.read()
    ############      Select District Radio Button
    select(var)
    br['rdbIndiaState']=['rdbState']
    br["drpState"]=StateCode
    br['rdbIndiaState']=['rdbDistrict']
    response = br.submit()
    var=response.read()
    return var
 
def createStateList():
    for i in range(1,36):
        l=[]
        if i <10:
            st='0'+str(i)
            l.append(st)
        else:
            st=str(i)
            l.append(st)
        state_list.append(l)

def scrape(var,sl_no):
    root=lxml.html.fromstring(var)
    flag=True
    row=[]
    count=0
    for el in root.cssselect("table#DG_District tr"):
        #print 'here'
        for el2 in el.cssselect("tr.GridAlternativeRows td"):
            #print 'here'
            text=el2.text_content().replace('\r\n','')
            text=text.replace('\t','')
            text=text.replace(',','')
            if count<6:
                count+=1
                row.append(text)
                #data_pts.append(text)
            if count==6:
                sl_no+=1
                count=0
                scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"District":row[1],"TRU":row[2],"Persons":row[3],"Males":row[4],"Females":row[5]})
                row=[]
        count=0
        for el2 in el.cssselect("tr.GridRows td"):
            text=el2.text_content().replace('\r\n','')
            text=text.replace('\t','')
            text=text.replace(',','')
            if count<6:
                count+=1
                row.append(text)
                #data_pts.append(text)
            if count==6:
                sl_no+=1
                count=0
                scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"District":row[1],"TRU":row[2],"Persons":row[3],"Males":row[4],"Females":row[5]})
                row=[]
        #print dat
    return sl_no

url="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Economic_Data/Total_Worker.aspx"
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
state_list=[]
createStateList()
dat=dict()
data_pts=[]
flag=True
sl_no=0
for i in state_list:
    var=getFinal(i)
    #print var
    print i
    sl_no=scrape(var,sl_no)
    #print var