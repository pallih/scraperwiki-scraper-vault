###############################################################################
#
# East Palo Alto City Department List (based on Mjumbe Poe's scraper for Boston 
# city departments) 
# Fields:
#      cab_name
#      cab_url
#      dept_name
#      dept_url
#      contact_name
#      contact_num
#      contact_email
#
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.ci.east-palo-alto.ca.us/departments.html'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# HTML markup has changed ;)
title = soup.find('td', {'id':'contentpanel'}) 
table = title.find('table')

rows = table.findAll('tr')

last_cab_name = ''
last_cab_url = ''

for row in rows[1:]:
    dept_name = ''
    dept_url = ''
    contact_person = ''
    contact_num = ''
    contact_email = ''
    
    cells = row.findAll('td')
    dept_cell = cells[0]

    dept_name = dept_cell.text
    dept_a = dept_cell.find('a')
    if dept_a:
        dept_url = 'http://www.ci.east-palo-alto.ca.us' + dept_a['href']
    
    # Fixed indentation here
    if dept_name[0:12] == "&nbsp;&nbsp;":
        dept_name = dept_name[12:]
    else:
        last_cab_name = dept_name
        last_cab_url = dept_url
    
    cab_name = last_cab_name
    cab_url = last_cab_url

    contact_person = cells[1].text   
    if contact_person == "&nbsp;":
        contact_person = ''
    contact_num = cells[2].text
    if contact_num == "&nbsp;":
        contact_num = ''
    contact_a = ''
    if len(cells) > 3:
        contact_a = cells[3].find('a')
    if contact_a:
        contact_email = contact_a['href']
        contact_email = contact_email[7:]

    record = { 
       'cab_name' : cab_name,
       'cab_url' : cab_url,
       'dept_name' : dept_name,
       'dept_url' : dept_url,
       'contact_person' : contact_person,
       'contact_num' : contact_num,
       'contact_email' : contact_email
    }

    if dept_url or contact_person or contact_num or contact_email:
        # "datastore" is deprecated use "sqlite" instead
        scraperwiki.sqlite.save(['cab_name','dept_name'],record)
###############################################################################
#
# East Palo Alto City Department List (based on Mjumbe Poe's scraper for Boston 
# city departments) 
# Fields:
#      cab_name
#      cab_url
#      dept_name
#      dept_url
#      contact_name
#      contact_num
#      contact_email
#
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.ci.east-palo-alto.ca.us/departments.html'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# HTML markup has changed ;)
title = soup.find('td', {'id':'contentpanel'}) 
table = title.find('table')

rows = table.findAll('tr')

last_cab_name = ''
last_cab_url = ''

for row in rows[1:]:
    dept_name = ''
    dept_url = ''
    contact_person = ''
    contact_num = ''
    contact_email = ''
    
    cells = row.findAll('td')
    dept_cell = cells[0]

    dept_name = dept_cell.text
    dept_a = dept_cell.find('a')
    if dept_a:
        dept_url = 'http://www.ci.east-palo-alto.ca.us' + dept_a['href']
    
    # Fixed indentation here
    if dept_name[0:12] == "&nbsp;&nbsp;":
        dept_name = dept_name[12:]
    else:
        last_cab_name = dept_name
        last_cab_url = dept_url
    
    cab_name = last_cab_name
    cab_url = last_cab_url

    contact_person = cells[1].text   
    if contact_person == "&nbsp;":
        contact_person = ''
    contact_num = cells[2].text
    if contact_num == "&nbsp;":
        contact_num = ''
    contact_a = ''
    if len(cells) > 3:
        contact_a = cells[3].find('a')
    if contact_a:
        contact_email = contact_a['href']
        contact_email = contact_email[7:]

    record = { 
       'cab_name' : cab_name,
       'cab_url' : cab_url,
       'dept_name' : dept_name,
       'dept_url' : dept_url,
       'contact_person' : contact_person,
       'contact_num' : contact_num,
       'contact_email' : contact_email
    }

    if dept_url or contact_person or contact_num or contact_email:
        # "datastore" is deprecated use "sqlite" instead
        scraperwiki.sqlite.save(['cab_name','dept_name'],record)
