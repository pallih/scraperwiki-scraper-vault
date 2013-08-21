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
            d3['sl_no']=sl_no
            d3['state']=state
            d3['district']=district
            print "here2"
            scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Number_of_primary_schools":d3["Number_of_primary_schools"],"Unirrigated_Area":d3["Unirrigated_Area"],"Area_not_available_for_cultivation":d3["Area_not_available_for_cultivation"],"River_water":d3["River_water"],"Number_of_maternity_home":d3["Number_of_maternity_home"],"Number_of_ayurvedic_dispensary":d3["Number_of_ayurvedic_dispensary"],"Number_of_primary_health_centre":d3["Number_of_primary_health_centre"],"Number_of_middle_schools":d3["Number_of_middle_schools"],"Number_of_family_welfare_centre":d3["Number_of_family_welfare_centre"],"Number_of_telegraph_office":d3["Number_of_telegraph_office"],"Number_of_forest_land":d3["Number_of_forest_land"],"River":d3["River"],"Number_of_cinema":d3["Number_of_cinema/video-hall"],"Number_of_ayurvedic_hospitals":d3["Number_of_ayurvedic_hospitals"],"Number_of_secondary_schools":d3["Number_of_secondary_schools"],"Bus_services":d3["Bus_services"],"Number_of_private_canal":d3["Number_of_private_canal"],"Number_of_primary_health_sub-centre":d3["Number_of_primary_health_sub-centre"],"Number_of_TB_clinic":d3["Number_of_T.B._clinic"],"Tube-well_without_electricity":d3["Tube-well_(without_electricity)"],"Number_of_stadium_auditorium_":d3["Number_of_stadium/auditorium_"],"Number_of_industrial_schools":d3["Number_of_industrial_schools"],"district":d3["district"],"Number_of_other_educational_schools":d3["Number_of_other_educational_schools"],"Number_of_tank_water":d3["Number_of_tank_water"],"Number_of_subsidised_medical_practitioners":d3["Number_of_subsidised_medical_practitioners"],"Number_of_adult_literacy_class_centres":d3["Number_of_adult_literacy_class/centres"],"Number_of_agricultural_credit_societies":d3["Number_of_agricultural_credit_societies"],"Number_of_colleges":d3["Number_of_colleges"],"Lakes":d3["Lakes"],"Number_of_homeopathic_dispensary":d3["Number_of_homeopathic_dispensary"],"Irrigated_Area":d3["Irrigated_Area"],"Tubewell_water":d3["Tubewell_water"],"state":d3["state"],"Waterfall":d3["Waterfall"],"Number_of_other_credit_societies":d3["Number_of_other_credit_societies"],"Number_of_Co-operative_commercial_bank":d3["Number_of_Co-operative_commercial_bank"],"Others":d3["Others"],"Number_of_unani_hospital":d3["Number_of_unani_hospital"],"Number_of_government_canal":d3["Number_of_government_canal"],"Number_of_allopathic_dispensary":d3["Number_of_allopathic_dispensary"],"Number_of_sub-districts":d3["Number_of_sub-districts"],"Tank":d3["Tank"],"Number_of_inhabited_villages":d3["Number_of_inhabited_villages"],"Other_drinking_water_sources":d3["Other_drinking_water_sources"],"Number_of_nursing_home":d3["Number_of_nursing_home"],"Number_of_other_medical_facilities":d3["Number_of_other_medical_facilities"],"Tube-well_with_electricity":d3["Tube-well_(with_electricity)"],"Lake":d3["Lake"],"Culturable_waste_including_gauchar_and_groves":d3["Culturable_waste_(including_gauchar_and_groves)"],"Number_of_commercial_bank":d3["Number_of_commercial_bank"],"Number_of_health_centre":d3["Number_of_health_centre"],"Number_of_unani_dispensary":d3["Number_of_unani_dispensary"],"Number_of_community_health_workers":d3["Number_of_community_health_workers"],"Railways_services":d3["Railways_services"],"Number_of_registered_private_medical_practiotioners":d3["Number_of_registered_private_medical_practiotioners"],"Canals":d3["Canals"],"Number_of_allopathic_hospitals":d3["Number_of_allopathic_hospitals"],"sl_no":d3["sl_no"],"Number_of_child_welfare_centre":d3["Number_of_child_welfare_centre"],"Navigable_water_way_including_river_canal_etc":d3["Navigable_water_way_including_river,_canal_etc."],"Number_of_maternity_and_child_welfare_centre":d3["Number_of_maternity_and_child_welfare_centre"],"Spring":d3["Spring"],"Number_of_non_agricultural_credit_societies":d3["Number_of_non_agricultural_credit_societies"],"Number_of_senior_secondary_schools":d3["Number_of_senior_secondary_schools"],"Number_of_post_office":d3["Number_of_post_office"],"Number_of_sports_club":d3["Number_of_sports_club"],"Number_of_training_schools":d3["Number_of_training_schools"],"Number_of_telephone_connections":d3["Number_of_telephone_connections"],"Handpumb":d3["Handpumb"],"Well_without_electricity":d3["Well_(without_electricity)"],"Tap_water":d3["Tap_water"],"Number_of_homeopathic_hospital":d3["Number_of_homeopathic_hospital"],"Well_water":d3["Well_water"],"Well_with_electricity":d3["Well_(with_electricity)"],"Number_of_post_and_telegraph_office":d3["Number_of_post_and_telegraph_office"]})
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
       # scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Number_of_primary_schools":d2["Number_of_primary_schools"],"Unirrigated_Area":d2["Unirrigated_Area"],"Area_not_available_for_cultivation":d2["Area_not_available_for_cultivation"],"River_water":d2["River_water"],"Number_of_maternity_home":d2["Number_of_maternity_home"],"Number_of_ayurvedic_dispensary":d2["Number_of_ayurvedic_dispensary"],"Number_of_primary_health_centre":d2["Number_of_primary_health_centre"],"Number_of_middle_schools":d2["Number_of_middle_schools"],"Number_of_family_welfare_centre":d2["Number_of_family_welfare_centre"],"Number_of_telegraph_office":d2["Number_of_telegraph_office"],"Number_of_forest_land":d2["Number_of_forest_land"],"River":d2["River"],"Number_of_cinema":d2["Number_of_cinema/video-hall"],"Number_of_ayurvedic_hospitals":d2["Number_of_ayurvedic_hospitals"],"Number_of_secondary_schools":d2["Number_of_secondary_schools"],"Bus_services":d2["Bus_services"],"Number_of_private_canal":d2["Number_of_private_canal"],"Number_of_primary_health_sub-centre":d2["Number_of_primary_health_sub-centre"],"Number_of_TB_clinic":d2["Number_of_T.B._clinic"],"Tube-well_without_electricity":d2["Tube-well_(without_electricity)"],"Number_of_stadium_auditorium_":d2["Number_of_stadium/auditorium_"],"Number_of_industrial_schools":d2["Number_of_industrial_schools"],"district":d2["district"],"Number_of_other_educational_schools":d2["Number_of_other_educational_schools"],"Number_of_tank_water":d2["Number_of_tank_water"],"Number_of_subsidised_medical_practitioners":d2["Number_of_subsidised_medical_practitioners"],"Number_of_adult_literacy_class_centres":d2["Number_of_adult_literacy_class/centres"],"Number_of_agricultural_credit_societies":d2["Number_of_agricultural_credit_societies"],"Number_of_colleges":d2["Number_of_colleges"],"Lakes":d2["Lakes"],"Number_of_homeopathic_dispensary":d2["Number_of_homeopathic_dispensary"],"Irrigated_Area":d2["Irrigated_Area"],"Tubewell_water":d2["Tubewell_water"],"state":d2["state"],"Waterfall":d2["Waterfall"],"Number_of_other_credit_societies":d2["Number_of_other_credit_societies"],"Number_of_Co-operative_commercial_bank":d2["Number_of_Co-operative_commercial_bank"],"Others":d2["Others"],"Number_of_unani_hospital":d2["Number_of_unani_hospital"],"Number_of_government_canal":d2["Number_of_government_canal"],"Number_of_allopathic_dispensary":d2["Number_of_allopathic_dispensary"],"Number_of_sub-districts":d2["Number_of_sub-districts"],"Tank":d2["Tank"],"Number_of_inhabited_villages":d2["Number_of_inhabited_villages"],"Other_drinking_water_sources":d2["Other_drinking_water_sources"],"Number_of_nursing_home":d2["Number_of_nursing_home"],"Number_of_other_medical_facilities":d2["Number_of_other_medical_facilities"],"Tube-well_with_electricity":d2["Tube-well_(with_electricity)"],"Lake":d2["Lake"],"Culturable_waste_including_gauchar_and_groves":d2["Culturable_waste_(including_gauchar_and_groves)"],"Number_of_commercial_bank":d2["Number_of_commercial_bank"],"Number_of_health_centre":d2["Number_of_health_centre"],"Number_of_unani_dispensary":d2["Number_of_unani_dispensary"],"Number_of_community_health_workers":d2["Number_of_community_health_workers"],"Railways_services":d2["Railways_services"],"Number_of_registered_private_medical_practiotioners":d2["Number_of_registered_private_medical_practiotioners"],"Canals":d2["Canals"],"Number_of_allopathic_hospitals":d2["Number_of_allopathic_hospitals"],"sl_no":d2["sl_no"],"Number_of_child_welfare_centre":d2["Number_of_child_welfare_centre"],"Navigable_water_way_including_river_canal_etc":d2["Navigable_water_way_including_river,_canal_etc."],"Number_of_maternity_and_child_welfare_centre":d2["Number_of_maternity_and_child_welfare_centre"],"Spring":d2["Spring"],"Number_of_non_agricultural_credit_societies":d2["Number_of_non_agricultural_credit_societies"],"Number_of_senior_secondary_schools":d2["Number_of_senior_secondary_schools"],"Number_of_post_office":d2["Number_of_post_office"],"Number_of_sports_club":d2["Number_of_sports_club"],"Number_of_training_schools":d2["Number_of_training_schools"],"Number_of_telephone_connections":d2["Number_of_telephone_connections"],"Handpumb":d2["Handpumb"],"Well_without_electricity":d2["Well_(without_electricity)"],"Tap_water":d2["Tap_water"],"Number_of_homeopathic_hospital":d2["Number_of_homeopathic_hospital"],"Well_water":d2["Well_water"],"Well_with_electricity":d2["Well_(with_electricity)"],"Number_of_post_and_telegraph_office":d2["Number_of_post_and_telegraph_office"]})
        flag=False
        continue


