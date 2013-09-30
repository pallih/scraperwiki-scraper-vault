import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
page = urllib2.urlopen("http://www.rushu.rush.edu/servlet/ContentServer?ProfileType=Short&c=RushUnivFaculty&pagename=Rush%2FRushUnivFaculty%2FFaculty_Staff_Profile_Detail_Page&cid=1305552289008")
xmlSoup = BeautifulStoneSoup(page)
table = xmlSoup.findAll(attrs={"class" : "NavBGC", "valign":"top"})
print table
import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
page = urllib2.urlopen("http://www.rushu.rush.edu/servlet/ContentServer?ProfileType=Short&c=RushUnivFaculty&pagename=Rush%2FRushUnivFaculty%2FFaculty_Staff_Profile_Detail_Page&cid=1305552289008")
xmlSoup = BeautifulStoneSoup(page)
table = xmlSoup.findAll(attrs={"class" : "NavBGC", "valign":"top"})
print table
