import scraperwiki
import urllib2
import lxml.etree

'''
Code to pull data out of the timing related press releases issued by FIA for Formula One races.
This code is provided solely for your own use, without guarantee, so you can publish F1 timing data,
according to license conditions specified by FIA,
without having to rekey the timing data as published on the PDF press releases yourself.

If you want to run the code in your own Python environment, you can what the pdftoxml function calls here:
https://bitbucket.org/ScraperWiki/scraperwiki/src/7d6c7a5393ed/scraperlibs/scraperwiki/utils.py
Essentially, it seems to be a call to the binary /usr/bin/pdftohtml ? [h/t @frabcus]

??pdf2html - this one? http://sourceforge.net/projects/pdftohtml/
'''

'''
To run the script, you need to provide a couple of bits of info...
Check out the PDF URLs on the F1 Media Centre timings page:
  http://www.fia.com/en-GB/mediacentre/f1_media/Pages/timing.aspx
You should see a common slug identifying the race (note that occasionally the slug may differ on the timing sheets)
'''

#Enter slug for race here
race='sin'
#chn, mal, aus, tur, esp, mco, can, eur, gbr, ger, hun, bel, ita
'''
...and then something relevant for the rest of the filename
'''
#enter slug for timing sheet here

racefilenames=["http://184.106.145.74/fia-f1/f1-2012/f1-2012-12/Race%20Preliminary%20Classification.pdf","http://184.106.145.74/fia-f1/f1-2012/f1-2012-12/Race%20Lap%20Analysis.pdf","http://184.106.145.74/fia-f1/f1-2012/f1-2012-12/Race%20Lap%20Chart.pdf","http://184.106.145.74/fia-f1/f1-2012/f1-2012-12/Race%20History%20Chart.pdf","http://184.106.145.74/fia-f1/f1-2012/f1-2012-12/Race%20Fastest%20Laps.pdf","http://184.106.145.74/fia-f1/f1-2012/f1-2012-12/Race%20Pit%20Stop%20Summary.pdf","http://184.106.145.74/fia-f1/f1-2012/f1-2012-12/Race%20Best%20Sector%20Times.pdf","http://184.106.145.74/fia-f1/f1-2012/f1-2012-12/Race%20Speed%20Trap.pdf","http://184.106.145.74/fia-f1/f1-2012/f1-2012-12/Race%20Maximum%20Speeds.pdf"]

qualifilenames=["http://184.106.145.74/fia-f1/f1-2012/f1-2012-12/Qualifying%20Session%20Lap%20Times.pdf",]

grab='quali'
if grab=='p1':typs=['session1-classification','session1-times']
elif grab=='p2':typs=['session2-classification','session2-times']
elif grab=='p12':typs=['session1-classification','session1-times','session2-classification','session2-times']
elif grab=='px':typs=['session1-times','session2-times']
elif grab=='p3':typs=['session3-classification','session3-times']
elif grab=='quali':typs=['qualifying-trap','qualifying-speeds','qualifying-sectors','qualifying-times','qualifying-classification']
elif grab=='race':
    typs=['race-classification','race-chart','race-analysis','race-laps','race-history','race-speeds','race-sectors','race-trap','race-summary']
    #typs=['race-classification','race-chart','race-analysis','race-laps']
    #typs=['race-history','race-speeds','race-sectors','race-trap','race-summary']
else: typs=[]
#typs=['race-chart']
#typs=['race-history']]

import simplejson
def ergastClassification():
    url='http://ergast.com/api/f1/current/last/results.json'
    json=simplejson.load(urllib2.urlopen(url))
    results=json['MRData']['RaceTable']['Races'][0]['Results']
    print results
    for driver in results:
        #number":"1","position":"1","points":"25","Driver":{"driverId":"vettel"
        print driver['number'],driver['position'],driver['Driver']['driverId']
        scraperwiki.sqlite.save(unique_keys=['driverNum'], table_name='erg_race_class', data={'driverNum':str(driver['number']),'pos':str(driver['position']),'driverLastname':driver['Driver']['driverId']})


if grab=='ergast':
    ergastClassification()
    exit(-1)

def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass

#enter page footer slug
slug="<b>2012 FORMULA 1"
#typ can be any of the following (if they use the same convention each race...)
src='f1mediacentreX'
'''
session1-classification.+
session1-times.x
session2-classification.+
session2-times.x
session3-classification.+
session3-times.x
x qualifying-classification
qualifying-trap.+
qualifying-speeds.+
qualifying-sectors.+
qualifying-times.x
race-chart.+
race-analysis.x
race-laps.+
race-history.+
race-speeds.+
race-sectors.+
race-trap.+
race-summary.+



**Note that race-analysis and *-times may have minor glitches**
The report list is a bit casual and occasionally a lap mumber is omitted and appears at the end of the list
A tidying pass on the data that I'm reporting is probably required...


BROKEN (IMPOSSIBLE AFTER SIGNING?)
race-classification <- under development; getting null response? Hmmm -seems to have turned to an photocopied image?
qualifying-classification <- seems like this gets signed and photocopied too :-(
IMPOSSIBLE?
race-grid
'''

#only go below here if you need to do maintenance on the script...
#...which you will have to do in part to get the data out in a usable form
#...at the moment, I only go so far as to preview what's there

#scraperwiki.sqlite.execute('drop table "qualifying-classification"')

#Here's where we construct the URL for the timing sheet.
#I assume a similar naming convention is used for each race?
#scraperwiki.sqlite.execute('drop table "qualifying_speeds"')


def pdfGrabber(typ):
    #if src =='f1mediacentre': url = "http://www.fia.com/en-GB/mediacentre/f1_media/Documents/"+race+"-"+typ+".pdf"
    #http://184.106.145.74/fia-f1/f1-2012/f1-2012-08/eur-f1-2012-fp1-times.pdf
    #http://184.106.145.74/fia-f1/f1-2012/f1-2012-08/eur-f1-2012-fp1-classification.pdf
    ##trying http://184.106.145.74/fia-f1/f1-2012/f1-2012-08/eur-fp1-classification.pdf
    rnum='08'
    typ2=typ.replace('session','fp')
    if src =='f1mediacentre': url = "http://184.106.145.74/fia-f1/f1-2012/f1-2012-"+rnum+"/"+race+"-f1-2012-"+typ2+".pdf"
    else: url="http://dl.dropbox.com/u/1156404/"+race+"-"+typ+".pdf"
    #url='http://dl.dropbox.com/u/1156404/mal-race-analysis.pdf'
    pdfdata = urllib2.urlopen(url).read()
    print "The pdf file has %d bytes" % len(pdfdata)

    xmldata = scraperwiki.pdftoxml(pdfdata)
    '''
    print "After converting to xml it has %d bytes" % len(xmldata)
    print "The first 2000 characters are: ", xmldata[:2000]
    '''

    root = lxml.etree.fromstring(xmldata)
    
    pages = list(root)
    #print 'pre',pages
    print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]
    return pages

#Pairs: from eg [a,b,c,d] return (a,b), (c,d)
def pairs(seq):
    it = iter(seq)
    try:
        while True:
            yield it.next(), it.next()
    except StopIteration:
        return



#Preferred time format
def formatTime(t):
    return float("%.3f" % t)
# Accept times in the form of hh:mm:ss.ss or mm:ss.ss
# Return the equivalent number of seconds
def getTime(ts):
    t=ts.strip()
    t=ts.split(':')
    if len(t)==3:
        tm=60*int(t[0])+60*int(t[1])+float(t[2])
    elif len(t)==2:
        tm=60*int(t[0])+float(t[1])
    else:
        tm=float(t[0])
    return formatTime(tm)


def tidyup(txt):
    txt=txt.strip()
    txt=txt.strip('\n')
    txt=txt.strip('<b>')
    txt=txt.strip('</b>')
    txt=txt.strip()
    return txt

def contains(theString, theQueryValue):
    return theString.find(theQueryValue) > -1

def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

#I use the stub() routine to preview the raw scrape for new documents...
def stub():
    page = pages[0]
    scraping=1
    for el in list(page)[:200]:
        if el.tag == "text":
            if scraping:
                print el.attrib,gettext_with_bi_tags(el)

#The scraper functions themselves
#I just hope the layout of the PDFs, and the foibles, are the same for all races!

import re
def storeRaceHistory(rawdata):
    for result in rawdata:
        lap=result[0]
        trackpos=1
        for cardata in result[1:]:
            if len(cardata)==2: gap=''
            else: gap= cardata[2]
            r=re.match(r"^(.*) LAP$",gap)
            if r!=None:
                lapsBehind=r.group(1)
            else: lapsBehind=0
            scraperwiki.sqlite.save(unique_keys=['lapDriver'], table_name=TYP, data={ 'lapDriver':lap+'_'+cardata[0], 'lap':lap,'driverNum':cardata[0],'time':getTime(cardata[1]), 'gap':gap,'trackpos':str(trackpos),'lapsBehind':lapsBehind})
            trackpos=trackpos+1


def race_history():
    lapdata=[]
    txt=''
    for page in pages:
        lapdata=race_history_page(page,lapdata)
        txt=txt+'new page'+str(len(lapdata))+'\n'
    #Here's the data
    for lap in lapdata:
        print lap
    print lapdata
    print txt
    print 'nlaps timing',str(len(lapdata))
    storeRaceHistory(lapdata)

def race_history_page(page,lapdata=[]):
    scraping=0
    cnt=0
    cntz=[2,2]
    laps={}
    lap=''
    results=[]
    microresults=[]
    headphase=0
    phase=0
    pos=1
    for el in list(page):
        if el.tag == "text":
            if scraping:
                #print el.attrib,gettext_with_bi_tags(el)
                txt=tidyup(gettext_with_bi_tags(el))
                if txt.startswith("LAP") or txt.startswith("Page"):
                    if lap!='' and microresults!=[]:
                        results.append(microresults)
                        laps[lap]=results
                        lapdata.append(results)
                        pos=2
                    else:
                        print ';;;;'
                    pos=1
                    lap=txt
                    headphase=1
                    results=[]
                    results.append(txt.split(' ')[1])
                    microresults=[]
                    cnt=0
                if headphase==1 and txt.startswith("TIME"):
                    headphase=0
                elif headphase==0:
                    if cnt<cntz[phase] or (pos==1 and txt=='PIT'):
                        microresults.append(txt)
                        cnt=cnt+1
                    else:
                        cnt=0
                        results.append(microresults)
                        #print microresults,phase,cnt,headphase,pos,'....'
                        microresults=[txt]
                    if phase==0:
                        phase=1
            else:
                txt=gettext_with_bi_tags(el)
                txt=txt.strip()
                if txt.startswith(slug):
                    scraping=1
    #print laps
    return lapdata

def storeSessionRaceChart(rawdata):
    for result in rawdata:
        #scraperwiki.sqlite.save(unique_keys=['lap'], table_name=TYP, data={'lap':result[0],'positions':'::'.join(result[1:])})
        lap=result[0]
        pos=1
        for carpos in result[1:]:
            if lap=="GRID": lapnum=0
            else: lapnum=lap.split(' ')[-1]
            scraperwiki.sqlite.save(unique_keys=['lapPos'], table_name=TYP, data={'lapnum':str(lapnum),'lapPos':lap+'_'+str(pos), 'lap':lap,'position':pos,'driverNum':carpos})
            pos=pos+1

def race_chart():
    laps=[]
    for page in pages:
        laps=race_chart_page(page,laps)
    #Here's the data
    for lap in laps:
        print lap
    print laps
    storeSessionRaceChart(laps)

def race_chart_page(page,laps):
    cnt=0
    cntz=[2,2]
    scraping=0
    lap=''
    results=[]
    headphase=0
    phase=0
    pos=1
    for el in list(page):
        if el.tag == "text":
            if scraping:
                #print el.attrib,gettext_with_bi_tags(el)
                txt=tidyup(gettext_with_bi_tags(el))
                if txt.startswith("GRID"):
                    lap=txt
                    results=[txt]
                elif txt.startswith("LAP"):
                    if lap !='':
                        laps.append(results)
                    lap=txt
                    results=[txt]
                elif txt.startswith("Page"):
                    laps.append(results)
                else:
                    for t in txt.split():
                        results.append(t)
            else:
                txt=gettext_with_bi_tags(el)
                txt=txt.strip()
                if txt.startswith(slug):
                    scraping=1
    #print laps
    return laps


def storeSessionRaceSummary(rawdata):
    for result in rawdata:
        scraperwiki.sqlite.save(unique_keys=['car_stop'], table_name=TYP, data={'car_stop':result[0]+'_'+result[3],'pos':result[0],'team':result[2],'stop':result[3],'lap':result[4],'name':result[1],'stoptime':result[6],'totalstoptime':result[7],'driverNum':result[0], 'timeOfDay':result[5]})

def race_summary():
    stops=[]
    for page in pages:
        stops=race_summary_page(page,stops)
    #Here's the data
    for stop in stops:
        print stop
    print stops
    storeSessionRaceSummary(stops)

def race_summary_page(page,stops=[]):
    scraping=0
    cnt=0
    cntz=6
    results=[]
    pos=1
    for el in list(page):
        if el.tag == "text":
            if scraping:
                #print el.attrib,gettext_with_bi_tags(el)
                txt=gettext_with_bi_tags(el)
                if cnt<cntz:
                    if cnt==0:
                        results.append([])
                    txt=txt.split("<b>")
                    for t in txt:
                        if t !='':
                            results[pos-1].append(tidyup(t))
                    cnt=cnt+1
                else:
                    cnt=0
                    txt=txt.split("<b>")
                    for t in txt:
                        results[pos-1].append(tidyup(t))
                    #print pos,results[pos-1]
                    pos=pos+1
            else:
                txt=gettext_with_bi_tags(el)
                txt=txt.strip()
                if txt.startswith(slug):
                    scraping=1
    for result in results:
        if not result[0].startswith("Page"):
            stops.append(result)
    return stops



def storeSessionTimes(rawdata):
    for result in rawdata:
        print result
        datapair=pairs(result)
        driverNum,driverName=datapair.next()
        for lap,laptime in datapair:
            scraperwiki.sqlite.save(unique_keys=['driverLap'], table_name=TYP, data={'driverLap':driverNum+'_'+lap,'lap':lap, 'laptime':laptime, 'name':driverName, 'driverNum':driverNum, 'laptimeInS':getTime(laptime)})

def qualifying_times():
    pos=1
    dpos=[]
    #pos,dpos=qualifying_times_page(pages[4],pos,dpos)
    for page in pages:
        pos,dpos=qualifying_times_page(page,pos,dpos)
    #Here's the data
    for pos in dpos:
        print pos
    
    dposcorr=[]
    for pos in dpos:
        dupe=[]
        print pos
        prev=0
        fixed=0
        for p in pos:
            if p.count(':')>0:
                if prev==1:
                    print "oops - need to do a shuffle here and insert element at [-1] here"
                    dupe.append(pos[-1])
                prev=1
            else:
                prev=0
            if len(dupe)<len(pos):
                dupe.append(p)
        print 'corr?',dupe
        print dposcorr.append(dupe)
    print dpos
    print 'hackfix',dposcorr
    storeSessionTimes(dposcorr)


def linebuffershuffle(oldbuffer, newitem):
    oldbuffer[2]=oldbuffer[1]
    oldbuffer[1]=oldbuffer[0]
    oldbuffer[0]=newitem
    return oldbuffer 


def qualifying_times_page(page,pos,dpos):
    #There are still a few issues with this one:
    #Some of the lap numbers appear in the wrong position in results list
    scraping=0
    cnt=0
    cntz=5
    drivers=[]
    results=[]
    phase=0
    linebuffer=["","",""]
    for el in list(page):
        if el.tag == "text":
            txt=gettext_with_bi_tags(el)
            txt=tidyup(txt)
            items=txt.split(" <b>")
            for item in items:
                linebuffer=linebuffershuffle(linebuffer, item)
                #print linebuffer
            if scraping:
                #print el.attrib,gettext_with_bi_tags(el)
                if phase==0 and txt.startswith("NO"):
                    phase=1
                    cnt=0
                    results=[]
                    print '??',linebuffer
                    results.append(linebuffer[2])
                    results.append(linebuffer[1])
                elif phase==1 and cnt<3:
                    cnt=cnt+1
                elif phase==1:
                    phase=2
                    results.append(txt)
                elif phase==2 and txt.startswith("NO"):
                    phase=1
                    print results,linebuffer[2],linebuffer[1]
                    if linebuffer[2] in results: results.remove(linebuffer[2])
                    if linebuffer[1] in results: results.remove(linebuffer[1])
                    for tmp in results:
                        if contains(tmp,'<b>'): results.remove(tmp)
                    print '>>>',pos,results
                    dpos.append(results)
                    pos=pos+1
                    drivers.append(results)
                    results=[]
                    cnt=0
                    results.append(linebuffer[2])
                    results.append(linebuffer[1])
                elif phase==2 and txt.startswith("Page"):
                    #print '>>>',pos,results
                    dpos.append(results)
                    drivers.append(results)
                    pos=pos+1
                elif phase==2:
                    items=txt.split(" <b>")
                    for item in items:
                        results.append(item)
            else:
                txt=gettext_with_bi_tags(el)
                txt=txt.strip()
                if txt.startswith(slug):
                    scraping=1
    return pos,dpos

def storeRaceAnalysis(rawdata):
    for result in rawdata:
        print result
        datapair=pairs(result)
        driverNum,driverName=datapair.next()
        for lap,laptime in datapair:
            scraperwiki.sqlite.save(unique_keys=['driverLap'], table_name=TYP, data={'driverLap':driverNum+'_'+lap,'lap':lap, 'laptime':laptime, 'name':driverName, 'driverNum':driverNum, 'laptimeInS':getTime(laptime)})

def race_analysis():
    pos=1
    dpos=[]
    dposcorr=[]
    for page in pages:
        pos,dpos=race_analysis_page(page,pos,dpos)
    #Here's the data
    for pos in dpos:
        print pos
        dupe=[]
        prev=0
        fixed=0
        for p in pos:
            if p.count(':')>0:
                if prev==1:
                    print "oops - need to do a shuffle here and insert element at [-1] here"
                    dupe.append(pos[-1])
                prev=1
            else:
                prev=0
            if len(dupe)<len(pos):
                dupe.append(p.strip())
        print dupe
        print dposcorr.append(dupe)
    print dpos
    print 'this one',dposcorr
    storeRaceAnalysis(dposcorr)

def race_analysis_page(page,pos,dpos):
    #There are still a few issues with this one:
    #Some of the lap numbers appear in the wrong position in results list
    scraping=0
    cnt=0
    cntz=5
    drivers=[]
    results=[]
    phase=0
    linebuffer=["","",""]
    for el in list(page):
        if el.tag == "text":
            txt=gettext_with_bi_tags(el)
            txt=tidyup(txt)
            items=txt.split(" <b>")
            for item in items:
                linebuffer=linebuffershuffle(linebuffer, item)
            if scraping:
                #print el.attrib,gettext_with_bi_tags(el)
                if phase==0 and txt.startswith("LAP"):
                    phase=1
                    cnt=0
                    results=[]
                    results.append(linebuffer[2])
                    results.append(linebuffer[1])
                elif phase==1 and cnt<3:
                    cnt=cnt+1
                elif phase==1:
                    phase=2
                    results.append(txt)
                elif phase==2 and txt.startswith("LAP"):
                    phase=1
                    if linebuffer[2] in results: results.remove(linebuffer[2])
                    if linebuffer[1] in results: results.remove(linebuffer[1])
                    for tmp in results:
                        if contains(tmp,'<b>'): results.remove(tmp)
                    print results,linebuffer[2],linebuffer[1]
                    #results.remove(linebuffer[2])
                    #results.remove(linebuffer[1])
                    #print '>>>',pos,results
                    dpos.append(results)
                    pos=pos+1
                    drivers.append(results)
                    results=[]
                    cnt=0
                    results.append(linebuffer[2])
                    results.append(linebuffer[1])
                elif phase==2 and txt.startswith("Page"):
                    #print '>>>',pos,results
                    dpos.append(results)
                    drivers.append(results)
                    pos=pos+1
                elif phase==2:
                    items=txt.split(" <b>")
                    for item in items:
                        results.append(item)
            else:
                txt=gettext_with_bi_tags(el)
                txt=txt.strip()
                if txt.startswith(slug):
                    scraping=1
    return pos,dpos

def storeSessionClassification(rawdata):
    #1 ['1', '7', 'M. SCHUMACHER', 'GER', 'Mercedes AMG Petronas F1 Team', '1:35.973', '204.470', '14:52:36', '32']
    #2 ['2', '4', 'L. HAMILTON', 'GBR', 'Vodafone McLaren Mercedes', '1:36.145', '0.172', '204.104', '14:54:25', '29']
    #4 ['4', '2', 'M. WEBBER', 'AUS', 'Red Bull Racing', '1:36.433', '0.460', '0.273', '203.494', '14:41:04', '24']
    for result in rawdata:
        if len(result)>6:
            scraperwiki.sqlite.save(unique_keys=['name','driverNum'], table_name=TYP, data={'pos':result[0],'fastlap':getTime(result[5]), 'name':result[2], 'team':result[4],'nationality':result[3],'driverNum':result[1], 'laps':result[-1], 'kph':result[-3]})
        else:
            scraperwiki.sqlite.save(unique_keys=['name','driverNum'], table_name=TYP, data={'pos':result[0],'fastlap':'', 'name':result[2], 'team':result[4],'nationality':result[3],'driverNum':result[1], 'laps':result[5], 'kph':''})



def session1_classification():
    page = pages[0]
    scraping=0
    cnt=0
    cntz=[7,8,9]
    results=[]
    pos=1
    phase=0
    print 'pages:',len(pages)
    for el in list(page):
        if el.tag == "text":
            txt=gettext_with_bi_tags(el)
            if scraping:
                print el.attrib,gettext_with_bi_tags(el),txt
                txt=tidyup(txt)
                if txt!='Timekeeper:':
                    if cnt<cntz[phase]:
                        if cnt==0:
                            results.append([])
                        txt=txt.split("<b>")
                        for t in txt:
                            results[pos-1].append(t.strip())
                        cnt=cnt+1
                    else:
                        if phase<2:
                            phase=phase+1
                        cnt=0
                        results[pos-1].append(txt)
                        print pos,results[pos-1]
                        pos=pos+1
            else:
                txt=gettext_with_bi_tags(el)
                txt=txt.strip()
                if txt.startswith("<b>TIME OF"):
                    scraping=1

    #Here is the data
    for pos in results:
        print pos
    '''
    #CRAPPY HACK
    rhack=results[:18]
    for x in results[18:]:
        xt=x[:5]
        xt.append('1')
        rhack.append(xt)
        rhack.append(x[6:])
    results=rhack
    for pos in results:
        print pos
    #END CRAPPY HACK
    '''
    print 'results:',results
    storeSessionClassification(results)

def storeSessionQualiSectors(rawdata):
    ss=1
    for sector in rawdata:
        for result in sector:
            scraperwiki.sqlite.save(unique_keys=['sector_pos','sector_driver'], table_name=TYP, data={'sector':str(ss),'sector_pos':str(ss)+'_'+result[0],'sector_driver':str(ss)+'_'+result[1],'pos':result[0],'name':result[2],'sectortime':result[3],'driverNum':result[1]})
        ss=ss+1


def qualifying_sectors():
    sectors=["<b>SECTOR 1</b>\n","<b>SECTOR 2</b>\n","<b>SECTOR 3</b>\n"]
    sector=1
    scraping=0
    results=[]
    sectorResults=[]
    pos=1
    cnt=0
    cntz=2
    page=pages[0]
    for el in list(page):
        if el.tag == "text":
            if scraping:
                #print el.attrib,gettext_with_bi_tags(el)
                txt=gettext_with_bi_tags(el)
                if txt in sectors:
                    sector=sector+1
                    sectorResults.append(results)
                    #print sectorResults
                    #print "Next sector"
                    scraping=0
                    continue
                if cnt<cntz:
                    if cnt==0:
                        results.append([])
                    txt=txt.strip()
                    txt=txt.split("<b>")
                    for t in txt:
                        t=tidyup(t)
                        results[pos-1].append(t)
                    cnt=cnt+1
                else:
                    cnt=0
                    txt=txt.strip()
                    txt=txt.split("<b>")
                    for t in txt:
                        t=tidyup(t)
                        results[pos-1].append(t)
                    #print pos,results[pos-1]
                    pos=pos+1
            else:
                txt=gettext_with_bi_tags(el)
                txt=txt.strip()
                if txt.startswith("<b>TIME"):
                    scraping=1
                    results=[]
                    pos=1
                    cnt=0
    sectorResults.append(results)
    #print sectorResults
    #Here's the data
    for result in sectorResults:
        print result
    print sectorResults
    storeSessionQualiSectors(sectorResults)

def storeSessionQualiSpeeds(rawdata):
    ss=1
    for sector in rawdata:
        for result in sector:
            scraperwiki.sqlite.save(unique_keys=['sector_pos','sector_driver'], table_name=TYP, data={'sector':str(ss),'sector_pos':str(ss)+'_'+result[0],'sector_driver':str(ss)+'_'+result[1],'pos':result[0],'name':result[2],'speed':result[3],'driverNum':result[1]})
        ss=ss+1


def qualifying_speeds():
    sessions=["<b>INTERMEDIATE 1</b>\n","<b>INTERMEDIATE 2</b>\n","<b>FINISH LINE</b>\n"]
    session=1
    scraping=0
    results=[]
    sessionResults=[]
    pos=1
    cnt=0
    cntz=2
    page=pages[0]
    for el in list(page):
        if el.tag == "text":
            if scraping:
                #print el.attrib,gettext_with_bi_tags(el)
                txt=gettext_with_bi_tags(el)
                if txt in sessions:
                    session=session+1
                    sessionResults.append(results)
                    #print sessionResults
                    #print "Next session"
                    scraping=0
                    continue
                if cnt<cntz:
                    if cnt==0:
                        results.append([])
                    txt=txt.strip()
                    txt=txt.split("<b>")
                    for t in txt:
                        t=tidyup(t)
                        results[pos-1].append(t)
                    cnt=cnt+1
                else:
                    cnt=0
                    txt=txt.strip()
                    txt=txt.split("<b>")
                    for t in txt:
                        txt=tidyup(t)
                        results[pos-1].append(t)
                    #print pos,results[pos-1]
                    pos=pos+1
            else:
                txt=gettext_with_bi_tags(el)
                txt=txt.strip()
                if txt.startswith("<b>KPH"):
                    scraping=1
                    results=[]
                    pos=1
                    cnt=0
    sessionResults.append(results)
    #Here's the data
    for session in sessionResults:
        for pos in session:
            print pos
    for session in sessionResults:
        print session
    print sessionResults
    storeSessionQualiSpeeds(sessionResults)

def storeSessionQualiTrap(rawdata):
    for result in rawdata:
        scraperwiki.sqlite.save(unique_keys=['pos','driverNum'], table_name=TYP, data={'pos':result[0],'name':result[2],'speed':result[3],'driverNum':result[1],'timeOfDay':result[4]})


def qualifying_trap():
    page = pages[0]
    scraping=0
    cnt=0
    cntz=3
    results=[]
    pos=1
    for el in list(page):
        if el.tag == "text":
            if scraping:
                #print el.attrib,gettext_with_bi_tags(el)
                txt=gettext_with_bi_tags(el)
                if cnt<cntz:
                    if cnt==0:
                        results.append([])
                    txt=txt.split("<b>")
                    for t in txt:
                        results[pos-1].append(tidyup(t))
                    cnt=cnt+1
                else:
                    cnt=0
                    txt=txt.split("<b>")
                    for t in txt:
                        results[pos-1].append(tidyup(t))
                    #print pos,results[pos-1]
                    pos=pos+1
            else:
                txt=gettext_with_bi_tags(el)
                txt=txt.strip()
                print txt
                if txt.startswith("<b>TIME OF"):
                    scraping=1
    #Here's the data
    for pos in results:
        print pos
    print results
    storeSessionQualiTrap(results)

def storeQualiClassification(rawdata):
    for result in rawdata:
        if len(result)>5: q1_laps=result[5]
        else: q1_laps=''
        if len(result)>9: q2_laps=result[9]
        else: q2_laps=''
        if len(result)>12: q3_laps=result[12]
        else: q3_laps=''
        if len(result)>4: q1_time=result[4]
        else: q1_time=''
        if len(result)>8: q2_time=result[8]
        else: q2_time=''
        if len(result)>11: q3_time=result[11]
        else: q3_time=''
        if result[4]=='DNF': fastlap=''
        else: fastlap=getTime(result[4])
        scraperwiki.sqlite.save(unique_keys=['name','driverNum','pos'], table_name=TYP, data={'pos':result[0],'fastlap':fastlap, 'name':result[2], 'team':result[3],'driverNum':result[1], 'q1_laps':q1_laps,'q2_laps':q2_laps,'q3_laps':q3_laps, 'q1_time':q1_time,'q2_time':q2_time,'q3_time':q3_time})


def qualifying_classification():
    # print the first hundred text elements from the first page
    page = pages[0]
    scraping=0
    session=1
    cnt=0
    pos=1
    results=[]
    cntz=[13,10,6]
    posz=[10,17,24]
    inDNS=0
    wasinDNS=0
    carryForward=0
    for el in list(page):
        if el.tag == "text":
            if scraping:
                #print el.attrib,gettext_with_bi_tags(el)
                txt=gettext_with_bi_tags(el)
                txt=tidyup(txt)
                if session<4:
                    if cnt<cntz[session-1]:
                        if cnt==0:
                            results.append([])
                            txt=txt.strip()
                            txt=txt.split()
                            print 'txt',txt
                            if txt[0]=='DNF':
                                print '...?'
                                txt.remove('DNF')
                                carryForward=1
                            if inDNS==1: print 'inDNS'
                            elif wasinDNS==1:
                                print 'wasinDNS'
                                if txt==['2']:txt=[]
                            for j in txt:
                                results[pos-1].append(j)
                                cnt=cnt+1
                        else:
                            if len(results[pos-1])>4:
                                txt=txt.split()
                                print '->',txt
                                for j in txt:
                                    results[pos-1].append(j)
                                    cnt=cnt+1
                                    if j=='DNS' or j=='DNF':
                                        inDNS=1
                                        print 'got a DNX'
                                        if session==1 or session==2:
                                            cnt=cnt+3
                                        else:
                                            cnt=cnt+1
                                    if inDNS==1 and cnt==cntz[session-1]-3:
                                        print 'Still in DNS'
                                        if cnt==cntz[session-1]-3:
                                            cnt=cnt+3
                                #HORRIBLE HACK
                                #if pos==17 and len(results[pos-1])==6:
                                #    print '************'
                                #    cnt=cnt+4
                                #END HORRIBLE HACK
                            else:
                                print 'x:',txt
                                if txt=='DNF':
                                    print 'DNF'
                                    inDNS=1
                                results[pos-1].append(txt)
                                cnt=cnt+1
                    else:
                        wasinDNS=inDNS
                        if pos==posz[session-1]:
                            session=session+1
                            print "session",session
                            inDNS=0
                        cnt=0
                        txt=txt.split()
                        for j in txt:
                            results[pos-1].append(j)
                        print txt,pos,results[pos-1]
                        pos=pos+1
                        #inDNS=0
            else:
                txt=gettext_with_bi_tags(el)
                txt=txt.strip()
                if txt.startswith(slug):
                    scraping=1
    #HORRIBLE HACK2
    #results=results[:-2]
    #END HORRIBLE HACK2

    #HACK
    #scraperwiki.sqlite.execute('drop table "qualifying-classification"')
    #x=['24']
    #x.extend(results[23][:5])
    #results=results[:23]
    #results.append(x)
    #END HACK


    #Here's the data
    for result in results:
        print 'result',result
    #del results[-1]
    print results
    storeQualiClassification(results)

def storeRaceClassification(rawdata):
    #scraperwiki.sqlite.execute('drop table "race-classification"')
    pos=1
    for result in rawdata:
        if result[0]!='FASTEST LAP':
            try: fastlap=getTime(result[5])
            except: fastlap=''
            try:
                scraperwiki.sqlite.save(unique_keys=['name','driverNum'], table_name=TYP, data={'pos':result[5],'fastlap':fastlap, 'name':result[1], 'team':result[3],'nationality':result[2],'driverNum':result[0], 'laps':result[4], 'result':pos, 'gap':result[6], 'fastlap':result[-2],'speed':result[-3]})
            except:pass
    pos=pos+1


def race_classification():
    #under development - need to handle 'NOT CLASSIFIED'

    page = pages[0]
    scraping=0
    cnt=0
    cntz=[8,9,10,11]
    results=[]
    pos=1
    phase=0
    nclass=0
    for el in list(page):
        #print "broken?",el
        if el.tag == "text":
            txt=gettext_with_bi_tags(el)
            if scraping:
                #print el.attrib,gettext_with_bi_tags(el)
                txt=tidyup(txt)
                if cnt<cntz[phase]:
                    if cnt==0:
                        results.append([])
                    txt=txt.split("<b>")
                    for t in txt:
                        if t.startswith("NOT CLASS"):
                            nclass=1
                            phase=3
                        else:
                            if nclass==1 and len(results[pos-1])==6:
                                results[pos-1].append('')
                                results[pos-1].append('')
                                cnt=cnt+2
                            results[pos-1].append(t.strip())
                    cnt=cnt+1
                else:
                    if phase<2:
                        phase=phase+1
                    cnt=0
                    if phase==3:phase=2
                    if txt.startswith("NOT CLASS"):
                        phase=3
                    else:
                        results[pos-1].append(txt)
                    print pos,results[pos-1]
                    pos=pos+1
            else:
                txt=gettext_with_bi_tags(el)
                txt=txt.strip()
                print "...",txt
                if txt.startswith("<b>LAP<"):
                    scraping=1
    print results 
    storeRaceClassification(results)

def scraperGet(typ):
    if typ=="qualifying-classification":
        print 'trying classification'
        qualifying_classification()
    elif typ=="qualifying-trap" or typ=="race-trap":
        print 'trying trap'
        qualifying_trap()
    elif typ=="qualifying-speeds" or typ=="race-speeds":
        print 'trying speeds'
        qualifying_speeds()
    elif typ=="qualifying-sectors" or typ=="race-sectors":
        print 'trying sectors'
        qualifying_sectors()
    elif typ=="session1-classification" or typ=="session2-classification" or typ=="session3-classification" or typ=="race-laps":
        session1_classification()

    if typ=="race-classification":
        race_classification()
    elif typ=="qualifying-times" or typ=="session3-times" or typ=="session2-times" or typ=="session1-times":
        print "Trying qualifying times"
        qualifying_times()

    if typ=="race-analysis":
        race_analysis()
    elif typ=="race-summary":
        race_summary()
    elif typ=="race-history":
        race_history()
    elif typ=="race-chart":
        race_chart()

# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/

for typ in typs:
    TYP=typ.replace('-','_')
    print 'trying to grab',typ
    pages=pdfGrabber(typ)
    #print 'grabbed',pages
    dropper(TYP)
    try:scraperGet(typ)
    except:pass