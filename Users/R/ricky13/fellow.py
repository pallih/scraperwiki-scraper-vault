import scraperwiki
import re
import urllib2
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
                       
scraperwiki.sqlite.execute("CREATE TABLE completedrexel ('Full name' string,'Degree' string,'Title' string, 'Department' string, 'Speciality' string,'Education' string,'Fellowship' string,'Residency' string, 'Internship' string,'Primary Practice name' string, 'Primary Practice address' string,'Phone' Phone' sring,Cnt' int)")
scraperwiki.sqlite.commit()
add = 'http://www.drexelmed.edu/Home/AboutOurFaculty/FacultyListing.aspx'
home = urlopen(add).read()
xmlSoup = BeautifulStoneSoup(home)
link = xmlSoup.findAll('a')
print len(link)
print link[101]
print link[677]
cnt = 0
list = [104,220]
prefix = 'http://www.drexelmed.edu'
if cnt >= 0:
    for link2 in link:
        #print cnt
        if cnt >= 101 :
            if cnt <= 677:
                rs = str(link2)
                #print 'rs = %s' %(rs)
                id = rs[rs.find('href="')+6:]
                id2 = id[:id.find('">')]
                #print 'url is %s' %(id2)
                url = prefix + id2
                page = urlopen(url).read()
                soup = BeautifulSoup(page)
                line = soup.findAll('h2')[1].renderContents()
                 if ',' in line:
                    fn = line[:line.find(',')]
                else :
                    fn  = line
                fn = fn.replace('"','')
                #print fn
                ftemp = str(fn)
                deg = '@'
                if  ',' in line:
                    deg = line[line.find(',')+1:]
                #print 'deg = %s' %(deg)
                title = Soup.findAll('h3')[0].renderContents()
                title = title.replace('"','')
                title = title.replace(',','$')
                
                #print title
                #<span>Department:</span>(.*)</li>
            
                patFinderdep = re.compile('<span>Department:</span>(.*)</li>')
                pdep = re.findall(patFinderdep,page)
                depart = '@'
                if pdep:
                    depart = pdep[0]
                else :
                    patFinderpra = re.compile('<span>Practice:</span>(.*)\s*<li><span>S')
                    ppra = re.findall(patFinderpra,page)
                    if ppra:
                        depart = ppra[0]
                if '<' in depart:
                    depart = depart[:depart.find('<')]
                depart = depart.replace(',','$')
                depart = depart.replace('"','')
                #print 'department is %s ' %(depart)
            
                spcl = '@'
                patFindersp = re.compile('<span>Specialty:</span>(.*)</li>')
                psp = re.findall(patFindersp,page)
                if psp:
                    spcl = psp[0]
            
                sp2 = str(spcl)
                if '<' in sp2:
                    sp2 = sp2[:sp2.find('<')]
                    spcl = sp2
                #print 'speciality is %s ' %(spcl)
            
            
                educat = '@'
                patFinderedu = re.compile('<span>Education:</span>(.*)</li>')
                ped = re.findall(patFinderedu,page)
                if ped:
                    educat = ped[0]
            
                ed2 = str(spcl)
                if '<' in ed2:
                    ed2 = ed2[:ed2.find('<')]
                    educat = ed2
                educat = educat.replace('&nbsp;','')
                educat = educat.replace('&nbsp','')
                educat = educat.replace('&nbsp','')
                educat = educat.replace(',','$')
                educat = educat.replace('<strong>','')
                educat = educat.replace('</strong>','')
                
                #print 'Education is %s ' %(educat)
            
            
                tabla = Soup.findAll('table')[:-1]
                limla = len(tabla)
                #print tabla[limla-1]
                st = str(tabla[limla-1])
                #print st
                prim2 = '@'
                prim1 = st[st.find('<b>')+3:]
                prim2 = prim1[:prim1.find('</b>')]
                prim2 = prim2.replace(',','$')
                #print 'pp is %s' %(prim2)

                pa2 = '@'
                pa1 = prim1[prim1.find('</b>')+8:]
                pa2 = pa1[:pa1.find('Ph')]
                pa2 = pa2.replace('<br>','')
                pa2 = pa2.replace('</br>','')
                pa2 = pa2.replace(',','$');
                #print 'p add is %s' %( pa2)
            
                ph2 = '@'
                ph1 = prim1[prim1.find('Phone')+7:]
                ph2 = ph1[:12]
                #headings = ['Internship', 'Residency', 'Fellowship','Practice Locations']
                fellow = '@'
                resi = '@'
                intern = '@'
                if cnt not in list:
                    x = soup.find('span', text='Fellowship')      
                    #print url  
                    if x:
                        if x.parent:
                            span_id = x.parent['id']
                            table_id = span_id.replace('dnnTITLE_lblTitle', 'Display_HtmlHolder')
                            fellow = soup.find('td', attrs={"id": table_id}).renderContents()                    
                    else:
                        fellow = '@'
    
                    x = soup.find('span', text='Residency')        
                    if x:
                        span_id = x.parent['id']
                        table_id = span_id.replace('dnnTITLE_lblTitle', 'Display_HtmlHolder')
                        resi = soup.find('td', attrs={"id": table_id}).renderContents()                    
                    else:
                        resi = '@'
                    
                    x = soup.find('span', text='Internship')        
                    if x:
                        span_id = x.parent['id']
                        table_id = span_id.replace('dnnTITLE_lblTitle', 'Display_HtmlHolder')
                        intern = soup.find('td', attrs={"id": table_id}).renderContents()                    
                    else:
                        intern = '@'

                fellow = fellow.replace('<ul>','')
                fellow = fellow.replace('<li>','')
                fellow = fellow.replace('</ul>','')
                fellow = fellow.replace('</li>','')
                resi = resi.replace('<ul>','')
                resi = resi.replace('<li>','')  
                resi = resi.replace('</ul>','')
                resi = resi.replace('</li>','')  
                intern = intern.replace('<ul>','')
                intern = intern.replace('<li>','')
                intern = intern.replace('</ul>','')
                intern = intern.replace('</li>','')

                scraperwiki.sqlite.execute("insert into rik1 values (?,?,?,?,?,?,?,?,?,?,?,?,?)", (fn,deg,title,depart,spcl,educat,fellow,resi,intern,prim2,pa2,ph2,cnt))
                scraperwiki.sqlite.commit()
                print 'fellow = %s  resi = %s,intern = %s' %(fellow,resi,intern )
        cnt = cnt+1
        print cnt
            import scraperwiki
import re
import urllib2
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
                       
scraperwiki.sqlite.execute("CREATE TABLE completedrexel ('Full name' string,'Degree' string,'Title' string, 'Department' string, 'Speciality' string,'Education' string,'Fellowship' string,'Residency' string, 'Internship' string,'Primary Practice name' string, 'Primary Practice address' string,'Phone' Phone' sring,Cnt' int)")
scraperwiki.sqlite.commit()
add = 'http://www.drexelmed.edu/Home/AboutOurFaculty/FacultyListing.aspx'
home = urlopen(add).read()
xmlSoup = BeautifulStoneSoup(home)
link = xmlSoup.findAll('a')
print len(link)
print link[101]
print link[677]
cnt = 0
list = [104,220]
prefix = 'http://www.drexelmed.edu'
if cnt >= 0:
    for link2 in link:
        #print cnt
        if cnt >= 101 :
            if cnt <= 677:
                rs = str(link2)
                #print 'rs = %s' %(rs)
                id = rs[rs.find('href="')+6:]
                id2 = id[:id.find('">')]
                #print 'url is %s' %(id2)
                url = prefix + id2
                page = urlopen(url).read()
                soup = BeautifulSoup(page)
                line = soup.findAll('h2')[1].renderContents()
                 if ',' in line:
                    fn = line[:line.find(',')]
                else :
                    fn  = line
                fn = fn.replace('"','')
                #print fn
                ftemp = str(fn)
                deg = '@'
                if  ',' in line:
                    deg = line[line.find(',')+1:]
                #print 'deg = %s' %(deg)
                title = Soup.findAll('h3')[0].renderContents()
                title = title.replace('"','')
                title = title.replace(',','$')
                
                #print title
                #<span>Department:</span>(.*)</li>
            
                patFinderdep = re.compile('<span>Department:</span>(.*)</li>')
                pdep = re.findall(patFinderdep,page)
                depart = '@'
                if pdep:
                    depart = pdep[0]
                else :
                    patFinderpra = re.compile('<span>Practice:</span>(.*)\s*<li><span>S')
                    ppra = re.findall(patFinderpra,page)
                    if ppra:
                        depart = ppra[0]
                if '<' in depart:
                    depart = depart[:depart.find('<')]
                depart = depart.replace(',','$')
                depart = depart.replace('"','')
                #print 'department is %s ' %(depart)
            
                spcl = '@'
                patFindersp = re.compile('<span>Specialty:</span>(.*)</li>')
                psp = re.findall(patFindersp,page)
                if psp:
                    spcl = psp[0]
            
                sp2 = str(spcl)
                if '<' in sp2:
                    sp2 = sp2[:sp2.find('<')]
                    spcl = sp2
                #print 'speciality is %s ' %(spcl)
            
            
                educat = '@'
                patFinderedu = re.compile('<span>Education:</span>(.*)</li>')
                ped = re.findall(patFinderedu,page)
                if ped:
                    educat = ped[0]
            
                ed2 = str(spcl)
                if '<' in ed2:
                    ed2 = ed2[:ed2.find('<')]
                    educat = ed2
                educat = educat.replace('&nbsp;','')
                educat = educat.replace('&nbsp','')
                educat = educat.replace('&nbsp','')
                educat = educat.replace(',','$')
                educat = educat.replace('<strong>','')
                educat = educat.replace('</strong>','')
                
                #print 'Education is %s ' %(educat)
            
            
                tabla = Soup.findAll('table')[:-1]
                limla = len(tabla)
                #print tabla[limla-1]
                st = str(tabla[limla-1])
                #print st
                prim2 = '@'
                prim1 = st[st.find('<b>')+3:]
                prim2 = prim1[:prim1.find('</b>')]
                prim2 = prim2.replace(',','$')
                #print 'pp is %s' %(prim2)

                pa2 = '@'
                pa1 = prim1[prim1.find('</b>')+8:]
                pa2 = pa1[:pa1.find('Ph')]
                pa2 = pa2.replace('<br>','')
                pa2 = pa2.replace('</br>','')
                pa2 = pa2.replace(',','$');
                #print 'p add is %s' %( pa2)
            
                ph2 = '@'
                ph1 = prim1[prim1.find('Phone')+7:]
                ph2 = ph1[:12]
                #headings = ['Internship', 'Residency', 'Fellowship','Practice Locations']
                fellow = '@'
                resi = '@'
                intern = '@'
                if cnt not in list:
                    x = soup.find('span', text='Fellowship')      
                    #print url  
                    if x:
                        if x.parent:
                            span_id = x.parent['id']
                            table_id = span_id.replace('dnnTITLE_lblTitle', 'Display_HtmlHolder')
                            fellow = soup.find('td', attrs={"id": table_id}).renderContents()                    
                    else:
                        fellow = '@'
    
                    x = soup.find('span', text='Residency')        
                    if x:
                        span_id = x.parent['id']
                        table_id = span_id.replace('dnnTITLE_lblTitle', 'Display_HtmlHolder')
                        resi = soup.find('td', attrs={"id": table_id}).renderContents()                    
                    else:
                        resi = '@'
                    
                    x = soup.find('span', text='Internship')        
                    if x:
                        span_id = x.parent['id']
                        table_id = span_id.replace('dnnTITLE_lblTitle', 'Display_HtmlHolder')
                        intern = soup.find('td', attrs={"id": table_id}).renderContents()                    
                    else:
                        intern = '@'

                fellow = fellow.replace('<ul>','')
                fellow = fellow.replace('<li>','')
                fellow = fellow.replace('</ul>','')
                fellow = fellow.replace('</li>','')
                resi = resi.replace('<ul>','')
                resi = resi.replace('<li>','')  
                resi = resi.replace('</ul>','')
                resi = resi.replace('</li>','')  
                intern = intern.replace('<ul>','')
                intern = intern.replace('<li>','')
                intern = intern.replace('</ul>','')
                intern = intern.replace('</li>','')

                scraperwiki.sqlite.execute("insert into rik1 values (?,?,?,?,?,?,?,?,?,?,?,?,?)", (fn,deg,title,depart,spcl,educat,fellow,resi,intern,prim2,pa2,ph2,cnt))
                scraperwiki.sqlite.commit()
                print 'fellow = %s  resi = %s,intern = %s' %(fellow,resi,intern )
        cnt = cnt+1
        print cnt
            