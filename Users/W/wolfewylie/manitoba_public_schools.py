import scraperwiki
import re
import time
import codecs
import chardet
from scraperwiki.sqlite import save

columns = [
    'Name', 'Address','City','Postal','Phone'
]

url = "http://web16.gov.mb.ca/school/school?action=school"
basehtml = scraperwiki.scrape(url)
relevantportion = re.search('Adolphe School #1632(.+?)<\/table>', basehtml, re.DOTALL|re.S)
relevantportion = relevantportion.group(1)

def schoolscraper(schoolhtml):
    name = re.search('class="sc_name">(.+?)<', schoolhtml)
    name = name.group(1)
    name = re.sub('&nbsp;', '', name)
    name = re.sub('#\d{4}', '', name)
    address = re.search('class="sc_name">(.+?)<(.+?)<div>(.+?)<br', schoolhtml)
    address = address.group(3)
    address = re.sub('&nbsp;', '', address)
    address = re.sub('#\d{4}', '', address)
    city = re.search('class="sc_name">(.+?)<(.+?)<div>(.+?)<br(.+?)>(.+?)<', schoolhtml)
    city = city.group(5)
    postal = re.search('class="sc_name">(.+?)<(.+?)<div>(.+?)<br(.+?)>(.+?)<(.+?)>(.+?)<br', schoolhtml)
    postal = postal.group(7)
    phone = re.search('Phone:<(.+?)<br', schoolhtml)
    phone = re.sub('&nbsp;', '', phone.group(1))
    phone = re.sub('\/strong>', '', phone)
    row_data = {'Name': name, 'Address': address, 'City': city, 'Postal': postal, 'Phone': phone}
    save([],row_data)
    time.sleep(1)

for every_school in re.finditer('name=\d{4}', relevantportion):
    schoolid = every_school.group(0)
    schoolid = re.sub('name=', '', schoolid)
    schoolurl = "http://web16.gov.mb.ca/school/school?action=singleschool&name=" + schoolid
    schoolhtml = scraperwiki.scrape(schoolurl)
    schoolhtml = schoolhtml.decode('Latin-1').encode('utf-8','replace')
    schoolscraper(schoolhtml)
    





import scraperwiki
import re
import time
import codecs
import chardet
from scraperwiki.sqlite import save

columns = [
    'Name', 'Address','City','Postal','Phone'
]

url = "http://web16.gov.mb.ca/school/school?action=school"
basehtml = scraperwiki.scrape(url)
relevantportion = re.search('Adolphe School #1632(.+?)<\/table>', basehtml, re.DOTALL|re.S)
relevantportion = relevantportion.group(1)

def schoolscraper(schoolhtml):
    name = re.search('class="sc_name">(.+?)<', schoolhtml)
    name = name.group(1)
    name = re.sub('&nbsp;', '', name)
    name = re.sub('#\d{4}', '', name)
    address = re.search('class="sc_name">(.+?)<(.+?)<div>(.+?)<br', schoolhtml)
    address = address.group(3)
    address = re.sub('&nbsp;', '', address)
    address = re.sub('#\d{4}', '', address)
    city = re.search('class="sc_name">(.+?)<(.+?)<div>(.+?)<br(.+?)>(.+?)<', schoolhtml)
    city = city.group(5)
    postal = re.search('class="sc_name">(.+?)<(.+?)<div>(.+?)<br(.+?)>(.+?)<(.+?)>(.+?)<br', schoolhtml)
    postal = postal.group(7)
    phone = re.search('Phone:<(.+?)<br', schoolhtml)
    phone = re.sub('&nbsp;', '', phone.group(1))
    phone = re.sub('\/strong>', '', phone)
    row_data = {'Name': name, 'Address': address, 'City': city, 'Postal': postal, 'Phone': phone}
    save([],row_data)
    time.sleep(1)

for every_school in re.finditer('name=\d{4}', relevantportion):
    schoolid = every_school.group(0)
    schoolid = re.sub('name=', '', schoolid)
    schoolurl = "http://web16.gov.mb.ca/school/school?action=singleschool&name=" + schoolid
    schoolhtml = scraperwiki.scrape(schoolurl)
    schoolhtml = schoolhtml.decode('Latin-1').encode('utf-8','replace')
    schoolscraper(schoolhtml)
    





