#import scraperwiki
import re
import urllib2
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
xy = 1;

if xy == 1:
    #url = 'http://www.drexelmed.edu/Home/AboutOurFaculty/ErikaAaron.aspx'
    #url = 'http://www.drexelmed.edu/Home/AboutOurFaculty/SandeepAggarwal.aspx'
    #url = 'http://www.drexelmed.edu/Home/AboutOurFaculty/KimberlyAccardi.aspx'
    #url = "http://www.drexelmed.edu/Home/AboutOurFaculty/ElenaAdamov.aspx"
    #url = 'http://www.drexelmed.edu/Home/AboutOurFaculty/NabilAbaza.aspx'
    #url = 'http://www.drexelmed.edu/Home/AboutOurFaculty/CarolArtlett.aspx'
    url = 'http://www.drexelmed.edu/Home/AboutOurFaculty/CarolArtlett.aspx'
    page = urlopen(url).read()
    Soup = BeautifulStoneSoup(page)
    line = Soup.findAll('h2')[1].renderContents()
    fn = line[:line.find(',')]
    print fn
    ftemp = str(fn)
    deg = ''
    if  ',' in line:
        deg = line[line.find(',')+1:]
    #print 'deg = %s' %(deg)
    title = Soup.findAll('h3')[0].renderContents()
    title = title.replace(',','$')
    
    #print title
    #<span>Department:</span>(.*)</li>

    patFinderdep = re.compile('<span>Department:</span>(.*)</li>')
    pdep = re.findall(patFinderdep,page)
    depart = ''
    if pdep:
        depart = pdep[0]
    else :
        patFinderpra = re.compile('<span>Practice:</span>(.*)\s*<li><span>S')
        ppra = re.findall(patFinderpra,page)
        if ppra:
            depart = ppra[0]

    print 'department is %s ' %(depart)

    spcl = ''
    patFindersp = re.compile('<span>Specialty:</span>(.*)</li>')
    psp = re.findall(patFindersp,page)
    if psp:
        spcl = psp[0]

    sp2 = str(spcl)
    if '<' in sp2:
        sp2 = sp2[:sp2.find('<')]
        spcl = sp2
    print 'speciality is %s ' %(spcl)


    educat = ''
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
    
    print 'Education is %s ' %(educat)


    
    
#import scraperwiki
import re
import urllib2
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
xy = 1;

if xy == 1:
    #url = 'http://www.drexelmed.edu/Home/AboutOurFaculty/ErikaAaron.aspx'
    #url = 'http://www.drexelmed.edu/Home/AboutOurFaculty/SandeepAggarwal.aspx'
    #url = 'http://www.drexelmed.edu/Home/AboutOurFaculty/KimberlyAccardi.aspx'
    #url = "http://www.drexelmed.edu/Home/AboutOurFaculty/ElenaAdamov.aspx"
    #url = 'http://www.drexelmed.edu/Home/AboutOurFaculty/NabilAbaza.aspx'
    #url = 'http://www.drexelmed.edu/Home/AboutOurFaculty/CarolArtlett.aspx'
    url = 'http://www.drexelmed.edu/Home/AboutOurFaculty/CarolArtlett.aspx'
    page = urlopen(url).read()
    Soup = BeautifulStoneSoup(page)
    line = Soup.findAll('h2')[1].renderContents()
    fn = line[:line.find(',')]
    print fn
    ftemp = str(fn)
    deg = ''
    if  ',' in line:
        deg = line[line.find(',')+1:]
    #print 'deg = %s' %(deg)
    title = Soup.findAll('h3')[0].renderContents()
    title = title.replace(',','$')
    
    #print title
    #<span>Department:</span>(.*)</li>

    patFinderdep = re.compile('<span>Department:</span>(.*)</li>')
    pdep = re.findall(patFinderdep,page)
    depart = ''
    if pdep:
        depart = pdep[0]
    else :
        patFinderpra = re.compile('<span>Practice:</span>(.*)\s*<li><span>S')
        ppra = re.findall(patFinderpra,page)
        if ppra:
            depart = ppra[0]

    print 'department is %s ' %(depart)

    spcl = ''
    patFindersp = re.compile('<span>Specialty:</span>(.*)</li>')
    psp = re.findall(patFindersp,page)
    if psp:
        spcl = psp[0]

    sp2 = str(spcl)
    if '<' in sp2:
        sp2 = sp2[:sp2.find('<')]
        spcl = sp2
    print 'speciality is %s ' %(spcl)


    educat = ''
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
    
    print 'Education is %s ' %(educat)


    
    
