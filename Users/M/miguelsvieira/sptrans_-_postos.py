# Blank Python
import scraperwiki
html = scraperwiki.scrape("http://200.99.150.170/PlanOperWeb/resultadoLocaisProximos2.asp?ExibirMapa=0&x=15&y=2&DfLogIDPostoAutorizado=1&numopcoes=5&MostrarTodos=1&TpNotID=100")

import re
map_re = re.compile(r'ABInfSvItiGoogleM.*\d{4}')
lat_re = re.compile(r'v_NotLat = .-\d{7}.')
long_re = re.compile(r'v_NotLong = .-\d{7}.')
import lxml.html
root = lxml.html.fromstring(html.replace("html",""))
for li in root.cssselect("#resultados li"):
    strngs = li.cssselect("strong")
    #data = {}
    
    data = {"name":strngs[0].text}  

    data["name"] = strngs[0].text
    data["address"] = strngs[1].tail
    data["hours"] = strngs[2].tail

    link = map_re.search(lxml.html.tostring(li))
    map_url = "http://200.99.150.170/PlanOperWeb/"+link.group(0).replace("[separador]", "&")
    
    map_html = scraperwiki.scrape(map_url)

    lat = lat_re.search(map_html)
    data["latitude"] = lat.group(0)[12:15] + "." + lat.group(0)[15:22]
#    data["latitude"] = lat.group(0)[12:22]
 
    long = long_re.search(map_html)
    data["longitude"] = long.group(0)[13:16] + "." + long.group(0)[16:23]
#    data["longitude"] = long.group(0)[13:23]
 
    scraperwiki.sqlite.save(unique_keys=['name'], data=data)# Blank Python
import scraperwiki
html = scraperwiki.scrape("http://200.99.150.170/PlanOperWeb/resultadoLocaisProximos2.asp?ExibirMapa=0&x=15&y=2&DfLogIDPostoAutorizado=1&numopcoes=5&MostrarTodos=1&TpNotID=100")

import re
map_re = re.compile(r'ABInfSvItiGoogleM.*\d{4}')
lat_re = re.compile(r'v_NotLat = .-\d{7}.')
long_re = re.compile(r'v_NotLong = .-\d{7}.')
import lxml.html
root = lxml.html.fromstring(html.replace("html",""))
for li in root.cssselect("#resultados li"):
    strngs = li.cssselect("strong")
    #data = {}
    
    data = {"name":strngs[0].text}  

    data["name"] = strngs[0].text
    data["address"] = strngs[1].tail
    data["hours"] = strngs[2].tail

    link = map_re.search(lxml.html.tostring(li))
    map_url = "http://200.99.150.170/PlanOperWeb/"+link.group(0).replace("[separador]", "&")
    
    map_html = scraperwiki.scrape(map_url)

    lat = lat_re.search(map_html)
    data["latitude"] = lat.group(0)[12:15] + "." + lat.group(0)[15:22]
#    data["latitude"] = lat.group(0)[12:22]
 
    long = long_re.search(map_html)
    data["longitude"] = long.group(0)[13:16] + "." + long.group(0)[16:23]
#    data["longitude"] = long.group(0)[13:23]
 
    scraperwiki.sqlite.save(unique_keys=['name'], data=data)