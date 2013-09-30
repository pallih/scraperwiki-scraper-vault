import scraperwiki
import re
import time
import codecs
import math
from scraperwiki.sqlite import save

columns = [
    'Address','City','Province','Postal', 'Phone',
]

def storescraper(storeURL):
    trycount = 0
    while trycount < 9:
        try:
            storesource = scraperwiki.scrape(storeURL)
            storeinfo = re.search('<h2>Store Details<(.+?)<h3>', storesource, re.DOTALL)
            storeinfo = storeinfo.group(1)
            address = re.search('<\/h2>(.+?)<p>(.+?)<br', storeinfo, re.DOTALL)
            address = address.group(2)
            city = re.search('\/>(.+?), (\D+) (\D\d\D \d\D\d)', storeinfo, re.DOTALL)
            city = city.group(1)
            province = re.search('\/>(.+?), (\D+) (\D\d\D \d\D\d)', storeinfo, re.DOTALL)
            province = province.group(2)
            postal =  re.search(', (\D+) (\D\d\D \d\D\d)', storeinfo, re.DOTALL)
            postal = postal.group(2)
            phone = re.search('Phone:(.+?)<br', storeinfo)
            phone = phone.group(1)
            row_data = {'Address': address, 'City': city, 'Province': province, 'Postal': postal, 'Phone': phone}
            save([],row_data)
        except:
            trycount = trycount + 1
            time.sleep(120)
        trycount = 10

def storelist(provinceURL):
    trycount = 0
    basestoreurl = "http://www.mystore411.com"
    while trycount < 9:
        try:
            storelistsource = scraperwiki.scrape(provinceURL)
            for every_store in re.finditer('"dotrow"><a href="(.+?)">', storelistsource):
                storeURL = basestoreurl + every_store.group(1)
                storescraper(storeURL)
                time.sleep(10)
        except:
            trycount = trycount + 1
            time.sleep(120)
        trycount = 10

def citylist(provinceURL):
    trycount = 0
    basecityurl = "http://www.mystore411.com"
    while trycount < 9:
        try:
            citylistsource = scraperwiki.scrape(provinceURL)
        except:
            trycount = trycount + 1
            time.sleep(60)
        trycount = 10
    for every_city in re.finditer("<td><a href='(.+?)'>", citylistsource):
        cityURL = basecityurl + every_city.group(1)
        storelist(cityURL)
        time.sleep(10)

def provincelist(baseURL):
    trycount = 0
    baseprovinceurl = "http://www.mystore411.com"
    while trycount < 9:
        try:
            provincelist = scraperwiki.scrape(baseURL)
        except:
            trycount = trycount + 1
            time.sleep(120)
        trycount = 10
    relevantprovinces = re.search('By State:<(.+?)<\/table>', provincelist, re.DOTALL)
    thisprovince = "/store/list_state/17/Saskatchewan/Canada/McDonald%27s-store-locations"
    provinceURL = baseprovinceurl + thisprovince
    storelist(provinceURL)

baseURL = "http://www.mystore411.com/store/listing/17/Canada/McDonald"
provincelist(baseURL)import scraperwiki
import re
import time
import codecs
import math
from scraperwiki.sqlite import save

columns = [
    'Address','City','Province','Postal', 'Phone',
]

def storescraper(storeURL):
    trycount = 0
    while trycount < 9:
        try:
            storesource = scraperwiki.scrape(storeURL)
            storeinfo = re.search('<h2>Store Details<(.+?)<h3>', storesource, re.DOTALL)
            storeinfo = storeinfo.group(1)
            address = re.search('<\/h2>(.+?)<p>(.+?)<br', storeinfo, re.DOTALL)
            address = address.group(2)
            city = re.search('\/>(.+?), (\D+) (\D\d\D \d\D\d)', storeinfo, re.DOTALL)
            city = city.group(1)
            province = re.search('\/>(.+?), (\D+) (\D\d\D \d\D\d)', storeinfo, re.DOTALL)
            province = province.group(2)
            postal =  re.search(', (\D+) (\D\d\D \d\D\d)', storeinfo, re.DOTALL)
            postal = postal.group(2)
            phone = re.search('Phone:(.+?)<br', storeinfo)
            phone = phone.group(1)
            row_data = {'Address': address, 'City': city, 'Province': province, 'Postal': postal, 'Phone': phone}
            save([],row_data)
        except:
            trycount = trycount + 1
            time.sleep(120)
        trycount = 10

def storelist(provinceURL):
    trycount = 0
    basestoreurl = "http://www.mystore411.com"
    while trycount < 9:
        try:
            storelistsource = scraperwiki.scrape(provinceURL)
            for every_store in re.finditer('"dotrow"><a href="(.+?)">', storelistsource):
                storeURL = basestoreurl + every_store.group(1)
                storescraper(storeURL)
                time.sleep(10)
        except:
            trycount = trycount + 1
            time.sleep(120)
        trycount = 10

def citylist(provinceURL):
    trycount = 0
    basecityurl = "http://www.mystore411.com"
    while trycount < 9:
        try:
            citylistsource = scraperwiki.scrape(provinceURL)
        except:
            trycount = trycount + 1
            time.sleep(60)
        trycount = 10
    for every_city in re.finditer("<td><a href='(.+?)'>", citylistsource):
        cityURL = basecityurl + every_city.group(1)
        storelist(cityURL)
        time.sleep(10)

def provincelist(baseURL):
    trycount = 0
    baseprovinceurl = "http://www.mystore411.com"
    while trycount < 9:
        try:
            provincelist = scraperwiki.scrape(baseURL)
        except:
            trycount = trycount + 1
            time.sleep(120)
        trycount = 10
    relevantprovinces = re.search('By State:<(.+?)<\/table>', provincelist, re.DOTALL)
    thisprovince = "/store/list_state/17/Saskatchewan/Canada/McDonald%27s-store-locations"
    provinceURL = baseprovinceurl + thisprovince
    storelist(provinceURL)

baseURL = "http://www.mystore411.com/store/listing/17/Canada/McDonald"
provincelist(baseURL)