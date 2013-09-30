from mechanize import Browser
from bs4 import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
import json 

from datetime import date, timedelta, datetime

mech = Browser()

#set date to recognise date of scraping

datum = date.today()

url = 'http://developer.android.com/about/dashboards/index.html'

page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

last_paragraph = soup.find_all('p', style='clear:both')[-1]
script_tag = last_paragraph.next_sibling.next_sibling
script_text = script_tag.text

lines = script_text.split('\n')
data_text = ''
for line in lines:

    if 'SCREEN_DATA' in line: break 
    data_text = data_text + line 

data_text = data_text.replace('var VERSION_DATA =', '')
# delete semicolon at the end 
data_text = data_text[:-1]

data = json.loads(data_text)
data = data[0]
print data#['data']

# TODO insert data into sqlite table

#something has to happen here
#data = (version, codename, api, percentage, datum)
#scraperwiki.sqlite.save(unique_keys=["api","datum"], data={"api":api, "perc":perc, "name":name, "datum":datum})



from mechanize import Browser
from bs4 import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
import json 

from datetime import date, timedelta, datetime

mech = Browser()

#set date to recognise date of scraping

datum = date.today()

url = 'http://developer.android.com/about/dashboards/index.html'

page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

last_paragraph = soup.find_all('p', style='clear:both')[-1]
script_tag = last_paragraph.next_sibling.next_sibling
script_text = script_tag.text

lines = script_text.split('\n')
data_text = ''
for line in lines:

    if 'SCREEN_DATA' in line: break 
    data_text = data_text + line 

data_text = data_text.replace('var VERSION_DATA =', '')
# delete semicolon at the end 
data_text = data_text[:-1]

data = json.loads(data_text)
data = data[0]
print data#['data']

# TODO insert data into sqlite table

#something has to happen here
#data = (version, codename, api, percentage, datum)
#scraperwiki.sqlite.save(unique_keys=["api","datum"], data={"api":api, "perc":perc, "name":name, "datum":datum})



