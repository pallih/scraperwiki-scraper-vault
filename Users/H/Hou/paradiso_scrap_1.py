###########################################
 ####################################
  # Scrapper Paradiso.nl  
 
 
import scraperwiki
import urlparse
import lxml.html
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import re
record = []
visited=[]
events={}
events_ids =[]
 # ---------------------------------------------------------------------------
 # START HERE: define your starting URL - then
 # call a function to scrape the first page in the series.
 # ---------------------------------------------------------------------------
 
def get_pardiso_events(urli) :
    results = scraperwiki.sqlite.select("ID,URL from swdata")

    #scraperwiki.sqlite.execute("update swdata set Image='f' where URL="http://www.paradiso.nl/web/Agenda-Item/Gino-Vannelli-1.htm"")
    #scraperwiki.sqlite.execute("insert into swdata (Image) Values ('up') Select URL from swdata where URL='http://www.paradiso.nl/web/Agenda-Item/Gino-Vannelli-1.htm'")
    #scraperwiki.sqlite.execute("alter table swdata Add Image VARCHAR(50)")
    #scraperwiki.sqlite.commit()
    print results 
    
    for result in results :
        url=result['URL']
        id = result['ID']
        #print url 
        #print id
        image_url =''
        html = scraperwiki.scrape('http://'+url)
        soup = BeautifulSoup(html)
        soup= soup.findAll('div',{'class':'richText'})
        for i in soup :
            image = i.findAll('img',src=re.compile("jpg"))  
            for im in image  :   
                image_url+= 'http://www.paradiso.nl'+ im['src']+' '
        scraperwiki.sqlite.execute("update swdata set Image=? where ID=?;" , (image_url  ,id))

        scraperwiki.sqlite.commit()
        print url
        print id
        print image_url
    #scrape_and_look_for_next_link(url)
    #scrape_and_look_for_previous_link(url)
    table = merge_visited_record ()
    print 'record'
    print record
    print len(record)
    print 'events_ids'
    print events_ids
    print len(events_ids)
    print 'visited'
    print visited
    print len(visited)
    print 'merged table'
    print table
    print len(table)
 
   
def scrape_and_look_for_next_link(url):
   try :
     html = scraperwiki.scrape(url)
     soup = BeautifulSoup(html)
     v_links = []
     next_links=[]
     verder_links=[]
     next_agenda=''
     print 'next'
     print url
    
     agenda= soup.find('div',id='agenda-next')
     if agenda != None :
        next_agenda= ((agenda.find('a')['href']).replace('\n','')).replace('\t','')  
        next_link=next_agenda
    
     if next_link in record :         
           next_links= j_events_notrecorded(soup)    
     if len(next_links) > 0 :
          next_link = next_links[0]
          
     
     if next_link not in visited :
         visited.append(next_link)
          
     #event_id=soup.find('input', {'name':'ididid_event_id'})
     retrieve_event_data (soup)
     if next_link not in record and next_link != '' :         
         record.append(next_link)
         next_url = urlparse.urljoin(base_url, next_link)         
         scrape_and_look_for_next_link(next_url)
             
     elif next_link != '' :
          v_links=  verder_events_all(soup)
          for v in v_links :
             if v not in record :
                 verder_links.append(v)       
          if len(verder_links) > 0 :
             first_verder = comparedates(verder_links,soup)
             scrape_and_look_for_previous_link(first_verder)
             scrape_and_look_for_next_link(first_verder)
          else :
            print 'no verder links --- scrape finished'
     else :
          print 'scrape finished'
   except :
    pass     

 
def retrieve_event_data (soup) :    
   
     try :
        movie =''      
        event_name=soup.find('input', {'name':'ididid_event_name'})
        event_id=soup.find('input', {'name':'ididid_event_id'})
        event_date = soup.find('input', {'name':'ididid_event_date'})
        event_end_date=  soup.find('input', {'name':'ididid_event_end_date'})
        event_url= soup.find('input', {'name':'ididid_event_url'})
        event_description = soup.find('input', {'name':'ididid_event_description'})
        #event_movie=soup.find('param',{'name':'movie'})
        event_movie=soup.find('param',{'name':'movie'})
        if event_movie :
            movie= event_movie['value']
        events_ids.append(event_id['value'])

        events = { "ID" : event_id['value'] ,
                   "URL" : event_url['value'],
                   "Name" : event_name['value'],
                   "Date" : event_date['value'],
                   "End date" : event_end_date['value'],
                   "URL" : event_url['value'],
                   "Description" : event_description['value'],
                   "Movie" : movie
                  }
        scraperwiki.datastore.save(["ID"], events )   
     except :
        pass
        


def comparedates(liste , soup):
     date = soup.find('input', {'name':'ididid_event_date'})
     urls = []  
     first_url ='nothing'
     if date :
         datevalue=date['value']
         current_date= datetime.strptime(datevalue, "%d-%m-%Y %H:%M")
         #print current_date
     for event in liste :
         url = urlparse.urljoin(base_url, event)
         html = scraperwiki.scrape(url)
         soup = BeautifulSoup(html)
         date = soup.find('input', {'name':'ididid_event_date'})
         if date :
             datevalue=date['value']
             dt= datetime.strptime(datevalue, "%d-%m-%Y %H:%M")
             delta = dt  - current_date
             if delta.days > 0  :        
                 urls.append(url)
                 #print 'urls'
                 #print urls           
             if len(urls) > 0 :
                 break
     return urls[0]
 
 
def scrape_and_look_for_previous_link(url):
    try :
     html = scraperwiki.scrape(url)
     print 'previous'
     print url   
     soup = BeautifulSoup(html)
     retrieve_event_data (soup)
     previous_agenda=''
     previous_agenda=  ((((soup.find('div',id='agenda-previous')).find('a')['href']).replace('\n','')).replace('\t','')).replace('  ','')
     print previous_agenda
     retrieve_journey_events (soup)
     if previous_agenda not in record  :
            record.append(previous_agenda)
            previous_url = urlparse.urljoin(base_url, previous_agenda)         
            scrape_and_look_for_previous_link(previous_url)        
     else :
         previous_links= j_events_notrecorded(soup)     
         if len(previous_links) > 0 :
             previous_agenda = previous_links[len(previous_links)-1]
             record.append(previous_agenda)
             #print 'previous agenda'
             #print previous_agenda  
             previous_url = urlparse.urljoin(base_url, previous_agenda)         
             scrape_and_look_for_previous_link(previous_url)
         else :
             print 'finished previous'
    except :   
        if previous_agenda in record :
            record.remove(previous_agenda)
        link = select_last_notrecorded_j_event()
        previous_url = urlparse.urljoin(base_url, link )  
        scrape_and_look_for_previous_link(previous_url)
        pass

def select_last_notrecorded_j_event ():
       table = []
       for j in range (0, len(visited)-1):
        if  visited [j] not in record :
           table.append (visited [j])
       return table[len(table)-1]


def merge_visited_record ():
       table=[]   
       for i in range (0, len(record) -1) :
         table.append (record[i])
       for j in range (0, len(visited)-1):
         if visited [j] not in record :
             table.append (visited [j])
             url = urlparse.urljoin(base_url, visited [j])
             try :
                html = scraperwiki.scrape(url)
                soup = BeautifulSoup(html)
                retrieve_event_data(soup)
               
             except :
                pass
       return table
  
def journey_events_all(soup) :
     j_events=[]
     journey_links = []
     journey = soup.findAll('div',{'class':'linklist'})
     for k in range(0,len(journey)) :
          div = journey[k].find('div')
          if div != None :
              text= div.text
              if text=='Deze dag ook in Paradiso' :
                 j_events=journey[k].findAll('a')
                 # print j_events
     for i in j_events:
          link = (i['href'].replace('\n','')).replace('\t','')  
          journey_links.append(link )
     return journey_links


def verder_events_all(soup) :
     v_events=[]
     verder_links = []
     journey = soup.findAll('div',{'class':'linklist'})
     for k in range(0,len(journey)) :
         div = journey[k].find('div')
         if div != None :
             text= div.text
             if text=='Verder in Paradiso' :
               v_events=journey[k].findAll('a')  
     for i in v_events:
          link = ((i['href'].replace('\n','')).replace('\t','')).replace(' ','')  
          verder_links.append(link )
     return verder_links
    
def j_events_notrecorded(soup) :
    next_links=[]
    journey_links = journey_events_all(soup)
    for j in journey_links :
         if j not in record :
              next_links.append(j)
    return next_links

def  retrieve_journey_events (soup) :
    journey_links = journey_events_all(soup)
    for j in journey_links :
          if j not in visited:
               visited.append(j)

#rrrrrrrrrrrrrrrrrr
base_url = 'http://paradiso.nl/'
starting_url  = urlparse.urljoin(base_url,'web/Agenda-Item/Gino-Vannelli-1.htm') #'web/Agenda-Item/Chris-Smither-Peter-Mulvey.htm')
#'web/Agenda-Item/Arbouretum-1.htm'
get_pardiso_events(starting_url)
record.append('web/Agenda-Item/Marianne-Faithfull-1.htm')
 ###########################################
 ####################################
  # Scrapper Paradiso.nl  
 
 
import scraperwiki
import urlparse
import lxml.html
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import re
record = []
visited=[]
events={}
events_ids =[]
 # ---------------------------------------------------------------------------
 # START HERE: define your starting URL - then
 # call a function to scrape the first page in the series.
 # ---------------------------------------------------------------------------
 
def get_pardiso_events(urli) :
    results = scraperwiki.sqlite.select("ID,URL from swdata")

    #scraperwiki.sqlite.execute("update swdata set Image='f' where URL="http://www.paradiso.nl/web/Agenda-Item/Gino-Vannelli-1.htm"")
    #scraperwiki.sqlite.execute("insert into swdata (Image) Values ('up') Select URL from swdata where URL='http://www.paradiso.nl/web/Agenda-Item/Gino-Vannelli-1.htm'")
    #scraperwiki.sqlite.execute("alter table swdata Add Image VARCHAR(50)")
    #scraperwiki.sqlite.commit()
    print results 
    
    for result in results :
        url=result['URL']
        id = result['ID']
        #print url 
        #print id
        image_url =''
        html = scraperwiki.scrape('http://'+url)
        soup = BeautifulSoup(html)
        soup= soup.findAll('div',{'class':'richText'})
        for i in soup :
            image = i.findAll('img',src=re.compile("jpg"))  
            for im in image  :   
                image_url+= 'http://www.paradiso.nl'+ im['src']+' '
        scraperwiki.sqlite.execute("update swdata set Image=? where ID=?;" , (image_url  ,id))

        scraperwiki.sqlite.commit()
        print url
        print id
        print image_url
    #scrape_and_look_for_next_link(url)
    #scrape_and_look_for_previous_link(url)
    table = merge_visited_record ()
    print 'record'
    print record
    print len(record)
    print 'events_ids'
    print events_ids
    print len(events_ids)
    print 'visited'
    print visited
    print len(visited)
    print 'merged table'
    print table
    print len(table)
 
   
def scrape_and_look_for_next_link(url):
   try :
     html = scraperwiki.scrape(url)
     soup = BeautifulSoup(html)
     v_links = []
     next_links=[]
     verder_links=[]
     next_agenda=''
     print 'next'
     print url
    
     agenda= soup.find('div',id='agenda-next')
     if agenda != None :
        next_agenda= ((agenda.find('a')['href']).replace('\n','')).replace('\t','')  
        next_link=next_agenda
    
     if next_link in record :         
           next_links= j_events_notrecorded(soup)    
     if len(next_links) > 0 :
          next_link = next_links[0]
          
     
     if next_link not in visited :
         visited.append(next_link)
          
     #event_id=soup.find('input', {'name':'ididid_event_id'})
     retrieve_event_data (soup)
     if next_link not in record and next_link != '' :         
         record.append(next_link)
         next_url = urlparse.urljoin(base_url, next_link)         
         scrape_and_look_for_next_link(next_url)
             
     elif next_link != '' :
          v_links=  verder_events_all(soup)
          for v in v_links :
             if v not in record :
                 verder_links.append(v)       
          if len(verder_links) > 0 :
             first_verder = comparedates(verder_links,soup)
             scrape_and_look_for_previous_link(first_verder)
             scrape_and_look_for_next_link(first_verder)
          else :
            print 'no verder links --- scrape finished'
     else :
          print 'scrape finished'
   except :
    pass     

 
def retrieve_event_data (soup) :    
   
     try :
        movie =''      
        event_name=soup.find('input', {'name':'ididid_event_name'})
        event_id=soup.find('input', {'name':'ididid_event_id'})
        event_date = soup.find('input', {'name':'ididid_event_date'})
        event_end_date=  soup.find('input', {'name':'ididid_event_end_date'})
        event_url= soup.find('input', {'name':'ididid_event_url'})
        event_description = soup.find('input', {'name':'ididid_event_description'})
        #event_movie=soup.find('param',{'name':'movie'})
        event_movie=soup.find('param',{'name':'movie'})
        if event_movie :
            movie= event_movie['value']
        events_ids.append(event_id['value'])

        events = { "ID" : event_id['value'] ,
                   "URL" : event_url['value'],
                   "Name" : event_name['value'],
                   "Date" : event_date['value'],
                   "End date" : event_end_date['value'],
                   "URL" : event_url['value'],
                   "Description" : event_description['value'],
                   "Movie" : movie
                  }
        scraperwiki.datastore.save(["ID"], events )   
     except :
        pass
        


def comparedates(liste , soup):
     date = soup.find('input', {'name':'ididid_event_date'})
     urls = []  
     first_url ='nothing'
     if date :
         datevalue=date['value']
         current_date= datetime.strptime(datevalue, "%d-%m-%Y %H:%M")
         #print current_date
     for event in liste :
         url = urlparse.urljoin(base_url, event)
         html = scraperwiki.scrape(url)
         soup = BeautifulSoup(html)
         date = soup.find('input', {'name':'ididid_event_date'})
         if date :
             datevalue=date['value']
             dt= datetime.strptime(datevalue, "%d-%m-%Y %H:%M")
             delta = dt  - current_date
             if delta.days > 0  :        
                 urls.append(url)
                 #print 'urls'
                 #print urls           
             if len(urls) > 0 :
                 break
     return urls[0]
 
 
def scrape_and_look_for_previous_link(url):
    try :
     html = scraperwiki.scrape(url)
     print 'previous'
     print url   
     soup = BeautifulSoup(html)
     retrieve_event_data (soup)
     previous_agenda=''
     previous_agenda=  ((((soup.find('div',id='agenda-previous')).find('a')['href']).replace('\n','')).replace('\t','')).replace('  ','')
     print previous_agenda
     retrieve_journey_events (soup)
     if previous_agenda not in record  :
            record.append(previous_agenda)
            previous_url = urlparse.urljoin(base_url, previous_agenda)         
            scrape_and_look_for_previous_link(previous_url)        
     else :
         previous_links= j_events_notrecorded(soup)     
         if len(previous_links) > 0 :
             previous_agenda = previous_links[len(previous_links)-1]
             record.append(previous_agenda)
             #print 'previous agenda'
             #print previous_agenda  
             previous_url = urlparse.urljoin(base_url, previous_agenda)         
             scrape_and_look_for_previous_link(previous_url)
         else :
             print 'finished previous'
    except :   
        if previous_agenda in record :
            record.remove(previous_agenda)
        link = select_last_notrecorded_j_event()
        previous_url = urlparse.urljoin(base_url, link )  
        scrape_and_look_for_previous_link(previous_url)
        pass

def select_last_notrecorded_j_event ():
       table = []
       for j in range (0, len(visited)-1):
        if  visited [j] not in record :
           table.append (visited [j])
       return table[len(table)-1]


def merge_visited_record ():
       table=[]   
       for i in range (0, len(record) -1) :
         table.append (record[i])
       for j in range (0, len(visited)-1):
         if visited [j] not in record :
             table.append (visited [j])
             url = urlparse.urljoin(base_url, visited [j])
             try :
                html = scraperwiki.scrape(url)
                soup = BeautifulSoup(html)
                retrieve_event_data(soup)
               
             except :
                pass
       return table
  
def journey_events_all(soup) :
     j_events=[]
     journey_links = []
     journey = soup.findAll('div',{'class':'linklist'})
     for k in range(0,len(journey)) :
          div = journey[k].find('div')
          if div != None :
              text= div.text
              if text=='Deze dag ook in Paradiso' :
                 j_events=journey[k].findAll('a')
                 # print j_events
     for i in j_events:
          link = (i['href'].replace('\n','')).replace('\t','')  
          journey_links.append(link )
     return journey_links


def verder_events_all(soup) :
     v_events=[]
     verder_links = []
     journey = soup.findAll('div',{'class':'linklist'})
     for k in range(0,len(journey)) :
         div = journey[k].find('div')
         if div != None :
             text= div.text
             if text=='Verder in Paradiso' :
               v_events=journey[k].findAll('a')  
     for i in v_events:
          link = ((i['href'].replace('\n','')).replace('\t','')).replace(' ','')  
          verder_links.append(link )
     return verder_links
    
def j_events_notrecorded(soup) :
    next_links=[]
    journey_links = journey_events_all(soup)
    for j in journey_links :
         if j not in record :
              next_links.append(j)
    return next_links

def  retrieve_journey_events (soup) :
    journey_links = journey_events_all(soup)
    for j in journey_links :
          if j not in visited:
               visited.append(j)

#rrrrrrrrrrrrrrrrrr
base_url = 'http://paradiso.nl/'
starting_url  = urlparse.urljoin(base_url,'web/Agenda-Item/Gino-Vannelli-1.htm') #'web/Agenda-Item/Chris-Smither-Peter-Mulvey.htm')
#'web/Agenda-Item/Arbouretum-1.htm'
get_pardiso_events(starting_url)
record.append('web/Agenda-Item/Marianne-Faithfull-1.htm')
 