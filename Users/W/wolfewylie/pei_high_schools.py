import scraperwiki
import re
import time
import codecs
import chardet
from scraperwiki.sqlite import save

columns = [
    'Name', 'Address','City','Postal','Phone'
]

baseurl = "http://www.edu.pe.ca/finder/schoolfinderresults.asp?searchtype=all"
basehtml = scraperwiki.scrape(baseurl)
basehtml = basehtml.decode('Latin-1').encode('utf-8','replace') 

for every_school in re.finditer('bgcolor=#EAEAEA(.+?)Grades:', basehtml, re.DOTALL|re.S):
    name = re.search('size=\+1(.+?)<\/font>', every_school.group(1), re.DOTALL|re.S)
    name = re.sub('face="Arial, Geneva">', '', name.group(1), re.DOTALL|re.S)
    name = re.sub('<\/?b>', '', name)
    address = re.search('Mailing Address:<\/b><br>(.+?)<', every_school.group(1))
    address = address.group(1)
    city = re.search('Civic Address:<\/b><br>(.+?)<br>(.+?)<', every_school.group(1))
    city = city.group(2)
    postal = "not available"
    if re.search('Mailing Address:(.+?)\D\d\D \d\D\d', every_school.group(1), re.DOTALL|re.S):
        postal = re.search('Mailing Address:(.+?)Civic', every_school.group(1), re.DOTALL|re.S)
        postal = re.search('\D\d\D \d\D\d', postal.group(1))
        postal = postal.group(0)
    phone = re.search('border="0"> \d{3}-\d{4}<', every_school.group(1))
    phone = re.sub('border="0"> ', '', phone.group(0))
    phone = re.sub('<', '', phone)
    phone = "902-" + phone
    row_data = {'Name': name, 'Address': address, 'City': city, 'Postal': postal, 'Phone': phone}
    save([],row_data)


import scraperwiki
import re
import time
import codecs
import chardet
from scraperwiki.sqlite import save

columns = [
    'Name', 'Address','City','Postal','Phone'
]

baseurl = "http://www.edu.pe.ca/finder/schoolfinderresults.asp?searchtype=all"
basehtml = scraperwiki.scrape(baseurl)
basehtml = basehtml.decode('Latin-1').encode('utf-8','replace') 

for every_school in re.finditer('bgcolor=#EAEAEA(.+?)Grades:', basehtml, re.DOTALL|re.S):
    name = re.search('size=\+1(.+?)<\/font>', every_school.group(1), re.DOTALL|re.S)
    name = re.sub('face="Arial, Geneva">', '', name.group(1), re.DOTALL|re.S)
    name = re.sub('<\/?b>', '', name)
    address = re.search('Mailing Address:<\/b><br>(.+?)<', every_school.group(1))
    address = address.group(1)
    city = re.search('Civic Address:<\/b><br>(.+?)<br>(.+?)<', every_school.group(1))
    city = city.group(2)
    postal = "not available"
    if re.search('Mailing Address:(.+?)\D\d\D \d\D\d', every_school.group(1), re.DOTALL|re.S):
        postal = re.search('Mailing Address:(.+?)Civic', every_school.group(1), re.DOTALL|re.S)
        postal = re.search('\D\d\D \d\D\d', postal.group(1))
        postal = postal.group(0)
    phone = re.search('border="0"> \d{3}-\d{4}<', every_school.group(1))
    phone = re.sub('border="0"> ', '', phone.group(0))
    phone = re.sub('<', '', phone)
    phone = "902-" + phone
    row_data = {'Name': name, 'Address': address, 'City': city, 'Postal': postal, 'Phone': phone}
    save([],row_data)


