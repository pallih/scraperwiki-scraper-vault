import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin

uri = "http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Online_Migration/Migration_Streams.aspx"

l_c=0
response = urlopen(uri)
#print response
forms = ParseResponse(response, backwards_compat=False)
form = forms[0]
#print form
form.set_value(["rdbState"], kind="singlelist", nr=0)

# form.click() returns a mechanize.Request object
# (see HTMLForm.click.__doc__ if you want to use only the forms support, and
# not the rest of mechanize)
#print urlopen(form.click()).read()
#print form.click()
response= urlopen(form.click())
#print response

forms = ParseResponse(response, backwards_compat=False)
#print forms
form = forms[0]
#print form
control = form.find_control("drpState", type="select")
#print control
#print control.name, control.value, control.type
#create list 1-35
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
#control.value = [l2]
#print control.name, control.value, control.type
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
        if l_c<6:
            row.append(i.text_content())
            l_c+=1
            #print l_c
        else:
            row.append(i.text_content())
            l_c=0
            data.append(row)
#            try:
            scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":sOdd,"Migrants":row[1],"Last_residence_TRU":row[2],"TRU":row[3],"Persons":row[4],"Males":row[5],"Females":row[6]})
#            except:
#                print state_count
#                print l2[state_count]
#                print s_no
#                print l_c
#                print row[0]
#                print row[1]
            #s_no+=2
            sOdd=sOdd+2
            row=[]

    s_no=serial+1
    for i in response.cssselect("tr.GridAlternativeRows td"):
        if l_c<6:
            row.append(i.text_content())
            l_c+=1
            #print l_c
        else:
            row.append(i.text_content())
            l_c=0
            data.append(row)
#            try:
            scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":sEven,"Migrants":row[1],"Last_residence_TRU":row[2],"TRU":row[3],"Persons":row[4],"Males":row[5],"Females":row[6]})
#            except:
#                print state_count
#                print l2[state_count]
#                print s_no
#                print l_c
#                print row[0]
#                print row[1]
            #s_no+=2
            sEven=sEven+2
            row=[]
            #serial=s_no
    state_count+=1
