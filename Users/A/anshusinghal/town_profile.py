import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin

uri="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Area_Profile/Town_Profile.aspx?cki=x3s1AFFHjC4"

response= urlopen(uri)
#print response.read()
forms = ParseResponse(response, backwards_compat=False)
#print forms
form = forms[0]
#print form
statecode=[]
serial=1
state=[]

for item in form.find_control("drpState").items:
    statecode.append(item.name)
    state.append(item.attrs['contents'])
#print state
#print statecode
statestore=0
for i in statecode:
    if(i==""):
        statestore+=1
        continue
    else:
        districtcode=[]
        district=[]
        form.set_value([i], name="drpState")
        content=urlopen(form.click())
        forms=ParseResponse(content, backwards_compat=False)
        form=forms[0]
        for item in form.find_control("drpDistrict").items:
            districtcode.append(item.name)
            #print item.attrs['contents']
            district.append(item.attrs['contents'])
        #print district
        districtstore=0
        for j in districtcode:

            if(j==""):
                districtstore+=1
                #print districtstore
                #print district[districtstore]
                continue
            else:
                towncode=[]
                town=[]
                form.set_value([j], name="drpDistrict")
                content=urlopen(form.click())
                forms=ParseResponse(content, backwards_compat=False)
                form=forms[0]
                for item in form.find_control("drpTown").items:
                    towncode.append(item.name)
                    town.append(item.attrs['contents'])
                #print town
                townstore=0
                for k in towncode:
                    if(k==""):
                        townstore+=1
                        #print town[townstore]
                        continue
                    else:
                        #print "now"
                        #print town[townstore]
                        form.set_value([k],name="drpTown")
                        content=urlopen(form.click())
                        response=lxml.html.fromstring(content.read())
                        row=[]
                        data=[]
                        l_c=0
                        s_no=serial
                        for l in response.cssselect("tr.GridRows td"):
                            if l_c<3:
                                row.append(l.text_content())
                                l_c+=1
                            else:
                                row.append(l.text_content())
                                l_c=0
                                data.append(row)
                                scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":state[statestore],"district":district[districtstore],"town":town[townstore]})
                                s_no+=2
                                row=[]

                        s_no=serial+1
                        for l in response.cssselect("tr.GridAlternativeRows td"):
                            if l_c<3:
                                row.append(l.text_content())
                                l_c+=1
                            else:
                                row.append(l.text_content())
                                l_c=0
                                data.append(row)
                                scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":state[statestore],"district":district[districtstore],"town":town[townstore]})
                                s_no+=2
                                row=[]
                        townstore+=1
                        serial=s_no-1
                    #print townstore
                districtstore+=1
                #print districtstore
    statestore+=1
import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin

uri="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Area_Profile/Town_Profile.aspx?cki=x3s1AFFHjC4"

response= urlopen(uri)
#print response.read()
forms = ParseResponse(response, backwards_compat=False)
#print forms
form = forms[0]
#print form
statecode=[]
serial=1
state=[]

for item in form.find_control("drpState").items:
    statecode.append(item.name)
    state.append(item.attrs['contents'])
#print state
#print statecode
statestore=0
for i in statecode:
    if(i==""):
        statestore+=1
        continue
    else:
        districtcode=[]
        district=[]
        form.set_value([i], name="drpState")
        content=urlopen(form.click())
        forms=ParseResponse(content, backwards_compat=False)
        form=forms[0]
        for item in form.find_control("drpDistrict").items:
            districtcode.append(item.name)
            #print item.attrs['contents']
            district.append(item.attrs['contents'])
        #print district
        districtstore=0
        for j in districtcode:

            if(j==""):
                districtstore+=1
                #print districtstore
                #print district[districtstore]
                continue
            else:
                towncode=[]
                town=[]
                form.set_value([j], name="drpDistrict")
                content=urlopen(form.click())
                forms=ParseResponse(content, backwards_compat=False)
                form=forms[0]
                for item in form.find_control("drpTown").items:
                    towncode.append(item.name)
                    town.append(item.attrs['contents'])
                #print town
                townstore=0
                for k in towncode:
                    if(k==""):
                        townstore+=1
                        #print town[townstore]
                        continue
                    else:
                        #print "now"
                        #print town[townstore]
                        form.set_value([k],name="drpTown")
                        content=urlopen(form.click())
                        response=lxml.html.fromstring(content.read())
                        row=[]
                        data=[]
                        l_c=0
                        s_no=serial
                        for l in response.cssselect("tr.GridRows td"):
                            if l_c<3:
                                row.append(l.text_content())
                                l_c+=1
                            else:
                                row.append(l.text_content())
                                l_c=0
                                data.append(row)
                                scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":state[statestore],"district":district[districtstore],"town":town[townstore]})
                                s_no+=2
                                row=[]

                        s_no=serial+1
                        for l in response.cssselect("tr.GridAlternativeRows td"):
                            if l_c<3:
                                row.append(l.text_content())
                                l_c+=1
                            else:
                                row.append(l.text_content())
                                l_c=0
                                data.append(row)
                                scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":state[statestore],"district":district[districtstore],"town":town[townstore]})
                                s_no+=2
                                row=[]
                        townstore+=1
                        serial=s_no-1
                    #print townstore
                districtstore+=1
                #print districtstore
    statestore+=1
