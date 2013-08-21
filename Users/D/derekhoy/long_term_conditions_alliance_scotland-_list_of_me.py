import re
import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'http://www.ltcas.org.uk/who-we-are/our-members/'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# class needs regex cos can have other classes
groups = soup.findAll('div', attrs={"class" : re.compile('project_box')})

print 'found', len(groups)

for group in groups:
    a = group.h3.a
    if a:
        name = a.text
        url = a['href']
    else:
        name = group.h3.text
        url = ''
    description = group.p.text.replace('&nbsp;', ' ')
    record = { 'name': name, 'url': url, 'description': description, 'locations': '', 'tags': '#ltcas-member' }
    scraperwiki.sqlite.save(["name"], record) 


