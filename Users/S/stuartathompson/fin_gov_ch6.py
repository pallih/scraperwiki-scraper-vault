import scraperwiki           
import lxml.html
import re
from BeautifulSoup import BeautifulSoup

for x in range(1,21):
    src = 'http://www.fin.gov.on.ca/en/reformcommission/chapters/ch%d.html' % (x)
    html = scraperwiki.scrape(src) 
    soup = BeautifulSoup(html)    
    filter = soup.findAll('p')
    for y in filter:
        z = y.find(re.compile('^strong'))
        if z: 
            a = z.find(text=re.compile('^Recommendation\s*'))
            if a: 
                location = y.getText().split(':')[0]
                text = y.getText().split(':')[1]
                chapter = location.split('-')[0].split(' ')[1]
                recId = location.split('-')[1]
                data = {
                'rec':chapter + '-' + recId,
                'chapter':chapter,
                'recId':recId,
                'data':text
                }
                scraperwiki.sqlite.save(unique_keys=["rec"], data=data)
import scraperwiki           
import lxml.html
import re
from BeautifulSoup import BeautifulSoup

for x in range(1,21):
    src = 'http://www.fin.gov.on.ca/en/reformcommission/chapters/ch%d.html' % (x)
    html = scraperwiki.scrape(src) 
    soup = BeautifulSoup(html)    
    filter = soup.findAll('p')
    for y in filter:
        z = y.find(re.compile('^strong'))
        if z: 
            a = z.find(text=re.compile('^Recommendation\s*'))
            if a: 
                location = y.getText().split(':')[0]
                text = y.getText().split(':')[1]
                chapter = location.split('-')[0].split(' ')[1]
                recId = location.split('-')[1]
                data = {
                'rec':chapter + '-' + recId,
                'chapter':chapter,
                'recId':recId,
                'data':text
                }
                scraperwiki.sqlite.save(unique_keys=["rec"], data=data)
