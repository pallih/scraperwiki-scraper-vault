import scraperwiki
import simplejson
import re

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'chanchosUY'
options = '&rpp=100&page='
page = 1
regexpChoque = '(.*)(choque|accidente|piña)(.*)'
regexpChanchos = '(.*)(chanchos|caminera|radar|Cami)(.*)'
regexpNiebla = '(.*)(niebla|visibilidad)(.*)'


while 1:
    try:

        url = base_url + q + options + str(page)
        html = scraperwiki.scrape(url)
        #print html
        soup = simplejson.loads(html)
        for result in soup['results']:
            data = {}
            data['id'] = result['id']
            texto = result['text']
            texto = re.sub("(.*)(\RT @.*?:) (.*)", "\\3", texto)            
            texto = re.sub("(.*)(\@.*?) (.*)", "\\3", texto)
            hayMatch = re.search(regexpChoque ,texto)
            if (hayMatch > 0): 
                tipo = 'accidente' 
            elif (re.search(regexpChanchos ,texto) > 0) :              
                tipo = 'chanchos' 
            elif (re.search(regexpNiebla ,texto) > 0) :              
                tipo = 'visibilidad' 
            else:
                tipo = 'otro'
                
            data['tipo '] = tipo 
            
            
            
            
            # print data['tipo'], "-> ",texto
            data['text'] = texto
            # data['from_user'] = result['from_user']
            data['GMap'] = "http://maps.google.com/maps?q='" + texto + "'"
            # print data['GMap']
            data['created_at']= result['created_at']   
            


            # save records to the datastore
            scraperwiki.sqlite.save(["id"], data) 
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        break# Blank Pythonimport scraperwiki
import simplejson
import re

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'chanchosUY'
options = '&rpp=100&page='
page = 1
regexpChoque = '(.*)(choque|accidente|piña)(.*)'
regexpChanchos = '(.*)(chanchos|caminera|radar|Cami)(.*)'
regexpNiebla = '(.*)(niebla|visibilidad)(.*)'


while 1:
    try:

        url = base_url + q + options + str(page)
        html = scraperwiki.scrape(url)
        #print html
        soup = simplejson.loads(html)
        for result in soup['results']:
            data = {}
            data['id'] = result['id']
            texto = result['text']
            texto = re.sub("(.*)(\RT @.*?:) (.*)", "\\3", texto)            
            texto = re.sub("(.*)(\@.*?) (.*)", "\\3", texto)
            hayMatch = re.search(regexpChoque ,texto)
            if (hayMatch > 0): 
                tipo = 'accidente' 
            elif (re.search(regexpChanchos ,texto) > 0) :              
                tipo = 'chanchos' 
            elif (re.search(regexpNiebla ,texto) > 0) :              
                tipo = 'visibilidad' 
            else:
                tipo = 'otro'
                
            data['tipo '] = tipo 
            
            
            
            
            # print data['tipo'], "-> ",texto
            data['text'] = texto
            # data['from_user'] = result['from_user']
            data['GMap'] = "http://maps.google.com/maps?q='" + texto + "'"
            # print data['GMap']
            data['created_at']= result['created_at']   
            


            # save records to the datastore
            scraperwiki.sqlite.save(["id"], data) 
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        break# Blank Python