import scraperwiki
import requests
import lxml.html

#set the user agent, x-requested-with and referer header
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5','referer':'https://efun.toronto.ca/torontofun/Activities/ActivitiesAdvSearch.asp','X-Requested-With':'XMLHttpRequest'}

s = requests.session()

#pick up a cookie
s.get('https://efun.toronto.ca/torontofun/Activities/ActivitiesAdvSearch.asp',verify=False, headers=headers) #verify false to avoid cert error

#options from drop down form to return all
payload = {'chkSearchAllCatogery':'on', 'AllCatogerySubcatogerySelectedHintText':'All categories/subcategories ', 'KeywordSearch':'', 'SuperDropDownFrom':'dd-mm-yyyy', 'SuperDropDownFrom':'0', 'SuperDropDownFrom':'0', 'SuperDropDownFrom':'0', 'DateRangeFrom':'', 'SuperDropDownTo':'dd-mm-yyyy', 'SuperDropDownTo':'0', 'SuperDropDownTo':'0', 'SuperDropDownTo':'0', 'DateRangeTo':'', 'chkWeekDay8':'9', 'chkKeywordRegistrationAvailable':'', 'ajax':'true'}

#create the url with the 'SCheck' cookie value
url = 'https://efun.toronto.ca/torontofun/Activities/ActivitiesAdvSearch.asp?AdvSearch=true&SDT=41030.9777546296&SCheck='+s.cookies['SCheck']
#post!
r = s.post(url,verify=False,headers=headers, data=payload)

#result!
print r.text
print r.headers


#what follows is a work in progress to paginate and extract results 

# https://efun.toronto.ca/torontofun/Activities/ActivitiesDetails.asp?AdvPage=true&ProcessWait=N&aid=1557&ComplexId=0&sEcho=2&iColumns=8&sColumns=&iDisplayStart=10&iDisplayLength=10&ajax=true

root = lxml.html.fromstring(r.text)
tds = root.xpath('//td[@width="100%"]')
for td in tds:
    print td[0].attrib['id'], td[0][0][0].text_content().strip() #attribute id for url and title
    print td[0][1].text_content().strip() 

import scraperwiki
import requests
import lxml.html

#set the user agent, x-requested-with and referer header
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5','referer':'https://efun.toronto.ca/torontofun/Activities/ActivitiesAdvSearch.asp','X-Requested-With':'XMLHttpRequest'}

s = requests.session()

#pick up a cookie
s.get('https://efun.toronto.ca/torontofun/Activities/ActivitiesAdvSearch.asp',verify=False, headers=headers) #verify false to avoid cert error

#options from drop down form to return all
payload = {'chkSearchAllCatogery':'on', 'AllCatogerySubcatogerySelectedHintText':'All categories/subcategories ', 'KeywordSearch':'', 'SuperDropDownFrom':'dd-mm-yyyy', 'SuperDropDownFrom':'0', 'SuperDropDownFrom':'0', 'SuperDropDownFrom':'0', 'DateRangeFrom':'', 'SuperDropDownTo':'dd-mm-yyyy', 'SuperDropDownTo':'0', 'SuperDropDownTo':'0', 'SuperDropDownTo':'0', 'DateRangeTo':'', 'chkWeekDay8':'9', 'chkKeywordRegistrationAvailable':'', 'ajax':'true'}

#create the url with the 'SCheck' cookie value
url = 'https://efun.toronto.ca/torontofun/Activities/ActivitiesAdvSearch.asp?AdvSearch=true&SDT=41030.9777546296&SCheck='+s.cookies['SCheck']
#post!
r = s.post(url,verify=False,headers=headers, data=payload)

#result!
print r.text
print r.headers


#what follows is a work in progress to paginate and extract results 

# https://efun.toronto.ca/torontofun/Activities/ActivitiesDetails.asp?AdvPage=true&ProcessWait=N&aid=1557&ComplexId=0&sEcho=2&iColumns=8&sColumns=&iDisplayStart=10&iDisplayLength=10&ajax=true

root = lxml.html.fromstring(r.text)
tds = root.xpath('//td[@width="100%"]')
for td in tds:
    print td[0].attrib['id'], td[0][0][0].text_content().strip() #attribute id for url and title
    print td[0][1].text_content().strip() 

