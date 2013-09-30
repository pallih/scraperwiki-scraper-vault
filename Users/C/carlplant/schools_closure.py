import scraperwiki
import lxml.html
import re
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.signal1.co.uk/schools.inc.htm')
#print html
root = lxml.html.fromstring(html)

#soup = BeautifulSoup(html)
#print soup
#items = soup.findAll('tr',"closed") 
#print items
rows = root.cssselect("table#schTable tr.closed") 
print rows

for row in rows:
    schools = row.cssselect("td.name")
    print schools
    if schools:
        school = schools[0].text_content()
        print school
        scraperwiki.sqlite.save(unique_keys=[], data={'School' : school})
    import scraperwiki
import lxml.html
import re
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.signal1.co.uk/schools.inc.htm')
#print html
root = lxml.html.fromstring(html)

#soup = BeautifulSoup(html)
#print soup
#items = soup.findAll('tr',"closed") 
#print items
rows = root.cssselect("table#schTable tr.closed") 
print rows

for row in rows:
    schools = row.cssselect("td.name")
    print schools
    if schools:
        school = schools[0].text_content()
        print school
        scraperwiki.sqlite.save(unique_keys=[], data={'School' : school})
    