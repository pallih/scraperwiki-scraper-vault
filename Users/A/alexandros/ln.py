import scraperwiki
import urllib2, urlparse
import lxml.etree, lxml.html
import re
import time
import datetime
import mechanize 
from StringIO import StringIO

loginurl = "http://www.solipsys.co.uk/LumpNetLogin.html"

br = mechanize.Browser()
response = br.open(loginurl)

br.select_form(nr=0)

br['LoginUsername'] = 'Alexandros'
br['LoginPassword'] = 'rudolf'

response = br.submit()
html = response.read()

page = lxml.html.parse(StringIO(html)).getroot()

posts = page.find('body/form').findall('table')[1].find('tr/td/table').findall('tr')

for i in range(0, len(posts), 4):
    print lxml.html.tostring(posts[i])
    item = {}
    item['uri'] = posts[i].find('td/a').attrib['href']
    item['title'] = posts[i].find('td/a').text
    infstr = posts[i+1].findall('td')[1].text
    item['user'] = infstr[14:infstr.find("Value")-3]
    item['value'] = infstr[infstr.find("Value:")+6:infstr.find("Age:")-2]
    item['age'] = infstr[infstr.find("Age:")+4:infstr.find("Score:")-2]
    item['score'] = infstr[infstr.find("Score:")+6:]
    scraperwiki.sqlite.save(unique_keys=['uri'], data=item)
    print infstr
    print item['score'], item['value']
import scraperwiki
import urllib2, urlparse
import lxml.etree, lxml.html
import re
import time
import datetime
import mechanize 
from StringIO import StringIO

loginurl = "http://www.solipsys.co.uk/LumpNetLogin.html"

br = mechanize.Browser()
response = br.open(loginurl)

br.select_form(nr=0)

br['LoginUsername'] = 'Alexandros'
br['LoginPassword'] = 'rudolf'

response = br.submit()
html = response.read()

page = lxml.html.parse(StringIO(html)).getroot()

posts = page.find('body/form').findall('table')[1].find('tr/td/table').findall('tr')

for i in range(0, len(posts), 4):
    print lxml.html.tostring(posts[i])
    item = {}
    item['uri'] = posts[i].find('td/a').attrib['href']
    item['title'] = posts[i].find('td/a').text
    infstr = posts[i+1].findall('td')[1].text
    item['user'] = infstr[14:infstr.find("Value")-3]
    item['value'] = infstr[infstr.find("Value:")+6:infstr.find("Age:")-2]
    item['age'] = infstr[infstr.find("Age:")+4:infstr.find("Score:")-2]
    item['score'] = infstr[infstr.find("Score:")+6:]
    scraperwiki.sqlite.save(unique_keys=['uri'], data=item)
    print infstr
    print item['score'], item['value']
