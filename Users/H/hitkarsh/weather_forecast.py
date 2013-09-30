import scraperwiki
import lxml.html

url="http://www.imd.gov.in/section/nhac/distforecast/"
states=['andra-pradesh.txt','arunachal-prades.txt']
#for i in states:
    #print url+i
html = scraperwiki.scrape(url)
url1=url+"state_list_new.htm"
html = scraperwiki.scrape(url1)
root = lxml.html.fromstring(html)
for statecaps in root.cssselect("form"):
    st=statecaps.text_content()
#print html

#states=[]
states=st.split('\t')
states.append('andra-pradesh')
states.append('arunachal-prades')
states.append('uttaranchal')
states=[states[1]]+states[4:-5]+states[-4:]
#print states
sf=[]
for i in states:
    sf.append(i.lower()+'.txt')
sl_no=0
for i1 in sf:
    html=scraperwiki.scrape(url+i1)
    root=lxml.html.fromstring(html)
    st=root.text_content()
    l1=st.split()
    district=[]
    rainfall=[]
    max_temp=[]
    min_temp=[]
    total_cloud_cover=[]
    max_rel_hum=[]
    min_rel_hum=[]
    wind_speed=[]
    wind_dir=[]
    i=0
    district=[]
    rainfall=[]
    day=[]
    while True:
        if l1[i]=="DAY-5":
            c=0
            i+=1
            while c<5:
                day.append(l1[i])
                c+=1
                i+=1
        if l1[i]=="DISTRICT":
            district.append(l1[i+2])
            i+=2
        if l1[i]=="Rainfall":
            i+=2
            c=0
            row=[]
            while c<5:
                row.append(l1[i])
                c+=1
                i+=1
            rainfall.append(row)
        if l1[i]=="Max" and l1[i+1]=="Temperature":
            i+=5
            c=0
            row=[]
            while c<5:
                row.append(l1[i])
                c+=1
                i+=1
            max_temp.append(row)
        if l1[i]=="Min" and l1[i+1]=="Temperature":
            i+=5
            c=0
            row=[]
            while c<5:
                row.append(l1[i])
                c+=1
                i+=1
            min_temp.append(row)
        if l1[i]=="(octa)":
             i+=1
             c=0
             row=[]
             while c<5:
                 row.append(l1[i])
                 c+=1
                 i+=1
             total_cloud_cover.append(row)
        if l1[i]=="Max" and l1[i+1]=="Relative":
              i+=4
              c=0
              row=[]
              while c<5:
                  row.append(l1[i])
                  c+=1
                  i+=1
              max_rel_hum.append(row)
        if l1[i]=="Min" and l1[i+1]=="Relative":
               i+=4
               c=0
               row=[]
               while c<5:
                   row.append(l1[i])
                   c+=1
                   i+=1
               min_rel_hum.append(row)
        if l1[i]=="(kmph)":
               i+=1
               c=0
               row=[]
               while c<5:
                   row.append(l1[i])
                   c+=1
                   i+=1
               wind_speed.append(row)
        if l1[i]=="direction":
                i+=2
                c=0
                row=[]
                while c<5:
                    row.append(l1[i])
                    c+=1
                    i+=1
                wind_dir.append(row)
        i+=1
        if i==len(l1):
            break  
    district=district[1:]
    for p in day:
        print p
    #for j in district:
    for j in range(len(district)):
        #for k in range(len(day)):
        for k in range(5):
            #for m in range(len(rainfall)):
            scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":sl_no,"state_name":i1,"date":day[k],"district_name":district[j],"rainfall":rainfall[j][k],"max_temp":max_temp[j][k],"min_temp":min_temp[j][k],"total_cloud_cover":total_cloud_cover[j][k], "max_rel_hum":max_rel_hum[j][k],"min_rel_hum":min_rel_hum[j][k],"wind_speed":wind_speed[j][k],"wind_dir":wind_dir[j][k]})
            sl_no+=1
    #print(district)
    #print(rainfall)
    #print(max_temp)
    #print(min_temp)
    #print(total_cloud_cover)
    #print(max_rel_hum)
    #print(min_rel_hum)
    #print(wind_speed)
    #print(wind_dir)import scraperwiki
import lxml.html

url="http://www.imd.gov.in/section/nhac/distforecast/"
states=['andra-pradesh.txt','arunachal-prades.txt']
#for i in states:
    #print url+i
html = scraperwiki.scrape(url)
url1=url+"state_list_new.htm"
html = scraperwiki.scrape(url1)
root = lxml.html.fromstring(html)
for statecaps in root.cssselect("form"):
    st=statecaps.text_content()
#print html

#states=[]
states=st.split('\t')
states.append('andra-pradesh')
states.append('arunachal-prades')
states.append('uttaranchal')
states=[states[1]]+states[4:-5]+states[-4:]
#print states
sf=[]
for i in states:
    sf.append(i.lower()+'.txt')
sl_no=0
for i1 in sf:
    html=scraperwiki.scrape(url+i1)
    root=lxml.html.fromstring(html)
    st=root.text_content()
    l1=st.split()
    district=[]
    rainfall=[]
    max_temp=[]
    min_temp=[]
    total_cloud_cover=[]
    max_rel_hum=[]
    min_rel_hum=[]
    wind_speed=[]
    wind_dir=[]
    i=0
    district=[]
    rainfall=[]
    day=[]
    while True:
        if l1[i]=="DAY-5":
            c=0
            i+=1
            while c<5:
                day.append(l1[i])
                c+=1
                i+=1
        if l1[i]=="DISTRICT":
            district.append(l1[i+2])
            i+=2
        if l1[i]=="Rainfall":
            i+=2
            c=0
            row=[]
            while c<5:
                row.append(l1[i])
                c+=1
                i+=1
            rainfall.append(row)
        if l1[i]=="Max" and l1[i+1]=="Temperature":
            i+=5
            c=0
            row=[]
            while c<5:
                row.append(l1[i])
                c+=1
                i+=1
            max_temp.append(row)
        if l1[i]=="Min" and l1[i+1]=="Temperature":
            i+=5
            c=0
            row=[]
            while c<5:
                row.append(l1[i])
                c+=1
                i+=1
            min_temp.append(row)
        if l1[i]=="(octa)":
             i+=1
             c=0
             row=[]
             while c<5:
                 row.append(l1[i])
                 c+=1
                 i+=1
             total_cloud_cover.append(row)
        if l1[i]=="Max" and l1[i+1]=="Relative":
              i+=4
              c=0
              row=[]
              while c<5:
                  row.append(l1[i])
                  c+=1
                  i+=1
              max_rel_hum.append(row)
        if l1[i]=="Min" and l1[i+1]=="Relative":
               i+=4
               c=0
               row=[]
               while c<5:
                   row.append(l1[i])
                   c+=1
                   i+=1
               min_rel_hum.append(row)
        if l1[i]=="(kmph)":
               i+=1
               c=0
               row=[]
               while c<5:
                   row.append(l1[i])
                   c+=1
                   i+=1
               wind_speed.append(row)
        if l1[i]=="direction":
                i+=2
                c=0
                row=[]
                while c<5:
                    row.append(l1[i])
                    c+=1
                    i+=1
                wind_dir.append(row)
        i+=1
        if i==len(l1):
            break  
    district=district[1:]
    for p in day:
        print p
    #for j in district:
    for j in range(len(district)):
        #for k in range(len(day)):
        for k in range(5):
            #for m in range(len(rainfall)):
            scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":sl_no,"state_name":i1,"date":day[k],"district_name":district[j],"rainfall":rainfall[j][k],"max_temp":max_temp[j][k],"min_temp":min_temp[j][k],"total_cloud_cover":total_cloud_cover[j][k], "max_rel_hum":max_rel_hum[j][k],"min_rel_hum":min_rel_hum[j][k],"wind_speed":wind_speed[j][k],"wind_dir":wind_dir[j][k]})
            sl_no+=1
    #print(district)
    #print(rainfall)
    #print(max_temp)
    #print(min_temp)
    #print(total_cloud_cover)
    #print(max_rel_hum)
    #print(min_rel_hum)
    #print(wind_speed)
    #print(wind_dir)