###########################################################################################
# scraper for http://www.statistik-berlin-brandenburg.de/Statistiken/inhalt-statistiken.asp
###########################################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import BeautifulSoup
from sets import Set

def run(url):
        visited = Set()
        #indicators = Set(['http://www.statistik-berlin-brandenburg.de/BasisZeitreiheGrafik/Zeit-Mikrozensus.asp?Ptyp=400&Sageb=12002&creg=BBB&anzwer=2'])
        indicators = Set()
        #'''
        queue = [url]
        while len(queue)>0:
            url = queue.pop()
            html = scraperwiki.scrape(url)
            soup = BeautifulSoup(html)
            topics_div = soup.find('div',id='mid-col-1')
            topics_table = topics_div.find('table')
            topics_a = topics_table.findAll('a')
            for topic in topics_a:
                href = topic['href']
                if topic.text == "Pressemitteilungen":
                    continue
                if topic.text == "Zeitreihen":
                    indicators.add('http://www.statistik-berlin-brandenburg.de/statistiken/'+href)      
                t = re.match(r".*Ptyp=(100|300).*", href)
                if t!=None:
                    id = re.match(r".*&Sageb=(?P<id>\w+)&.*", href).group('id')
                    if id not in visited:
                        visited.add(id)
                        queue.insert(0, 'http://www.statistik-berlin-brandenburg.de/statistiken/'+href)
        #'''
        #print len(indicators)
        for url in indicators:
            #print url
            html = scraperwiki.scrape(url)
            soup = BeautifulSoup(html)
            indicators_div = soup.find('div',id='mid-col-2')
            indicators_table = indicators_div.findAll('table')[1]
            [sup.extract() for sup in indicators_table.findAll('sup')]
            thead = indicators_table.find('thead')
            if thead != None:
                rows = indicators_table.thead.findAllNext('tr')             
            else:
                rows = indicators_table.findAll('tr')         
            topic_id = re.match(r".*&Sageb=(?P<topic_id>\w+)&.*", url).group('topic_id')
            counter = 1
            name = None
            for row in rows:
                row = BeautifulStoneSoup(str(row),convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
                col = row.find('td',{ "class" : "tabl-leer"})
                if col != None:
                    name= None
                    continue
                col = row.find('td',{ "class" : "ueber1-center" })                
                if col != None:                    
                    name = col.text
                    #print name
                    id = topic_id+str(counter)
                    counter = counter+1
                    continue
                if name != None:
                    cols = row.findAll(['th','td'])
                    if len(cols)==4:
                        value = cols[1].text.replace(' ','').replace(',','.')
                        record = {'indicator_id':id,'indicator_name':name,'topic_id':topic_id,'date': cols[0].text,'country':'DE','NUTS_name':'Berlin','NUTS_code':'DE3','value':value}
                        scraperwiki.datastore.save(['indicator_id','date','NUTS_code'], record)
                        value = cols[2].text.replace(' ','').replace(',','.')
                        record = {'indicator_id':id,'indicator_name':name,'topic_id':topic_id,'date': cols[0].text,'country':'DE','NUTS_name':'Brandenburg','NUTS_code':'DE4','value':value}
                        scraperwiki.datastore.save(['indicator_id','date','NUTS_code'], record)

#print "begin"
run('http://www.statistik-berlin-brandenburg.de/statistiken/inhalt-statistiken.asp')
#print "end"

    ###########################################################################################
# scraper for http://www.statistik-berlin-brandenburg.de/Statistiken/inhalt-statistiken.asp
###########################################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import BeautifulSoup
from sets import Set

def run(url):
        visited = Set()
        #indicators = Set(['http://www.statistik-berlin-brandenburg.de/BasisZeitreiheGrafik/Zeit-Mikrozensus.asp?Ptyp=400&Sageb=12002&creg=BBB&anzwer=2'])
        indicators = Set()
        #'''
        queue = [url]
        while len(queue)>0:
            url = queue.pop()
            html = scraperwiki.scrape(url)
            soup = BeautifulSoup(html)
            topics_div = soup.find('div',id='mid-col-1')
            topics_table = topics_div.find('table')
            topics_a = topics_table.findAll('a')
            for topic in topics_a:
                href = topic['href']
                if topic.text == "Pressemitteilungen":
                    continue
                if topic.text == "Zeitreihen":
                    indicators.add('http://www.statistik-berlin-brandenburg.de/statistiken/'+href)      
                t = re.match(r".*Ptyp=(100|300).*", href)
                if t!=None:
                    id = re.match(r".*&Sageb=(?P<id>\w+)&.*", href).group('id')
                    if id not in visited:
                        visited.add(id)
                        queue.insert(0, 'http://www.statistik-berlin-brandenburg.de/statistiken/'+href)
        #'''
        #print len(indicators)
        for url in indicators:
            #print url
            html = scraperwiki.scrape(url)
            soup = BeautifulSoup(html)
            indicators_div = soup.find('div',id='mid-col-2')
            indicators_table = indicators_div.findAll('table')[1]
            [sup.extract() for sup in indicators_table.findAll('sup')]
            thead = indicators_table.find('thead')
            if thead != None:
                rows = indicators_table.thead.findAllNext('tr')             
            else:
                rows = indicators_table.findAll('tr')         
            topic_id = re.match(r".*&Sageb=(?P<topic_id>\w+)&.*", url).group('topic_id')
            counter = 1
            name = None
            for row in rows:
                row = BeautifulStoneSoup(str(row),convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
                col = row.find('td',{ "class" : "tabl-leer"})
                if col != None:
                    name= None
                    continue
                col = row.find('td',{ "class" : "ueber1-center" })                
                if col != None:                    
                    name = col.text
                    #print name
                    id = topic_id+str(counter)
                    counter = counter+1
                    continue
                if name != None:
                    cols = row.findAll(['th','td'])
                    if len(cols)==4:
                        value = cols[1].text.replace(' ','').replace(',','.')
                        record = {'indicator_id':id,'indicator_name':name,'topic_id':topic_id,'date': cols[0].text,'country':'DE','NUTS_name':'Berlin','NUTS_code':'DE3','value':value}
                        scraperwiki.datastore.save(['indicator_id','date','NUTS_code'], record)
                        value = cols[2].text.replace(' ','').replace(',','.')
                        record = {'indicator_id':id,'indicator_name':name,'topic_id':topic_id,'date': cols[0].text,'country':'DE','NUTS_name':'Brandenburg','NUTS_code':'DE4','value':value}
                        scraperwiki.datastore.save(['indicator_id','date','NUTS_code'], record)

#print "begin"
run('http://www.statistik-berlin-brandenburg.de/statistiken/inhalt-statistiken.asp')
#print "end"

    