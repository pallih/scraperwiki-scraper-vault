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
    
def getSemiFinal(StateCode):
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
    br["drpState"]=StateCode
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

def getFinal(StateCode,DistCode):
    f=True
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
    br["drpState"]=StateCode
    response = br.submit()
    var=response.read()
    ############      Select District Radio Button
    select(var)
    br['rdbIndiaState']=['rdbState']
    br["drpState"]=StateCode
    br['rdbIndiaState']=['rdbDistrict']
    response = br.submit()
    var=response.read()
    ###########       Select District
    try:
        select(var)
        br['rdbIndiaState']=['rdbState']
        br["drpState"]=StateCode
        br['rdbIndiaState']=['rdbDistrict']
        br["drpDistrict"]=DistCode
        response = br.submit()
        var=response.read()
    except:
        var=''
        f=False
    return var,f
 
def createList(n):
    ret=[]
    for i in range(1,n+1):
        l=[]
        if i <10:
            st='0'+str(i)
            l.append(st)
        else:
            st=str(i)
            l.append(st)
        ret.append(l)
    return ret

def scrape(var,sl_no,distCode,stateCode):
    root=lxml.html.fromstring(var)
    flag=True
    row=[]
    count=0
    soup=BeautifulSoup(var)
    state=''
    district=''
    for item in soup.find_all('option',{"value" : distCode}):
        district=''.join(str(item.find(text=True)))
    for item in soup.find_all('option',{"value" : stateCode}):
        state=''.join(str(item.find(text=True)))
        break
    for el in root.cssselect("table#DG_District tr"):
        #print 'here'
        for el2 in el.cssselect("tr.GridAlternativeRows td"):
            #print 'here'
            text=el2.text_content().replace('\r\n','')
            text=text.replace('\t','')
            text=text.replace(',','')
            if count<5:
                count+=1
                row.append(text)
                #data_pts.append(text)
            if count==5:
                sl_no+=1
                count=0
                scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Age Group":row[1],"Persons":row[2],"Males":row[3],"Females":row[4],"State":state,"District":district})
                row=[]
        count=0
        for el2 in el.cssselect("tr.GridRows td"):
            text=el2.text_content().replace('\r\n','')
            text=text.replace('\t','')
            text=text.replace(',','')
            if count<5:
                count+=1
                row.append(text)
                #data_pts.append(text)
            if count==5:
                sl_no+=1
                count=0
                scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Age Group":row[1],"Persons":row[2],"Males":row[3],"Females":row[4],"State":state,"District":district})
                row=[]
        #print dat
    print state+'*'*5+district
    return sl_no

url="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Social_and_cultural/Age_Groups.aspx"
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
state_list=[]
state_list=createList(35)
state_list=state_list[8:9]
district_list=[]
district_list=createList(72)
dat=dict()
data_pts=[]
flag=True
sl_no=0
for i in state_list:
    #var=getSemiFinal(i)
    for j in district_list:
        print str(i)+" "+str(j)
        var,f=getFinal(i,j)
        if not f:
            break
        #print var
        #print i
        sl_no=scrape(var,sl_no,j[0],i[0])
        #print var
