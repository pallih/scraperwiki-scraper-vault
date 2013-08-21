import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin


list1=list(range(1,36))
list2=[]
for i in list1:
    list2.append(str(i))

for i in range(9):
    list2[i]='0'+list2[i]

print list2
state_count=0
l_c=0

serial=1
unique=1

uri ="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Household_Population/Normal_Households_by_Household_Size.aspx"

response = urlopen(uri)

forms = ParseResponse(response, backwards_compat=False)
print forms
form = forms[0]
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

form.set_value(['36'], name="drpState")
content=urlopen(form.click())
response=lxml.html.fromstring(content.read())
#print response.read()
row=[]
data=[]
l_c=0
s_no=1
for i in response.cssselect("tr.GridRows td"):
    if l_c<12:
        row.append(i.text_content())
        l_c+=1
    else:
        row.append(i.text_content())
        l_c=0
        data.append(row)
        scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"State":row[1],"No_of_households":row[2],"1":row[3],"2":row[4],"3":row[5],"4":row[6],"5":row[7],"6":row[8],"7-10":row[9],"10-14":row[10],"15":row[11],"Mean":row[12]})
        s_no+=2
        row=[]

s_no=2
for i in response.cssselect("tr.GridAlternativeRows td"):
    if l_c<12:
        row.append(i.text_content())
        l_c+=1
    else:
        row.append(i.text_content())
        l_c=0
        data.append(row)
        scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"State":row[1],"No_of_households":row[2],"1":row[3],"2":row[4],"3":row[5],"4":row[6],"5":row[7],"6":row[8],"7-10":row[9],"10-14":row[10],"15":row[11],"Mean":row[12]})
        s_no+=2
        row=[]
