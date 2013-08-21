import scraperwiki
import requests
import lxml.html

url = 'http://uhaul.com'

s = requests.session()

start = s.get(url)
cookies = start_html.cookies
print cookies
root = lxml.html.fromstring(start.text)

#post values:
VIEWSTATE = root.xpath('//input[@name="__VIEWSTATE"]')[0].attrib['value']
EVENTVALIDATION = root.xpath('//input[@name="__EVENTVALIDATION"]')[0].attrib['value']
EVENTTARGET = ''
EVENTARGUMENT = ''
departure = 'New York, NY'
destination = 'Dallas, TX'
date = '11/26/2012'
submit = 'Get rates'
zip = 'Zip/postal code'
js = '1'
search_text = 'Search'
wtDCSURI='/'
wtDCSQRY=''
wtTZ='0'
wtBH='9'
wtUL='en-US'
wtCD='24'
wtSR='1280x800'
wtJO='Yes'
wtTI='U-Haul: Your moving and storage resource'
wtJS='Yes'
wtJV='1.5'



payload = {'__EVENTTARGET':EVENTTARGET,
    '__EVENTARGUMENT':EVENTARGUMENT,
    '__VIEWSTATE':VIEWSTATE,
    '__EVENTVALIDATION':EVENTVALIDATION,
    'ctl00$ContentPlaceHolder1$ctrlSharedEquipmentSearch1$dpMoveDate':date,
    'ctl00$ContentPlaceHolder1$ctrlSharedEquipmentSearch1$tbPickupLocation':departure,
    'ctl00$ContentPlaceHolder1$ctrlSharedEquipmentSearch1$tbDropOffLocation':destination,
    'ctl00$ContentPlaceHolder1$ctrlSharedEquipmentSearch1$btnSubmit':submit,
    'ctl00$ContentPlaceHolder1$txtZipCode':zip,
    'js':js,
    'ctl00$SearchBox1$SearchText=Search':search_text,
    'wtDCSURI': wtDCSURI,
    'wtDCSQRY':wtDCSQRY,
    'wtTZ':wtTZ,
    'wtBH':wtBH,
    'wtUL':wtUL,
    'wtCD':wtCD,
    'wtSR':wtSR,
    'wtJO':wtJO,
    'wtTI':wtTI,
    'wtJS':wtJS,
    'wtJV':wtJV}


headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1',
            'Referer':'http://www.uhaul.com/',
            'Origin':'http://www.uhaul.com',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Host':'www.uhaul.com'}

response = s.post('http://uhaul.com/',data=payload,headers=headers)

print response.text
print response.headers
print response.cookies
print response.request.headers
print response.history
print response.history[0].cookies
print response.history[1].cookies



