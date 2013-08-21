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

starturl='http://www.indiapost.gov.in/pin/'
s=requests.session()
r1 = s.get(starturl)
html=get_start()
root = lxml.html.fromstring(html)
l=[]
count=0
br=0
sl_no=1
for el in root.cssselect("table#gvw_offices tr"):
    for el2 in el.cssselect("tr td"):
        var=el2.text_content()
        #print el2.text_content()
        if count<3:
            l.append(var)
            count+=1
        else:
            l.append(var)
            scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Office Name":l[1],"Pincode":l[2],"District":l[3]})
            sl_no+=1
            #print l[1:]
            count=0
            l=[]
            br+=1
            if br==10:
                break
    if br==10:
        break
i=1
bias=1
#for i in range(15537):
#for i in range(7767):
while i<8540:
    if i==0:
        i+=1
        continue
    print i
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
    root=lxml.html.fromstring(html)
    l=[]
    count=0
    br=0
    if i<4540:
        #if i==21:
        #    i+=5
        #else:
         #   i+=5
        if i%10 is 0:
            i+=1
        else:
            i=bias*10
            print "i is"+str(i)
            bias+=1
        #i+=i%10
        print "skipped"
        continue
    else:
        i+=1
    for el in root.cssselect("table#gvw_offices tr"):
        for el2 in el.cssselect("tr td"):
            var=el2.text_content()
            #print el2.text_content()
            if count<3:
                l.append(var)
                count+=1
            else:
                l.append(var)
                scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Office Name":l[1],"Pincode":l[2],"District":l[3]})
                sl_no+=1
                #print l[1:]
                count=0
                l=[]
                br+=1
                if br==10:
                    break
        if br==10:
            break