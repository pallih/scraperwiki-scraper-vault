#import scraperwiki
from bs4 import BeautifulSoup

import urllib2

result = urllib2.urlopen("http://mgaleg.maryland.gov/webmga/frmmain.aspx?pid=legisrpage&tab=subject6")
soup  = BeautifulSoup(result.read())
#soup = fromstring(doc)

# http://www.crummy.com/software/BeautifulSoup/bs4/doc/


print ("2",soup.title)
print "xxxxxx111xxxxxxxxx"
print soup.title.name
print "xxxxxxx222xxxxxxxx"
print soup.title.string

print "xxxxxx333xxxxxxxxx"
print soup.title.parent.name

print "xxxxxx444xxxxxxxxx"
print soup.p

print "xxxxx555xxxxxxxxxx"
print soup.p['class']

print "xxxxxxx666xxxxxxxx"
print soup.a

print "xxxxx777xxxxxxxxxx"
print soup.find_all('a')

print "xxxxxxx888xxxxxxxx"
soup.find(id="link3")

print "xxxxxxxx999xxxxxxx"
for link in soup.find_all('a'):
    print(link.get('href'))




#import scraperwiki
from bs4 import BeautifulSoup

import urllib2

result = urllib2.urlopen("http://mgaleg.maryland.gov/webmga/frmmain.aspx?pid=legisrpage&tab=subject6")
soup  = BeautifulSoup(result.read())
#soup = fromstring(doc)

# http://www.crummy.com/software/BeautifulSoup/bs4/doc/


print ("2",soup.title)
print "xxxxxx111xxxxxxxxx"
print soup.title.name
print "xxxxxxx222xxxxxxxx"
print soup.title.string

print "xxxxxx333xxxxxxxxx"
print soup.title.parent.name

print "xxxxxx444xxxxxxxxx"
print soup.p

print "xxxxx555xxxxxxxxxx"
print soup.p['class']

print "xxxxxxx666xxxxxxxx"
print soup.a

print "xxxxx777xxxxxxxxxx"
print soup.find_all('a')

print "xxxxxxx888xxxxxxxx"
soup.find(id="link3")

print "xxxxxxxx999xxxxxxx"
for link in soup.find_all('a'):
    print(link.get('href'))




