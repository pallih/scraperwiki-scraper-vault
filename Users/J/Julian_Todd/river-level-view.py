#########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "environment-agency-river-level-monitors"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 200  
offset = 0

m = list(getData(sourcescraper, limit, offset))

def ks(a):
    v = a.get('proportion')
    if not v:
        return 0.0
    return -float(v)

m.sort(key=ks)
for a in m[:200]:
    if not a.get('low'):
        continue
    low = float(a.get('low'))
    high = float(a.get('high'))
    level = float(a.get('level'))
    proportion= float(a.get('proportion'))
    letter = level >0.5 and "W" or "L"
    img = "http://www.ocean30.us/idx/prop-list.html?page=1" % (int(proportion*100))

    #print "<tr><td>%s</td><td><a href=\"%s\">%s</a></td><td>%s" % (a["proportion"], a["url"], 
    print '<span>%s <img src="%s"></span>' % (a["River"], img)


    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "environment-agency-river-level-monitors"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 200  
offset = 0

m = list(getData(sourcescraper, limit, offset))

def ks(a):
    v = a.get('proportion')
    if not v:
        return 0.0
    return -float(v)

m.sort(key=ks)
for a in m[:200]:
    if not a.get('low'):
        continue
    low = float(a.get('low'))
    high = float(a.get('high'))
    level = float(a.get('level'))
    proportion= float(a.get('proportion'))
    letter = level >0.5 and "W" or "L"
    img = "http://www.ocean30.us/idx/prop-list.html?page=1" % (int(proportion*100))

    #print "<tr><td>%s</td><td><a href=\"%s\">%s</a></td><td>%s" % (a["proportion"], a["url"], 
    print '<span>%s <img src="%s"></span>' % (a["River"], img)


    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "environment-agency-river-level-monitors"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 200  
offset = 0

m = list(getData(sourcescraper, limit, offset))

def ks(a):
    v = a.get('proportion')
    if not v:
        return 0.0
    return -float(v)

m.sort(key=ks)
for a in m[:200]:
    if not a.get('low'):
        continue
    low = float(a.get('low'))
    high = float(a.get('high'))
    level = float(a.get('level'))
    proportion= float(a.get('proportion'))
    letter = level >0.5 and "W" or "L"
    img = "http://www.ocean30.us/idx/prop-list.html?page=1" % (int(proportion*100))

    #print "<tr><td>%s</td><td><a href=\"%s\">%s</a></td><td>%s" % (a["proportion"], a["url"], 
    print '<span>%s <img src="%s"></span>' % (a["River"], img)


    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "environment-agency-river-level-monitors"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 200  
offset = 0

m = list(getData(sourcescraper, limit, offset))

def ks(a):
    v = a.get('proportion')
    if not v:
        return 0.0
    return -float(v)

m.sort(key=ks)
for a in m[:200]:
    if not a.get('low'):
        continue
    low = float(a.get('low'))
    high = float(a.get('high'))
    level = float(a.get('level'))
    proportion= float(a.get('proportion'))
    letter = level >0.5 and "W" or "L"
    img = "http://www.ocean30.us/idx/prop-list.html?page=1" % (int(proportion*100))

    #print "<tr><td>%s</td><td><a href=\"%s\">%s</a></td><td>%s" % (a["proportion"], a["url"], 
    print '<span>%s <img src="%s"></span>' % (a["River"], img)


    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "environment-agency-river-level-monitors"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 200  
offset = 0

m = list(getData(sourcescraper, limit, offset))

def ks(a):
    v = a.get('proportion')
    if not v:
        return 0.0
    return -float(v)

m.sort(key=ks)
for a in m[:200]:
    if not a.get('low'):
        continue
    low = float(a.get('low'))
    high = float(a.get('high'))
    level = float(a.get('level'))
    proportion= float(a.get('proportion'))
    letter = level >0.5 and "W" or "L"
    img = "http://www.ocean30.us/idx/prop-list.html?page=1" % (int(proportion*100))

    #print "<tr><td>%s</td><td><a href=\"%s\">%s</a></td><td>%s" % (a["proportion"], a["url"], 
    print '<span>%s <img src="%s"></span>' % (a["River"], img)


    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "environment-agency-river-level-monitors"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 200  
offset = 0

m = list(getData(sourcescraper, limit, offset))

def ks(a):
    v = a.get('proportion')
    if not v:
        return 0.0
    return -float(v)

m.sort(key=ks)
for a in m[:200]:
    if not a.get('low'):
        continue
    low = float(a.get('low'))
    high = float(a.get('high'))
    level = float(a.get('level'))
    proportion= float(a.get('proportion'))
    letter = level >0.5 and "W" or "L"
    img = "http://www.ocean30.us/idx/prop-list.html?page=1" % (int(proportion*100))

    #print "<tr><td>%s</td><td><a href=\"%s\">%s</a></td><td>%s" % (a["proportion"], a["url"], 
    print '<span>%s <img src="%s"></span>' % (a["River"], img)


    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "environment-agency-river-level-monitors"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 200  
offset = 0

m = list(getData(sourcescraper, limit, offset))

def ks(a):
    v = a.get('proportion')
    if not v:
        return 0.0
    return -float(v)

m.sort(key=ks)
for a in m[:200]:
    if not a.get('low'):
        continue
    low = float(a.get('low'))
    high = float(a.get('high'))
    level = float(a.get('level'))
    proportion= float(a.get('proportion'))
    letter = level >0.5 and "W" or "L"
    img = "http://www.ocean30.us/idx/prop-list.html?page=1" % (int(proportion*100))

    #print "<tr><td>%s</td><td><a href=\"%s\">%s</a></td><td>%s" % (a["proportion"], a["url"], 
    print '<span>%s <img src="%s"></span>' % (a["River"], img)


    