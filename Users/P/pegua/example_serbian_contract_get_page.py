import scraperwiki


import lxml.html 
import requests 
starturl = 'http://portal.ujn.gov.rs/Izvestaji.aspx' 
s = requests.session() # create a session object 
r1 = s.get(starturl) #get page 1 
html = r1.text 
#process page one 
root = lxml.html.fromstring(html) 
 #pick up the javascript values 
EVENTVALIDATION = root.xpath('//input[@name="__EVENTVALIDATION"]')[0].attrib['value'] 
#find the __EVENTVALIDATION value 
VIEWSTATE = root.xpath('//input[@name="__VIEWSTATE"]')[0].attrib['value'] 
#find the __VIEWSTATE value 
# build a dictionary to post to the site with the values we have  collected. The __EVENTARGUMENT can be changed to fetch another result  page (3,4,5 etc.) 
#in this case, fetching page 16 for gathering EVENTVALIDATION and VIEWSTATE
payload = {'__EVENTTARGET': 'ctl00$ContentPlaceHolder3$grwIzvestaji', '__EVENTARGUMENT': 'Page$16','referer':'http://portal.ujn.gov.rs/Izvestaji.aspx','__EVENTVALIDATION':EVENTVALIDATION,'__VIEWSTATE':VIEWSTATE,'ctl00$txtUser':'','ctl00$txtPass':'','ctl00$ContentPlaceHolder1$txtSearchIzvestaj':'','__VIEWSTATEENCRYPTED':''} 
 # post it 
r16 = s.post(starturl, data=payload) 
 # our response is now page 16 
print r16.text 

#tryng to get page 20 with old values
payload = {'__EVENTTARGET': 'ctl00$ContentPlaceHolder3$grwIzvestaji', '__EVENTARGUMENT': 'Page$20','referer':'http://portal.ujn.gov.rs/Izvestaji.aspx','__EVENTVALIDATION':EVENTVALIDATION,'__VIEWSTATE':VIEWSTATE,'ctl00$txtUser':'','ctl00$txtPass':'','ctl00$ContentPlaceHolder1$txtSearchIzvestaj':'','__VIEWSTATEENCRYPTED':''} 
# post it 
r20_not_working = s.post(starturl, data=payload)
 
#no table in the response
print "Error page:"
print r20_not_working.text

#now try to extract values from page 16, same code as for page1:
html = r16.text 

root = lxml.html.fromstring(html) 

EVENTVALIDATION = root.xpath('//input[@name="__EVENTVALIDATION"]')[0].attrib['value'] 
VIEWSTATE = root.xpath('//input[@name="__VIEWSTATE"]')[0].attrib['value'] 

#now tryng to get page 20 with new javascript values
payload = {'__EVENTTARGET': 'ctl00$ContentPlaceHolder3$grwIzvestaji', '__EVENTARGUMENT': 'Page$20','referer':'http://portal.ujn.gov.rs/Izvestaji.aspx','__EVENTVALIDATION':EVENTVALIDATION,'__VIEWSTATE':VIEWSTATE,'ctl00$txtUser':'','ctl00$txtPass':'','ctl00$ContentPlaceHolder1$txtSearchIzvestaj':'','__VIEWSTATEENCRYPTED':''} 

r20 = s.post(starturl,data=payload)

#proper page 20 now returned
print "Page 20"
print r20.text
