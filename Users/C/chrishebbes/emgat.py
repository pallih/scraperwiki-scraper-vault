import scraperwiki
import mechanize
import re
from BeautifulSoup import BeautifulSoup
import urllib2

br = mechanize.Browser()
br.add_password("http://www.emgat.org.uk/mailer/mailster.php", "emgat", "3mgat")
br.open("http://www.emgat.org.uk/mailer/mailster.php")
response = br.reload()      
html = response.read()
#invalid_tags = ['div', 'html', 'head']
soup = BeautifulSoup(html)
#for tag in invalid_tags: 
#    for match in soup.findAll(tag):
#        match.replaceWithChildren()
print soup

for row in soup('table')[0].tbody('tr'):
    tds = row('td')
    record={'received':tds[0].string,
    'from':tds[1].text,
    'subject':tds[2].string,
    'html':tds[3].text}
    scraperwiki.sqlite.save(["received"], record)




import scraperwiki
import mechanize
import re
from BeautifulSoup import BeautifulSoup
import urllib2

br = mechanize.Browser()
br.add_password("http://www.emgat.org.uk/mailer/mailster.php", "emgat", "3mgat")
br.open("http://www.emgat.org.uk/mailer/mailster.php")
response = br.reload()      
html = response.read()
#invalid_tags = ['div', 'html', 'head']
soup = BeautifulSoup(html)
#for tag in invalid_tags: 
#    for match in soup.findAll(tag):
#        match.replaceWithChildren()
print soup

for row in soup('table')[0].tbody('tr'):
    tds = row('td')
    record={'received':tds[0].string,
    'from':tds[1].text,
    'subject':tds[2].string,
    'html':tds[3].text}
    scraperwiki.sqlite.save(["received"], record)




