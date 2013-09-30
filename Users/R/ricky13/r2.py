import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
page = urllib2.urlopen("http://www.rushu.rush.edu/servlet/Satellite?ProfileType=Short&c=RushUnivFaculty&cid=1200925139723&pagename=Rush%2FRushUnivFaculty%2FFaculty_Staff_Profile_Detail_Page")
xmlSoup = BeautifulStoneSoup(page)
cols = xmlSoup.findAll(attrs={"class" : "NavBGC", "valign":"top"})
#print cols
lines=[]
for td in cols:
    text=td.nextSibling.renderContents().strip(' ')
    text.replace
    lines.append(text)
print lines
import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
page = urllib2.urlopen("http://www.rushu.rush.edu/servlet/Satellite?ProfileType=Short&c=RushUnivFaculty&cid=1200925139723&pagename=Rush%2FRushUnivFaculty%2FFaculty_Staff_Profile_Detail_Page")
xmlSoup = BeautifulStoneSoup(page)
cols = xmlSoup.findAll(attrs={"class" : "NavBGC", "valign":"top"})
#print cols
lines=[]
for td in cols:
    text=td.nextSibling.renderContents().strip(' ')
    text.replace
    lines.append(text)
print lines
