import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin

uri="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Area_Profile/SubDistrict_Profile.aspx?cki=h0nEiOToTDs"

response= urlopen(uri)
#print response.read()
forms = ParseResponse(response, backwards_compat=False)
print forms
form = forms[0]
print form
statecode=[]
serial=1

for item in form.find_control("drpState").items:
    statecode.append(item.name)
print statecode

for i in statecode:
    if(i==""):
        continue
    else:
        districtcode=[]
        form.set_value([i], name="drpState")
        content=urlopen(form.click())
        forms=ParseResponse(content, backwards_compat=False)
        form=forms[0]
        for item in form.find_control("drpDistrict").items:
            districtcode.append(item.name)
        for j in districtcode:
            if(j==""):
                continue
            else:

                subdistrictcode=[]
                form.set_value([j], name="drpDistrict")
                content=urlopen(form.click())
                forms=ParseResponse(content, backwards_compat=False)
                form=forms[0]
                for item in form.find_control("drpTeshil").items:
                    subdistrictcode.append(item.name)
                for l in subdistrictcode:
                    if(l==""):
                        continue
                else:





                    form.set_value([l],name="drpTeshil")
                    content=urlopen(form.click())
                    response=lxml.html.fromstring(content.read())
                    row=[]
                    data=[]
                    l_c=0
                    s_no=serial
                    for k in response.cssselect("tr.GridRows td"):
                        if l_c<3:
                            row.append(k.text_content())
                            l_c+=1
                        else:
                            row.append(k.text_content())
                            l_c=0
                            data.append(row)
                            scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":i,"district":j,"subdistrict":l})
                            s_no+=2
                            row=[]

                    s_no=serial+1
                    for k in response.cssselect("tr.GridAlternativeRows td"):
                        if l_c<3:
                            row.append(k.text_content())
                            l_c+=1
                        else:
                            row.append(k.text_content())
                            l_c=0
                            data.append(row)
                            scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":i,"district":j,"subdistrict":l})
                            s_no+=2
                            row=[]
                    serial=s_no-1

import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin

uri="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Area_Profile/SubDistrict_Profile.aspx?cki=h0nEiOToTDs"

response= urlopen(uri)
#print response.read()
forms = ParseResponse(response, backwards_compat=False)
print forms
form = forms[0]
print form
statecode=[]
serial=1

for item in form.find_control("drpState").items:
    statecode.append(item.name)
print statecode

for i in statecode:
    if(i==""):
        continue
    else:
        districtcode=[]
        form.set_value([i], name="drpState")
        content=urlopen(form.click())
        forms=ParseResponse(content, backwards_compat=False)
        form=forms[0]
        for item in form.find_control("drpDistrict").items:
            districtcode.append(item.name)
        for j in districtcode:
            if(j==""):
                continue
            else:

                subdistrictcode=[]
                form.set_value([j], name="drpDistrict")
                content=urlopen(form.click())
                forms=ParseResponse(content, backwards_compat=False)
                form=forms[0]
                for item in form.find_control("drpTeshil").items:
                    subdistrictcode.append(item.name)
                for l in subdistrictcode:
                    if(l==""):
                        continue
                else:





                    form.set_value([l],name="drpTeshil")
                    content=urlopen(form.click())
                    response=lxml.html.fromstring(content.read())
                    row=[]
                    data=[]
                    l_c=0
                    s_no=serial
                    for k in response.cssselect("tr.GridRows td"):
                        if l_c<3:
                            row.append(k.text_content())
                            l_c+=1
                        else:
                            row.append(k.text_content())
                            l_c=0
                            data.append(row)
                            scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":i,"district":j,"subdistrict":l})
                            s_no+=2
                            row=[]

                    s_no=serial+1
                    for k in response.cssselect("tr.GridAlternativeRows td"):
                        if l_c<3:
                            row.append(k.text_content())
                            l_c+=1
                        else:
                            row.append(k.text_content())
                            l_c=0
                            data.append(row)
                            scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":i,"district":j,"subdistrict":l})
                            s_no+=2
                            row=[]
                    serial=s_no-1

