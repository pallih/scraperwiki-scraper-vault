import scraperwiki
import BeautifulSoup         
import urllib2
from datetime import datetime

html = urllib2.urlopen("http://jobs.workzoneonline.co.uk/vacancylist.cfm").read()
page = BeautifulSoup.BeautifulSoup(html)
table = page.find('table', {'class': 'datatable'})

id = 0
title = ''
location = ''
salary = ''
hours = ''

for tr in table.findAll('tr', {'class': True}):
    tds = tr.findAll('td')
    if len(tds) == 4:
        id = tds[0].find('a', {'name':True})['name'].replace('v', '')
        title = tds[0].find('a', {'href': True}).string
        location = tds[1].string.strip()
        salary = tds[2].string.strip()
        hours = tds[3].string.strip()

    elif len(tds) == 1:
        description = ' '.join(tds[0].text.split())
   
        link = 'http://jobs.workzoneonline.co.uk/viewvacancies.cfm?ID=' + id
        print id, title, location, salary, hours, description, link

        data = {
            'id' : id,
            'title' : title,
            'location' : location,
            'salary' : salary,
            'hours' : hours,
            'description' : description,
            'date_scraped' : datetime.now(),
            'link' : link
        }
        if len(scraperwiki.sqlite.select("NULL FROM swdata WHERE id=" + id)) > 0:
            updatesql = "UPDATE swdata SET title = '" + title + "', location = '" + location + "', salary = '" + salary + "', hours = '" + hours + "', description = '" + description + "', link = '" + link + "' WHERE id=" + id
            scraperwiki.sqlite.execute(updatesql)
            scraperwiki.sqlite.commit()
        else:
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)

    


import scraperwiki
import BeautifulSoup         
import urllib2
from datetime import datetime

html = urllib2.urlopen("http://jobs.workzoneonline.co.uk/vacancylist.cfm").read()
page = BeautifulSoup.BeautifulSoup(html)
table = page.find('table', {'class': 'datatable'})

id = 0
title = ''
location = ''
salary = ''
hours = ''

for tr in table.findAll('tr', {'class': True}):
    tds = tr.findAll('td')
    if len(tds) == 4:
        id = tds[0].find('a', {'name':True})['name'].replace('v', '')
        title = tds[0].find('a', {'href': True}).string
        location = tds[1].string.strip()
        salary = tds[2].string.strip()
        hours = tds[3].string.strip()

    elif len(tds) == 1:
        description = ' '.join(tds[0].text.split())
   
        link = 'http://jobs.workzoneonline.co.uk/viewvacancies.cfm?ID=' + id
        print id, title, location, salary, hours, description, link

        data = {
            'id' : id,
            'title' : title,
            'location' : location,
            'salary' : salary,
            'hours' : hours,
            'description' : description,
            'date_scraped' : datetime.now(),
            'link' : link
        }
        if len(scraperwiki.sqlite.select("NULL FROM swdata WHERE id=" + id)) > 0:
            updatesql = "UPDATE swdata SET title = '" + title + "', location = '" + location + "', salary = '" + salary + "', hours = '" + hours + "', description = '" + description + "', link = '" + link + "' WHERE id=" + id
            scraperwiki.sqlite.execute(updatesql)
            scraperwiki.sqlite.commit()
        else:
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)

    


