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
sl_no=0
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
#state_list=state_list[:1]
#district_list=district_list[:1]
#for i in state_list:
   # print i
for i in state_list:
    #print i
    
    #state selection done
    for j in district_list:
        
        sl_no+=1
        
        response = br.open(url)
        VAR1 = response.read() #reads the source file for the web page
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
        print i,j
        br["drpState"]=i
        
        response = br.submit()
        #response = br.open(url)
        var=response.read()
        print response.read()
        root=lxml.html.fromstring(var)
        br.select_form("Form1")
        br.set_all_readonly(False)
        for control in br.form.controls:
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
            #print state,district
            #print data
            d1=dict()
            d2=dict()
            d3=dict()
            print "here1"
            for k in range(len(data)):
                if k%4==0:
                    key=data[k]
                if k%4==1:
                    if data[k]==' ':
                        d1[key]=0
                    else:
                        d1[key]=data[k]
                if k%4==2:
                    if data[k]==' ':
                        d2[key]=0
                    else:
                        d2[key]=data[k]
                if k%4==3:
                    if data[k]==' ':
                        d3[key]=0
                    else:
                        d3[key]=data[k]
            d1['sl_no']=sl_no
            d1['state']=state
            d1['district']=district
            print "here2"
            scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Number_of_primary_schools":d1["Number_of_primary_schools"],"Unirrigated_Area":d1["Unirrigated_Area"],"Area_not_available_for_cultivation":d1["Area_not_available_for_cultivation"],"River_water":d1["River_water"],"Number_of_maternity_home":d1["Number_of_maternity_home"],"Number_of_ayurvedic_dispensary":d1["Number_of_ayurvedic_dispensary"],"Number_of_primary_health_centre":d1["Number_of_primary_health_centre"],"Number_of_middle_schools":d1["Number_of_middle_schools"],"Number_of_family_welfare_centre":d1["Number_of_family_welfare_centre"],"Number_of_telegraph_office":d1["Number_of_telegraph_office"],"Number_of_forest_land":d1["Number_of_forest_land"],"River":d1["River"],"Number_of_cinema":d1["Number_of_cinema/video-hall"],"Number_of_ayurvedic_hospitals":d1["Number_of_ayurvedic_hospitals"],"Number_of_secondary_schools":d1["Number_of_secondary_schools"],"Bus_services":d1["Bus_services"],"Number_of_private_canal":d1["Number_of_private_canal"],"Number_of_primary_health_sub-centre":d1["Number_of_primary_health_sub-centre"],"Number_of_TB_clinic":d1["Number_of_T.B._clinic"],"Tube-well_without_electricity":d1["Tube-well_(without_electricity)"],"Number_of_stadium_auditorium_":d1["Number_of_stadium/auditorium_"],"Number_of_industrial_schools":d1["Number_of_industrial_schools"],"district":d1["district"],"Number_of_other_educational_schools":d1["Number_of_other_educational_schools"],"Number_of_tank_water":d1["Number_of_tank_water"],"Number_of_subsidised_medical_practitioners":d1["Number_of_subsidised_medical_practitioners"],"Number_of_adult_literacy_class_centres":d1["Number_of_adult_literacy_class/centres"],"Number_of_agricultural_credit_societies":d1["Number_of_agricultural_credit_societies"],"Number_of_colleges":d1["Number_of_colleges"],"Lakes":d1["Lakes"],"Number_of_homeopathic_dispensary":d1["Number_of_homeopathic_dispensary"],"Irrigated_Area":d1["Irrigated_Area"],"Tubewell_water":d1["Tubewell_water"],"state":d1["state"],"Waterfall":d1["Waterfall"],"Number_of_other_credit_societies":d1["Number_of_other_credit_societies"],"Number_of_Co-operative_commercial_bank":d1["Number_of_Co-operative_commercial_bank"],"Others":d1["Others"],"Number_of_unani_hospital":d1["Number_of_unani_hospital"],"Number_of_government_canal":d1["Number_of_government_canal"],"Number_of_allopathic_dispensary":d1["Number_of_allopathic_dispensary"],"Number_of_sub-districts":d1["Number_of_sub-districts"],"Tank":d1["Tank"],"Number_of_inhabited_villages":d1["Number_of_inhabited_villages"],"Other_drinking_water_sources":d1["Other_drinking_water_sources"],"Number_of_nursing_home":d1["Number_of_nursing_home"],"Number_of_other_medical_facilities":d1["Number_of_other_medical_facilities"],"Tube-well_with_electricity":d1["Tube-well_(with_electricity)"],"Lake":d1["Lake"],"Culturable_waste_including_gauchar_and_groves":d1["Culturable_waste_(including_gauchar_and_groves)"],"Number_of_commercial_bank":d1["Number_of_commercial_bank"],"Number_of_health_centre":d1["Number_of_health_centre"],"Number_of_unani_dispensary":d1["Number_of_unani_dispensary"],"Number_of_community_health_workers":d1["Number_of_community_health_workers"],"Railways_services":d1["Railways_services"],"Number_of_registered_private_medical_practiotioners":d1["Number_of_registered_private_medical_practiotioners"],"Canals":d1["Canals"],"Number_of_allopathic_hospitals":d1["Number_of_allopathic_hospitals"],"sl_no":d1["sl_no"],"Number_of_child_welfare_centre":d1["Number_of_child_welfare_centre"],"Navigable_water_way_including_river_canal_etc":d1["Navigable_water_way_including_river,_canal_etc."],"Number_of_maternity_and_child_welfare_centre":d1["Number_of_maternity_and_child_welfare_centre"],"Spring":d1["Spring"],"Number_of_non_agricultural_credit_societies":d1["Number_of_non_agricultural_credit_societies"],"Number_of_senior_secondary_schools":d1["Number_of_senior_secondary_schools"],"Number_of_post_office":d1["Number_of_post_office"],"Number_of_sports_club":d1["Number_of_sports_club"],"Number_of_training_schools":d1["Number_of_training_schools"],"Number_of_telephone_connections":d1["Number_of_telephone_connections"],"Handpumb":d1["Handpumb"],"Well_without_electricity":d1["Well_(without_electricity)"],"Tap_water":d1["Tap_water"],"Number_of_homeopathic_hospital":d1["Number_of_homeopathic_hospital"],"Well_water":d1["Well_water"],"Well_with_electricity":d1["Well_(with_electricity)"],"Number_of_post_and_telegraph_office":d1["Number_of_post_and_telegraph_office"]})
            print "done"
            print "here"
        except:
            print "works"
            flag=True
            break
        if flag:
            break
        #print j
    if flag:
        flag=False
        continue


