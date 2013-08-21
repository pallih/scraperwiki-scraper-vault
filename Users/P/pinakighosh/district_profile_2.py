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
try:
    scraperwiki.sqlite.execute("drop table total")
    scraperwiki.sqlite.execute("create table total ('State' string,'District' string,'Number_of_sub-districts' string,'Number_of_inhabited_village' string,'Number_of_primary_schools' string,'Number_of_middle_schools' string,'Number_of_secondary_schools' string,'Number_of_senior_secondary_schools' string,'Number_of_colleges' string,'Number_of_adult_literacy_class/centres' string,'Number_of_industrial_schools' string,'Number_of_training_schools' string,'Number_of_other_educational_schools' string,'Number_of_allopathic_hospitals' string,'Number_of_ayurvedic_hospitals' string,'Number_of_unani_hospital' string,'Number_of_homeopathic_hospital' string,'Number_of_allopathic_dispensary' string,'Number_of_ayurvedic_dispensary' string,'Number_of_unani_dispensary' string,'Number_of_homeopathic_dispensary' string,'Number_of_maternity_and_child_welfare_centre' string,'Number_of_maternity_home' string,'Number_of_child_welfare_centre' string,'Number_of_health_centre' string,'Number_of_primary_health_centre' string,'Number_of_primary_health_sub-centre' string,'Number_of_family_welfare_centre' string,'Number_of_T.B._clinic' string,'Number_of_nursing_home' string,'Number_of_registered_private_medical_practiotioners' string,'Number_of_subsidised_medical_practitioners' string,'Number_of_community_health_workers' string,'Number_of_other_medical_facilities' string,'Tap_water' string,'Well_water' string,'Number_of_tank_water' string,'Tubewell_water' string,'Handpumb' string,'River_water' string,'Canals' string,'Lakes' string,'Spring' string,'Other_drinking_water_sources' string,'Number_of_post_office' string,'Number_of_telegraph_office' string,'Number_of_post_and_telegraph_office' string,'Number_of_telephone_connections' string,'Bus_services' string,'Railways_services' string,'Navigable_water_way_including_river,_canal_etc.' string,'Number_of_commercial_bank' string,'Number_of_Co-operative_commercial_bank' string,'Number_of_agricultural_credit_societies' string,'Number_of_non_agricultural_credit_societies' string,'Number_of_other_credit_societies' string,'Number_of_cinema/video-hall' string,'Number_of_sports_club' string,'Number_of_stadium/auditorium' string,'Number_of_forest_land' string,'Number_of_government_canal' string,'Number_of_private_canal' string,'Well_(without_electricity)' string,'Well_(with_electricity)' string,'Tube-well_(without_electricity)' string,'Tube-well_(with_electricity)' string,'Tank' string,'River' string,'Lake' string,'Waterfall' string,'Others' string,'Irrigated_Area' string,'Unirrigated_Area' string,'Culturable_waste_(including_gauchar_and_groves)' string,'Area_not_available_for_cultivation' string)")
except:
    scraperwiki.sqlite.execute("create table total('State' string,'District' string,'Number_of_sub-districts' string,'Number_of_inhabited_village' string,'Number_of_primary_schools' string,'Number_of_middle_schools' string,'Number_of_secondary_schools' string,'Number_of_senior_secondary_schools' string,'Number_of_colleges' string,'Number_of_adult_literacy_class/centres' string,'Number_of_industrial_schools' string,'Number_of_training_schools' string,'Number_of_other_educational_schools' string,'Number_of_allopathic_hospitals' string,'Number_of_ayurvedic_hospitals' string,'Number_of_unani_hospital' string,'Number_of_homeopathic_hospital' string,'Number_of_allopathic_dispensary' string,'Number_of_ayurvedic_dispensary' string,'Number_of_unani_dispensary' string,'Number_of_homeopathic_dispensary' string,'Number_of_maternity_and_child_welfare_centre' string,'Number_of_maternity_home' string,'Number_of_child_welfare_centre' string,'Number_of_health_centre' string,'Number_of_primary_health_centre' string,'Number_of_primary_health_sub-centre' string,'Number_of_family_welfare_centre' string,'Number_of_T.B._clinic' string,'Number_of_nursing_home' string,'Number_of_registered_private_medical_practiotioners' string,'Number_of_subsidised_medical_practitioners' string,'Number_of_community_health_workers' string,'Number_of_other_medical_facilities' string,'Tap_water' string,'Well_water' string,'Number_of_tank_water' string,'Tubewell_water' string,'Handpumb' string,'River_water' string,'Canals' string,'Lakes' string,'Spring' string,'Other_drinking_water_sources' string,'Number_of_post_office' string,'Number_of_telegraph_office' string,'Number_of_post_and_telegraph_office' string,'Number_of_telephone_connections' string,'Bus_services' string,'Railways_services' string,'Navigable_water_way_including_river,_canal_etc.' string,'Number_of_commercial_bank' string,'Number_of_Co-operative_commercial_bank' string,'Number_of_agricultural_credit_societies' string,'Number_of_non_agricultural_credit_societies' string,'Number_of_other_credit_societies' string,'Number_of_cinema/video-hall' string,'Number_of_sports_club' string,'Number_of_stadium/auditorium' string,'Number_of_forest_land' string,'Number_of_government_canal' string,'Number_of_private_canal' string,'Well_(without_electricity)' string,'Well_(with_electricity)' string,'Tube-well_(without_electricity)' string,'Tube-well_(with_electricity)' string,'Tank' string,'River' string,'Lake' string,'Waterfall' string,'Others' string,'Irrigated_Area' string,'Unirrigated_Area' string,'Culturable_waste_(including_gauchar_and_groves)' string,'Area_not_available_for_cultivation' string)")
    
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
            
            query='insert into total values(:state,:district'
            for i in d1:
                query+=',:'+i
            
            query=query[:-1]+'), ({"state":'+state+',"district":'+district+','
            for i in d1:
                query+='"'+i+'":"'+d1[i]+'",'
            
            query=query[:-1]
            query+='}'
            
            print query
            scraperwiki.sqlite.execute(query)
            #for i in d1:
                #print i,d1[i]
        except:
            print "works"
            flag=True
            break
        if flag:
            break
        print j
    if flag:
        scraperwiki.sqlite.execute(query)
        flag=False
        continue
        


