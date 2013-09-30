import urllib2, re, scraperwiki, htmlentitydefs
from BeautifulSoup import BeautifulSoup
def convertentity(m):
       if m.group(1)=='#':
           try:
               return chr(int(m.group(2)))
           except ValueError:
               return '&#%s;' % m.group(2)
           try:
               return htmlentitydefs.entitydefs[m.group(2)]
           except KeyError:
               return '&%s;' % m.group(2)
def converthtml(s):
    return re.sub(r'&(#?)(.+?);',convertentity,s)
itemNum = '03131455'
url = "http://www1.mscdirect.com/cgi/NNSRIT2?PMAKA=" + itemNum
soup = BeautifulSoup(scraperwiki.scrape(url))
spec = soup.find('table' ,cellpadding="3")
count = 0
data={}
data['itemNumber'] = itemNum 
for i in spec('tr'):
    this = i.next.next.next.renderContents()
    for  j in i('td'):
        if count == 1 :
            data[this] = converthtml(j.next)
        else:
            count = 0    
        count += 1
scraperwiki.datastore.save(['itemNumber'], data)import urllib2, re, scraperwiki, htmlentitydefs
from BeautifulSoup import BeautifulSoup
def convertentity(m):
       if m.group(1)=='#':
           try:
               return chr(int(m.group(2)))
           except ValueError:
               return '&#%s;' % m.group(2)
           try:
               return htmlentitydefs.entitydefs[m.group(2)]
           except KeyError:
               return '&%s;' % m.group(2)
def converthtml(s):
    return re.sub(r'&(#?)(.+?);',convertentity,s)
itemNum = '03131455'
url = "http://www1.mscdirect.com/cgi/NNSRIT2?PMAKA=" + itemNum
soup = BeautifulSoup(scraperwiki.scrape(url))
spec = soup.find('table' ,cellpadding="3")
count = 0
data={}
data['itemNumber'] = itemNum 
for i in spec('tr'):
    this = i.next.next.next.renderContents()
    for  j in i('td'):
        if count == 1 :
            data[this] = converthtml(j.next)
        else:
            count = 0    
        count += 1
scraperwiki.datastore.save(['itemNumber'], data)