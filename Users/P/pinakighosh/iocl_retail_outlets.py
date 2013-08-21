import scraperwiki
import lxml.html
url="http://www.petrolpump.co.in/oil-companies/iocl/retail-outlets/Andhra-Pradesh.htm"
html=scraperwiki.scrape(url)
root=lxml.html.fromstring(html)
#print html
test="""                 The Petrol Pump Management Software  The Supermarket Management Software  Mobile Phone Shop Management Software  Medical Store Management Software"""
states=[]
for el in root.cssselect("p a"):
    #print el.text_content()
    states.append(el.text_content().replace(' ','-'))
states=states[3:]
states_url=[]
states_url.append("http://www.petrolpump.co.in/oil-companies/iocl/retail-outlets/Andaman-Nicobar.htm")
test="""                 The Petrol Pump Management Software  The Supermarket Management Software  Mobile Phone Shop Management Software  Medical Store Management Software"""
sl_no=0
for i in states:
    #print i
    states_url.append("http://www.petrolpump.co.in/oil-companies/iocl/retail-outlets/"+i+".htm")
for i in states_url:
    html=scraperwiki.scrape(i)
    root=lxml.html.fromstring(html)
    #print html    
    for el in root.cssselect("table td"):
        text=el.text_content()
        l=text.split(':')
        #print l
        if l[0]=="\r\nOutlet Name":
            l1=text.split('\r\n')
            l1=l1[1:]
            row=[]
            data=dict()
            flag=False
            for i in l1:
                row.append(i.split(':'))
            for i in row:
                if flag:
                    data['State']=(' '.join(i))
                    break
                if i[0]=="Outlet Name":
                    data['Outlet Name']=i[1]
                if i[0]=="Contact Person":
                    data['Contact Person']=i[1]
                if i[0]=="Tel":
                    data['Tel']=i[1]
                if i[0]=="Dist":
                    data['Dist']=i[1]
                    flag=True
            
                    #print i[1]
                #print row
            #print data
            if 'Tel' not in data:
                data['Tel']=0
            if 'State' not in data:
                data['State']=0
            if 'Outlet Name' not in data:
                data['Outlet Name']=0
            if 'Contact Person' not in data:
                data['Contact Person']=0
            if 'Dist' not in data:
                data['Dist']=0
            scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"state":data['State'],"district":data['Dist'],"Outlet_name":data['Outlet Name'],"Telephone":data['Tel'],"Contact_person":data['Contact Person']})
            sl_no+=1
        if text==test:
            break


