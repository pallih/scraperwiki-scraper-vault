###############################################################################
# Scrapper melkweg.nl
###############################################################################

import sys
import os
from operator import itemgetter
import urllib2,urllib
from xml.dom.minidom import parseString
import time,socket

from BeautifulSoup import BeautifulSoup
import scraperwiki
import re
import urlparse
eventsscrap= {}
def scrape_for_next ():
   
    URLS =[]  
    start_url = 'http://www.melkweg.nl/voorpagina.jsp?offset=0&disciplineid=muziek&vandaag=1272664800&batchno=1' # starting from 2010-05-01
    #start_url = 'http://www.melkweg.nl/voorpagina.jsp?offset=0&disciplineid=muziek&vandaag=1272664800&batchno=1'
    year = 2010
    nextYear = bool(0)
    #print url  
    URLS.append(start_url )
    html = scraperwiki.scrape(start_url )
    soup = BeautifulSoup(html)
    soup = soup.findAll('div', {'class':'rightalign'})
    #print soup    
    rows = soup[0].findAll('a')
    
    
    
    for i in range(0, len(rows)-1) :
        #print (rows[i])['href']
        ref=(rows[i])['href']
        ref_url= urlparse.urljoin(base_url,ref)
        URLS.append(ref_url)       
        #print ref_url
    
    for url in URLS :
        #print url
        
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        prog = re.compile("event\d+")
        idate=re.compile("idate")
 
        events = soup.findAll('div',id=prog )
        for e in events:
            EndDate=DateTime=''
            month=day=ed_time=endMonth=endDay='0'
            if prog.match(e['id']):
                EventID=  e['id'].replace('event','')
                eventsscrap["ID"] = EventID
                #print EventID
            if e['class'] != u'item muziek':
                continue
            alldiv = e.findAll('div')
            
            title=''
            DateTime = ''
            eventURL =''
            for div in alldiv:
                if div ['class'] == 'rc' :
                    rc= div.findAll('div')
                    for rcclass in rc :
                        if rcclass ['class'].find('ititle')>-1 :
                            if rcclass.span.h2.a.string != None:
                                title = rcclass.span.h2.a.string
                            
                            print title
                            eventURL= urlparse.urljoin(base_url, rcclass.a['href'])
                            
                            retrieveEventData (eventURL)
                            #retrieve Event data
                        elif rcclass['class']== 'iprice':
                            dds = rcclass.findAll('dd')
                            times = []
                            endtimes=[]
                            for dd in dds:
                                if len(dd) ==0:
                                    continue
                                t = dd.string.strip()
                                print t
                                #print t 
                                if re.match('\d\d[:.,]\d\d uur',t):
                                    times.append(t.replace(' uur',''))
                                elif re.search('aanvang',t):
                                    tt=t.split('/')
                                    if len(tt) > 1 :
                                        aavang=''
                                        for av in tt :
                                            if re.search('aanvang',av) :
                                                aavang=av
                                        av_number=re.findall(r"\d\d.\d\d uur",aavang)
                                        if len(av_number) >  0 :
                                            times.append((av_number[0].replace('aanvang:','')).replace('uur','').replace(' ','').replace('.',':') )
                                elif re.search('t/m',t):
                                    if not re.search('€',t) :
                                        findtime= re.findall(r"\d\d.\d\d",t)
                                    
                                        if len(findtime) > 0 :                                        
                                            times.append(findtime[0].replace('.',':'))
                                            print times
                                    
                                        if len(findtime) > 1 :     
                                            endtimes.append(findtime[1].replace('.',':'))
                                            print endtimes
                                    

                                    
                                         
                                
                            if  len(times) > 0 :
                                ed_time = end_time = times[0]
                                
                          

                            else :
                                ed_time = end_time  = '00:00'
                            if  len(endtimes) > 0 :
                                end_time = endtimes[0]

                            if  not nextYear:
                                if int(month)< 5 :
                                    year+=1
                                    nextYear= bool(1)
                        
                            EndYear= year
                            if endMonth != '0' and (int(month)-int(endMonth)) > 0 :
                                EndYear+=1
                            
                            DateTime=day+'/'+month+'/'+ str(year)+ ' ' +ed_time+':00'
                            if endDay !='0' and endMonth != '0' :
                                EndDate=endDay+'/'+endMonth+'/'+ str(EndYear)+ ' ' +end_time+':00'                           
                            
                                
                 

                if div['class'] =='lc':
                    t1=div.findAll('div')
                    
                    for info in t1:
                        
                        if idate.match(info['class']):
                            #print  'idate    ' +str(info['class'])
                            dates = info.findAll('span')
                            for d in dates:
                                if d['class']== 'dm':
                                    month = d.contents[0]
                                elif d['class']== 'dn':
                                    day = d.contents[0]
                                elif d['class']== 'adn':
                                    endDay=d.contents[0]
                                elif d['class']== 'adm':
                                    endMonth=d.contents[0]
                    
                                     
            
            eventsscrap["Category"] = 'muziek'
            eventsscrap["Date"] = DateTime
            eventsscrap["EndDate"] = EndDate
            eventsscrap["Name"] = title
            eventsscrap["URL"] = eventURL
            
            #print eventsscrap
            scraperwiki.datastore.save(["ID"], eventsscrap)
       
             

def retrieveEventData (eventURL) :
    #eventURL='http://www.melkweg.nl/artikelpagina.jsp?language=nederlands&batchno=22&offset=252&artikelid=186584&disciplineid=cinema&agendaitemid=209246'
    Eventhtml = scraperwiki.scrape(eventURL)
    Eventsoup = BeautifulSoup(Eventhtml)   
    Alldetails= Eventsoup.findAll('div',{'class':'item detail muziek'})    
    #print Alldetails
    imageURL=''
    MovieURL =''
    contentDesc=''
    for detail in Alldetails :
         divDetail=detail.findAll('div')
         for t in divDetail :             
             try :
                 if t['class'] :
                    if t['class'] =='iimg':                                  
                        images=t.findAll('a')                     
                        for im in images :
                             image= im['href']
                             imageURL+= urlparse.urljoin(base_url,image)+ "##"                       
                             #print imageURL                  

                    elif t['class'] =='iinfo':
                        #print 'desc'
                        description = t.findAll('p')
                        contentDesc=''
                        nobr = re.compile('<.*?')                        
                        obj=re.compile('<object.*?')
                        bold = re.compile('<b>')
                        #print description
                        for desc in description :
                            #print desc.contents
                            if not obj.search(str(desc)) :
                            #nobr.sub(' ', str(desc) )
                            #s = str(desc).replace('<br />','')
                            #print  desc.contents
                                
                                for content in desc.contents :
                                    #print content
                                    if bold.match (str(content)):
                                            boldstr = content
                                            #print boldstr 
                                            if boldstr.string != None : 
                                                #print boldstr.string
                                                contentDesc+=boldstr.string.replace(u'\xa0','').replace('\r\n','').replace('\t','').replace('\n',' ').replace('&quot;',' ')+' '
                                                
                                    elif content !='\n' and not nobr.match(str(content)) :
                                        
                                        contentDesc+=content.string.replace(u'\xa0','').replace('\r\n','').replace('\t','').replace('\n',' ').replace('&quot;',' ')+' '  
                                        #print content  #desc.contents[0].replace('\t','').replace('\n','')
                        
                        params = t.findAll('param')                    
                        for param in params :
                            if param ['name'] == 'movie' :
                                MovieURL += param ['value'] + "##"


                        
                        #print contentDesc
                        embeds = t.findAll('embed')  
                        for embed in embeds :
                               if MovieURL.find(str(embed ['src'])) == -1:
                                   MovieURL += embed ['src'] + "##"

                        frames= t.findAll('iframe')
                        for frame in frames:
                               if MovieURL.find(str(frame ['src'])) == -1:                                   
                                   MovieURL += frame ['src'] + "##"
                    
                 else :
                    continue       
                        
             except :                
                #print "Unexpected error:", sys.exc_info()[0]
                pass
                

    eventsscrap["Movie"] = MovieURL
    eventsscrap["Image"] = imageURL
    eventsscrap["Description"] = contentDesc    


base_url = 'http://www.melkweg.nl'                
scrape_for_next ()
#retrieveEventData ()



###############################################################################
# Scrapper melkweg.nl
###############################################################################

import sys
import os
from operator import itemgetter
import urllib2,urllib
from xml.dom.minidom import parseString
import time,socket

from BeautifulSoup import BeautifulSoup
import scraperwiki
import re
import urlparse
eventsscrap= {}
def scrape_for_next ():
   
    URLS =[]  
    start_url = 'http://www.melkweg.nl/voorpagina.jsp?offset=0&disciplineid=muziek&vandaag=1272664800&batchno=1' # starting from 2010-05-01
    #start_url = 'http://www.melkweg.nl/voorpagina.jsp?offset=0&disciplineid=muziek&vandaag=1272664800&batchno=1'
    year = 2010
    nextYear = bool(0)
    #print url  
    URLS.append(start_url )
    html = scraperwiki.scrape(start_url )
    soup = BeautifulSoup(html)
    soup = soup.findAll('div', {'class':'rightalign'})
    #print soup    
    rows = soup[0].findAll('a')
    
    
    
    for i in range(0, len(rows)-1) :
        #print (rows[i])['href']
        ref=(rows[i])['href']
        ref_url= urlparse.urljoin(base_url,ref)
        URLS.append(ref_url)       
        #print ref_url
    
    for url in URLS :
        #print url
        
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        prog = re.compile("event\d+")
        idate=re.compile("idate")
 
        events = soup.findAll('div',id=prog )
        for e in events:
            EndDate=DateTime=''
            month=day=ed_time=endMonth=endDay='0'
            if prog.match(e['id']):
                EventID=  e['id'].replace('event','')
                eventsscrap["ID"] = EventID
                #print EventID
            if e['class'] != u'item muziek':
                continue
            alldiv = e.findAll('div')
            
            title=''
            DateTime = ''
            eventURL =''
            for div in alldiv:
                if div ['class'] == 'rc' :
                    rc= div.findAll('div')
                    for rcclass in rc :
                        if rcclass ['class'].find('ititle')>-1 :
                            if rcclass.span.h2.a.string != None:
                                title = rcclass.span.h2.a.string
                            
                            print title
                            eventURL= urlparse.urljoin(base_url, rcclass.a['href'])
                            
                            retrieveEventData (eventURL)
                            #retrieve Event data
                        elif rcclass['class']== 'iprice':
                            dds = rcclass.findAll('dd')
                            times = []
                            endtimes=[]
                            for dd in dds:
                                if len(dd) ==0:
                                    continue
                                t = dd.string.strip()
                                print t
                                #print t 
                                if re.match('\d\d[:.,]\d\d uur',t):
                                    times.append(t.replace(' uur',''))
                                elif re.search('aanvang',t):
                                    tt=t.split('/')
                                    if len(tt) > 1 :
                                        aavang=''
                                        for av in tt :
                                            if re.search('aanvang',av) :
                                                aavang=av
                                        av_number=re.findall(r"\d\d.\d\d uur",aavang)
                                        if len(av_number) >  0 :
                                            times.append((av_number[0].replace('aanvang:','')).replace('uur','').replace(' ','').replace('.',':') )
                                elif re.search('t/m',t):
                                    if not re.search('€',t) :
                                        findtime= re.findall(r"\d\d.\d\d",t)
                                    
                                        if len(findtime) > 0 :                                        
                                            times.append(findtime[0].replace('.',':'))
                                            print times
                                    
                                        if len(findtime) > 1 :     
                                            endtimes.append(findtime[1].replace('.',':'))
                                            print endtimes
                                    

                                    
                                         
                                
                            if  len(times) > 0 :
                                ed_time = end_time = times[0]
                                
                          

                            else :
                                ed_time = end_time  = '00:00'
                            if  len(endtimes) > 0 :
                                end_time = endtimes[0]

                            if  not nextYear:
                                if int(month)< 5 :
                                    year+=1
                                    nextYear= bool(1)
                        
                            EndYear= year
                            if endMonth != '0' and (int(month)-int(endMonth)) > 0 :
                                EndYear+=1
                            
                            DateTime=day+'/'+month+'/'+ str(year)+ ' ' +ed_time+':00'
                            if endDay !='0' and endMonth != '0' :
                                EndDate=endDay+'/'+endMonth+'/'+ str(EndYear)+ ' ' +end_time+':00'                           
                            
                                
                 

                if div['class'] =='lc':
                    t1=div.findAll('div')
                    
                    for info in t1:
                        
                        if idate.match(info['class']):
                            #print  'idate    ' +str(info['class'])
                            dates = info.findAll('span')
                            for d in dates:
                                if d['class']== 'dm':
                                    month = d.contents[0]
                                elif d['class']== 'dn':
                                    day = d.contents[0]
                                elif d['class']== 'adn':
                                    endDay=d.contents[0]
                                elif d['class']== 'adm':
                                    endMonth=d.contents[0]
                    
                                     
            
            eventsscrap["Category"] = 'muziek'
            eventsscrap["Date"] = DateTime
            eventsscrap["EndDate"] = EndDate
            eventsscrap["Name"] = title
            eventsscrap["URL"] = eventURL
            
            #print eventsscrap
            scraperwiki.datastore.save(["ID"], eventsscrap)
       
             

def retrieveEventData (eventURL) :
    #eventURL='http://www.melkweg.nl/artikelpagina.jsp?language=nederlands&batchno=22&offset=252&artikelid=186584&disciplineid=cinema&agendaitemid=209246'
    Eventhtml = scraperwiki.scrape(eventURL)
    Eventsoup = BeautifulSoup(Eventhtml)   
    Alldetails= Eventsoup.findAll('div',{'class':'item detail muziek'})    
    #print Alldetails
    imageURL=''
    MovieURL =''
    contentDesc=''
    for detail in Alldetails :
         divDetail=detail.findAll('div')
         for t in divDetail :             
             try :
                 if t['class'] :
                    if t['class'] =='iimg':                                  
                        images=t.findAll('a')                     
                        for im in images :
                             image= im['href']
                             imageURL+= urlparse.urljoin(base_url,image)+ "##"                       
                             #print imageURL                  

                    elif t['class'] =='iinfo':
                        #print 'desc'
                        description = t.findAll('p')
                        contentDesc=''
                        nobr = re.compile('<.*?')                        
                        obj=re.compile('<object.*?')
                        bold = re.compile('<b>')
                        #print description
                        for desc in description :
                            #print desc.contents
                            if not obj.search(str(desc)) :
                            #nobr.sub(' ', str(desc) )
                            #s = str(desc).replace('<br />','')
                            #print  desc.contents
                                
                                for content in desc.contents :
                                    #print content
                                    if bold.match (str(content)):
                                            boldstr = content
                                            #print boldstr 
                                            if boldstr.string != None : 
                                                #print boldstr.string
                                                contentDesc+=boldstr.string.replace(u'\xa0','').replace('\r\n','').replace('\t','').replace('\n',' ').replace('&quot;',' ')+' '
                                                
                                    elif content !='\n' and not nobr.match(str(content)) :
                                        
                                        contentDesc+=content.string.replace(u'\xa0','').replace('\r\n','').replace('\t','').replace('\n',' ').replace('&quot;',' ')+' '  
                                        #print content  #desc.contents[0].replace('\t','').replace('\n','')
                        
                        params = t.findAll('param')                    
                        for param in params :
                            if param ['name'] == 'movie' :
                                MovieURL += param ['value'] + "##"


                        
                        #print contentDesc
                        embeds = t.findAll('embed')  
                        for embed in embeds :
                               if MovieURL.find(str(embed ['src'])) == -1:
                                   MovieURL += embed ['src'] + "##"

                        frames= t.findAll('iframe')
                        for frame in frames:
                               if MovieURL.find(str(frame ['src'])) == -1:                                   
                                   MovieURL += frame ['src'] + "##"
                    
                 else :
                    continue       
                        
             except :                
                #print "Unexpected error:", sys.exc_info()[0]
                pass
                

    eventsscrap["Movie"] = MovieURL
    eventsscrap["Image"] = imageURL
    eventsscrap["Description"] = contentDesc    


base_url = 'http://www.melkweg.nl'                
scrape_for_next ()
#retrieveEventData ()



