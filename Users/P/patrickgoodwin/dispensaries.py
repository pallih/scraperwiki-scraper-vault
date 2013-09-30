import scraperwiki
import lxml.html
import lxml.etree
import urllib 
import geopy 
from geopy import geocoders   
import string 

us = geocoders.GeocoderDotUS()  
gn = geocoders.GeoNames()   


html_a = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/n-seattlekingsnohomish")
root_a = lxml.html.fromstring(html_a)
    
x = 0
while x < 42:
    x += 1
    for elt in root_a.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_a = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_a)

html_b = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/seattleking-county")
root_b = lxml.html.fromstring(html_b)
    
x = 0
while x < 42:
    x += 1
    for elt in root_b.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_b = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_b)

html_c = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/tacomapierce-county")
root_c = lxml.html.fromstring(html_c)
    
x = 0
while x < 38:
    x += 1
    for elt in root_c.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_c = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_c)

html_d = scraperwiki.scrape("https://scraperwiki.com/scrapers/olympia_dispensaries/")
root_d = lxml.html.fromstring(html_d)
    
x = 0
while x < 25:
    x += 1
    for elt in root_d.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_d = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_d)


html_e = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/n-tacoma-federal-way")
root_e = lxml.html.fromstring(html_e)
    
x = 0
while x < 24:
    x += 1
    for elt in root_e.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_e = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_e)

html_f = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/everettsnohomish")
root_f = lxml.html.fromstring(html_f)
    
x = 0
while x < 19:
    x += 1
    for elt in root_f.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_f = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_f)

html_g = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/spokaneeastern-washington")
root_g = lxml.html.fromstring(html_g)

x = 0
while x < 16:
    x += 1
    for elt in root_g.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_g = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_g)

html_h = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/eastside-seattle")
root_h = lxml.html.fromstring(html_h)

x = 0
while x < 13:
    x += 1
    for elt in root_h.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_h = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_h)

html_j = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/washington-state")
root_j = lxml.html.fromstring(html_j)

x = 0
while x < 10:
    x += 1
    for elt in root_j.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_j = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_j)

html_k = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/vancouver-washington")
root_k = lxml.html.fromstring(html_k)

x = 0
while x < 8:
    x += 1
    for elt in root_k.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_k = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_k)

html_l = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/kent")
root_l = lxml.html.fromstring(html_l)

x = 0
while x < 9:
    x += 1
    for elt in root_l.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_l = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_l)

html_m = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/olympic-peninsula")
root_m = lxml.html.fromstring(html_m)

x = 0
while x < 6:
    x += 1
    for elt in root_m.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_m = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_m)

html_n = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/yakimatri-cities")
root_n = lxml.html.fromstring(html_n)

x = 0
while x < 2:
    x += 1
    for elt in root_n.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_n = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_n)import scraperwiki
import lxml.html
import lxml.etree
import urllib 
import geopy 
from geopy import geocoders   
import string 

us = geocoders.GeocoderDotUS()  
gn = geocoders.GeoNames()   


html_a = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/n-seattlekingsnohomish")
root_a = lxml.html.fromstring(html_a)
    
x = 0
while x < 42:
    x += 1
    for elt in root_a.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_a = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_a)

html_b = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/seattleking-county")
root_b = lxml.html.fromstring(html_b)
    
x = 0
while x < 42:
    x += 1
    for elt in root_b.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_b = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_b)

html_c = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/tacomapierce-county")
root_c = lxml.html.fromstring(html_c)
    
x = 0
while x < 38:
    x += 1
    for elt in root_c.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_c = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_c)

html_d = scraperwiki.scrape("https://scraperwiki.com/scrapers/olympia_dispensaries/")
root_d = lxml.html.fromstring(html_d)
    
x = 0
while x < 25:
    x += 1
    for elt in root_d.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_d = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_d)


html_e = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/n-tacoma-federal-way")
root_e = lxml.html.fromstring(html_e)
    
x = 0
while x < 24:
    x += 1
    for elt in root_e.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_e = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_e)

html_f = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/everettsnohomish")
root_f = lxml.html.fromstring(html_f)
    
x = 0
while x < 19:
    x += 1
    for elt in root_f.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_f = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_f)

html_g = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/spokaneeastern-washington")
root_g = lxml.html.fromstring(html_g)

x = 0
while x < 16:
    x += 1
    for elt in root_g.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_g = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_g)

html_h = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/eastside-seattle")
root_h = lxml.html.fromstring(html_h)

x = 0
while x < 13:
    x += 1
    for elt in root_h.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_h = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_h)

html_j = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/washington-state")
root_j = lxml.html.fromstring(html_j)

x = 0
while x < 10:
    x += 1
    for elt in root_j.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_j = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_j)

html_k = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/vancouver-washington")
root_k = lxml.html.fromstring(html_k)

x = 0
while x < 8:
    x += 1
    for elt in root_k.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_k = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_k)

html_l = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/kent")
root_l = lxml.html.fromstring(html_l)

x = 0
while x < 9:
    x += 1
    for elt in root_l.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_l = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_l)

html_m = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/olympic-peninsula")
root_m = lxml.html.fromstring(html_m)

x = 0
while x < 6:
    x += 1
    for elt in root_m.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_m = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_m)

html_n = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington/yakimatri-cities")
root_n = lxml.html.fromstring(html_n)

x = 0
while x < 2:
    x += 1
    for elt in root_n.cssselect("div [class='listings']"):
        name = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getchildren()[0].text[:]
        address = elt.getchildren()[x].getchildren()[0].getnext().getchildren()[0].getnext().text[:]
        returned = us.geocode(address)     
        if returned != None:          
            place, (lat, lng) = returned     
        else:         
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")         
            place = "FAILED TO GEOCODE"      
        print "%s: %.5f, %.5f" % (place, lat, lng)           
        data_n = {
            'name': name,
            'address': address,
            'lat': lat,         
            'long': lng,         
            'geocoder result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data_n)