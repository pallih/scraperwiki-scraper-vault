import scraperwiki
import sys
import lxml.html
from urllib import urlencode
import json
import re
import time
from BeautifulSoup import BeautifulSoup

#Importa elenco Aziende, in base al CAP

def get_href(el):
    match = re.search(r'href=[\'"]?([^\'" >]+)', str(el))
    if match:
        match = "/" + match.group(0).replace ('"','').replace ('href=','')
        match = match.replace ("//","/")
        return  match
    else:
        return ''


scraperwiki.sqlite.attach("elencocapitalia")
data = scraperwiki.sqlite.select(           
    '''distinct CAP from ElencoCapItalia.swdata 
   '''
)

for d in data:
    searchURL = "http://www.youinweb.it/profiles_it/" + d["CAP"]
    
    try:
        html = scraperwiki.scrape(searchURL)
        time.sleep(1) # don't overload
        html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
        tables = html.findAll('table')
    except:
        sys.exc_clear()
        
            
    rows = tables[0].findAll('tr')
    li = {}
    for row in rows:
        try:
            cells = row.findChildren('td')

            #print cells[1].text
            URL = searchURL+get_href (cells[1])
            #print URL
            li['CAP'] = d["CAP"]
            li['URL'] = URL
            scraperwiki.sqlite.save(unique_keys=['URL'], data=li)

        except:
            sys.exc_clear()
