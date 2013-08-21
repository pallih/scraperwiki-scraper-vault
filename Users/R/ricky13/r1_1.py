import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
page = urllib2.urlopen("http://www.rushu.rush.edu/servlet/Satellite?FirstName=&LastName=b&ClinicalTerms=&LaboratoryTech=&MetaFacultyStaff=&pagename=Rush%2FFaculty%2FSearchForm&Submit=Search")
xmlSoup = BeautifulStoneSoup(page)
#cols = xmlSoup.findAll(attrs={"class" : "NavBGC", "valign":"top"})
#print cols

link = xmlSoup.findAll('a')
print len(link)
limit = len(link)
cnt = 0
for link2 in link:
    if link2.has_key('href'):
        if cnt >= 82:
            #print 'atleast here'
            #print cnt
            if cnt <= limit-17:
                #print type(link2)
                #print link2['href']
                te = link2['href']
                unicode.join(u'\n',map(unicode,te))
                
                #print type(te)
                ve = te + ' avinash '
                #ve[0] = 'T'
                print type(ve)
                print ve
                #var = 'avinash'
                #print type(var)

    cnt = cnt + 1
print cnt
