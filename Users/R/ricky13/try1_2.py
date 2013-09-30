#! /usr/bin/python
import scraperwiki
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import re
                            
scraperwiki.sqlite.execute("CREATE TABLE dukeurest ('Full name' string,'Title' string,'Department' string,'Division' string,'Address' string,'Phone' string,'Fax' string,'Email' string)")
scraperwiki.sqlite.commit()
scraperwiki.sqlite.execute("insert into  dukeurest values (?,?,?,?,?,?,?,?)", ('Full name','tity','Department','Division','Address','Phone','Fax','Email'))
scraperwiki.sqlite.commit()


first = 'https://faculty.duhs.duke.edu/faculty/advanced-search?pLastName='
second = '&pDepartment=ANY&pKeywordOperator=all&pKeyword=&pKeyword=&pKeyword=&pIncludeMeSH=true&pButton=Search'
letters = ['o','p','q','r','s','t','u','v','w','x','y','z']
fis = 'Full name'+','+'Titles'+','+'Department'+','+'Division'+','+'Address'+','+'Phone'+','+'Fax'+','+'Email'+'\n'
print(fis)
for ch in letters:
    url = first + ch + second
    articlepage = urlopen(url).read()
    patFinderTitle = re.compile('<a href=.*>(.*)</a>')
    patFinderTitle2 = re.compile('<a href=.*<td>(.*)</td>')
    patFinderLink = re.compile('<a href="(.*)">.*</a>')
    findPatTitle = re.findall(patFinderTitle,articlepage)
    findPatTitle2 = re.findall(patFinderTitle2,articlepage)                            
    findPatLink = re.findall(patFinderLink,articlepage)
    num = len(findPatLink)
    listIterator = []
    listIterator[:] = range(5,num)

    for i in listIterator:
        
        app = 'https://faculty.duhs.duke.edu/faculty/'        
        newpage=app+findPatLink[i]
        articlepage = urlopen(newpage).read()
        patFinderFullname = re.compile('<span class="facultyName">(.*)</span>')
        patFinderPTitle = re.compile('<span class="primaryTitle">(.*)</span>')
        patFinderSTitle = re.compile('<span class="secondaryTitle">(.*)</span>')
        patFinderDepartment = re.compile('<span class="label">Department:</span>\s+&nbsp;&nbsp;\s+</td><td>(.*)</td>')
        patFinderDivision = re.compile('<span class="label">Division:</span>\s+&nbsp;&nbsp;\s+</td><td>(.*)</td>')
        patFinderEmail = re.compile('<span class="label">email:</span></td><td><a href=".*">(.*)</a></td>')
        patFinderAddress = re.compile('<td><span class="label">Address:</span></td>.*?</td>')
        patFinderPhone = re.compile('<td><span class="label">Phone:</span>\s*</td><td>\s*^\s*.*\s*^\s*.*<br>',re.M)
        patFinderFax = re.compile('<td><span class="label">FAX:</span>\s*</td><td>\s*^\s*.*\s*^\s*.*</td>',re.M)

        fullname = re.findall(patFinderFullname,articlepage)
        ptitle = re.findall(patFinderPTitle,articlepage)
        stitle = re.findall(patFinderSTitle,articlepage)
        division = re.findall(patFinderDivision,articlepage)
        department = re.findall(patFinderDepartment,articlepage)
        address = re.findall(patFinderAddress,articlepage)
        phone = re.findall(patFinderPhone,articlepage)
        fax = re.findall(patFinderFax,articlepage)
        email = re.findall(patFinderEmail,articlepage)

        if not fullname:
            fn  = 'Null'
        else :
            fn = fullname[0]
            fn = fn.replace(',', ' ')
                
        if not ptitle:
            pt = ''
        else :
            pt = ptitle[0]
            pt = pt.replace('--<i>', ' ')
            pt = pt.replace('--<i>', ' ')
            pt = pt.replace('</i>', '')
            pt = pt.replace(',', ' ')
            pt = pt.replace(',', ' ')
            re.sub("\s\s+" , " ", pt)
            pt = pt.replace('   ',' ')
            
        if not stitle:
            st = ''
        else :
            st = stitle[0]
            st = st.replace(',', ' ')
            re.sub("\s\s+" , " ", st)
            st = st.replace('   ',' ')
        if not department:
            dp = 'Null'
        else :
            dp = department[0]
            dp = dp.replace(',', ' ')
            re.sub("\s\s+" , " ", dp)
            dp = dp.replace('   ',' ')

        if not division:
            di = 'Null'
        else :
            di = division[0]
            di = di.replace(',', ' ')
            re.sub("\s\s+" , " ", di)
            di = di.replace('   ',' ')


        if address:
            ad = address[0]
            ad = ad.replace('<td><span class="label">Address:</span></td>', '')
            ad = ad.replace('&nbsp;', '')
            ad = ad.replace('<br>', ' ')
            re.sub("\s\s+" , " ", ad)
            ad = ad.replace('</td>', '')
            ad = ad.replace('<td>', '')
            ad = ad.replace('&amp;', '')
            ad = ad.replace(',', ' ')
            ad = ad.replace('   ',' ')
            
            
        else :
            ad = 'Null'

        if phone:
            ph =  phone[0]
            ph = phone[0]
            ph = ph.replace('<td><span class="label">Phone:</span></td>', '')
            ph = ph.replace('&nbsp;', '')
            ph = ph.replace('<br>', '')
            ph = ph.replace('</td>', '')
            re.sub("\s\s+" , " ", ph)
            ph = ph.replace('<td>', '')
            ph = ph.replace('\n', ' ')
            ph = ph.replace('   ', ' ')
            ph = ph.replace(' ', '')
            ph = ph.replace('&amp;', '')
        else :
            ph = 'Null'

        if fax:
            fa = fax[0]
            fa = fa.replace('<td><span class="label">FAX:</span></td>', '')
            fa = fa.replace('&nbsp;', '')
            fa = fa.replace('<br>', '')
            fa = fa.replace('</td>', '')
            fa = fa.replace('<td>', '')
            fa = fa.replace('\n', ' ')
            re.sub("\s\s+" , "", fa)
            fa = fa.replace('   ', '')
        else :
            fa = 'Null'

        if email:
            em = email[0]
        else :
            em = 'Null'
        
        if not ptitle:
            if not stitle :
                tity = 'Null'
        else :
            if not stitle:
                tity = ptitle[0]
            else :
                tity = ptitle[0]+';'+stitle[0]
        
        scraperwiki.sqlite.execute("insert into dukeurest values (?,?,?,?,?,?,?,?)", (fn,tity,dp,di,ad,ph,fa,em))
        scraperwiki.sqlite.commit()
        #line_new = fn+','+pt+';'+st+','+dp+','+di+','+ad+','+ph+','+fa+','+em+'\n'
        #re.sub("\s\s+" , " ", line_new)
        #print(line_new)
#! /usr/bin/python
import scraperwiki
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import re
                            
scraperwiki.sqlite.execute("CREATE TABLE dukeurest ('Full name' string,'Title' string,'Department' string,'Division' string,'Address' string,'Phone' string,'Fax' string,'Email' string)")
scraperwiki.sqlite.commit()
scraperwiki.sqlite.execute("insert into  dukeurest values (?,?,?,?,?,?,?,?)", ('Full name','tity','Department','Division','Address','Phone','Fax','Email'))
scraperwiki.sqlite.commit()


first = 'https://faculty.duhs.duke.edu/faculty/advanced-search?pLastName='
second = '&pDepartment=ANY&pKeywordOperator=all&pKeyword=&pKeyword=&pKeyword=&pIncludeMeSH=true&pButton=Search'
letters = ['o','p','q','r','s','t','u','v','w','x','y','z']
fis = 'Full name'+','+'Titles'+','+'Department'+','+'Division'+','+'Address'+','+'Phone'+','+'Fax'+','+'Email'+'\n'
print(fis)
for ch in letters:
    url = first + ch + second
    articlepage = urlopen(url).read()
    patFinderTitle = re.compile('<a href=.*>(.*)</a>')
    patFinderTitle2 = re.compile('<a href=.*<td>(.*)</td>')
    patFinderLink = re.compile('<a href="(.*)">.*</a>')
    findPatTitle = re.findall(patFinderTitle,articlepage)
    findPatTitle2 = re.findall(patFinderTitle2,articlepage)                            
    findPatLink = re.findall(patFinderLink,articlepage)
    num = len(findPatLink)
    listIterator = []
    listIterator[:] = range(5,num)

    for i in listIterator:
        
        app = 'https://faculty.duhs.duke.edu/faculty/'        
        newpage=app+findPatLink[i]
        articlepage = urlopen(newpage).read()
        patFinderFullname = re.compile('<span class="facultyName">(.*)</span>')
        patFinderPTitle = re.compile('<span class="primaryTitle">(.*)</span>')
        patFinderSTitle = re.compile('<span class="secondaryTitle">(.*)</span>')
        patFinderDepartment = re.compile('<span class="label">Department:</span>\s+&nbsp;&nbsp;\s+</td><td>(.*)</td>')
        patFinderDivision = re.compile('<span class="label">Division:</span>\s+&nbsp;&nbsp;\s+</td><td>(.*)</td>')
        patFinderEmail = re.compile('<span class="label">email:</span></td><td><a href=".*">(.*)</a></td>')
        patFinderAddress = re.compile('<td><span class="label">Address:</span></td>.*?</td>')
        patFinderPhone = re.compile('<td><span class="label">Phone:</span>\s*</td><td>\s*^\s*.*\s*^\s*.*<br>',re.M)
        patFinderFax = re.compile('<td><span class="label">FAX:</span>\s*</td><td>\s*^\s*.*\s*^\s*.*</td>',re.M)

        fullname = re.findall(patFinderFullname,articlepage)
        ptitle = re.findall(patFinderPTitle,articlepage)
        stitle = re.findall(patFinderSTitle,articlepage)
        division = re.findall(patFinderDivision,articlepage)
        department = re.findall(patFinderDepartment,articlepage)
        address = re.findall(patFinderAddress,articlepage)
        phone = re.findall(patFinderPhone,articlepage)
        fax = re.findall(patFinderFax,articlepage)
        email = re.findall(patFinderEmail,articlepage)

        if not fullname:
            fn  = 'Null'
        else :
            fn = fullname[0]
            fn = fn.replace(',', ' ')
                
        if not ptitle:
            pt = ''
        else :
            pt = ptitle[0]
            pt = pt.replace('--<i>', ' ')
            pt = pt.replace('--<i>', ' ')
            pt = pt.replace('</i>', '')
            pt = pt.replace(',', ' ')
            pt = pt.replace(',', ' ')
            re.sub("\s\s+" , " ", pt)
            pt = pt.replace('   ',' ')
            
        if not stitle:
            st = ''
        else :
            st = stitle[0]
            st = st.replace(',', ' ')
            re.sub("\s\s+" , " ", st)
            st = st.replace('   ',' ')
        if not department:
            dp = 'Null'
        else :
            dp = department[0]
            dp = dp.replace(',', ' ')
            re.sub("\s\s+" , " ", dp)
            dp = dp.replace('   ',' ')

        if not division:
            di = 'Null'
        else :
            di = division[0]
            di = di.replace(',', ' ')
            re.sub("\s\s+" , " ", di)
            di = di.replace('   ',' ')


        if address:
            ad = address[0]
            ad = ad.replace('<td><span class="label">Address:</span></td>', '')
            ad = ad.replace('&nbsp;', '')
            ad = ad.replace('<br>', ' ')
            re.sub("\s\s+" , " ", ad)
            ad = ad.replace('</td>', '')
            ad = ad.replace('<td>', '')
            ad = ad.replace('&amp;', '')
            ad = ad.replace(',', ' ')
            ad = ad.replace('   ',' ')
            
            
        else :
            ad = 'Null'

        if phone:
            ph =  phone[0]
            ph = phone[0]
            ph = ph.replace('<td><span class="label">Phone:</span></td>', '')
            ph = ph.replace('&nbsp;', '')
            ph = ph.replace('<br>', '')
            ph = ph.replace('</td>', '')
            re.sub("\s\s+" , " ", ph)
            ph = ph.replace('<td>', '')
            ph = ph.replace('\n', ' ')
            ph = ph.replace('   ', ' ')
            ph = ph.replace(' ', '')
            ph = ph.replace('&amp;', '')
        else :
            ph = 'Null'

        if fax:
            fa = fax[0]
            fa = fa.replace('<td><span class="label">FAX:</span></td>', '')
            fa = fa.replace('&nbsp;', '')
            fa = fa.replace('<br>', '')
            fa = fa.replace('</td>', '')
            fa = fa.replace('<td>', '')
            fa = fa.replace('\n', ' ')
            re.sub("\s\s+" , "", fa)
            fa = fa.replace('   ', '')
        else :
            fa = 'Null'

        if email:
            em = email[0]
        else :
            em = 'Null'
        
        if not ptitle:
            if not stitle :
                tity = 'Null'
        else :
            if not stitle:
                tity = ptitle[0]
            else :
                tity = ptitle[0]+';'+stitle[0]
        
        scraperwiki.sqlite.execute("insert into dukeurest values (?,?,?,?,?,?,?,?)", (fn,tity,dp,di,ad,ph,fa,em))
        scraperwiki.sqlite.commit()
        #line_new = fn+','+pt+';'+st+','+dp+','+di+','+ad+','+ph+','+fa+','+em+'\n'
        #re.sub("\s\s+" , " ", line_new)
        #print(line_new)
