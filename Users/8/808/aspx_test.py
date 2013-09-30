import scraperwiki


import lxml.html 
import requests

starturl = 'https://healthri.mylicense.com/Verification/Search.aspx'
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
# build a dictionary to post to the site with the values we have collected. The __EVENTARGUMENT can be changed to fetch another result page (3,4,5 etc.)
payload = {'__EVENTTARGET': 'ctl00$ContentPlaceHolder3$grwIzvestaji', 
'__EVENTARGUMENT':'Page$2','referer':'https://healthri.mylicense.com/Verification/Search.aspx','__EVENTVALIDATION':EVENTVALIDATION,'__VIEWSTATE':VIEWSTATE,'ctl00$txtUser':'','ctl00$txtPass':'','ctl00$ContentPlaceHolder1$txtSearchIzvestaj':'','__VIEWSTATEENCRYPTED':''}
# post it 
r2 = s.post(starturl, data=payload)
# our response is now page 2 
print r2.text 
 
import scraperwiki


import lxml.html 
import requests

starturl = 'https://healthri.mylicense.com/Verification/Search.aspx'
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
# build a dictionary to post to the site with the values we have collected. The __EVENTARGUMENT can be changed to fetch another result page (3,4,5 etc.)
payload = {'__EVENTTARGET': 'ctl00$ContentPlaceHolder3$grwIzvestaji', 
'__EVENTARGUMENT':'Page$2','referer':'https://healthri.mylicense.com/Verification/Search.aspx','__EVENTVALIDATION':EVENTVALIDATION,'__VIEWSTATE':VIEWSTATE,'ctl00$txtUser':'','ctl00$txtPass':'','ctl00$ContentPlaceHolder1$txtSearchIzvestaj':'','__VIEWSTATEENCRYPTED':''}
# post it 
r2 = s.post(starturl, data=payload)
# our response is now page 2 
print r2.text 
 
import scraperwiki


import lxml.html 
import requests

starturl = 'https://healthri.mylicense.com/Verification/Search.aspx'
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
# build a dictionary to post to the site with the values we have collected. The __EVENTARGUMENT can be changed to fetch another result page (3,4,5 etc.)
payload = {'__EVENTTARGET': 'ctl00$ContentPlaceHolder3$grwIzvestaji', 
'__EVENTARGUMENT':'Page$2','referer':'https://healthri.mylicense.com/Verification/Search.aspx','__EVENTVALIDATION':EVENTVALIDATION,'__VIEWSTATE':VIEWSTATE,'ctl00$txtUser':'','ctl00$txtPass':'','ctl00$ContentPlaceHolder1$txtSearchIzvestaj':'','__VIEWSTATEENCRYPTED':''}
# post it 
r2 = s.post(starturl, data=payload)
# our response is now page 2 
print r2.text 
 
import scraperwiki


import lxml.html 
import requests

starturl = 'https://healthri.mylicense.com/Verification/Search.aspx'
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
# build a dictionary to post to the site with the values we have collected. The __EVENTARGUMENT can be changed to fetch another result page (3,4,5 etc.)
payload = {'__EVENTTARGET': 'ctl00$ContentPlaceHolder3$grwIzvestaji', 
'__EVENTARGUMENT':'Page$2','referer':'https://healthri.mylicense.com/Verification/Search.aspx','__EVENTVALIDATION':EVENTVALIDATION,'__VIEWSTATE':VIEWSTATE,'ctl00$txtUser':'','ctl00$txtPass':'','ctl00$ContentPlaceHolder1$txtSearchIzvestaj':'','__VIEWSTATEENCRYPTED':''}
# post it 
r2 = s.post(starturl, data=payload)
# our response is now page 2 
print r2.text 
 
