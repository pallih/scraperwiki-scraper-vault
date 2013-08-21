import scraperwiki
import mechanize 
import re
import lxml.html
import sys
import requests
from bs4 import BeautifulSoup

url="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Area_Profile/SubDistrict_Profile.aspx?cki=7H7pnwQvpHZ"
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
state_list=[]
flag=True
sl_no=0
dat=dict()
data_pts=[]
state=''
district=''
error=[]
end=False
for i in range(1,36):
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
tehsil_list=[]
for i in range (1,1000):
    l=[]
    if i <10:
        st='000'+str(i)
        l.append(st)
    elif i<100:
        st='00'+str(i)
        l.append(st)
    elif i<1000:
        st='0'+str(i)
        l.append(st)
    else:
        st=str(i)
        l.append(st)
    #print st
    tehsil_list.append(l)
        
#state_list=state_list[:1]
#district_list=district_list[:1]
#for i in state_list:
   # print i
for i in state_list:
    print i
    
    #state selection done
    for j in district_list:
        #district selection
        for k in tehsil_list:
        
            sl_no+=1
        
            response = br.open(url)
            VAR1 = response.read() #reads the source file for the web page
            #print VAR1
            #br.select_form("Form1")
            br.select_form("aspnetForm")
            br.set_all_readonly(False)
            d=dict()
            for control in br.form.controls:
                d[control.name]=br[control.name]
            br["__EVENTTARGET"]=d['__EVENTTARGET']
            br["__EVENTARGUMENT"]=d['__EVENTARGUMENT']
            br["__LASTFOCUS"]=d['__LASTFOCUS']
            br["__VIEWSTATE"]=d['__VIEWSTATE']
            br["__EVENTVALIDATION"]=d['__EVENTVALIDATION']
            
            br["ctl00$Body_Content$drpState"]=i
        
            response = br.submit()
            #response = br.open(url)
            #####################
            #####################     code to get option values ########
            var=response.read()
            #soup=BeautifulSoup(var)
            #for opt in soup.findAll('select',{"name" : "drpDistrict"}):
                #for option in opt.findAll('option'):
                    #print option.get('value')
            ############################################################
            #print var
            #print 'HELLO'+response.read()
            #print var
            root=lxml.html.fromstring(var)
            br.select_form("aspnetForm")
            br.set_all_readonly(False)
            for control in br.form.controls:
                d[control.name]=br[control.name]
            dat=dict()
            row=[]
            try:
                print i,j,k
                br["__EVENTTARGET"]=d['__EVENTTARGET']
                br["__EVENTARGUMENT"]=d['__EVENTARGUMENT']
                br["__LASTFOCUS"]=d['__LASTFOCUS']
                br["__VIEWSTATE"]=d['__VIEWSTATE']
                br["__EVENTVALIDATION"]=d['__EVENTVALIDATION']
                br["ctl00$Body_Content$drpState"]=i
                br["ctl00$Body_Content$drpDistrict"]=j
                response = br.submit()
                var=response.read()
                #print var
                root=lxml.html.fromstring(var)
                br.select_form("aspnetForm")
                br.set_all_readonly(False)
                for control in br.form.controls:
                    d[control.name]=br[control.name]
                dat=dict()
                row=[]
                
                try:
                    
                    br["__EVENTTARGET"]=d['__EVENTTARGET']
                    br["__EVENTARGUMENT"]=d['__EVENTARGUMENT']
                    br["__LASTFOCUS"]=d['__LASTFOCUS']
                    br["__VIEWSTATE"]=d['__VIEWSTATE']
                    br["__EVENTVALIDATION"]=d['__EVENTVALIDATION']
                    br["ctl00$Body_Content$drpState"]=i
                    br["ctl00$Body_Content$drpDistrict"]=j
                    br["ctl00$Body_Content$drpTeshil"]=k
                    response = br.submit()
                    var=response.read()
                    print var
                    root=lxml.html.fromstring(var)
                    #print type(data)
                    #print root
                    for el in root.cssselect("div#ctl00_Body_Content_pnlStateProfile table#Table2"):
                        #print 'here table2'
                        for el2 in root.cssselect("tr td.GridHeader1"):
                            #print 'here'
                            for el3 in el2.cssselect("span#ctl00_Body_Content_lblsubDistrictName"):
                                sub_dist=el3.text_content()
                                #print 'here'
                                print sub_dist
                            for el3 in el2.cssselect("span#ctl00_Body_Content_lblDistrictName"):
                                district=el3.text_content()
                                print district
                            for el3 in el2.cssselect("span#ctl00_Body_Content_lblStateName"):
                                state=el3.text_content()
                                print state
                        for el2 in root.cssselect("tr.GridAlternativeRows1 td"):
                            #print el2.text_content()
                            text=el2.text_content().replace('\r\n','')
                            text=text.replace('\t','')
                            if flag:
                                flag=False
                                row.append(text)
                                data_pts.append(text)
                            else:
                                row.append(text)
                                #print row
                                dat[row[0]]=row[1]
                                flag=True
                                row=[]
                        for el2 in root.cssselect("tr.GridRows1 td"):
                            #print el2.text_content()
                            text=el2.text_content().replace('\r\n','')
                            text=text.replace('\t','')
                            if flag:
                                flag=False
                                row.append(text)
                                data_pts.append(text)
                            else:
                                row.append(text)
                                dat[row[0]]=row[1].replace(',','')
                                flag=True
                                row=[]
                                #print type(data)
                                #print type(data)
                        print dat
                        scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Population Total":dat['Population-Total'],"Proportion of Urban Population Percentage":dat['Proportion of Urban Population (%)'],"Population Urban":dat['Population-Urban'],"Sex Ratio 0 to 6 Year":dat['Sex Ratio(0-6 Year)'],"SC Population":dat['SC Population'],"Sex Ratio of ST":dat['Sex Ratio (ST)'],"Literates":dat['Literates'],"Proportion of ST Percentage":dat['Proportion of ST (%)'],"Total Workers":dat['Total Workers'],"Work Participation Rate Percentage":dat['Work Participation Rate (%)'],"Marginal Worker":dat['Marginal Worker'],"Percentage of Marginal Worker":dat['% of Marginal Worker'],"CL Main and Marginal":dat['CL (Main+Marginal)'],"Proportion of CL Percentage":dat['Proportion of CL (%)'],"HHI Main plus Marginal":dat['HHI (Main+Marginal)'],"Proportion of HHI Percentage":dat['Proportion of HHI (%)'],"Number of Households":dat['Number of Households'],"Average Household Size per Household":dat['Average Household Size(per Household)'],"Population Rural":dat['Population-Rural'],"Sex Ratio":dat['Sex Ratio'],"Population 0 to 6 Years":dat['Population(0-6Years)'],"Sex Ratio SC":dat['Sex Ratio (SC)'],"ST Population":dat['ST Population'],"Proportion of SC Percentage":dat['Proportion of SC (%)'],"Illiterates":dat['Illiterates'],"Literacy Rate Percentage":dat['Literacy Rate (%)'],"Main Worker":dat['Main Worker'],"Percentage of Main Workers":dat['% of Main Workers'],"Non Worker":dat['Non Worker'],"Percentage of non Workers":dat['% of non Workers'],"Al Main plus Marginal":dat['Al (Main+Marginal)'],"Proportion of AL percentage":dat['Proportion of AL (%)'],"OW Main Marginal":dat['OW (Main+Marginal)'],"Proportion of OW Percentage":dat['Proportion of OW (%)'],"State Name":state,"District Name":district,"Sub District Name":sub_dist})
                        state='#'
                        district='#'
                        sub_district='#'
                
                except:
                     print 'hehe'
                     break         
            except:
                #break
                print 'haha'
                if state=='#' and district=='#':
                    break
                else:
                    error.append(state+';'+district)
print error