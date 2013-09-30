import scraperwiki
import mechanize
import cookielib
import urllib2
import csv
import re
from BeautifulSoup import BeautifulSoup
import time
from datetime import date, timedelta
import math
import random
import sys
import string
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta



#####################################################
## Mechanize Presets ##
#####################################################

br = mechanize.Browser()

###Cookie Jar###
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

###Browser options###
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

##Follows refresh 0 but not hangs on refresh > 0##
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

###Mechanize Debugging###
#~ br.set_debug_http(True)
#~ br.set_debug_redirects(True)
#~ br.set_debug_responses(True)

###User-Agent###
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

###################################################


base_url = "http://www.ethics.state.tx.us/php/cesearchAdvanced.html"

####Query Dates####

#UNCOMMENT BELOW FOR MONTHLY RUNS
#begin_date=(date.today() + relativedelta(months=-1)+ relativedelta(days=+1))
#end_date=date.today()

#UNCOMMENT BELOW FOR SPECIFIC DATE RUNS
#DATES ARE INCLUSIVE
begin_date = date(2013,04,30)
end_date = date(2013,05,30)

#date range
query_dates = []
while begin_date < end_date:
    query_dates.append(begin_date)
    begin_date += timedelta(days=1)
print query_dates




#This shouldn't change
search_trans_list=["rcpt_src","expn_src","pldg_src","loan_src","guar_src","CRED_SRC"]


#UNCOMMENT IF FIRST RUN TO CREATE TABLES
for trans in search_trans_list:
    create_table_string="create table "+trans+" ('Report Num' string)"
    scraperwiki.sqlite.execute(create_table_string)
scraperwiki.sqlite.commit()  


for q_date in query_dates:

    print q_date.strftime('%m/%d/%Y')

    for search_trans in search_trans_list:
        print "Query Type: " + search_trans
    
        #for search_alpha in string.uppercase: #Don't need this loop
            #print "Query Alpha: " + search_alpha
    
        br.open(base_url)
        br.form = list(br.forms())[0]
        br.form.set_all_readonly(False)
                
        #needed to set a bunch of form field values to list objects. For some reason...
        br["transaction"]=[search_trans]
        br["searchtype"]=["1"]
        br["datetype"]=["2"]
        br["filnamsearchA"]=["2"]
        #br["inameA"]=search_alpha #Commenting out for all alpha..
        br["begin_dateA"]=q_date.strftime('%m/%d/%Y')
        br["end_dateA"]=q_date.strftime('%m/%d/%Y')
        br["repyearA"]=["0"]
        br["filertypeA"]=["ALL"]
        br["namesearch"]=["3"]
        br["repyearB"]=["0"]
        br["filertypeC"]=["ALL"]
        br["filnamsearchB"]=["2"]
        br["filertypeB"]=["ALL"]
        br["sortorder"]=["name"]
        br["ad"]=["ascend"]
        br["format"]="Retrieve HTML"
        br["begin_date"]=q_date.strftime('%m/%d/%Y')
        br["end_date"]=q_date.strftime('%m/%d/%Y')
        br["repyear"]="0"
        br["filnamsearch"]="undefined"
        #br["iname"]=search_alpha
        br["filertype"]="ALL"
        
        br.form.set_all_readonly(True)
        
        
        response=br.submit()
        response_read=response.read()
        soup=BeautifulSoup(response_read)
        
        tables = soup.findAll('table', {'cellpadding':'4'})
        
        table_i=0  
                   
        for table in tables:
            
    
            
            header_list=[]
            ths=table.findChildren('th')
            for th in ths:
                header_list.append(th.text.encode('utf-8').replace('&nbsp;',' ').replace('#','Num').replace("'","").strip())
            for punc in string.punctuation:
                header_list=[hl.replace(punc,'') for hl in header_list]
    
                
            trs=table.findAll('tr')
            for tr in trs:
            
                tds=tr.findAll('td')
                data={}
                i=0
                for td in tds:
                    data[header_list[i]]=td.text.encode('utf-8').replace('&nbsp;',' ').replace('---','')
                    i+=1
                if tr['bgcolor'].upper() == "#D7F4FF":
                    data["Corrected_Report"]="Y"
                
        
                scraperwiki.sqlite.save(unique_keys=[], data=data, table_name=search_trans, verbose=2)import scraperwiki
import mechanize
import cookielib
import urllib2
import csv
import re
from BeautifulSoup import BeautifulSoup
import time
from datetime import date, timedelta
import math
import random
import sys
import string
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta



#####################################################
## Mechanize Presets ##
#####################################################

br = mechanize.Browser()

###Cookie Jar###
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

###Browser options###
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

##Follows refresh 0 but not hangs on refresh > 0##
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

###Mechanize Debugging###
#~ br.set_debug_http(True)
#~ br.set_debug_redirects(True)
#~ br.set_debug_responses(True)

###User-Agent###
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

###################################################


base_url = "http://www.ethics.state.tx.us/php/cesearchAdvanced.html"

####Query Dates####

#UNCOMMENT BELOW FOR MONTHLY RUNS
#begin_date=(date.today() + relativedelta(months=-1)+ relativedelta(days=+1))
#end_date=date.today()

#UNCOMMENT BELOW FOR SPECIFIC DATE RUNS
#DATES ARE INCLUSIVE
begin_date = date(2013,04,30)
end_date = date(2013,05,30)

#date range
query_dates = []
while begin_date < end_date:
    query_dates.append(begin_date)
    begin_date += timedelta(days=1)
print query_dates




#This shouldn't change
search_trans_list=["rcpt_src","expn_src","pldg_src","loan_src","guar_src","CRED_SRC"]


#UNCOMMENT IF FIRST RUN TO CREATE TABLES
for trans in search_trans_list:
    create_table_string="create table "+trans+" ('Report Num' string)"
    scraperwiki.sqlite.execute(create_table_string)
scraperwiki.sqlite.commit()  


for q_date in query_dates:

    print q_date.strftime('%m/%d/%Y')

    for search_trans in search_trans_list:
        print "Query Type: " + search_trans
    
        #for search_alpha in string.uppercase: #Don't need this loop
            #print "Query Alpha: " + search_alpha
    
        br.open(base_url)
        br.form = list(br.forms())[0]
        br.form.set_all_readonly(False)
                
        #needed to set a bunch of form field values to list objects. For some reason...
        br["transaction"]=[search_trans]
        br["searchtype"]=["1"]
        br["datetype"]=["2"]
        br["filnamsearchA"]=["2"]
        #br["inameA"]=search_alpha #Commenting out for all alpha..
        br["begin_dateA"]=q_date.strftime('%m/%d/%Y')
        br["end_dateA"]=q_date.strftime('%m/%d/%Y')
        br["repyearA"]=["0"]
        br["filertypeA"]=["ALL"]
        br["namesearch"]=["3"]
        br["repyearB"]=["0"]
        br["filertypeC"]=["ALL"]
        br["filnamsearchB"]=["2"]
        br["filertypeB"]=["ALL"]
        br["sortorder"]=["name"]
        br["ad"]=["ascend"]
        br["format"]="Retrieve HTML"
        br["begin_date"]=q_date.strftime('%m/%d/%Y')
        br["end_date"]=q_date.strftime('%m/%d/%Y')
        br["repyear"]="0"
        br["filnamsearch"]="undefined"
        #br["iname"]=search_alpha
        br["filertype"]="ALL"
        
        br.form.set_all_readonly(True)
        
        
        response=br.submit()
        response_read=response.read()
        soup=BeautifulSoup(response_read)
        
        tables = soup.findAll('table', {'cellpadding':'4'})
        
        table_i=0  
                   
        for table in tables:
            
    
            
            header_list=[]
            ths=table.findChildren('th')
            for th in ths:
                header_list.append(th.text.encode('utf-8').replace('&nbsp;',' ').replace('#','Num').replace("'","").strip())
            for punc in string.punctuation:
                header_list=[hl.replace(punc,'') for hl in header_list]
    
                
            trs=table.findAll('tr')
            for tr in trs:
            
                tds=tr.findAll('td')
                data={}
                i=0
                for td in tds:
                    data[header_list[i]]=td.text.encode('utf-8').replace('&nbsp;',' ').replace('---','')
                    i+=1
                if tr['bgcolor'].upper() == "#D7F4FF":
                    data["Corrected_Report"]="Y"
                
        
                scraperwiki.sqlite.save(unique_keys=[], data=data, table_name=search_trans, verbose=2)