import scraperwiki

import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin


list1=list(range(1,36))
list2=[]
for i in list1:
    list2.append(str(i))

for i in range(9):
    list2[i]='0'+list2[i]

#print list2
state_count=0
l_c=0

serial=1
unique=1

uri ="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Social_and_cultural/SC_Attending_educational_institutions.aspx"

response = urlopen(uri)

forms = ParseResponse(response, backwards_compat=False)
form = forms[0]
print forms
form.set_value(["rdbState"], kind="singlelist", nr=0)

# form.click() returns a mechanize.Request object
# (see HTMLForm.click.__doc__ if you want to use only the forms support, and
# not the rest of mechanize)
#print urlopen(form.click()).read()
#print form.click()

response= urlopen(form.click())
forms = ParseResponse(response, backwards_compat=False)
form = forms[0]
control = form.find_control("drpState", type="select")
#print control.name, control.value, control.type
#control.value = ["01"]
#print control.name, control.value, control.type

while state_count<35:

    form.set_value([list2[state_count] ], name="drpState")
    print form
    
    item=control.get(list2[state_count] )
    print item.attrs

    content=urlopen(form.click())
    print content
    response=lxml.html.fromstring(content.read())
    print response
    s_no=unique
    row=[]
    data=[]

    for i in response.cssselect("tr.GridRows td"):
        if l_c<5:
            row.append(i.text_content())
            l_c+=1
        else:
            row.append(i.text_content())
            l_c=0
            data.append(row)

            scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"State":item.attrs,"Age_Groups":row[1],"Total_Population":row[2],"Persons":row[3],"Males":row[4],"Females":row[5]})
            s_no+=2
            row=[]

    s_no=unique+1
    for i in response.cssselect("tr.GridAlternativeRows td"):
        if l_c<5:
            row.append(i.text_content())
            l_c+=1
        else:
            row.append(i.text_content())
            l_c=0
            data.append(row)
            scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"State":item.attrs,"Age_Groups":row[1],"Total_Population":row[2],"Persons":row[3],"Males":row[4],"Females":row[5]})
            s_no+=2
            unique=s_no-1
            row=[]
    state_count+=1
    serial=s_no+1
