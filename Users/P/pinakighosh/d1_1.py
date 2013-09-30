import scraperwiki
import mechanize 
import re
import lxml.html
import sys
import requests
from bs4 import BeautifulSoup

url="http://www.censusindia.gov.in/Census_Data_2001/Village_Directory/View_data/Dist_Profile.aspx"
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
state_list=[]
flag=False
for i in range(1,35):
    l=[]
    if i <10:
        st='0'+str(i)
        l.append(st)
    else:
        st=str(i)
        l.append(st)
    #print st
    state_list.append(l)
district_list=[]
for i in range(1,72):
    l=[]
    if i <10:
        st='0'+str(i)
        l.append(st)
    else:
        st=str(i)
        l.append(st)
    #print st
    district_list.append(l)
#for i in state_list:
    #print i
state_list=state_list[:1]
district_list=district_list[:1]
for i in state_list:
    
    #state selection done
    for j in district_list:
        response = br.open(url)
        VAR1 = response.read() #reads the source file for the web page
        br.select_form("Form1")
        br.set_all_readonly(False)
        d=dict()
        for control in br.form.controls:
            #print control
            #print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])
            #if control.name == 'drpState':
                #print br[control.name]
                #print control.value
            d[control.name]=br[control.name]
        br["__EVENTTARGET"]=d['__EVENTTARGET']
        br["__EVENTARGUMENT"]=d['__EVENTARGUMENT']
        br["__LASTFOCUS"]=d['__LASTFOCUS']
        br["__VIEWSTATE"]=d['__VIEWSTATE']
        br["__EVENTVALIDATION"]=d['__EVENTVALIDATION']
        br["drpState"]=i
        response = br.submit()
        #response = br.open(url)
        var=response.read()
        print response.read()
        root=lxml.html.fromstring(var)
        br.select_form("Form1")
        br.set_all_readonly(False)
        for control in br.form.controls:
            #print control
            #print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])
            d[control.name]=br[control.name]
        try:
            br["__EVENTTARGET"]=d['__EVENTTARGET']
            br["__EVENTARGUMENT"]=d['__EVENTARGUMENT']
            br["__LASTFOCUS"]=d['__LASTFOCUS']
            br["__VIEWSTATE"]=d['__VIEWSTATE']
            br["__EVENTVALIDATION"]=d['__EVENTVALIDATION']
            br["drpState"]=i
            br["drpDistrict"]=j
            response = br.submit()
            var=response.read()
            print response.read()
            root=lxml.html.fromstring(var)
            #print "here"
            count=0
            f=False
            data=[]
            for el in root.cssselect("tr.TableRows td"):
                text1=el.text_content()
                text=text1.replace('\n','')
                text=text.replace('\r','')
                text=text.replace('\t','')
                text=text.replace(' ','_')
                if f:
                    data.append(text)
                if text=='State:':
                    #print text
                    f=True
                    #count=1
            state=data[0]
            district=data[2]
            data=data[4:-1]
            print state,district
            #print data
            d1=dict()
            d2=dict()
            d3=dict()
            for i in range(len(data)):
                if i%4==0:
                    key=data[i]
                if i%4==1:
                    if data[i]==' ':
                        d1[key]=0
                    else:
                        d1[key]=data[i]
                if i%4==2:
                    if data[i]==' ':
                        d2[key]=0
                    else:
                        d2[key]=data[i]
                if i%4==3:
                    if data[i]==' ':
                        d3[key]=0
                    else:
                        d3[key]=data[i]
            
            
            for i in d1:
                print i,d1[i]
        except:
            print "works"
            flag=True
            break
        if flag:
            break
        print j
    if flag:
        flag=False
        continue
        


import scraperwiki
import mechanize 
import re
import lxml.html
import sys
import requests
from bs4 import BeautifulSoup

url="http://www.censusindia.gov.in/Census_Data_2001/Village_Directory/View_data/Dist_Profile.aspx"
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
state_list=[]
flag=False
for i in range(1,35):
    l=[]
    if i <10:
        st='0'+str(i)
        l.append(st)
    else:
        st=str(i)
        l.append(st)
    #print st
    state_list.append(l)
district_list=[]
for i in range(1,72):
    l=[]
    if i <10:
        st='0'+str(i)
        l.append(st)
    else:
        st=str(i)
        l.append(st)
    #print st
    district_list.append(l)
#for i in state_list:
    #print i
state_list=state_list[:1]
district_list=district_list[:1]
for i in state_list:
    
    #state selection done
    for j in district_list:
        response = br.open(url)
        VAR1 = response.read() #reads the source file for the web page
        br.select_form("Form1")
        br.set_all_readonly(False)
        d=dict()
        for control in br.form.controls:
            #print control
            #print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])
            #if control.name == 'drpState':
                #print br[control.name]
                #print control.value
            d[control.name]=br[control.name]
        br["__EVENTTARGET"]=d['__EVENTTARGET']
        br["__EVENTARGUMENT"]=d['__EVENTARGUMENT']
        br["__LASTFOCUS"]=d['__LASTFOCUS']
        br["__VIEWSTATE"]=d['__VIEWSTATE']
        br["__EVENTVALIDATION"]=d['__EVENTVALIDATION']
        br["drpState"]=i
        response = br.submit()
        #response = br.open(url)
        var=response.read()
        print response.read()
        root=lxml.html.fromstring(var)
        br.select_form("Form1")
        br.set_all_readonly(False)
        for control in br.form.controls:
            #print control
            #print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])
            d[control.name]=br[control.name]
        try:
            br["__EVENTTARGET"]=d['__EVENTTARGET']
            br["__EVENTARGUMENT"]=d['__EVENTARGUMENT']
            br["__LASTFOCUS"]=d['__LASTFOCUS']
            br["__VIEWSTATE"]=d['__VIEWSTATE']
            br["__EVENTVALIDATION"]=d['__EVENTVALIDATION']
            br["drpState"]=i
            br["drpDistrict"]=j
            response = br.submit()
            var=response.read()
            print response.read()
            root=lxml.html.fromstring(var)
            #print "here"
            count=0
            f=False
            data=[]
            for el in root.cssselect("tr.TableRows td"):
                text1=el.text_content()
                text=text1.replace('\n','')
                text=text.replace('\r','')
                text=text.replace('\t','')
                text=text.replace(' ','_')
                if f:
                    data.append(text)
                if text=='State:':
                    #print text
                    f=True
                    #count=1
            state=data[0]
            district=data[2]
            data=data[4:-1]
            print state,district
            #print data
            d1=dict()
            d2=dict()
            d3=dict()
            for i in range(len(data)):
                if i%4==0:
                    key=data[i]
                if i%4==1:
                    if data[i]==' ':
                        d1[key]=0
                    else:
                        d1[key]=data[i]
                if i%4==2:
                    if data[i]==' ':
                        d2[key]=0
                    else:
                        d2[key]=data[i]
                if i%4==3:
                    if data[i]==' ':
                        d3[key]=0
                    else:
                        d3[key]=data[i]
            
            
            for i in d1:
                print i,d1[i]
        except:
            print "works"
            flag=True
            break
        if flag:
            break
        print j
    if flag:
        flag=False
        continue
        


