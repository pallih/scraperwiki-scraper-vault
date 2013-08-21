import scraperwiki
import re
import time
import codecs
import math
from scraperwiki.sqlite import save

columns = [
    'Name', 'Address','City','Province','Image', 'Storeys', 'Height', 'Finished date', 'Usage'
]

provinceurl = "http://skyscraperpage.com/cities/?stateID=7"

cityurlender = "&statusID=1"

def buildingscraper(buildingID, cityname):
    trycount = 0
    while trycount < 3:
        try:
            buildingurl = "http://skyscraperpage.com/cities/?buildingID=" + str(buildingID)
            buildingscrape = scraperwiki.scrape(buildingurl)
            name = re.search('<html><head><title>(.+?),', buildingscrape)
            name = name.group(1)
            if re.search('class="lrgb">(.+?)class="med"><tr><td>(.+?)<br>' + cityname, buildingscrape):
                address = re.search('class="lrgb">(.+?)class="med"><tr><td>(.+?)<br>' + cityname, buildingscrape)
                address = address.group(2)
                address = re.sub('&amp;', 'and', address)
            else:
                address = name
            city = cityname
            city = cityname
            province = "Ontario"
            if re.search("'drawingID']=(.+?);", buildingscrape):
                image = re.search("'drawingID']=(.+?);", buildingscrape)
                image = image.group(1)
                image = "http://skyscraperpage.com/diagrams/images/" + str(image) + ".gif"
            else:
                image = "none available"
            if re.search('Floor Count</td><td align="center">(.+?)<', buildingscrape):
                storeys = re.search('Floor Count</td><td align="center">(.+?)<', buildingscrape)
                storeys = storeys.group(1)
            else:
                storeys = "1"
            if re.search('id="height_(.+?)">(.+?)<', buildingscrape):
                height = re.search('id="height_(.+?)">(.+?)<', buildingscrape)
                height = re.sub(' ft', '', height.group(2))
                height = re.sub('">', '', height)
            else:
                height = "0"
            if re.search('Finished(.+?)">(.+?)<', buildingscrape):
                date = re.search('Finished(.+?)">(.+?)<', buildingscrape)
                date = date.group(2)
            else:
                date = "unavailable"
            usage = re.search('Building Uses(.+?)<b>(.+?)<\/b>', buildingscrape)
            usage = usage.group(2)
            row_data = {'Name': name, 'Address': address, 'City': city, 'Province': province, 'Image': image, 'Storeys': storeys, 'Height': height, 'Finished Date': date, 'Usage': usage}
            save([],row_data)
            trycount = 3
        except:
            time.sleep(60)
            trycount = trycount + 1
    
def buildinglist(listscrape, cityname):
    for each_building in re.finditer('"\?buildingID=(.+?)"', listscrape):
        buildingID = each_building.group(1)
        buildingscraper(buildingID, cityname)
        time.sleep(5)

def cityscraper(buildingcount, cityurl, cityname):
    offsetcount = 0
    while offsetcount < buildingcount:
        citytrycount = 0
        while citytrycount < 3:
            try:
                listurl = cityurl + str(offsetcount) + cityurlender
                listscrape = scraperwiki.scrape(listurl)
                buildinglist(listscrape, cityname)
                offsetcount = offsetcount + 100
                citytrycount = 3
            except:
                time.sleep(60)
                trycount = trycount + 1

provincesource = scraperwiki.scrape(provinceurl)

for every_city in re.finditer('<tr><td>(.+?)</td><td></td><td><a href="\?cityID=(.+?)" class="bhu">(.+?)</a></td><td></td><td align="right">(.+?)</td><td></td><td align="right">(.+?)</td></tr>', provincesource):
    citycode = int(every_city.group(2))
    cityurl = "http://skyscraperpage.com/cities/?cityID=" + str(citycode) + "&offset="
    cityname = every_city.group(3)
    buildingcount = re.sub(',', '', (every_city.group(5)))
    buildingcount = int(buildingcount)
    if buildingcount > 100:
        buildingcount = (round(buildingcount, -2)) + 1
    else:
        buildingcount = 50
    cityscraper(buildingcount, cityurl, cityname)
    
     

