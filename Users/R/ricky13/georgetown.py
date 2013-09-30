import scraperwiki

import re
import urllib2
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
                        


#scraperwiki.sqlite.execute("CREATE TABLE george ('Full name' string,'Title' string,'Department' string,'Phone' string,'Email' string,'Location' string,'Education' string)")
scraperwiki.sqlite.commit()


letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
for ch in letters:
    print ch
    add = 'http://explore.georgetown.edu/faculty/index.cfm?Action=List&Letter='+ch.upper()+'&AffiliationID=210'
    home = urlopen(add).read()
    xmlSoup = BeautifulStoneSoup(home)
    first = 'http://explore.georgetown.edu/people/'
    second = '/?Action=View&'
    link = xmlSoup.findAll('a')
    #print type(link)
    #print len(link)
    limit = len(link)
    cnt = 0
    for link2 in link:
        if cnt >= 27 :
            rs = str(link2)
            #print 'rs = %s' %(rs)
            id = rs[rs.find('NetID=')+6:]
            id2 = id[:id.find('&')]
            #print 'id = %s' %(id2)
            url = first+id2+second
            #print 'url = %s' %(url)

            fn = ''
            ti = ''
            de = ''
            ph = ''
            ema = ''
            locat = ''
            edustring = ''
            page = urlopen(url).read()
            Soup = BeautifulStoneSoup(page)
            fn = Soup.head.title.renderContents()
            tab = Soup.findAll(name = 'div', attrs = {"class":"gu_profileitemcontent"})
            #print tab
            tabstr =  unicode.join(u'\n',map(unicode,tab)).strip()
            #print tabstr
            if len(tab) > 0:
                ti = tab[0].renderContents()
                ti = ti.replace('<br>','')
                ti =ti.replace('</br>','')
                ti =ti.replace(',','$')
                ti = ti.replace('\n','')
            
            if len(tab) > 1:
                de = tab[1].renderContents()
                de = de.replace('<br>',' ')
                de =de.replace('</br>','')
                de =de.replace(',','')
                de = de.replace('\n','')
            
            patFinderphone = re.compile('<div class="gu_profileitem gu_profileitem_phone"><h4 class="gu_profileitemlabel">Phone</h4><div class="gu_profileitemcontent">(.*)</div></div>')
            phu = re.findall(patFinderphone,page)
            if phu:
                ph = phu[0][:phu[0].find('</div>')]

            if len(tabstr) > 0 :
                em = tabstr[tabstr.find('a href='):]

                if len(em) > 7:
                    em2 = em[:em.find('">')]
                    ema = em2[em2.find('mailto:')+7:]
                    ema = ema.replace('\n','')
            
            patFinderlocat = re.compile('<div class="gu_profileitem gu_profileitem_location"><h4 class="gu_profileitemlabel">Location</h4><div class="gu_profileitemcontent">(.*)</div></div>')
            loc = re.findall(patFinderlocat,page)
            if loc:
                locat = loc[0][:loc[0].find('</div>')]
                re.sub('[\s+]','\s',locat)
                locat = locat.replace('\n','')
                locat = locat.replace('    ',' ');
                locat = locat.replace('   ',' ');
                locat = locat.replace('  ',' ');
                

            rows = Soup.findAll('li')[28:]
            edustring = ''
            for link2 in rows:
                if not link2.has_key('href'):
                    if not link2.a:
                        educon = link2.renderContents().strip()
                        if not 'speak' in educon:
                            #print educon
                            edustring = edustring + ';' + educon

            edustring = edustring.replace(',','$')
            edustring = edustring[1:]
            edustring = edustring.replace('\n','')
            


            #print 'First Name = %s' %(fn)
            #print 'title = %s' %(ti)
            #print 'Department = %s' %(de)
            #print 'Phone = %s' %(ph)
            #print 'Email = %s' %(ema)
            #print 'Location = %s' %(locat)
            #print 'Education = %s' %(edustring)
            scraperwiki.sqlite.execute("insert into george values (?,?,?,?,?,?,?)", (fn,ti,de,ph,ema,locat,edustring))
            scraperwiki.sqlite.commit()

            
            
        cnt = cnt+1
    #print 'cnt = %d' %(cnt)
print 'Completed %c' %(ch)




import scraperwiki

import re
import urllib2
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
                        


#scraperwiki.sqlite.execute("CREATE TABLE george ('Full name' string,'Title' string,'Department' string,'Phone' string,'Email' string,'Location' string,'Education' string)")
scraperwiki.sqlite.commit()


letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
for ch in letters:
    print ch
    add = 'http://explore.georgetown.edu/faculty/index.cfm?Action=List&Letter='+ch.upper()+'&AffiliationID=210'
    home = urlopen(add).read()
    xmlSoup = BeautifulStoneSoup(home)
    first = 'http://explore.georgetown.edu/people/'
    second = '/?Action=View&'
    link = xmlSoup.findAll('a')
    #print type(link)
    #print len(link)
    limit = len(link)
    cnt = 0
    for link2 in link:
        if cnt >= 27 :
            rs = str(link2)
            #print 'rs = %s' %(rs)
            id = rs[rs.find('NetID=')+6:]
            id2 = id[:id.find('&')]
            #print 'id = %s' %(id2)
            url = first+id2+second
            #print 'url = %s' %(url)

            fn = ''
            ti = ''
            de = ''
            ph = ''
            ema = ''
            locat = ''
            edustring = ''
            page = urlopen(url).read()
            Soup = BeautifulStoneSoup(page)
            fn = Soup.head.title.renderContents()
            tab = Soup.findAll(name = 'div', attrs = {"class":"gu_profileitemcontent"})
            #print tab
            tabstr =  unicode.join(u'\n',map(unicode,tab)).strip()
            #print tabstr
            if len(tab) > 0:
                ti = tab[0].renderContents()
                ti = ti.replace('<br>','')
                ti =ti.replace('</br>','')
                ti =ti.replace(',','$')
                ti = ti.replace('\n','')
            
            if len(tab) > 1:
                de = tab[1].renderContents()
                de = de.replace('<br>',' ')
                de =de.replace('</br>','')
                de =de.replace(',','')
                de = de.replace('\n','')
            
            patFinderphone = re.compile('<div class="gu_profileitem gu_profileitem_phone"><h4 class="gu_profileitemlabel">Phone</h4><div class="gu_profileitemcontent">(.*)</div></div>')
            phu = re.findall(patFinderphone,page)
            if phu:
                ph = phu[0][:phu[0].find('</div>')]

            if len(tabstr) > 0 :
                em = tabstr[tabstr.find('a href='):]

                if len(em) > 7:
                    em2 = em[:em.find('">')]
                    ema = em2[em2.find('mailto:')+7:]
                    ema = ema.replace('\n','')
            
            patFinderlocat = re.compile('<div class="gu_profileitem gu_profileitem_location"><h4 class="gu_profileitemlabel">Location</h4><div class="gu_profileitemcontent">(.*)</div></div>')
            loc = re.findall(patFinderlocat,page)
            if loc:
                locat = loc[0][:loc[0].find('</div>')]
                re.sub('[\s+]','\s',locat)
                locat = locat.replace('\n','')
                locat = locat.replace('    ',' ');
                locat = locat.replace('   ',' ');
                locat = locat.replace('  ',' ');
                

            rows = Soup.findAll('li')[28:]
            edustring = ''
            for link2 in rows:
                if not link2.has_key('href'):
                    if not link2.a:
                        educon = link2.renderContents().strip()
                        if not 'speak' in educon:
                            #print educon
                            edustring = edustring + ';' + educon

            edustring = edustring.replace(',','$')
            edustring = edustring[1:]
            edustring = edustring.replace('\n','')
            


            #print 'First Name = %s' %(fn)
            #print 'title = %s' %(ti)
            #print 'Department = %s' %(de)
            #print 'Phone = %s' %(ph)
            #print 'Email = %s' %(ema)
            #print 'Location = %s' %(locat)
            #print 'Education = %s' %(edustring)
            scraperwiki.sqlite.execute("insert into george values (?,?,?,?,?,?,?)", (fn,ti,de,ph,ema,locat,edustring))
            scraperwiki.sqlite.commit()

            
            
        cnt = cnt+1
    #print 'cnt = %d' %(cnt)
print 'Completed %c' %(ch)




