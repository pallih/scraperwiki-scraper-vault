import scraperwiki,re
from BeautifulSoup import BeautifulSoup

# English version
url = 'http://gamla.menntagatt.is/default.aspx?pageid=381'

#Icelandic version is here (the same scraper code should work for that):
# url = 'http://menntagatt.is/default.aspx?pageid=270'



html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)
soup.prettify()
table = soup.find('table', {'id' : '_ctl0__ctl0_dgTestDegree' })

print "**** STARTING ****"

tr = table.findAll('tr')[1:]

for td in tr:
    data = {}
    id = td.findNext('td')
    data['id'] = id.text
    profession = id.findNext('td')
    data['profession'] = profession.text
    ministry = profession.findNext('td')
    data['ministry'] = ministry.text
    group = ministry.findNext('td')
    data['group'] = group.text
    directive = group.findNext('td')
    data['directive'] = directive.text

    print data
    scraperwiki.datastore.save(["id"], data)

print " **** ALL DONE ****"
