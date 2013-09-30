import scraperwiki
import re
import urllib2
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
xy = 1;

if xy == 1:
    #url = 'http://explore.georgetown.edu/people/clg34/?Action=View&'
    #url = 'http://explore.georgetown.edu/people/ag523/?Action=View&'
    url = "http://explore.georgetown.edu/people/rg26/?Action=View&"
    page = urlopen(url).read()
    Soup = BeautifulStoneSoup(page)
    fn = Soup.head.title.renderContents()
    print 'First Name = %s' %(fn)
    tab = Soup.findAll(name = 'div', attrs = {"class":"gu_profileitemcontent"})
    print tab
    
    phone = ""
    tabp = Soup.findAll(name = 'div', attrs = { "class":"gu_profileitem gu_profileitem_phone"})[0]
    print tabp
    #general = Soup.findAll(name = 'div', attrs = {"class":"gu_profilesection", "id":"gu_profilesectiongeneral"})
    #print general

    #ti = tab[0].renderContents()
    #ti = ti.replace('<br>',' ')
    #ti =ti.replace('</br>','')
    #print 'title = %s' %(ti)

    #de = tab[1].renderContents()
    #de = de.replace('<br>',' ')
    #de =de.replace('</br>','')
    #print 'Department = %s' %(de)
    print len(tab)
    #print ti
    #print se
    i = 1
    for t in tab:
        #print i
        #print t.renderContents()
        i = i+1





import scraperwiki
import re
import urllib2
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
xy = 1;

if xy == 1:
    #url = 'http://explore.georgetown.edu/people/clg34/?Action=View&'
    #url = 'http://explore.georgetown.edu/people/ag523/?Action=View&'
    url = "http://explore.georgetown.edu/people/rg26/?Action=View&"
    page = urlopen(url).read()
    Soup = BeautifulStoneSoup(page)
    fn = Soup.head.title.renderContents()
    print 'First Name = %s' %(fn)
    tab = Soup.findAll(name = 'div', attrs = {"class":"gu_profileitemcontent"})
    print tab
    
    phone = ""
    tabp = Soup.findAll(name = 'div', attrs = { "class":"gu_profileitem gu_profileitem_phone"})[0]
    print tabp
    #general = Soup.findAll(name = 'div', attrs = {"class":"gu_profilesection", "id":"gu_profilesectiongeneral"})
    #print general

    #ti = tab[0].renderContents()
    #ti = ti.replace('<br>',' ')
    #ti =ti.replace('</br>','')
    #print 'title = %s' %(ti)

    #de = tab[1].renderContents()
    #de = de.replace('<br>',' ')
    #de =de.replace('</br>','')
    #print 'Department = %s' %(de)
    print len(tab)
    #print ti
    #print se
    i = 1
    for t in tab:
        #print i
        #print t.renderContents()
        i = i+1





