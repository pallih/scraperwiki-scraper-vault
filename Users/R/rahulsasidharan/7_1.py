import scraperwiki
import mechanize 
import re
import lxml.html
import sys
import requests

def get_start():
    url="http://www.indiapost.gov.in/Pin/"
    br = mechanize.Browser()
    response = br.open(url)
    response = br.response()  # this is a copy of response
    headers = response.info()  # currently, this is a mimetools.Message
    headers["Content-type"] = "text/html; charset=utf-8"
    response.set_data(response.get_data().replace("<!---", "<!--"))
    br.set_response(response)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    br = mechanize.Browser()
    response = br.open(url)
    VAR1=response.read()
    response.set_data(response.get_data()[717:])
    br.set_response(response)
    br.select_form(nr = 0)
    br.set_all_readonly(False)
    response = br.submit()
    VAR2 = response.read() # source code after submitting show all
    #print VAR2
    root = lxml.html.fromstring(VAR2)
    return VAR2

def get_all(html,count,dis):
    l=[]
    starturl='http://www.indiapost.gov.in/pin/'
    root=lxml.html.fromstring(html)
    EVENTARGUMENT='Select$'+str(count)
    EVENTVALIDATION = root.xpath('//input[@name="__EVENTVALIDATION"]')[0].attrib['value'] 
    #print EVENTVALIDATION
    #find the __EVENTVALIDATION value 
    VIEWSTATE = root.xpath('//input[@name="__VIEWSTATE"]')[0].attrib['value']
    payload = {'__EVENTTARGET':'gvw_offices','__EVENTARGUMENT':EVENTARGUMENT,'referer':'http://www.indiapost.gov.in/pin/','__EVENTVALIDATION':EVENTVALIDATION,'__VIEWSTATE':VIEWSTATE,'__VIEWSTATEENCRYPTED':''}
    ret=s.post(starturl,data=payload)
    html=ret.text
    root=lxml.html.fromstring(html)
    #print html
    #print "in get all"
    for el in root.cssselect("div table#dvw_detail"):
        #print "in for"
        for el2 in el.cssselect("tr td"):
            #print el2.text_content()  
            var=el2.text_content()
            var1=var.encode('utf-8')
            if var == None or var == " " or var==' ' or var1=='Â ':
                l.append('-')
            else:
                l.append(var1)
    if dis is None or dis is " " or dis ==' ' or dis.encode('utf-8') == 'Â ':
        l.append('-')
    else:
        l.append(dis)
    return l

starturl='http://www.indiapost.gov.in/pin/'
s=requests.session()
r1 = s.get(starturl)
html=get_start()
root = lxml.html.fromstring(html)
l=[]
count=0
br=0
sl_no=1
data=[]
##################################################
for el in root.cssselect("table#gvw_offices tr"):
        for el2 in el.cssselect("tr td"):
            var=el2.text_content()
            #print el2.text_content()
            if count<3:
                data.append(var)
                count+=1
            else:
                data.append(var)
                l=get_all(html,br,data[3])
                #scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Office Name":l[1],"Pincode":l[2],"District":l[3]})
                #print len(l)
                scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Office Name":l[1],"Pincode":l[3],"Status":l[5],"Head Office":l[7],"Location":l[9],"Telephone":l[11],"SPCC":l[13],"Postal Dept Info":l[15],"District":l[16]})
                sl_no+=1
                #print l[1:]
                count=0
                data=[]
                l=[]
                br+=1
                if br==10:
                    break
        if br==10:
            break

i=1
bias=1
while i<6500:#for i in range(4000):
#for i in range(7767):
    if i==0:
        continue
    print i+1
    #pick up the javascript values 
    EVENTVALIDATION = root.xpath('//input[@name="__EVENTVALIDATION"]')[0].attrib['value'] 
    #print EVENTVALIDATION
    #find the __EVENTVALIDATION value 
    VIEWSTATE = root.xpath('//input[@name="__VIEWSTATE"]')[0].attrib['value']
    #print VIEWSTATE
    EVENTARGUMENT='Page$'+str(i+1)
    #payload={}
    payload = {'__EVENTTARGET':'gvw_offices','__EVENTARGUMENT':EVENTARGUMENT,'referer':'http://www.indiapost.gov.in/pin/','__EVENTVALIDATION':EVENTVALIDATION,'__VIEWSTATE':VIEWSTATE,'__VIEWSTATEENCRYPTED':''}
    ret=s.post(starturl,data=payload)
    html=ret.text
    #l=[]
    #l=get_all(html
    root=lxml.html.fromstring(html)
    l=[]
    count=0
    br=0
    data=[]
    if i<6250:
        if i%10==0:
            i+=1
        else:
            i=bias*10
            bias+=1
            print "i is"+str(i)
        print "skipped"
        continue
    else:
        i+=1
    for el in root.cssselect("table#gvw_offices tr"):
        for el2 in el.cssselect("tr td"):
            var=el2.text_content()
            #print el2.text_content()
            if count<3:
                data.append(var)
                count+=1
            else:
                data.append(var)
                l=get_all(html,br,data[3])
                #print len(l)
                #scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Office Name":l[1],"Pincode":l[2],"District":l[3]})
                #if sl_no==15:
                    #print l
                try:
                    scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Office Name":l[1],"Pincode":l[3],"Status":l[5],"Head Office":l[7],"Location":l[9],"Telephone":l[11],"SPCC":l[13],"Postal Dept Info":l[15],"District":l[16]})
                except:
                    scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Office Name":data[1],"Pincode":data[2],"District":data[3]})
                sl_no+=1
                #print l[1:]
                count=0
                data=[]
                l=[]
                br+=1
                if br==10:
                    break
        if br==10:
            break
