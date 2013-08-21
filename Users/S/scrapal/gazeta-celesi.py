#!/usr/bin/env python
# encoding: utf-8
import scraperwiki

from bs4 import BeautifulSoup
import feedparser
import dateutil.parser
import lxml.html
import urlparse        
import urllib, urllib2, re, time
import urllib2
import socket
import sys
import simplejson   # for the geo-coder
from BeautifulSoup import BeautifulSoup
from time import strftime

# API-key I got for scraperwiki: ABQIAAAAgxlWnsfEg93hC1qDK2BFvhQWj4N4t6Xmv-CV_W48hf2y5mqxJRTcXxIPbJU4VsgoiOrAxZdN7z9pAg

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def geowiki(quarter):
    try:
        print "geowiki"
        lat = "41.4147"
        lon = "19.7206"

        wikiurl = "http://api.wikimapia.org/?function=search&key=352E4AA4-44F16978-A27EA6D2-D7E1A56F-9263A296-D29EB2B4-88CB7DFE-7F6B469F"
        wikiurl = wikiurl + "&q="+quarter+"&lat=41&lon=19"
 
        georeq = urllib2.Request(wikiurl)
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        req.add_header('Accept-Encoding    gzip, deflate')
        req.add_header('Accept-Language    en-US,en;q=0.5')
        req.add_header('Connection    keep-alive')
        req.add_header('Host    api.wikimapia.org')
        req.add_header('User-Agent    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0')

        georesponse = urllib2.urlopen(georeq)
        data = georesponse.read()
        print data

        #geocode = simplejson.loads(data)
        matching = [s for s in data if "lat" in s]
        if matching:
            root = lxml.html.fromstring(data)

            #lat = geocode['folder'][0]['place']['location']['lat']#/folder/place/location/lon
            #lat = geocode['folder'][0]['place']['location']['lat']#/folder/place/location/lat
            lat = root.xpath("/folder/place/location/lon")[0].text_content()
            lon = root.xpath("/folder/place/location/lon")[0].text_content()       

        return lat, lon

    except:
        print "geowiki failed", sys.exc_info()[0]
        return lat, lon

def get_coordinates(quarter, city):
    print quarter
    
    #return geowiki(quarter)    

    lat = "41.4147"
    lon = "19.7206"

    #tirana e re: 41.319656,19.80011
    #unaza e re:

    try:
        # a function to geocode a place.
        # geocoding from this tutorial: http://scraperwiki.com/scrapers/geocoding_examples/edit/
        geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote_plus(quarter+", "+city+", Albania")+'&sensor=false&output=json'
               
        #print geocode_url
        georeq = urllib2.Request(geocode_url)
        geo_response = urllib2.urlopen(georeq)
        geocode = simplejson.loads(geo_response.read())
        #print geocode
            
        if geocode['status'] != 'OVER_QUERY_LIMIT' and geocode['status'] != 'ZERO_RESULTS':
            lat = geocode['results'][0]['geometry']['location']['lat']
            lon = geocode['results'][0]['geometry']['location']['lng']
            print "geocode worked."+str(geocode['results'])
        else:
            lat = ''
            lon = ''
            print "geocode failed. address:"+geocode_adress
            return geowiki(quarter)
        return lat, lon
    except:
        print "geocode failed", sys.exc_info()[0]
        return geowiki(quarter)


def scrap_category(cat, itype, option , city , cityid, areaType):
    
    # starting point
    urlbase = "http://www.gazetacelesi.al/"+cat +"/"+itype +"/"+option +"/"+city +"/"+cityid +"/lista_e_njoftimeve.aspx?PAG="
    base = "http://www.gazetacelesi.al"
    
    
    # the number of pages of media releases we should page through
    numpages = 10
    
    for x in range(1, numpages):
    
        url = urlbase + str(x)
        print "list:"+url
        
        #html = scraperwiki.scrape(url)              
        req= urllib2.Request(url)
        req.add_header('Content-Type', 'text/html;charset=utf-8')
        resp = urllib2.urlopen(req)
        html = resp.read()
        html = html.decode("UTF-8")

        root = lxml.html.fromstring(html)
    
        #//root.xpath("[starts-with(@id, "idAnn")]")
        #//root.xpath("//*[@id='idAnn*']")
    
        for link in root.xpath("//*[starts-with(@id, 'idAnn')]"):
            print "page:"+link.attrib['href']
        
            try:
                link2 = base+link.attrib['href'].encode("UTF-8")
                page_content = scraperwiki.scrape(link2)  
        
                #tblDatiAnnuncio
                root2 = lxml.html.fromstring(page_content)
                #print "root2:"+lxml.html.tostring(root2)
    
                txtData = root2.xpath("//*[@id='tdTxt']")
                tdImg= root2.xpath("//*[@id='ctl00_barra_dx_incDettaglioAnnuncio_imgAnnuncio']")
                photoUrl = tdImg[0].attrib['src']
        
                #Celular:<b>x<b> (tr[2]/tr[3])
                contact = root2.xpath("//*[@id='ctl00_barra_dx_incDettaglioAnnuncio_trRecapitoCellulare']")
                print "phone:"+contact[0][0].text_content().replace("Celular:","").strip()
                phone = contact[0][0].text_content().replace("Celular:","").strip()
                cel = ""
    
                #Noftim i vendosur me:<b>x<b><br>
                datestr = root2.xpath("//*[@id='ctl00_barra_dx_incDettaglioAnnuncio_lnkBrdCat']")
                print "date:"+datestr[0].getprevious().getprevious().text_content().strip()
                pubDate = datestr[0].getprevious().getprevious().text_content().strip()
        
                #print lxml.html.tostring(txtData[0])
                print "text:"+txtData[0].text_content()
        
                item = txtData[0].text_content().strip().encode("UTF-8").split(',')
                #print "text:"+item [0]
    
                matching = [s for s in item if "qera" in s]
                if matching:
                    continue
    
                if item[1].startswith("shitet") :
                    option = "For sale"
                    city = "Tirane"
                    itype = item[1].replace("shitet ","").strip()
                    quarter = item[0].strip()
                    addressDesc = ""
                else:
                    option = "For sale"
                    city = "Tirane"
                    itype = item[2].replace("shitet ","").strip()
                    quarter = item[0].strip()
                    addressDesc = item[1].strip()
                    
                if 'ballkon' in item:
                    balcony = 1
                else:
                    balcony = 0
    
                if quarter.startswith("Tek "):
                    quarter = quarter.replace("Tek ","")
    
                if quarter.startswith("Te "):
                    quarter = quarter.replace("Te ","")
    
                if quarter.startswith("Pas "):
                    quarter = quarter.replace("Pas ","")
    
                if quarter.startswith("Prane "):
                    quarter = quarter.replace("Prane ","")
    
                if quarter.startswith("Ne "):
                    quarter = quarter.replace("Ne ","")
    
                if quarter.startswith("Mbi "):
                    quarter = quarter.replace("Mbi ","")
    
                quarter = quarter.replace("Shitet "+areaType,"")
                print quarter

                area = 1
                matching = [s for s in item if "m2" in s]
                if matching:
                    area = matching[0].replace("m2","").strip()
    
                matching = [s for s in item if "mÂ²" in s]
                if matching:
                    area = matching[0].replace("mÂ²","").strip()
     
                matching = [s for s in area if "sip." in s]
                if matching:
                    area = matching[0].replace("sip.","").strip()
    
                ccy = ""
                matching = [s for s in item if "Euro" in s]
                if matching:
                    price = matching[0].replace("Euro","").strip().replace(",","").replace(".","")
                    ccy = "Euro"
                else:
                    price = 1
        
                matching = [s for s in item if "euro" in s]
                if matching:
                    price = matching[0].replace("euro","").strip().replace(",","").replace(".","")
                    ccy = "Euro"
        
                matching = [s for s in item if "Lek" in s]
                if ccy == "" and matching:
                    price = matching[0].replace("Lek","").strip().replace(",","").replace(".","")
                    ccy = "Lek"
        
                areaPrice = 0
                if not isinstance( price, ( int, long ) ) :
                    print "price:"+str(price)
        
                    if price > 0 and "m2" in price:
                        price = price.replace(" m2","").strip()
        
                    if price > 0 and "/mÂ²" in price:
                        price = price.replace("/mÂ²","").strip()
        
                    print "price:"+str(price)
        
                    price = price.replace("çmimi: ","").strip()
                    price = price.replace("iÃ§mimi:","").strip()
                    price = price.replace("i diskutueshem","").strip()
                    price = price.replace("-","").strip()
                    price = price.replace("shitet","").strip()
                    price = price.split(' ')[0].strip()
               
                if not isinstance( area, ( int, long ) ) and ccy in area:
                    matching = [s for s in item if "m2" in s]
                    if matching:
                        area = matching[0].replace("m2","").strip()
        
                    matching = [s for s in item if "/mÂ²" in s]
                    if matching:
                        area = matching[0].replace("/mÂ²","").strip()
        
                print "price:"+str(price)
                print "area:"+str(area)
                print "ccy:"+ccy
        
                if not is_number(price):
                    print "skipped1"
                    continue
        
                if int(price) > 5000:
                    areaPrice = int(price)/float(area)
                else:
                    areaPrice = int(price)
        
                if ccy == "Lek":
                    areaPrice = areaPrice / 140
        
                print "areaPrice:"+str(areaPrice)
                if areaPrice < 10:
                    print "skipped2"
                    continue
        
                matching = [s for s in item if "kati" in s]
                if matching:
                    floor = matching[0].replace("kati","").replace("banim","").replace("i fundit","").strip()
                print "floor :"+floor 
        
                orientation = "-"
                matching = [s for s in item if "orientimi" in s]
                if matching:
                    orientation = matching[0].replace("orientimi","").strip()
        
                matching = [s for s in item if "drejtimi" in s]
                if matching:
                    orientation = matching[0].replace("drejtimi ","").strip()
        
                matching = [s for s in orientation if "i fundit" in s]
                if matching:
                    orientation = matching[0].replace("i fundit","").strip()
                    lastFloor = "1"
                else:
                    lastFloor = "0"
        
                matching = [s for s in item if "tarrace" in s]
                if matching:
                    terrace = "1"
                else:
                    terrace  = "0"
        
                #pubdate
                
                #find lat lon by address
                #lat
                #lon
                lat, lon = get_coordinates(quarter, city)
                
                matching = [s for s in item if "i ri" in s]
                if matching:
                    isNew = "1"
                else:
                    isNew = "0"
        
                matching = [s for s in item if "kompletuar" in s]
                if matching:
                    isFull= "1"
                else:
                    isFull= "0"
        
                matching = [s for s in item if "diskutueshem" in s]
                if matching:
                    canNegotiate= "1"
                else:
                    canNegotiate= "0"
        
                totPrice = int(price)
                if price < 10000:
                    totPrice = int(price) * float(area)
         
                record = {"link" : link2,
                          "pubdate" : pubDate,
                          "city" : city,
                          "quarter":quarter ,                  
                          "addresDesc" : addressDesc,
                          "lat" : lat,
                          "lon" : lon,
        
                          "type" : areaType,
                          "option" : "For sale",
                          
                          "area": area,                  
                          "price" : totPrice,
                          "areaPrice" : areaPrice,
                          "floor":floor,
                          "orientation": orientation,
                          "lastFloor": lastFloor ,
                          "terrace" : terrace,
                          "balcony": balcony,
                          
                          "phone" : phone,
                          "mobile" : cel,
                          "photo" : photoUrl,
        
                          "isNew" : isNew,                  
                          "isFull" : isFull,
                          "canNegotiate" : canNegotiate,
        
                          "data" : txtData[0].text_content().strip().encode("UTF-8")}
            
                scraperwiki.sqlite.save(unique_keys=["link"], data=record)
            except:
                print "Error:", sys.exc_info()[0]

    return

try:
    print "started.."
    scrap_category("Pasuri_t%C3%AB_patundshme", "Shes-Blej_apartamente,_sht%C3%ABpi_dhe_vila",
               "Shitet_garsoniere_dhe_1-1", "TIRANE", "856", "1+1")


    scrap_category("Pasuri_t%C3%AB_patundshme", "Shes-Blej_apartamente,_sht%C3%ABpi_dhe_vila",
               "Shitet_2-1", "TIRANE", "929", "2+1")

    scrap_category("Pasuri_t%C3%AB_patundshme", "Shes-Blej_apartamente,_sht%C3%ABpi_dhe_vila",
               "Shitet_3-1_e_me_shume", "TIRANE", "3+", "994")
except:
    print "Error:", sys.exc_info()[0]
