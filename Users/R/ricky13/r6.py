import scraperwiki
import re
import urllib2
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

scraperwiki.sqlite.execute("CREATE TABLE rush8 ('Last Name' string,'First Name' string,'Middle Initial' string,'Degree & Certifications' string,'Endowed Professorship' string,'Rank & Title' string,'Department' string,'College' string,'Office Location' string, 'Laboratory Location' string, 'Phone' string,'Fax' string,'Email' string)")
scraperwiki.sqlite.commit()
#scraperwiki.sqlite.execute("insert into rush8 values (?,?,?,?,?,?,?,?,?,?,?,?,?)", ('Last Name','First Name' ,'Middle Initial' ,'Degree & Certifications','Endowed Professorship','Rank & Title' ,'Department' ,'College' ,'Office Location' , 'Laboratory Location' , 'Phone' ,'Fax' ,'Email' ))

scraperwiki.sqlite.commit()

first = 'http://www.rushu.rush.edu/servlet/Satellite?FirstName=&LastName='
second = '&ClinicalTerms=&LaboratoryTech=&MetaFacultyStaff=&pagename=Rush%2FFaculty%2FSearchForm&Submit=Search'
letters = ['b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
#letters = ['a']
for ch in letters:
    print ch
    url = first + ch + second
    page = urlopen(url).read()
    xmlSoup = BeautifulStoneSoup(page)
    link = xmlSoup.findAll('a')
    #print len(link)
    limit = len(link)
    cnt = 0
    for link2 in link:
        if link2.has_key('href'):
            if cnt >= 82:
                article = 'http://www.rushu.rush.edu'
                if cnt <= limit-18:
                    now = link2['href']
                    #atricle = article.append(now)
                    article = article + now
                    ppage = urllib2.urlopen(article)
                    xmlSoup2 = BeautifulStoneSoup(ppage)
                    cols = xmlSoup2.findAll(attrs={"class" : "NavBGC", "valign":"top"})
                    #print cols
                    lines=[]
                    for td in cols:
                        text=td.nextSibling.renderContents().strip(' ')
                        lines.append(text)
                    nb = len(cols)
                    st = 0
                    #print 'nd'
                    #print nd
                    while st < nb:
                        lines[st]=lines[st].replace(',',';')
                        lines[st]=lines[st].replace('<br>','')
                        lines[st]=lines[st].replace('</br>','')
                        lines[st] = re.sub('[\t\r\n-"]','',lines[st])
                    #    print st
                        st = st+1                   
                    
                    #print lines
                    #print lines[1]                 
                    scraperwiki.sqlite.execute("insert into  rush7 values (?,?,?,?,?,?,?,?,?,?,?,?,?)", (lines[0],lines[1],lines[2],lines[3],lines[4],lines[5],lines[6],lines[7],lines[8],lines[9],lines[10],lines[11],lines[12]))
                    scraperwiki.sqlite.commit()
        cnt = cnt + 1
print ch







