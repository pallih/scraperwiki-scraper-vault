import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin
import mechanize
import lxml.html
uri="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Area_Profile/Town_Profile.aspx?cki=6QHuVhlb10a"

response= urlopen(uri)

forms = ParseResponse(response, backwards_compat=False)
print forms
form = forms[0]

print form
statecode=[]
serial=1
st=[]
dt=[]
sb=[]
for item in form.find_control("drpState").items:
    if item.name!='':
        statecode.append(item.name)
control=form.find_control("drpState")
if control.type == "select" and control.name=="drpState": # means it's class ClientForm.SelectControl
    for item in control.items:
        st.append(([label.text for label in item.get_labels()]))
print statecode
st=st[1:]


v1=0
v2=0
print st
for i in statecode:
    if v1>len(st):
        break
    m1=0
    m2=0
    
    
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
        if len(dt)==0:
            control=form.find_control("drpDistrict")
            if control.type == "select" and control.name=="drpDistrict" : # means it's class ClientForm.SelectControl
                for item in control.items:
                    dt.append(([label.text for label in item.get_labels()]))
            dt=dt[1:]
            print dt
        print dt
        for j in districtcode:
            if m1>len(dt):
                break
            b1=0
            b2=0
            
            if(j==""):
                
                continue
            else:

                subdistrictcode=[]
                form.set_value([j], name="drpDistrict")
                content=urlopen(form.click())
                forms=ParseResponse(content, backwards_compat=False)
                form=forms[0]
                for item in form.find_control("drpTown").items:
                    subdistrictcode.append(item.name)
                if len(sb)==0:
                    control=form.find_control("drpTown")
                    if control.type == "select" and control.name=="drpTown" : # means it's class ClientForm.SelectControl
                        for item in control.items:
                            sb.append(([label.text for label in item.get_labels()]))
                    sb=sb[1:]  
                    print sb
                
                for l in subdistrictcode:
                    if b1>len(sb):
                        break
                    
                    if(l==""):
                        
                        continue
                    else:
                        form.set_value([l],name="drpTown")
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
                            
                                scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":st[v1][v2],"district":dt[m1][m2],"subdistrict":sb[b1][b2]})
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
                                scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":st[v1][v2],"district":dt[m1][m2],"subdistrict":sb[b1][b2]})
                                s_no+=2
                                row=[]
                            #st=[]
                        serial=s_no-1
                    b1+=1
            sb=[]
            m1+=1
    dt=[]
    v1+=1
st=[]   
import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin
import mechanize
import lxml.html
uri="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Area_Profile/Town_Profile.aspx?cki=6QHuVhlb10a"

response= urlopen(uri)

forms = ParseResponse(response, backwards_compat=False)
print forms
form = forms[0]

print form
statecode=[]
serial=1
st=[]
dt=[]
sb=[]
for item in form.find_control("drpState").items:
    if item.name!='':
        statecode.append(item.name)
control=form.find_control("drpState")
if control.type == "select" and control.name=="drpState": # means it's class ClientForm.SelectControl
    for item in control.items:
        st.append(([label.text for label in item.get_labels()]))
print statecode
st=st[1:]


v1=0
v2=0
print st
for i in statecode:
    if v1>len(st):
        break
    m1=0
    m2=0
    
    
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
        if len(dt)==0:
            control=form.find_control("drpDistrict")
            if control.type == "select" and control.name=="drpDistrict" : # means it's class ClientForm.SelectControl
                for item in control.items:
                    dt.append(([label.text for label in item.get_labels()]))
            dt=dt[1:]
            print dt
        print dt
        for j in districtcode:
            if m1>len(dt):
                break
            b1=0
            b2=0
            
            if(j==""):
                
                continue
            else:

                subdistrictcode=[]
                form.set_value([j], name="drpDistrict")
                content=urlopen(form.click())
                forms=ParseResponse(content, backwards_compat=False)
                form=forms[0]
                for item in form.find_control("drpTown").items:
                    subdistrictcode.append(item.name)
                if len(sb)==0:
                    control=form.find_control("drpTown")
                    if control.type == "select" and control.name=="drpTown" : # means it's class ClientForm.SelectControl
                        for item in control.items:
                            sb.append(([label.text for label in item.get_labels()]))
                    sb=sb[1:]  
                    print sb
                
                for l in subdistrictcode:
                    if b1>len(sb):
                        break
                    
                    if(l==""):
                        
                        continue
                    else:
                        form.set_value([l],name="drpTown")
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
                            
                                scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":st[v1][v2],"district":dt[m1][m2],"subdistrict":sb[b1][b2]})
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
                                scraperwiki.sqlite.save(unique_keys=["S_no"],data={"S_no":s_no,"Column1":row[0],"Column2":row[1],"Column3":row[2],"Column4":row[3],"State":st[v1][v2],"district":dt[m1][m2],"subdistrict":sb[b1][b2]})
                                s_no+=2
                                row=[]
                            #st=[]
                        serial=s_no-1
                    b1+=1
            sb=[]
            m1+=1
    dt=[]
    v1+=1
st=[]   
