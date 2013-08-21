import scraperwiki
import lxml.html
url="http://censusindia.gov.in/Census_Data_2001/Village_Directory/List_of_Villages/List_of_Villages_Alphabetical.aspx?cki=&State_Code="

import string
#create list 1-35
l1=list(range(1,19))
l2=[]
s_no=0
#convert numbers in l2 to string
for i in l1:
        l2.append(str(i))
#append a 0 for single digit numbers
for i in range(10):
    l2[i]='0'+l2[i]
state_count=0
c=1
data=[]
#run loop for all state and union territories
#while state_count<19:
while state_count<1:
#add state code to the url
    url1=url+l2[state_count]+"&SearchKey="
    state_count+=1
    count=0
    l_c=0
    #data=[]
    row=[]
#run loop for alphabets
    #while count<26:
    while count<2:
#add search alphabet to the url
        url2=url1
        html = scraperwiki.scrape(url2)
        print "html"
        print html
        root = lxml.html.fromstring(html)
        print "root"
        print root
        count+=1
           
#select div where data exists
        for el in root.cssselect("div#printarea td"):
#select appropriate table row
            for el2 in el.cssselect("tr.GridAlternativeRows td"):
                if l_c<4:
                    row.append(el2.text_content())
                    l_c+=1
                else:
                     row.append(el2.text_content())
                     l_c=0
                     data.append(row)
#save to data base
                     scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":s_no,"village_name":row[1], 

"village_code":row[2],"Sub_district_Name":row[3],"District_Name":row[4]})
                     s_no+=1
                     row=[]
#select appropriate table row
            for el2 in el.cssselect("tr.GridRows td"):
                if l_c<4:
                    row.append(el2.text_content())
                    l_c+=1
                else:
                    row.append(el2.text_content())
                    l_c=0
                    data.append(row)
#save to data base
                    scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":s_no,"village_name":row[1], 

"village_code":row[2],"Sub_district_Name":row[3],"District_Name":row[4]})
                    s_no+=1
                    row=[]
print "completed scrapping"