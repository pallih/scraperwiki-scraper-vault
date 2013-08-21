import lxml.html, urllib,csv,scraperwiki



def flatten(el):          
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)



#get races from year
#<li class="listheader"><span><a href="/results/season/2012/">
#www.formula1.com/results/season/2012/





#,["http://www.formula1.com/results/season/2011/848/6835/","CHINA"]

#http://www.formula1.com/results/season/2011/844/6825/fastest_laps.html

def dropper(table):
    if nodrop==1: return
    print "dropping",table
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass



#Preferred time format
def formatTime(t):
    return float("%.3f" % t)
# Accept times in the form of hh:mm:ss.ss or mm:ss.ss
# Return the equivalent number of seconds
def getTime(ts):
    tm=''
    if ts.find(':')>-1:
        t=ts.strip()
        t=ts.split(':')
        if len(t)==3:
            tm=60*int(t[0])+60*int(t[1])+float(t[2])
        elif len(t)==2:
            tm=60*int(t[0])+float(t[1])
        tm=formatTime(tm)
    else:
        try:
            tm=float(ts)
            tm=formatTime(tm)
        except:tm=''
    return tm

def qSpeedScraper(sessions,tn,year):    
    dropper(tn)
    bigdata=[]
    for quali in sessions:
        url=quali[0]+'speed_trap.html'
        print 'trying',url
        content=urllib.urlopen(url).read()
        page=lxml.html.fromstring(content)
        for table in page.findall('.//table'):
            for row in table.findall('.//tr')[1:]:
                #print flatten(row)
                cells=row.findall('.//td')
                #data=[quali[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4])]
                #writer.writerow(data)
                data={'year':year,'race':quali[1],'pos':flatten(cells[0]),'driverNum':flatten(cells[1]),'driverName':flatten(cells[2]),'timeOfDay':flatten(cells[3]),'qspeed':flatten(cells[4])}

                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)


def qSectorsScraper(sessions,tn,year):
    dropper(tn)
    bigdata=[]
    for quali in sessions:
        url=quali[0]+'best_sector_times.html'
        print 'trying',url
        content=urllib.urlopen(url).read()
        page=lxml.html.fromstring(content)
        sector=0
        for table in page.findall('.//table'):
            sector=sector+1
            for row in table.findall('.//tr')[2:]:
                #print row,flatten(row)
                cells=row.findall('.//td')
                #data=[quali[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),sector,flatten(cells[3])]
                #writer.writerow(data)
                data={'year':year,'race':quali[1],'pos':flatten(cells[0]),'driverNum':flatten(cells[1]),'driverName':flatten(cells[2]),'sector':sector,'sectortime':flatten(cells[3])}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()
    
def qResults(qualis,year):
    tn='qualiResults'
    dropper(tn)
    bigdata=[]
    for quali in qualis:
        url=quali[0]+'results.html'
        print 'trying',url
        content=urllib.urlopen(url).read()
        page=lxml.html.fromstring(content)
        for table in page.findall('.//table'):
            for row in table.findall('.//tr')[1:]:
                #print flatten(row)
                cells=row.findall('.//td')
                if flatten(cells[0])=='':continue
                #data=[quali[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4]),getTime(flatten(cells[4])),flatten(cells[5]),getTime(flatten(cells[5])),flatten(cells[6]),getTime(flatten(cells[6])),flatten(cells[7])]
                #writer.writerow(data)
                data={'year':year,'race':quali[1], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'q1natTime':flatten(cells[4]), 'q1time':getTime(flatten(cells[4])), 'q2natTime':flatten(cells[5]), 'q2time':getTime(flatten(cells[5])), 'q3natTime':flatten(cells[6]), 'q3time':getTime(flatten(cells[6])), 'qlaps':flatten(cells[7])}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)


def practiceResults(sessions,tn,year):
    dropper(tn)
    bigdata=[]
    for session in sessions:
        url=session[0]+'results.html'
        print 'trying',url
        content=urllib.urlopen(url).read()
        page=lxml.html.fromstring(content)
        for table in page.findall('.//table'):
            for row in table.findall('.//tr')[1:]:
                #print flatten(row)
                cells=row.findall('.//td')
                #data=[quali[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4]),getTime(flatten(cells[4])),flatten(cells[5]),getTime(flatten(cells[5])),flatten(cells[6]),getTime(flatten(cells[6])),flatten(cells[7])]
                #writer.writerow(data)
                if flatten(cells[0])=="1":
                    gap=0
                    natGap=0
                else:
                    natGap=flatten(cells[5])
                    gap=getTime(flatten(cells[5]))
                data={'year':year,'race':session[1], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'natTime':flatten(cells[4]), 'time':getTime(flatten(cells[4])), 'natGap':natGap, 'gap':gap, 'laps':flatten(cells[6])}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)

def resScraper(races,year):
    tn='raceResults'
    dropper(tn)
    bigdata=[]
    raceNum=0
    for race in races:
        raceNum=raceNum+1
        url=race[0]+'results.html'
        print 'trying',url
        content=urllib.urlopen(url).read()
        page=lxml.html.fromstring(content)
        for table in page.findall('.//table'):
            for row in table.findall('.//tr')[1:]:
                #print flatten(row)
                cells=row.findall('.//td')
                #data=[race[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4]),flatten(cells[5]),flatten(cells[6]),flatten(cells[7])]
                #writer.writerow(data)
                data={'year':year,'raceNum':raceNum,'race':race[1], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'laps':flatten(cells[4]), 'timeOrRetired':flatten(cells[5]), 'grid':flatten(cells[6]), 'points':flatten(cells[7])}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()

def pitScraper(races,year):
    tn='racePits'
    dropper(tn)
    bigdata=[]
    raceNum=0
    for race in races:
        raceNum=raceNum+1
        url=race[0]+'pit_stop_summary.html'
        print 'trying',url
        content=urllib.urlopen(url).read()
        page=lxml.html.fromstring(content)
        for table in page.findall('.//table'):
            for row in table.findall('.//tr')[1:]:
                #print flatten(row)
                cells=row.findall('.//td')
                #data=[race[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4]),flatten(cells[5]),flatten(cells[6]),getTime(flatten(cells[6])),flatten(cells[7]),getTime(flatten(cells[7]))]
                #writer.writerow(data)
                data={'year':year,'raceNum':raceNum,'race':race[1], 'stops':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'lap':flatten(cells[4]), 'timeOfDay':flatten(cells[5]), 'natPitTime':flatten(cells[6]), 'pitTime':getTime(flatten(cells[6])), 'natTotalPitTime':flatten(cells[7]), 'totalPitTime':getTime(flatten(cells[7]))}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)

def flapScraper(races,year):
    tn='raceFastlaps'
    dropper(tn)
    bigdata=[]
    raceNum=0
    for race in races:
        raceNum=raceNum+1
        url=race[0]+'fastest_laps.html'
        print 'trying',url
        content=urllib.urlopen(url).read()
        page=lxml.html.fromstring(content)
        for table in page.findall('.//table'):
            for row in table.findall('.//tr')[1:]:
                #print flatten(row)
                cells=row.findall('.//td')
                data={'year':year,'raceNum':raceNum,'race':race[1], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'lap':flatten(cells[4]), 'timeOfDay':flatten(cells[5]), 'speed':flatten(cells[6]), 'natTime':flatten(cells[7]), 'stime':getTime(flatten(cells[7]))}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)



nodrop=1
latest=0
scraping=7

def liaparse(ul):
    d=[]
    lis=ul.findall('.//li')
    for li in lis:
        a=li.find('a')
        u=a.get('href')
        r=flatten(li)
        print u,r
        d.append((u,r))
    return d

#import mechanize


def yearGrabber(year):
    urlstub='http://www.formula1.com/results/season'
    url='/'.join( [urlstub,str(year) ])
    print 'trying',url
    content=urllib.urlopen(url).read()
    page=lxml.html.fromstring(content)
    uls =page.findall('.//ul')

    #lis=uls[14].findall('.//li')
    ah=liaparse(uls[14])
    #for li in lis[1:]:
    #    a=li.find('a')
    #    u=a.get('href')
    #    r=flatten(li)
    #    print u,r
    s1=[]
    s2=[]
    s3=[]
    qualis=[]
    races=[]

    for (u,r) in ah[1:]:
        print u,r
        print 'trying',u
        content2=urllib.urlopen('http://formula1.com'+u).read()

        #br = mechanize.Browser()
        #response = br.open(url)
        #content=response.read()
        page2=lxml.html.fromstring(content2)
        uls2 =page2.findall('.//ul')
        print len(uls2),content

        ah2=liaparse(uls2[15])
        for (u2,r2) in ah2:
            print '\t',u2,r2
            if '1' in r2:
                s1.append(['http://formula1.com'+u2,r.strip()])
            elif '2' in r2:
                s2.append(['http://formula1.com'+u2,r.strip()])
            elif '3' in r2 or 'SATURDAY' in r2:
                s3.append(['http://formula1.com'+u2,r.strip()])
            elif 'QUALI' in r2:
                qualis.append(['http://formula1.com'+u2,r.strip()])
            elif 'RACE' in r2:
                races.append(['http://formula1.com'+u2,r.strip()])
        print s1,s2,s3,qualis,races
        #exit(-1)
    #exit(-1)
    if scraping==1:scrapeset=["P1","P2","P3"]
    if scraping==2:scrapeset=["P1","P2"]
    if scraping==3:scrapeset=["P3"]
    if scraping==4:scrapeset=["P3","Q"]
    if scraping==5:scrapeset=["Q"]
    if scraping==6:scrapeset=["R"]
    if scraping==7:scrapeset=["P1","P2","P3","Q","R"]

    #Practice: best_sector_times.html, speed_trap.html
    #s1=[]
    if (latest==1): s1=[s1[-1]]
    #s2=[]
    if (latest==1): s2=[s2[-1]]
    #s3=[]
    if (latest==1): s3=[s3[-1]]

    #best_sector_times.html, speed_trap.html, results.html
    #qualis=[]
    if (latest==1): qualis=[qualis[-1]]

    #pit_stop_summary.html, fastest_laps.html, results.html
    #races=[]
    if (latest==1): races=[races[-1]]

    print ("Race")
    if "R" in scrapeset:
        flapScraper(races,year)
        resScraper(races,year)
        pitScraper(races,year)

    print("Quali")
    if "Q" in scrapeset:
        qSpeedScraper(qualis,'qualiSpeeds',year)
        qResults(qualis,year)
        qSectorsScraper(qualis,'qualiSectors',year)


    print("P1")
    if "P1" in scrapeset:
        qSpeedScraper(s1,"p1Speeds",year)
        qSectorsScraper(s1,"p1Sectors",year)
        practiceResults(s1,"p1Results",year)

    print("P2")
    if "P2" in scrapeset:
        qSpeedScraper(s2,"p2Speeds",year)
        qSectorsScraper(s2,"p2Sectors",year)
        practiceResults(s2,"p2Results",year)

    print("P3")
    if "P3" in scrapeset:
        qSpeedScraper(s3,"p3Speeds",year)
        qSectorsScraper(s3,"p3Sectors",year)
        practiceResults(s3,"p3Results",year)

for y in ['2012','2011','2010','2009','2008','2007','2006']:
    yearGrabber(y)

exit(-1)

