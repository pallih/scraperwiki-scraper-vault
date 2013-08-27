from BeautifulSoup import BeautifulSoup
import scraperwiki
import xmltodict
import urllib

#url = "http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml"
#result = urlopen('http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml');
example = urllib.urlopen('http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml')
#doc = xmltodict.parse(example)
#doc = xmltodict.parse(example,attr_prefix='_') 
#xml_attribs=False
feed = xmltodict.parse(example,xml_attribs=False) 
#print doc
#whatnow?
article = {}

#for item in items:
doc = {}
doc = feed['rss']['channel']['item']
#print docs
#print items
#print items[2]
#for doc in docs: #.keys()
for key, value in doc.iteritems():
    #print doc

    article['title'] = doc['title'] #[0]
    article['link'] = doc['link'] #[0]
    article['desc'] = doc['ol'] #['#text']
    article['guid'] = doc['guid']
    article['pubdate'] = doc['pubDate']
    article['liveDate'] = doc['pi:liveDate']
    article['activity'] = doc['pi:activity']    
    article['screenshot'] = doc['pi:screenshot']    
    article['source'] = doc['source']    
    #article['tags'] = doc['pi:tags']
    tags = {}
    article['tags'] = doc['pi:tags']
    if doc['pi:tags'] is not None:         
        tags = doc['pi:tags']
        #print tags
        for tag in tags:
            #print tag
            article['tag'] = tags['pi:tag']
    #article['tag'] = tag['pi:tag'] #['agenda_tag'] # #[0]
       # article['tag'] = xtag['pi:tag']
 #  article['tags'] = doc['pi:tags'] 
    
    article['agenda'] = doc['pi:agenda']    
    #article['tags'] = doc['pi:tags']
    #if doc['pi:agenda'] is not None:
    #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time'] is not None:      
        #agendaitems = doc['pi:agenda']
        #print agendaitems
        #for agendaitem in agendaitems:
        #print agendaitems
        #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:
            #print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id']
            #article['agendaid'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id']
        #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text'] is not None:
            #print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text']      
            #article['agendatext'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text']
        #article['agendatime'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time'] is not None: 
            #print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #myvar = doc['pi:agenda']['pi:agenda_item']['pi:agenda_time']
        #try:
        #    print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id']
        #    article['agendatime'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id']
        #except KeyError:
        #    print "no time"

        #try:
        #    print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text']  
        #    article['agendatime'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text']  
        #except KeyError:
        #    print "no time"

        #try:
        #    print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #    article['agendatime'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #except KeyError:
        #    print "no time"
    
    
    agenda = {}
    #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:      
    if doc['pi:agenda'] is not None:     
        agendas = doc['pi:agenda']
            #print tags
        
        agendaitem = {}
        #for agenda in agendas: #.keys():
        for key, value in agendas.iteritems():
    #print key, value
            
            agendaitems = agendas['pi:agenda_item'] #['#text']
            print agendaitems
      #      try:
       #     #print tag
       #         print "agendaitems"
       #         print  agendaitems['pi:agenda_item']                
       #         article['agendaitem'] = agendaitems['pi:agenda_item']
       #     except KeyError:
       #         print "no agenda"
        #article['tags'] = doc['pi:tags']
    
    #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:      
        #if doc['pi:agenda']['pi:agenda_item'] is not None:     
        #agendaitems = doc['pi:agenda']
            #print tags
        #for agendaitem in agendaitems:
            #print tag
            #for agendaitem in agendaitems:
            for key, value in agendaitems.iteritems():
                try:
                    print "agendatext"
                    print agendaitems['pi:agenda_text'] #['#text']
                    article['agendatext'] = agendaitems['pi:agenda_text'] #['#text']
                except KeyError:
                    print "no text"
    
        #article['agenda'] = doc['pi:agenda']
    #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:      
        #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:     
        #agendaitems = doc['pi:agenda']
            #print tags
        #for agendaitem in agendaitems:
            #print tag
                try:
                    print "agenda_id"
                    print agendaitems['pi:agenda_id']
                    article['agendaid'] = agendaitems['pi:agenda_id']
                except KeyError:
                    print "no id"
    else:
        print "no agenda"
           # article['agendatext'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #article['agendaid'] = agendaitems['pi:agenda_item']['pi:agenda_id']['#text']
        #article['agendatext'] = agendaitems['pi:agenda_item']['pi:agenda_text']['#text']
        #print article['agendatext']
    
    
    scraperwiki.sqlite.save(["title"], article)from BeautifulSoup import BeautifulSoup
import scraperwiki
import xmltodict
import urllib

#url = "http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml"
#result = urlopen('http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml');
example = urllib.urlopen('http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml')
#doc = xmltodict.parse(example)
#doc = xmltodict.parse(example,attr_prefix='_') 
#xml_attribs=False
feed = xmltodict.parse(example,xml_attribs=False) 
#print doc
#whatnow?
article = {}

#for item in items:
doc = {}
doc = feed['rss']['channel']['item']
#print docs
#print items
#print items[2]
#for doc in docs: #.keys()
for key, value in doc.iteritems():
    #print doc

    article['title'] = doc['title'] #[0]
    article['link'] = doc['link'] #[0]
    article['desc'] = doc['ol'] #['#text']
    article['guid'] = doc['guid']
    article['pubdate'] = doc['pubDate']
    article['liveDate'] = doc['pi:liveDate']
    article['activity'] = doc['pi:activity']    
    article['screenshot'] = doc['pi:screenshot']    
    article['source'] = doc['source']    
    #article['tags'] = doc['pi:tags']
    tags = {}
    article['tags'] = doc['pi:tags']
    if doc['pi:tags'] is not None:         
        tags = doc['pi:tags']
        #print tags
        for tag in tags:
            #print tag
            article['tag'] = tags['pi:tag']
    #article['tag'] = tag['pi:tag'] #['agenda_tag'] # #[0]
       # article['tag'] = xtag['pi:tag']
 #  article['tags'] = doc['pi:tags'] 
    
    article['agenda'] = doc['pi:agenda']    
    #article['tags'] = doc['pi:tags']
    #if doc['pi:agenda'] is not None:
    #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time'] is not None:      
        #agendaitems = doc['pi:agenda']
        #print agendaitems
        #for agendaitem in agendaitems:
        #print agendaitems
        #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:
            #print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id']
            #article['agendaid'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id']
        #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text'] is not None:
            #print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text']      
            #article['agendatext'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text']
        #article['agendatime'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time'] is not None: 
            #print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #myvar = doc['pi:agenda']['pi:agenda_item']['pi:agenda_time']
        #try:
        #    print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id']
        #    article['agendatime'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id']
        #except KeyError:
        #    print "no time"

        #try:
        #    print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text']  
        #    article['agendatime'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text']  
        #except KeyError:
        #    print "no time"

        #try:
        #    print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #    article['agendatime'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #except KeyError:
        #    print "no time"
    
    
    agenda = {}
    #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:      
    if doc['pi:agenda'] is not None:     
        agendas = doc['pi:agenda']
            #print tags
        
        agendaitem = {}
        #for agenda in agendas: #.keys():
        for key, value in agendas.iteritems():
    #print key, value
            
            agendaitems = agendas['pi:agenda_item'] #['#text']
            print agendaitems
      #      try:
       #     #print tag
       #         print "agendaitems"
       #         print  agendaitems['pi:agenda_item']                
       #         article['agendaitem'] = agendaitems['pi:agenda_item']
       #     except KeyError:
       #         print "no agenda"
        #article['tags'] = doc['pi:tags']
    
    #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:      
        #if doc['pi:agenda']['pi:agenda_item'] is not None:     
        #agendaitems = doc['pi:agenda']
            #print tags
        #for agendaitem in agendaitems:
            #print tag
            #for agendaitem in agendaitems:
            for key, value in agendaitems.iteritems():
                try:
                    print "agendatext"
                    print agendaitems['pi:agenda_text'] #['#text']
                    article['agendatext'] = agendaitems['pi:agenda_text'] #['#text']
                except KeyError:
                    print "no text"
    
        #article['agenda'] = doc['pi:agenda']
    #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:      
        #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:     
        #agendaitems = doc['pi:agenda']
            #print tags
        #for agendaitem in agendaitems:
            #print tag
                try:
                    print "agenda_id"
                    print agendaitems['pi:agenda_id']
                    article['agendaid'] = agendaitems['pi:agenda_id']
                except KeyError:
                    print "no id"
    else:
        print "no agenda"
           # article['agendatext'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #article['agendaid'] = agendaitems['pi:agenda_item']['pi:agenda_id']['#text']
        #article['agendatext'] = agendaitems['pi:agenda_item']['pi:agenda_text']['#text']
        #print article['agendatext']
    
    
    scraperwiki.sqlite.save(["title"], article)from BeautifulSoup import BeautifulSoup
import scraperwiki
import xmltodict
import urllib

#url = "http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml"
#result = urlopen('http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml');
example = urllib.urlopen('http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml')
#doc = xmltodict.parse(example)
#doc = xmltodict.parse(example,attr_prefix='_') 
#xml_attribs=False
feed = xmltodict.parse(example,xml_attribs=False) 
#print doc
#whatnow?
article = {}

#for item in items:
doc = {}
doc = feed['rss']['channel']['item']
#print docs
#print items
#print items[2]
#for doc in docs: #.keys()
for key, value in doc.iteritems():
    #print doc

    article['title'] = doc['title'] #[0]
    article['link'] = doc['link'] #[0]
    article['desc'] = doc['ol'] #['#text']
    article['guid'] = doc['guid']
    article['pubdate'] = doc['pubDate']
    article['liveDate'] = doc['pi:liveDate']
    article['activity'] = doc['pi:activity']    
    article['screenshot'] = doc['pi:screenshot']    
    article['source'] = doc['source']    
    #article['tags'] = doc['pi:tags']
    tags = {}
    article['tags'] = doc['pi:tags']
    if doc['pi:tags'] is not None:         
        tags = doc['pi:tags']
        #print tags
        for tag in tags:
            #print tag
            article['tag'] = tags['pi:tag']
    #article['tag'] = tag['pi:tag'] #['agenda_tag'] # #[0]
       # article['tag'] = xtag['pi:tag']
 #  article['tags'] = doc['pi:tags'] 
    
    article['agenda'] = doc['pi:agenda']    
    #article['tags'] = doc['pi:tags']
    #if doc['pi:agenda'] is not None:
    #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time'] is not None:      
        #agendaitems = doc['pi:agenda']
        #print agendaitems
        #for agendaitem in agendaitems:
        #print agendaitems
        #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:
            #print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id']
            #article['agendaid'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id']
        #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text'] is not None:
            #print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text']      
            #article['agendatext'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text']
        #article['agendatime'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time'] is not None: 
            #print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #myvar = doc['pi:agenda']['pi:agenda_item']['pi:agenda_time']
        #try:
        #    print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id']
        #    article['agendatime'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id']
        #except KeyError:
        #    print "no time"

        #try:
        #    print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text']  
        #    article['agendatime'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_text']  
        #except KeyError:
        #    print "no time"

        #try:
        #    print doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #    article['agendatime'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #except KeyError:
        #    print "no time"
    
    
    agenda = {}
    #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:      
    if doc['pi:agenda'] is not None:     
        agendas = doc['pi:agenda']
            #print tags
        
        agendaitem = {}
        #for agenda in agendas: #.keys():
        for key, value in agendas.iteritems():
    #print key, value
            
            agendaitems = agendas['pi:agenda_item'] #['#text']
            print agendaitems
      #      try:
       #     #print tag
       #         print "agendaitems"
       #         print  agendaitems['pi:agenda_item']                
       #         article['agendaitem'] = agendaitems['pi:agenda_item']
       #     except KeyError:
       #         print "no agenda"
        #article['tags'] = doc['pi:tags']
    
    #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:      
        #if doc['pi:agenda']['pi:agenda_item'] is not None:     
        #agendaitems = doc['pi:agenda']
            #print tags
        #for agendaitem in agendaitems:
            #print tag
            #for agendaitem in agendaitems:
            for key, value in agendaitems.iteritems():
                try:
                    print "agendatext"
                    print agendaitems['pi:agenda_text'] #['#text']
                    article['agendatext'] = agendaitems['pi:agenda_text'] #['#text']
                except KeyError:
                    print "no text"
    
        #article['agenda'] = doc['pi:agenda']
    #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:      
        #if doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_id'] is not None:     
        #agendaitems = doc['pi:agenda']
            #print tags
        #for agendaitem in agendaitems:
            #print tag
                try:
                    print "agenda_id"
                    print agendaitems['pi:agenda_id']
                    article['agendaid'] = agendaitems['pi:agenda_id']
                except KeyError:
                    print "no id"
    else:
        print "no agenda"
           # article['agendatext'] = doc['pi:agenda']['pi:agenda_item'][0]['pi:agenda_time']
        #article['agendaid'] = agendaitems['pi:agenda_item']['pi:agenda_id']['#text']
        #article['agendatext'] = agendaitems['pi:agenda_item']['pi:agenda_text']['#text']
        #print article['agendatext']
    
    
    scraperwiki.sqlite.save(["title"], article)