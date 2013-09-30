import scraperwiki
import lxml.html
url="http://censusindia.gov.in/Census_Data_2001/Village_Directory/List_of_Villages/List_of_Villages_Alphabetical.aspx?cki=&State_Code=19"
import string
#create list of upper case alphabets
l=list(string.ascii_uppercase)
#append a 0 for single digit numbers
html=scraperwiki.scrape(url)
root=lxml.html.fromstring(html)
for i in range(10):
        l[i]='0'+l[i];

#select div where print area is there
        for el in root.cssselect("div#printarea td"):
           
#select appropriate table row
            for el2 in el.cssselect("tr.GridAlternativeRows td"):
                  row.append(el2.text_content())
                  data.append(row)
#save to data base
                  scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":s_no,"village_name":row[1], 

"village_code":row[2],"District_Name":row[4]})
                  s_no+=1
                  row=[]
#select appropriate table row
            for el2 in el.cssselect("tr.GridRows td"):
                
                    row.append(el2.text_content())
                  
               
                    data.append(row)
#save to data base
                    scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":s_no,"village_name":row[1], 

"village_code":row[2],"District_Name":row[4]})
                    s_no+=1
                    row=[]
print "completed scrapping"import scraperwiki
import lxml.html
url="http://censusindia.gov.in/Census_Data_2001/Village_Directory/List_of_Villages/List_of_Villages_Alphabetical.aspx?cki=&State_Code=19"
import string
#create list of upper case alphabets
l=list(string.ascii_uppercase)
#append a 0 for single digit numbers
html=scraperwiki.scrape(url)
root=lxml.html.fromstring(html)
for i in range(10):
        l[i]='0'+l[i];

#select div where print area is there
        for el in root.cssselect("div#printarea td"):
           
#select appropriate table row
            for el2 in el.cssselect("tr.GridAlternativeRows td"):
                  row.append(el2.text_content())
                  data.append(row)
#save to data base
                  scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":s_no,"village_name":row[1], 

"village_code":row[2],"District_Name":row[4]})
                  s_no+=1
                  row=[]
#select appropriate table row
            for el2 in el.cssselect("tr.GridRows td"):
                
                    row.append(el2.text_content())
                  
               
                    data.append(row)
#save to data base
                    scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":s_no,"village_name":row[1], 

"village_code":row[2],"District_Name":row[4]})
                    s_no+=1
                    row=[]
print "completed scrapping"