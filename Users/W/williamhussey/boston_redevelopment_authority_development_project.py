import scraperwiki
from BeautifulSoup import BeautifulSoup
import urllib2

html = urllib2.urlopen("http://bostonredevelopmentauthority.com/DevelopmentProjects/devprojects.asp?action=ViewStatus&StatusID=8")
soup = BeautifulSoup(html)
soupie = soup.prettify()
print soupieimport scraperwiki
from BeautifulSoup import BeautifulSoup
import urllib2

html = urllib2.urlopen("http://bostonredevelopmentauthority.com/DevelopmentProjects/devprojects.asp?action=ViewStatus&StatusID=8")
soup = BeautifulSoup(html)
soupie = soup.prettify()
print soupie