import urllib2
import StringIO
import lxml.html as lh
import scraperwiki
import cgi

base_url = "http://access.bytbil.com"
start_url = 'http://access.bytbil.com/bilkompanietcom/Access/Home/lista/EGADUDIAAcMv7oAUDnkAAA__!'

def clearDataStore():
    scraperwiki.sqlite.execute("DELETE FROM swdata")           
    scraperwiki.sqlite.commit()


def getDoc(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent ,"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()

    doc = lh.fromstring(the_page)
    return doc

def saveCarsFromDoc(doc):

    searchList = doc.cssselect('div.GalleryView')[0]
    
    for carListItem in searchList.cssselect('a'):
    
        car = {}
        car["link"] = base_url + carListItem.attrib["href"]
        car["name"] = carListItem.cssselect('span.name')[0].text.strip()
        car["miles"] = carListItem.cssselect('span.miles')[0].text.strip().split(".")[0]
        car["place"] = carListItem.cssselect('span.miles')[0].text.strip().split(".")[1].replace(" ", "")
        car["price"] = carListItem.cssselect('span.regular-price')[0].text.strip()
        car["imageURL"] = cgi.escape(carListItem.cssselect('span.ItemPicture img')[0].attrib["src"])

        # Spara bara bilarna från öjebyn
        #if car["place"] == u"\xd6JEBYN":
        #    print "saving", car["name"] 
        #    scraperwiki.sqlite.save(unique_keys=["name"], data=car)

        scraperwiki.sqlite.save(unique_keys=["name"], data=car)
    
    try:
        nextPageUrl = base_url + doc.cssselect('a.IconRight')[0].attrib["href"]
    except:
        nextPageUrl = None

    return nextPageUrl

# Hämta första

# Rensa datastore först så det bara är de senaste
clearDataStore()

#TODO rensa bara om det gick bra att hämta datan

next_link = start_url
while next_link != None:
    doc = getDoc(next_link)
    next_link = saveCarsFromDoc(doc)


import urllib2
import StringIO
import lxml.html as lh
import scraperwiki
import cgi

base_url = "http://access.bytbil.com"
start_url = 'http://access.bytbil.com/bilkompanietcom/Access/Home/lista/EGADUDIAAcMv7oAUDnkAAA__!'

def clearDataStore():
    scraperwiki.sqlite.execute("DELETE FROM swdata")           
    scraperwiki.sqlite.commit()


def getDoc(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent ,"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()

    doc = lh.fromstring(the_page)
    return doc

def saveCarsFromDoc(doc):

    searchList = doc.cssselect('div.GalleryView')[0]
    
    for carListItem in searchList.cssselect('a'):
    
        car = {}
        car["link"] = base_url + carListItem.attrib["href"]
        car["name"] = carListItem.cssselect('span.name')[0].text.strip()
        car["miles"] = carListItem.cssselect('span.miles')[0].text.strip().split(".")[0]
        car["place"] = carListItem.cssselect('span.miles')[0].text.strip().split(".")[1].replace(" ", "")
        car["price"] = carListItem.cssselect('span.regular-price')[0].text.strip()
        car["imageURL"] = cgi.escape(carListItem.cssselect('span.ItemPicture img')[0].attrib["src"])

        # Spara bara bilarna från öjebyn
        #if car["place"] == u"\xd6JEBYN":
        #    print "saving", car["name"] 
        #    scraperwiki.sqlite.save(unique_keys=["name"], data=car)

        scraperwiki.sqlite.save(unique_keys=["name"], data=car)
    
    try:
        nextPageUrl = base_url + doc.cssselect('a.IconRight')[0].attrib["href"]
    except:
        nextPageUrl = None

    return nextPageUrl

# Hämta första

# Rensa datastore först så det bara är de senaste
clearDataStore()

#TODO rensa bara om det gick bra att hämta datan

next_link = start_url
while next_link != None:
    doc = getDoc(next_link)
    next_link = saveCarsFromDoc(doc)


