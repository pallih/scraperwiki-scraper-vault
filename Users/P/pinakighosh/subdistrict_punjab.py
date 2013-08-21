import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin

uri="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Area_Profile/SubDistrict_Profile.aspx?cki=AoDoRSqLMhi"

response= urlopen(uri)
#print response.read()
forms = ParseResponse(response, backwards_compat=False)
#print forms
form = forms[0]
#print form
statecode=[]
serial=1
statename=[]

#for item in form.find_control("drpState").items:
 #   statecode.append(item.name)
 #   statename.append(item.attrs['contents'])
#print statename
#print statecode
#statecount=0
#for i in statecode:
#    if(i==""):
#        statecount+=1
#        continue
#    else:
districtcode=[]
districtname=[]
form.set_value(['03'], name="drpState")
content=urlopen(form.click())
forms=ParseResponse(content, backwards_compat=False)
form=forms[0]
#print form
for item in form.find_control("drpDistrict").items:
    districtcode.append(item.name)
    districtname.append(item.attrs['contents'])
    districtcount=0
for j in districtcode:
    if(j==""):
        districtcount+=1
        continue
    else:
        sub_districtcode=[]
        sub_districtname=[]
        form.set_value([j],name="drpDistrict")
        content=urlopen(form.click())
        forms=ParseResponse(content, backwards_compat=False)
        form=forms[0]
        sub_districtname=[]
        for item in form.find_control("drpTeshil").items:
            sub_districtcode.append(item.name)
            sub_districtname.append(item.attrs['contents'])
            #print sub_districtname
        print sub_districtcode
        sub_districtcount=0
        for l in sub_districtcode:
            if(l==""):
                sub_districtcount+=1
                continue
            else:
                form.set_value([l],name="drpTeshil")
                content=urlopen(form.click())
                response=lxml.html.fromstring(content.read())
                #print response
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
                        scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":'Punjab',"district":districtname[districtcount],"Sub_district":sub_districtname[sub_districtcount]})
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
                        scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":'Punjab',"district":districtname[districtcount],"Sub_district":sub_districtname[sub_districtcount]})
                        s_no+=2
                        row=[]
                serial=s_no-1
            sub_districtcount+=1
            
    districtcount+=1
#    statecount+=1