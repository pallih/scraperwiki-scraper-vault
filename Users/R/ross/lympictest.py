import urllib2
import lxml.html

request = urllib2.Request('http://www.london2012.com/athletes/initial=z/index,page=1.htmx')
request.add_header('User-Agent', 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.57 Safari/537.1')
request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')


data = urllib2.urlopen(request).read()
page = lxml.html.fromstring(data)
athletes = page.cssselect('ul.athletesList')

for athlete in athletes:
    passimport urllib2
import lxml.html

request = urllib2.Request('http://www.london2012.com/athletes/initial=z/index,page=1.htmx')
request.add_header('User-Agent', 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.57 Safari/537.1')
request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')


data = urllib2.urlopen(request).read()
page = lxml.html.fromstring(data)
athletes = page.cssselect('ul.athletesList')

for athlete in athletes:
    pass