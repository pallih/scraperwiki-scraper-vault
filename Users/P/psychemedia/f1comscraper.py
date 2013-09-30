import lxml.html, urllib,csv,scraperwiki

nodrop=1
latest=0
scraping=7

if scraping==1:scrapeset=["P1","P2","P3"]
if scraping==2:scrapeset=["P1","P2"]
if scraping==3:scrapeset=["P3"]
if scraping==4:scrapeset=["P3","Q"]
if scraping==5:scrapeset=["Q"]
if scraping==6:scrapeset=["R"]
if scraping==7:scrapeset=["P1","P2","P3","Q","R"]

#Practice: best_sector_times.html, speed_trap.html
s1=[["http://www.formula1.com/results/season/2012/864/7169/","AUSTRALIA"],
["http://www.formula1.com/results/season/2012/865/7085/","MALAYSIA"], ["http://www.formula1.com/results/season/2012/866/7133/","CHINA"], ["http://www.formula1.com/results/season/2012/867/7163/","BAHRAIN"], ["http://www.formula1.com/results/season/2012/868/7067/","SPAIN"], ["http://www.formula1.com/results/season/2012/869/7079/", "MONACO"],
["http://origin.formula1.com/results/season/2012/870/7139/","CANADA"],
["http://origin.formula1.com/results/season/2012/871/7127/","EUROPE"],
["http://origin.formula1.com/results/season/2012/872/7145/","GREAT BRITAIN"],
["http://origin.formula1.com/results/season/2012/873/7121/","GERMANY"],
["http://www.formula1.com/results/season/2012/874/7115/","HUNGARY"],["http://www.formula1.com/results/season/2012/875/7157/","BELGIUM"],
["http://www.formula1.com/results/season/2012/876/7103/","ITALY"],["http://www.formula1.com/results/season/2012/877/7073/","SINGAPORE"],
["http://www.formula1.com/results/season/2012/878/7097/","JAPAN"],["http://www.formula1.com/results/season/2012/879/7091/","KOREA"],
["http://www.formula1.com/results/season/2012/880/7109/","INDIA"],["http://www.formula1.com/results/season/2012/881/7175/","ABU DHABI"],
["http://www.formula1.com/results/season/2012/882/7181/","UNITED STATES"],["http://www.formula1.com/results/season/2012/883/7151/","BRAZIL"]]
if (latest==1): s1=[s1[-1]]
s2=[["http://www.formula1.com/results/season/2012/864/7170/","AUSTRALIA"],
["http://www.formula1.com/results/season/2012/865/7086/","MALAYSIA"], ["http://www.formula1.com/results/season/2012/866/7134/", "CHINA"], ["http://www.formula1.com/results/season/2012/867/7164/","BAHRAIN"], ["http://www.formula1.com/results/season/2012/868/7068/","SPAIN"], ["http://www.formula1.com/results/season/2012/869/7080/", "MONACO"],
["http://origin.formula1.com/results/season/2012/870/7140/","CANADA"],
["http://origin.formula1.com/results/season/2012/871/7128/","EUROPE"],
["http://origin.formula1.com/results/season/2012/872/7146/","GREAT BRITAIN"],
["http://origin.formula1.com/results/season/2012/873/7122/","GERMANY"],
["http://www.formula1.com/results/season/2012/874/7116/","HUNGARY"],
["http://www.formula1.com/results/season/2012/875/7158/","BELGIUM"],
["http://www.formula1.com/results/season/2012/876/7104/","ITALY"],
["http://www.formula1.com/results/season/2012/877/7074/","SINGAPORE"],
["http://www.formula1.com/results/season/2012/878/7098/","JAPAN"],["http://www.formula1.com/results/season/2012/879/7092/","KOREA"],
["http://www.formula1.com/results/season/2012/880/7110/","INDIA"],["http://www.formula1.com/results/season/2012/881/7176/","ABU DHABI"],
["http://www.formula1.com/results/season/2012/882/7182/","UNITED STATES"],["http://www.formula1.com/results/season/2012/883/7152/","BRAZIL"]]
if (latest==1): s2=[s2[-1]]

s3=[["http://www.formula1.com/results/season/2012/864/7171/","AUSTRALIA"],
["http://www.formula1.com/results/season/2012/865/7087/","MALAYSIA"], ["http://www.formula1.com/results/season/2012/866/7135/","CHINA"], ["http://www.formula1.com/results/season/2012/867/7165/","BAHRAIN"], ["http://www.formula1.com/results/season/2012/868/7069/","SPAIN"], ["http://www.formula1.com/results/season/2012/869/7081/", "MONACO"],
["http://origin.formula1.com/results/season/2012/870/7141/","CANADA"],
["http://origin.formula1.com/results/season/2012/871/7129/","EUROPE"],
["http://origin.formula1.com/results/season/2012/872/7147/","GREAT BRITAIN"],
["http://origin.formula1.com/results/season/2012/873/7123/","GERMANY"],
["http://www.formula1.com/results/season/2012/874/7117/","HUNGARY"],["http://www.formula1.com/results/season/2012/875/7159/","BELGIUM"],
["http://www.formula1.com/results/season/2012/876/7105/","ITALY"],
["http://www.formula1.com/results/season/2012/877/7075/","SINGAPORE"],
["http://www.formula1.com/results/season/2012/878/7099/","JAPAN"],["http://www.formula1.com/results/season/2012/879/7093/","KOREA"],
["http://www.formula1.com/results/season/2012/880/7111/","INDIA"],["http://www.formula1.com/results/season/2012/881/7177/","ABU DHABI"],
["http://www.formula1.com/results/season/2012/882/7183/","UNITED STATES"],["http://www.formula1.com/results/season/2012/883/7153/","BRAZIL"]]
if (latest==1): s3=[s3[-1]]

#pit_stop_summary.html, fastest_laps.html, results.html
races=[["http://www.formula1.com/results/season/2012/864/7173/","AUSTRALIA"], ["http://www.formula1.com/results/season/2012/865/7089/","MALAYSIA"], ["http://www.formula1.com/results/season/2012/866/7137/","CHINA"],
["http://www.formula1.com/results/season/2012/867/7167/","BAHRAIN"], ["http://www.formula1.com/results/season/2012/868/7071/","SPAIN"], ["http://www.formula1.com/results/season/2012/869/7083/","MONACO"],
["http://origin.formula1.com/results/season/2012/870/7143/","CANADA"],
["http://origin.formula1.com/results/season/2012/871/7131/","EUROPE"],
["http://origin.formula1.com/results/season/2012/872/7149/","GREAT BRITAIN"],
["http://origin.formula1.com/results/season/2012/873/7125/","GERMANY"],
["http://www.formula1.com/results/season/2012/874/7119/","HUNGARY"],["http://www.formula1.com/results/season/2012/875/7161/","BELGIUM"],
['http://www.formula1.com/results/season/2012/876/7107/','ITALY'],['http://www.formula1.com/results/season/2012/877/7077/','SINGAPORE'],
["http://www.formula1.com/results/season/2012/878/7101/","JAPAN"],["http://www.formula1.com/results/season/2012/879/7095/","KOREA"],
["http://www.formula1.com/results/season/2012/880/7113/","INDIA"],["http://www.formula1.com/results/season/2012/881/7179/","ABU DHABI"],
["http://www.formula1.com/results/season/2012/882/7185/","UNITED STATES"],["http://www.formula1.com/results/season/2012/883/7155/","BRAZIL"]]
if (latest==1): races=[races[-1]]

#,["http://www.formula1.com/results/season/2011/848/6837/","CHINA"],["http://www.formula1.com/results/season/2011/850/6843/","TURKEY"],["http://www.formula1.com/results/season/2011/853/6849/","SPAIN"],["http://www.formula1.com/results/season/2011/855/6855/","MONACO"],,["http://www.formula1.com/results/season/2011/859/6885/","HUNGARY"],["http://www.formula1.com/results/season/2011/858/6891/","BELGIUM"],["http://www.formula1.com/results/season/2011/856/6897/","ITALY"],["http://www.formula1.com/results/season/2011/854/6903/","SINGAPORE"],["http://www.formula1.com/results/season/2011/852/6909/","JAPAN"],["http://www.formula1.com/results/season/2011/851/6915/","KOREA"],["http://www.formula1.com/results/season/2011/863/6939/","INDIA"],["http://www.formula1.com/results/season/2011/847/6927/","ABU DHABI"],["http://www.formula1.com/results/season/2011/845/6933/","BRAZIL"]]

#best_sector_times.html, speed_trap.html, results.html
qualis=[["http://www.formula1.com/results/season/2012/864/7172/","AUSTRALIA"],["http://www.formula1.com/results/season/2012/865/7088/","MALAYSIA"], ["http://www.formula1.com/results/season/2012/866/7136/","CHINA"], ["http://www.formula1.com/results/season/2012/867/7166/","BAHRAIN"], ["http://www.formula1.com/results/season/2012/868/7070/","SPAIN"], ["http://www.formula1.com/results/season/2012/869/7082/","MONACO"],
["http://origin.formula1.com/results/season/2012/870/7142/","CANADA"],
["http://origin.formula1.com/results/season/2012/871/7130/","EUROPE"],
["http://origin.formula1.com/results/season/2012/872/7148/","GREAT BRITAIN"],
["http://origin.formula1.com/results/season/2012/873/7124/","GERMANY"],
["http://www.formula1.com/results/season/2012/874/7118/","HUNGARY"],["http://www.formula1.com/results/season/2012/875/7160/","BELGIUM"],
["http://www.formula1.com/results/season/2012/876/7106/","ITALY"],["http://www.formula1.com/results/season/2012/877/7076/","SINGAPORE"],
["http://www.formula1.com/results/season/2012/878/7100/","JAPAN"],["http://www.formula1.com/results/season/2012/879/7094","KOREA"],
["http://www.formula1.com/results/season/2012/880/7112/","INDIA"],["http://www.formula1.com/results/season/2012/881/7178/","ABU DHABI"],
["http://www.formula1.com/results/season/2012/882/7184/",'UNITED STATES'],["http://www.formula1.com/results/season/2012/883/7154/","BRAZIL"]]
if (latest==1): qualis=[qualis[-1]]
#,["http://www.formula1.com/results/season/2011/848/6835/","CHINA"],["http://www.formula1.com/results/season/2011/850/6841/","TURKEY"],["http://www.formula1.com/results/season/2011/853/6847/","SPAIN"],["http://www.formula1.com/results/season/2011/855/6853/","MONACO"],["http://www.formula1.com/results/season/2011/861/6871/","GREAT BRITAIN"],["http://www.formula1.com/results/season/2011/862/6877/","GERMANY"],["http://www.formula1.com/results/season/2011/859/6883/","HUNGARY"],["http://www.formula1.com/results/season/2011/858/6889/","BELGIUM"],["http://www.formula1.com/results/season/2011/856/6895/","ITALY"],["http://www.formula1.com/results/season/2011/854/6901/","SINGAPORE"],["http://www.formula1.com/results/season/2011/852/6907/","JAPAN"],["http://www.formula1.com/results/season/2011/851/6913/","KOREA"],["http://www.formula1.com/results/season/2011/863/6938/","INDIA"],["http://www.formula1.com/results/season/2011/847/6925/","ABU DHABI"],["http://www.formula1.com/results/season/2011/845/6931/","BRAZIL"]]

#http://www.formula1.com/results/season/2011/844/6825/fastest_laps.html

def dropper(table):
    if nodrop==1: return
    print "dropping",table
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass


def flatten(el):          
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)

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

def qSpeedScraper(fn,sessions,tn='qualiSpeeds'):
    #fout=open(fn,'wb')
    #writer = csv.writer(fout)
    #writer.writerow(['race','pos','driverNum','driverName','timeOfDay','qspeed'])
    
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
                data={'race':quali[1],'pos':flatten(cells[0]),'driverNum':flatten(cells[1]),'driverName':flatten(cells[2]),'timeOfDay':flatten(cells[3]),'qspeed':flatten(cells[4])}

                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()

def qSectorsScraper(fn,sessions,tn='qualiSectors'):
    #fout=open(fn,'wb')
    #writer = csv.writer(fout)
    #writer.writerow(['race','pos','driverNum','driverName','sector','sectortime'])
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
                data={'race':quali[1],'pos':flatten(cells[0]),'driverNum':flatten(cells[1]),'driverName':flatten(cells[2]),'sector':sector,'sectortime':flatten(cells[3])}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()
    
def qResults(fn):
    #fout=open(fn,'wb')
    #writer = csv.writer(fout)
    #writer.writerow(['race','pos','driverNum','driverName','team','q1natTime','q1time','q2natTime','q2time','q3natTime','q3time','qlaps'])
    tn='qualiResults'
    dropper(tn)
    bigdata=[]
    for quali in qualis:
        url=quali[0]+'results.html'
        print 'trying',url
        content=urllib.urlopen(url).read()
        page=lxml.html.fromstring(content)
        for table in page.findall('.//table'):
            for row in table.findall('.//tr')[1:-1]:
                #print flatten(row)
                cells=row.findall('.//td')
                #data=[quali[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4]),getTime(flatten(cells[4])),flatten(cells[5]),getTime(flatten(cells[5])),flatten(cells[6]),getTime(flatten(cells[6])),flatten(cells[7])]
                #writer.writerow(data)
                data={'race':quali[1], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'q1natTime':flatten(cells[4]), 'q1time':getTime(flatten(cells[4])), 'q2natTime':flatten(cells[5]), 'q2time':getTime(flatten(cells[5])), 'q3natTime':flatten(cells[6]), 'q3time':getTime(flatten(cells[6])), 'qlaps':flatten(cells[7])}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()

def practiceResults(sessions,tn):
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
                data={'race':session[1], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'natTime':flatten(cells[4]), 'time':getTime(flatten(cells[4])), 'natGap':natGap, 'gap':gap, 'laps':flatten(cells[6])}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)

def resScraper(fn):
    #fout=open(fn,'wb')
    #writer = csv.writer(fout)
    #writer.writerow(['race','pos','driverNum','driverName','team','laps','timeOrRetired','grid','points'])
    tn='raceResults'
    dropper(tn)
    bigdata=[]
    for race in races:
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
                data={'race':race[1], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'laps':flatten(cells[4]), 'timeOrRetired':flatten(cells[5]), 'grid':flatten(cells[6]), 'points':flatten(cells[7])}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()

def pitScraper(fn):
    #fout=open(fn,'wb')
    #writer = csv.writer(fout)
    #writer.writerow(['race','stops','driverNum','driverName','team','lap','timeOfDay','natPitTime','pitTime','natTotalPitTime','totalPitTime'])
    tn='racePits'
    dropper(tn)
    bigdata=[]
    for race in races:
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
                data={'race':race[1], 'stops':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'lap':flatten(cells[4]), 'timeOfDay':flatten(cells[5]), 'natPitTime':flatten(cells[6]), 'pitTime':getTime(flatten(cells[6])), 'natTotalPitTime':flatten(cells[7]), 'totalPitTime':getTime(flatten(cells[7]))}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()

def flapScraper(fn):
    #fout=open(fn,'wb')
    #writer = csv.writer(fout)
    #writer.writerow(['race','pos','driverNum','driverName','team','lap','timeOfDay','speed','natTime','stime'])
    tn='raceFastlaps'
    dropper(tn)
    bigdata=[]
    for race in races:
        url=race[0]+'fastest_laps.html'
        print 'trying',url
        content=urllib.urlopen(url).read()
        page=lxml.html.fromstring(content)
        for table in page.findall('.//table'):
            for row in table.findall('.//tr')[1:]:
                #print flatten(row)
                cells=row.findall('.//td')
                #data=[race[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4]),flatten(cells[5]),flatten(cells[6]),flatten(cells[7]),getTime(flatten(cells[7]))]
                #writer.writerow(data)
                data={'race':race[1], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'lap':flatten(cells[4]), 'timeOfDay':flatten(cells[5]), 'speed':flatten(cells[6]), 'natTime':flatten(cells[7]), 'stime':getTime(flatten(cells[7]))}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()

def csvParser(fn):
    data={}
    fin=open(fn,'rb')
    reader=    csv.DictReader(fin)
    for row in reader:
        print row
    fin.close()
    return data


#fn='fastestLaps2012.csv'        

print ("Race")
if "R" in scrapeset:
    flapScraper('fastestLaps2012.csv')
    resScraper('raceResults2012.csv')
    pitScraper('pitSummary2012.csv')

print("Quali")
if "Q" in scrapeset:
    qSpeedScraper('qualiSpeeds2012.csv',qualis)
    qResults('qualiResults2012.csv')
    qSectorsScraper('qualiSectors2012.csv',qualis)


print("P1")
if "P1" in scrapeset:
    qSpeedScraper('qualiSpeeds2012.csv',s1,"p1Speeds")
    qSectorsScraper('qualiSectors2012.csv',s1,"p1Sectors")
    practiceResults(s1,"p1Results")

print("P2")
if "P2" in scrapeset:
    qSpeedScraper('qualiSpeeds2012.csv',s2,"p2Speeds")
    qSectorsScraper('qualiSectors2012.csv',s2,"p2Sectors")
    practiceResults(s2,"p2Results")

print("P3")
if "P3" in scrapeset:
    qSpeedScraper('qualiSpeeds2012.csv',s3,"p3Speeds")
    qSectorsScraper('qualiSectors2012.csv',s3,"p3Sectors")
    practiceResults(s3,"p3Results")


#data=csvParser(fn)    
    
#parse aggregated file

#find min times/fastest speed by race
#find percent from min time/fastest speed
#in R, plot lines for each car across racesimport lxml.html, urllib,csv,scraperwiki

nodrop=1
latest=0
scraping=7

if scraping==1:scrapeset=["P1","P2","P3"]
if scraping==2:scrapeset=["P1","P2"]
if scraping==3:scrapeset=["P3"]
if scraping==4:scrapeset=["P3","Q"]
if scraping==5:scrapeset=["Q"]
if scraping==6:scrapeset=["R"]
if scraping==7:scrapeset=["P1","P2","P3","Q","R"]

#Practice: best_sector_times.html, speed_trap.html
s1=[["http://www.formula1.com/results/season/2012/864/7169/","AUSTRALIA"],
["http://www.formula1.com/results/season/2012/865/7085/","MALAYSIA"], ["http://www.formula1.com/results/season/2012/866/7133/","CHINA"], ["http://www.formula1.com/results/season/2012/867/7163/","BAHRAIN"], ["http://www.formula1.com/results/season/2012/868/7067/","SPAIN"], ["http://www.formula1.com/results/season/2012/869/7079/", "MONACO"],
["http://origin.formula1.com/results/season/2012/870/7139/","CANADA"],
["http://origin.formula1.com/results/season/2012/871/7127/","EUROPE"],
["http://origin.formula1.com/results/season/2012/872/7145/","GREAT BRITAIN"],
["http://origin.formula1.com/results/season/2012/873/7121/","GERMANY"],
["http://www.formula1.com/results/season/2012/874/7115/","HUNGARY"],["http://www.formula1.com/results/season/2012/875/7157/","BELGIUM"],
["http://www.formula1.com/results/season/2012/876/7103/","ITALY"],["http://www.formula1.com/results/season/2012/877/7073/","SINGAPORE"],
["http://www.formula1.com/results/season/2012/878/7097/","JAPAN"],["http://www.formula1.com/results/season/2012/879/7091/","KOREA"],
["http://www.formula1.com/results/season/2012/880/7109/","INDIA"],["http://www.formula1.com/results/season/2012/881/7175/","ABU DHABI"],
["http://www.formula1.com/results/season/2012/882/7181/","UNITED STATES"],["http://www.formula1.com/results/season/2012/883/7151/","BRAZIL"]]
if (latest==1): s1=[s1[-1]]
s2=[["http://www.formula1.com/results/season/2012/864/7170/","AUSTRALIA"],
["http://www.formula1.com/results/season/2012/865/7086/","MALAYSIA"], ["http://www.formula1.com/results/season/2012/866/7134/", "CHINA"], ["http://www.formula1.com/results/season/2012/867/7164/","BAHRAIN"], ["http://www.formula1.com/results/season/2012/868/7068/","SPAIN"], ["http://www.formula1.com/results/season/2012/869/7080/", "MONACO"],
["http://origin.formula1.com/results/season/2012/870/7140/","CANADA"],
["http://origin.formula1.com/results/season/2012/871/7128/","EUROPE"],
["http://origin.formula1.com/results/season/2012/872/7146/","GREAT BRITAIN"],
["http://origin.formula1.com/results/season/2012/873/7122/","GERMANY"],
["http://www.formula1.com/results/season/2012/874/7116/","HUNGARY"],
["http://www.formula1.com/results/season/2012/875/7158/","BELGIUM"],
["http://www.formula1.com/results/season/2012/876/7104/","ITALY"],
["http://www.formula1.com/results/season/2012/877/7074/","SINGAPORE"],
["http://www.formula1.com/results/season/2012/878/7098/","JAPAN"],["http://www.formula1.com/results/season/2012/879/7092/","KOREA"],
["http://www.formula1.com/results/season/2012/880/7110/","INDIA"],["http://www.formula1.com/results/season/2012/881/7176/","ABU DHABI"],
["http://www.formula1.com/results/season/2012/882/7182/","UNITED STATES"],["http://www.formula1.com/results/season/2012/883/7152/","BRAZIL"]]
if (latest==1): s2=[s2[-1]]

s3=[["http://www.formula1.com/results/season/2012/864/7171/","AUSTRALIA"],
["http://www.formula1.com/results/season/2012/865/7087/","MALAYSIA"], ["http://www.formula1.com/results/season/2012/866/7135/","CHINA"], ["http://www.formula1.com/results/season/2012/867/7165/","BAHRAIN"], ["http://www.formula1.com/results/season/2012/868/7069/","SPAIN"], ["http://www.formula1.com/results/season/2012/869/7081/", "MONACO"],
["http://origin.formula1.com/results/season/2012/870/7141/","CANADA"],
["http://origin.formula1.com/results/season/2012/871/7129/","EUROPE"],
["http://origin.formula1.com/results/season/2012/872/7147/","GREAT BRITAIN"],
["http://origin.formula1.com/results/season/2012/873/7123/","GERMANY"],
["http://www.formula1.com/results/season/2012/874/7117/","HUNGARY"],["http://www.formula1.com/results/season/2012/875/7159/","BELGIUM"],
["http://www.formula1.com/results/season/2012/876/7105/","ITALY"],
["http://www.formula1.com/results/season/2012/877/7075/","SINGAPORE"],
["http://www.formula1.com/results/season/2012/878/7099/","JAPAN"],["http://www.formula1.com/results/season/2012/879/7093/","KOREA"],
["http://www.formula1.com/results/season/2012/880/7111/","INDIA"],["http://www.formula1.com/results/season/2012/881/7177/","ABU DHABI"],
["http://www.formula1.com/results/season/2012/882/7183/","UNITED STATES"],["http://www.formula1.com/results/season/2012/883/7153/","BRAZIL"]]
if (latest==1): s3=[s3[-1]]

#pit_stop_summary.html, fastest_laps.html, results.html
races=[["http://www.formula1.com/results/season/2012/864/7173/","AUSTRALIA"], ["http://www.formula1.com/results/season/2012/865/7089/","MALAYSIA"], ["http://www.formula1.com/results/season/2012/866/7137/","CHINA"],
["http://www.formula1.com/results/season/2012/867/7167/","BAHRAIN"], ["http://www.formula1.com/results/season/2012/868/7071/","SPAIN"], ["http://www.formula1.com/results/season/2012/869/7083/","MONACO"],
["http://origin.formula1.com/results/season/2012/870/7143/","CANADA"],
["http://origin.formula1.com/results/season/2012/871/7131/","EUROPE"],
["http://origin.formula1.com/results/season/2012/872/7149/","GREAT BRITAIN"],
["http://origin.formula1.com/results/season/2012/873/7125/","GERMANY"],
["http://www.formula1.com/results/season/2012/874/7119/","HUNGARY"],["http://www.formula1.com/results/season/2012/875/7161/","BELGIUM"],
['http://www.formula1.com/results/season/2012/876/7107/','ITALY'],['http://www.formula1.com/results/season/2012/877/7077/','SINGAPORE'],
["http://www.formula1.com/results/season/2012/878/7101/","JAPAN"],["http://www.formula1.com/results/season/2012/879/7095/","KOREA"],
["http://www.formula1.com/results/season/2012/880/7113/","INDIA"],["http://www.formula1.com/results/season/2012/881/7179/","ABU DHABI"],
["http://www.formula1.com/results/season/2012/882/7185/","UNITED STATES"],["http://www.formula1.com/results/season/2012/883/7155/","BRAZIL"]]
if (latest==1): races=[races[-1]]

#,["http://www.formula1.com/results/season/2011/848/6837/","CHINA"],["http://www.formula1.com/results/season/2011/850/6843/","TURKEY"],["http://www.formula1.com/results/season/2011/853/6849/","SPAIN"],["http://www.formula1.com/results/season/2011/855/6855/","MONACO"],,["http://www.formula1.com/results/season/2011/859/6885/","HUNGARY"],["http://www.formula1.com/results/season/2011/858/6891/","BELGIUM"],["http://www.formula1.com/results/season/2011/856/6897/","ITALY"],["http://www.formula1.com/results/season/2011/854/6903/","SINGAPORE"],["http://www.formula1.com/results/season/2011/852/6909/","JAPAN"],["http://www.formula1.com/results/season/2011/851/6915/","KOREA"],["http://www.formula1.com/results/season/2011/863/6939/","INDIA"],["http://www.formula1.com/results/season/2011/847/6927/","ABU DHABI"],["http://www.formula1.com/results/season/2011/845/6933/","BRAZIL"]]

#best_sector_times.html, speed_trap.html, results.html
qualis=[["http://www.formula1.com/results/season/2012/864/7172/","AUSTRALIA"],["http://www.formula1.com/results/season/2012/865/7088/","MALAYSIA"], ["http://www.formula1.com/results/season/2012/866/7136/","CHINA"], ["http://www.formula1.com/results/season/2012/867/7166/","BAHRAIN"], ["http://www.formula1.com/results/season/2012/868/7070/","SPAIN"], ["http://www.formula1.com/results/season/2012/869/7082/","MONACO"],
["http://origin.formula1.com/results/season/2012/870/7142/","CANADA"],
["http://origin.formula1.com/results/season/2012/871/7130/","EUROPE"],
["http://origin.formula1.com/results/season/2012/872/7148/","GREAT BRITAIN"],
["http://origin.formula1.com/results/season/2012/873/7124/","GERMANY"],
["http://www.formula1.com/results/season/2012/874/7118/","HUNGARY"],["http://www.formula1.com/results/season/2012/875/7160/","BELGIUM"],
["http://www.formula1.com/results/season/2012/876/7106/","ITALY"],["http://www.formula1.com/results/season/2012/877/7076/","SINGAPORE"],
["http://www.formula1.com/results/season/2012/878/7100/","JAPAN"],["http://www.formula1.com/results/season/2012/879/7094","KOREA"],
["http://www.formula1.com/results/season/2012/880/7112/","INDIA"],["http://www.formula1.com/results/season/2012/881/7178/","ABU DHABI"],
["http://www.formula1.com/results/season/2012/882/7184/",'UNITED STATES'],["http://www.formula1.com/results/season/2012/883/7154/","BRAZIL"]]
if (latest==1): qualis=[qualis[-1]]
#,["http://www.formula1.com/results/season/2011/848/6835/","CHINA"],["http://www.formula1.com/results/season/2011/850/6841/","TURKEY"],["http://www.formula1.com/results/season/2011/853/6847/","SPAIN"],["http://www.formula1.com/results/season/2011/855/6853/","MONACO"],["http://www.formula1.com/results/season/2011/861/6871/","GREAT BRITAIN"],["http://www.formula1.com/results/season/2011/862/6877/","GERMANY"],["http://www.formula1.com/results/season/2011/859/6883/","HUNGARY"],["http://www.formula1.com/results/season/2011/858/6889/","BELGIUM"],["http://www.formula1.com/results/season/2011/856/6895/","ITALY"],["http://www.formula1.com/results/season/2011/854/6901/","SINGAPORE"],["http://www.formula1.com/results/season/2011/852/6907/","JAPAN"],["http://www.formula1.com/results/season/2011/851/6913/","KOREA"],["http://www.formula1.com/results/season/2011/863/6938/","INDIA"],["http://www.formula1.com/results/season/2011/847/6925/","ABU DHABI"],["http://www.formula1.com/results/season/2011/845/6931/","BRAZIL"]]

#http://www.formula1.com/results/season/2011/844/6825/fastest_laps.html

def dropper(table):
    if nodrop==1: return
    print "dropping",table
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass


def flatten(el):          
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)

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

def qSpeedScraper(fn,sessions,tn='qualiSpeeds'):
    #fout=open(fn,'wb')
    #writer = csv.writer(fout)
    #writer.writerow(['race','pos','driverNum','driverName','timeOfDay','qspeed'])
    
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
                data={'race':quali[1],'pos':flatten(cells[0]),'driverNum':flatten(cells[1]),'driverName':flatten(cells[2]),'timeOfDay':flatten(cells[3]),'qspeed':flatten(cells[4])}

                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()

def qSectorsScraper(fn,sessions,tn='qualiSectors'):
    #fout=open(fn,'wb')
    #writer = csv.writer(fout)
    #writer.writerow(['race','pos','driverNum','driverName','sector','sectortime'])
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
                data={'race':quali[1],'pos':flatten(cells[0]),'driverNum':flatten(cells[1]),'driverName':flatten(cells[2]),'sector':sector,'sectortime':flatten(cells[3])}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()
    
def qResults(fn):
    #fout=open(fn,'wb')
    #writer = csv.writer(fout)
    #writer.writerow(['race','pos','driverNum','driverName','team','q1natTime','q1time','q2natTime','q2time','q3natTime','q3time','qlaps'])
    tn='qualiResults'
    dropper(tn)
    bigdata=[]
    for quali in qualis:
        url=quali[0]+'results.html'
        print 'trying',url
        content=urllib.urlopen(url).read()
        page=lxml.html.fromstring(content)
        for table in page.findall('.//table'):
            for row in table.findall('.//tr')[1:-1]:
                #print flatten(row)
                cells=row.findall('.//td')
                #data=[quali[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4]),getTime(flatten(cells[4])),flatten(cells[5]),getTime(flatten(cells[5])),flatten(cells[6]),getTime(flatten(cells[6])),flatten(cells[7])]
                #writer.writerow(data)
                data={'race':quali[1], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'q1natTime':flatten(cells[4]), 'q1time':getTime(flatten(cells[4])), 'q2natTime':flatten(cells[5]), 'q2time':getTime(flatten(cells[5])), 'q3natTime':flatten(cells[6]), 'q3time':getTime(flatten(cells[6])), 'qlaps':flatten(cells[7])}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()

def practiceResults(sessions,tn):
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
                data={'race':session[1], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'natTime':flatten(cells[4]), 'time':getTime(flatten(cells[4])), 'natGap':natGap, 'gap':gap, 'laps':flatten(cells[6])}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)

def resScraper(fn):
    #fout=open(fn,'wb')
    #writer = csv.writer(fout)
    #writer.writerow(['race','pos','driverNum','driverName','team','laps','timeOrRetired','grid','points'])
    tn='raceResults'
    dropper(tn)
    bigdata=[]
    for race in races:
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
                data={'race':race[1], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'laps':flatten(cells[4]), 'timeOrRetired':flatten(cells[5]), 'grid':flatten(cells[6]), 'points':flatten(cells[7])}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()

def pitScraper(fn):
    #fout=open(fn,'wb')
    #writer = csv.writer(fout)
    #writer.writerow(['race','stops','driverNum','driverName','team','lap','timeOfDay','natPitTime','pitTime','natTotalPitTime','totalPitTime'])
    tn='racePits'
    dropper(tn)
    bigdata=[]
    for race in races:
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
                data={'race':race[1], 'stops':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'lap':flatten(cells[4]), 'timeOfDay':flatten(cells[5]), 'natPitTime':flatten(cells[6]), 'pitTime':getTime(flatten(cells[6])), 'natTotalPitTime':flatten(cells[7]), 'totalPitTime':getTime(flatten(cells[7]))}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()

def flapScraper(fn):
    #fout=open(fn,'wb')
    #writer = csv.writer(fout)
    #writer.writerow(['race','pos','driverNum','driverName','team','lap','timeOfDay','speed','natTime','stime'])
    tn='raceFastlaps'
    dropper(tn)
    bigdata=[]
    for race in races:
        url=race[0]+'fastest_laps.html'
        print 'trying',url
        content=urllib.urlopen(url).read()
        page=lxml.html.fromstring(content)
        for table in page.findall('.//table'):
            for row in table.findall('.//tr')[1:]:
                #print flatten(row)
                cells=row.findall('.//td')
                #data=[race[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4]),flatten(cells[5]),flatten(cells[6]),flatten(cells[7]),getTime(flatten(cells[7]))]
                #writer.writerow(data)
                data={'race':race[1], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'lap':flatten(cells[4]), 'timeOfDay':flatten(cells[5]), 'speed':flatten(cells[6]), 'natTime':flatten(cells[7]), 'stime':getTime(flatten(cells[7]))}
                #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                bigdata.append(data.copy())
                if len(bigdata)>1000:
                    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()

def csvParser(fn):
    data={}
    fin=open(fn,'rb')
    reader=    csv.DictReader(fin)
    for row in reader:
        print row
    fin.close()
    return data


#fn='fastestLaps2012.csv'        

print ("Race")
if "R" in scrapeset:
    flapScraper('fastestLaps2012.csv')
    resScraper('raceResults2012.csv')
    pitScraper('pitSummary2012.csv')

print("Quali")
if "Q" in scrapeset:
    qSpeedScraper('qualiSpeeds2012.csv',qualis)
    qResults('qualiResults2012.csv')
    qSectorsScraper('qualiSectors2012.csv',qualis)


print("P1")
if "P1" in scrapeset:
    qSpeedScraper('qualiSpeeds2012.csv',s1,"p1Speeds")
    qSectorsScraper('qualiSectors2012.csv',s1,"p1Sectors")
    practiceResults(s1,"p1Results")

print("P2")
if "P2" in scrapeset:
    qSpeedScraper('qualiSpeeds2012.csv',s2,"p2Speeds")
    qSectorsScraper('qualiSectors2012.csv',s2,"p2Sectors")
    practiceResults(s2,"p2Results")

print("P3")
if "P3" in scrapeset:
    qSpeedScraper('qualiSpeeds2012.csv',s3,"p3Speeds")
    qSectorsScraper('qualiSectors2012.csv',s3,"p3Sectors")
    practiceResults(s3,"p3Results")


#data=csvParser(fn)    
    
#parse aggregated file

#find min times/fastest speed by race
#find percent from min time/fastest speed
#in R, plot lines for each car across races