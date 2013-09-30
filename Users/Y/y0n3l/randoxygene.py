import scraperwiki
from datetime import datetime, date
from httplib import IncompleteRead
from lxml.html.soupparser import fromstring
from os import path
from urllib2 import URLError
import os.path
import urllib
import urllib2

CATEGORY_RANDO_PEDESTRE = 1
CATEGORY_VTT = 2
CATEGORY_CLUES_CANYONS = 3
CATEGORY_RAQUETTES = 4

def stringForCategory(cat):
    if cat==CATEGORY_RANDO_PEDESTRE:
        return u"Rando p\u00E9destre"
    elif cat==CATEGORY_VTT:
        return "VTT"
    elif cat==CATEGORY_CLUES_CANYONS:
        return "Clues et canyons"
    elif cat==CATEGORY_RAQUETTES:
        return "Raquettes"
    else:
        return "UNKNOWN_CATEGORY"

def syncRandosForCategory(categoryType):
    url = 'http://randoxygene.org/pge/cartographie/index.php?rubrique=%d' % (categoryType)
    print "url is " + url
    response = urllib2.urlopen(url)
    html = response.read()
    root = fromstring(html)
    navigation = root.xpath("//div[@id='navigation']")[0]
    areasLevel1 = navigation.xpath("./h1")
    for area1 in areasLevel1:
        n1 = area1.xpath("string(.)")
        print "************* %s **************" % n1 
        #xPathExpress = 
        areas2 = navigation.xpath("./h2[preceding-sibling::h1[1][.='%s']]"%n1)
        for area2 in areas2:
            n2 = area2.xpath("string(.)")
            print n2
            randosUrl = area2.xpath("./following-sibling::ul[1]/li/a/@href")
            for randoUrl in randosUrl:
                url = "http://randoxygene.org/pge/rando_pe/%s" % randoUrl.replace("../rando_pe/","")
                rando = getRandoAtUrl(url)
                rando['areaLevel1'] = n1
                rando['areaLevel2'] = n2
                rando['category']=stringForCategory(categoryType)
                scraperwiki.sqlite.save(unique_keys=["url"], data= rando)

def getRandoAtUrl(url):
    print "syncing " + url
    response = urllib2.urlopen(url)
    html = response.read()
    root = fromstring(html)
    content = root.xpath("//td[@class='col_content']")[0]
    name = content.xpath("string(span[@class='rando_titre']/text())")
    start = content.xpath("string(span[@class='rando_depart']/text())").replace(u"Au d\u00E9part de","")
    description = content.xpath("string(p[@class='rando_description']/text())")
    if description=="":
        description = content.xpath("string(span[@class='rando_itineraire']/text())") 
    itinerary = content.xpath("string(span[@class='rando_itineraire']/text())")
    propertiesTable = root.xpath(u"//th[starts-with(.,'Caract\u00E9ristiques')]/../following-sibling::tr/td/table")[0]
    props = propertiesTable.xpath(".//tr/td[2]")
    place = props[0].xpath("string(.)")
    placeInfo = props[1].xpath("string(.)")
    startAltitude = props[2].xpath("string(.)").replace(u"Alt. au d\u00E9p.","")
    rise = props[3].xpath("string(.)").replace(u"Mont\u00E9e","")
    descent = props[4].xpath("string(.)").replace("Descente","")
    duration = props[5].xpath("string(.)").replace(u"Dur\u00E9e","")
    difficulty = props[6].xpath("string(.)").replace(u"Difficult\u00E9e","")
    bestPeriod = props[7].xpath("string(.)").replace(u"P\u00E9riode conseill\u00E9e","")
    howToGetThere = root.xpath(u"string(//th[starts-with(.,'Acc\u00E8s Routier')]/../following-sibling::tr/td[@class='module_texte']/text())")

    rando = {"url":url, "name":name, "start":start, "description":description, "itinerary":itinerary, "place":place, "placeinfo":placeInfo, "startaltitude":startAltitude, "rise":rise, "descent":descent, "duration":duration, "difficulty":difficulty, "bestperiod":bestPeriod, "howtogetthere":howToGetThere}  
    return rando

def getRando(areaNb, randoNb):
    url = 'http://randoxygene.org/pge/rando_pe/affiche_rando.php?zone=%d&rando=%d' %(areaNb, randoNb)
    return getRandoAtUrl(url)    


syncRandosForCategory(CATEGORY_RANDO_PEDESTRE)
import scraperwiki
from datetime import datetime, date
from httplib import IncompleteRead
from lxml.html.soupparser import fromstring
from os import path
from urllib2 import URLError
import os.path
import urllib
import urllib2

CATEGORY_RANDO_PEDESTRE = 1
CATEGORY_VTT = 2
CATEGORY_CLUES_CANYONS = 3
CATEGORY_RAQUETTES = 4

def stringForCategory(cat):
    if cat==CATEGORY_RANDO_PEDESTRE:
        return u"Rando p\u00E9destre"
    elif cat==CATEGORY_VTT:
        return "VTT"
    elif cat==CATEGORY_CLUES_CANYONS:
        return "Clues et canyons"
    elif cat==CATEGORY_RAQUETTES:
        return "Raquettes"
    else:
        return "UNKNOWN_CATEGORY"

def syncRandosForCategory(categoryType):
    url = 'http://randoxygene.org/pge/cartographie/index.php?rubrique=%d' % (categoryType)
    print "url is " + url
    response = urllib2.urlopen(url)
    html = response.read()
    root = fromstring(html)
    navigation = root.xpath("//div[@id='navigation']")[0]
    areasLevel1 = navigation.xpath("./h1")
    for area1 in areasLevel1:
        n1 = area1.xpath("string(.)")
        print "************* %s **************" % n1 
        #xPathExpress = 
        areas2 = navigation.xpath("./h2[preceding-sibling::h1[1][.='%s']]"%n1)
        for area2 in areas2:
            n2 = area2.xpath("string(.)")
            print n2
            randosUrl = area2.xpath("./following-sibling::ul[1]/li/a/@href")
            for randoUrl in randosUrl:
                url = "http://randoxygene.org/pge/rando_pe/%s" % randoUrl.replace("../rando_pe/","")
                rando = getRandoAtUrl(url)
                rando['areaLevel1'] = n1
                rando['areaLevel2'] = n2
                rando['category']=stringForCategory(categoryType)
                scraperwiki.sqlite.save(unique_keys=["url"], data= rando)

def getRandoAtUrl(url):
    print "syncing " + url
    response = urllib2.urlopen(url)
    html = response.read()
    root = fromstring(html)
    content = root.xpath("//td[@class='col_content']")[0]
    name = content.xpath("string(span[@class='rando_titre']/text())")
    start = content.xpath("string(span[@class='rando_depart']/text())").replace(u"Au d\u00E9part de","")
    description = content.xpath("string(p[@class='rando_description']/text())")
    if description=="":
        description = content.xpath("string(span[@class='rando_itineraire']/text())") 
    itinerary = content.xpath("string(span[@class='rando_itineraire']/text())")
    propertiesTable = root.xpath(u"//th[starts-with(.,'Caract\u00E9ristiques')]/../following-sibling::tr/td/table")[0]
    props = propertiesTable.xpath(".//tr/td[2]")
    place = props[0].xpath("string(.)")
    placeInfo = props[1].xpath("string(.)")
    startAltitude = props[2].xpath("string(.)").replace(u"Alt. au d\u00E9p.","")
    rise = props[3].xpath("string(.)").replace(u"Mont\u00E9e","")
    descent = props[4].xpath("string(.)").replace("Descente","")
    duration = props[5].xpath("string(.)").replace(u"Dur\u00E9e","")
    difficulty = props[6].xpath("string(.)").replace(u"Difficult\u00E9e","")
    bestPeriod = props[7].xpath("string(.)").replace(u"P\u00E9riode conseill\u00E9e","")
    howToGetThere = root.xpath(u"string(//th[starts-with(.,'Acc\u00E8s Routier')]/../following-sibling::tr/td[@class='module_texte']/text())")

    rando = {"url":url, "name":name, "start":start, "description":description, "itinerary":itinerary, "place":place, "placeinfo":placeInfo, "startaltitude":startAltitude, "rise":rise, "descent":descent, "duration":duration, "difficulty":difficulty, "bestperiod":bestPeriod, "howtogetthere":howToGetThere}  
    return rando

def getRando(areaNb, randoNb):
    url = 'http://randoxygene.org/pge/rando_pe/affiche_rando.php?zone=%d&rando=%d' %(areaNb, randoNb)
    return getRandoAtUrl(url)    


syncRandosForCategory(CATEGORY_RANDO_PEDESTRE)
