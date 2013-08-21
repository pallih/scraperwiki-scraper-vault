import scraperwiki

import lxml.html
import string
url="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Online_Migration/By_Place_of_Birth.aspx"

state_count=0
c=1
while state_count<35:
    data=[]
    count=0
    l_c=0
    row=[]

br = mechanize.Browser()
    
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
                     scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":s_no,"migrants":row[1], "persons":row[2],"males":row[3],"Females":row[4]})
                     s_no+=1
                     row=[]
