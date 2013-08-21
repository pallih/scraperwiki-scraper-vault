import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin

uri = "http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Online_Migration/Duration_of_Residence_By_LastResidence.aspx"

l_c=0
response = urlopen(uri)
forms = ParseResponse(response, backwards_compat=False)
form = forms[0]
form.set_value(["rdbState"], kind="singlelist", nr=0)

response= urlopen(form.click())

forms = ParseResponse(response, backwards_compat=False)
form = forms[0]
control = form.find_control("drpState", type="select")

l1=list(range(1,36))
l2=[]
#convert numbers in l2 to string
for i in l1:
        l2.append(str(i))
#append a 0 for single digit numbers
for i in range(9):
    l2[i]='0'+l2[i]
    #print l2
state_count=0
c=1
serial=1
s_no=serial
sOdd=1
sEven=2

#run loop for all state and union territories
while state_count<35:
    form.set_value([l2[state_count] ], name="drpState")
    #print form

    content=urlopen(form.click())
    #print content
    response=lxml.html.fromstring(content.read())
    #print response
    
    data=[]
    row=[]
    l_c=0
    for i in response.cssselect("tr.GridRows td"):
        if l_c<5:
            row.append(i.text_content())
            l_c+=1
            #print l_c
        else:
            row.append(i.text_content())
            l_c=0
            data.append(row)

            scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":sOdd,"Duration_of_residence":row[1],"Last_residence":row[2],"Persons":row[3],"Males":row[4],"Females":row[5]})

            sOdd=sOdd+2
            row=[]

    s_no=serial+1
    for i in response.cssselect("tr.GridAlternativeRows td"):
        if l_c<5:
            row.append(i.text_content())
            l_c+=1
        else:
            row.append(i.text_content())
            l_c=0
            data.append(row)
            scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":sEven,"Duration_of_residence":row[1],"Last_residence":row[2],"Persons":row[3],"Males":row[4],"Females":row[5]})
            #s_no+=2
            sEven=sEven+2
            row=[]
            #serial=s_no
    state_count+=1
