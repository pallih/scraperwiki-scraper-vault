import urllib2
from BeautifulSoup import BeautifulSoup

page = urllib2.urlopen("http://www.devour.com")
soup = BeautifulSoup(page)

titleTag = soup.html.head.title

print titleTagimport urllib2
from BeautifulSoup import BeautifulSoup

page = urllib2.urlopen("http://www.devour.com")
soup = BeautifulSoup(page)

titleTag = soup.html.head.title

print titleTag