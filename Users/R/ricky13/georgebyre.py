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
    print 'stringwa'
    tabstr =  unicode.join(u'\n',map(unicode,tab)).strip()
    print tabstr
    print 'donewa'
    
    em = tabstr[tabstr.find('a href='):]
    em2 = em[:em.find('">')]
    em3 = em2[em2.find('mailto:')+7:]
    print em3

    patFinderlocat = re.compile('<div class="gu_profileitem gu_profileitem_location"><h4 class="gu_profileitemlabel">Location</h4><div class="gu_profileitemcontent">(.*)</div></div>')
    loc = re.findall(patFinderlocat,page)
    print 'lubelow'
    locat = loc[0][:loc[0].find('</div>')]
    re.sub('[\s+]','\s',locat)
    print locat
    #print phu

    #<div class="gu_profileitem gu_profileitem_location"><h4 class="gu_profileitemlabel">Location</h4><div class="gu_profileitemcontent">LL S183                                            LCC                 #                              </div>
    
    #padh = Soup.findAll(name = 'div',attrs = {"class":"gu_profileitem gu_profileitem_education"})
    #print 'padh below'
    #print padh.li
    
    #patFinderedu = re.compile('<div class="gu_profileitem gu_profileitem_education"><h4 class="gu_profileitemlabel">Education</h4><div class="gu_profileitemcontent"><ul>(.*)</li>')
    #patFinderedu = re.compile('<div class="gu_profileitem gu_profileitem_education"><h4 class="gu_profileitemlabel">Education</h4><div class="gu_profileitemcontent"><ul>.*\s*^.*\s*^</ul>',re.M)
    #educ = re.findall(patFinderedu,page)
    #print 'EDUbelow'
    #print educ

    

# Get a list of all the <tr>s in the table, skip the header row
    rows = Soup.findAll('li')[29:]

    print len(rows)
    #print rows

    print 'Education Below'
    for link2 in rows:
        if not link2.has_key('href'):
            if not link2.a:
                if not 'speak' in link2
                    print link2
                    #print link2.parent
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
    print 'stringwa'
    tabstr =  unicode.join(u'\n',map(unicode,tab)).strip()
    print tabstr
    print 'donewa'
    
    em = tabstr[tabstr.find('a href='):]
    em2 = em[:em.find('">')]
    em3 = em2[em2.find('mailto:')+7:]
    print em3

    patFinderlocat = re.compile('<div class="gu_profileitem gu_profileitem_location"><h4 class="gu_profileitemlabel">Location</h4><div class="gu_profileitemcontent">(.*)</div></div>')
    loc = re.findall(patFinderlocat,page)
    print 'lubelow'
    locat = loc[0][:loc[0].find('</div>')]
    re.sub('[\s+]','\s',locat)
    print locat
    #print phu

    #<div class="gu_profileitem gu_profileitem_location"><h4 class="gu_profileitemlabel">Location</h4><div class="gu_profileitemcontent">LL S183                                            LCC                 #                              </div>
    
    #padh = Soup.findAll(name = 'div',attrs = {"class":"gu_profileitem gu_profileitem_education"})
    #print 'padh below'
    #print padh.li
    
    #patFinderedu = re.compile('<div class="gu_profileitem gu_profileitem_education"><h4 class="gu_profileitemlabel">Education</h4><div class="gu_profileitemcontent"><ul>(.*)</li>')
    #patFinderedu = re.compile('<div class="gu_profileitem gu_profileitem_education"><h4 class="gu_profileitemlabel">Education</h4><div class="gu_profileitemcontent"><ul>.*\s*^.*\s*^</ul>',re.M)
    #educ = re.findall(patFinderedu,page)
    #print 'EDUbelow'
    #print educ

    

# Get a list of all the <tr>s in the table, skip the header row
    rows = Soup.findAll('li')[29:]

    print len(rows)
    #print rows

    print 'Education Below'
    for link2 in rows:
        if not link2.has_key('href'):
            if not link2.a:
                if not 'speak' in link2
                    print link2
                    #print link2.parent
