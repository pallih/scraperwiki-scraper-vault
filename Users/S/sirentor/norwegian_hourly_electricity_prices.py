import scraperwiki
from datetime import datetime 
import lxml.html, re 
import urllib2  
for city in ["trondheim", "oslo", "tromso", "kristiansand", "bergen" ]:
    url = "http://wwwdynamic.nordpoolspot.com/marketinfo/elspot/" + city + "/elspot.cgi?interval=last8&ccurrency=eur&type=html"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)     
    nodes = root.cssselect("td")      
    price = []     
    for node in nodes[8::9]: # We fetch every 9th number to get all contents of column number 9         
        if node.text != None:             
            result = node.text.strip()
            if re.match(r"^(\d+)\.(\d+)\.(\d+)$",result ) != None:      # Dates are at the following format xx.xx.xx
                dato = result
            if re.match(r"^(\d+)\.(\d+)$", result) != None: #Prices are at the following format xx.xx 
                price.append(result)    

    data = { 
            'DateAndCity' : dato + "_" + city,      
            'Price' : price,             
            }  
    scraperwiki.sqlite.save(unique_keys=['DateAndCity'],data=data)  import scraperwiki
from datetime import datetime 
import lxml.html, re 
import urllib2  
for city in ["trondheim", "oslo", "tromso", "kristiansand", "bergen" ]:
    url = "http://wwwdynamic.nordpoolspot.com/marketinfo/elspot/" + city + "/elspot.cgi?interval=last8&ccurrency=eur&type=html"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)     
    nodes = root.cssselect("td")      
    price = []     
    for node in nodes[8::9]: # We fetch every 9th number to get all contents of column number 9         
        if node.text != None:             
            result = node.text.strip()
            if re.match(r"^(\d+)\.(\d+)\.(\d+)$",result ) != None:      # Dates are at the following format xx.xx.xx
                dato = result
            if re.match(r"^(\d+)\.(\d+)$", result) != None: #Prices are at the following format xx.xx 
                price.append(result)    

    data = { 
            'DateAndCity' : dato + "_" + city,      
            'Price' : price,             
            }  
    scraperwiki.sqlite.save(unique_keys=['DateAndCity'],data=data)  