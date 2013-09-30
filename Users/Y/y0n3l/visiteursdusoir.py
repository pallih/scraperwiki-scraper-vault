import scraperwiki
from datetime import datetime, date
from httplib import IncompleteRead
from lxml.html.soupparser import fromstring
from os import path
from urllib2 import URLError
import os.path
import urllib
import urllib2

def firstValue(array):
    return array[0] if len(array)>0 else ""

def getDetailsFromUrl(address):
    url = 'http://lesvisiteursdusoir.com' + address
    response = urllib2.urlopen(url)
    html = response.read()
    root = fromstring(html)
    titleArray = root.xpath("//h1[@class='title']/text()")
    yearArray = root.xpath("//div[@class='field field-name-field-annee-realisation field-type-date field-label-inline clearfix']//span/text()")
    durationArray = root.xpath("string(//div[@class='field field-name-field-duree-txt field-type-text field-label-inline clearfix']//div[@class='field-item even']/text())")
    countryArray = root.xpath("//div[@class='field field-name-field-pays field-type-text field-label-inline clearfix']//div[@class='field-item even']/text()")
    directorArray = root.xpath("//div[@class='field field-name-field-realisateur field-type-text field-label-inline clearfix']//div[@class='field-item even']/text()")
    synopsisArray = root.xpath("//div[@class='field field-name-field-synopsis field-type-text-long field-label-above']//p/text()");
    imageArray = root.xpath("//div[@class='field field-name-field-affiche field-type-image field-label-hidden']//img/@src");
    allocineShortcutArray = root.xpath("//div[@class='region region-content']//div[@class='content']/a/@href");    
    #print title,  duration, country, director, synopsis, image, allocineShortcut
    details = {"title": firstValue(titleArray), "duration": firstValue(durationArray), "country": firstValue(countryArray), "year":firstValue(yearArray), "synopsis" : firstValue(synopsisArray), "director": firstValue(directorArray), "url": url, "poster":firstValue(imageArray), "allocine":firstValue(allocineShortcutArray)}
    return details

response = urllib2.urlopen('http://lesvisiteursdusoir.com/les-films-a-l-affiche')
html = response.read()
root = fromstring(html)
movies = root.xpath("//div[@class='node node-affiche node-teaser clearfix']")
for movie in movies:
    title = movie.xpath('h2/a/text()')
    #print title
    detailsUrl = movie.xpath('h2/a/@href')
    movieInfo = getDetailsFromUrl(detailsUrl[0])
    schedules = movie.xpath("div/div/div/div/span[@class='date-display-single']/@content")
    for schedule in schedules: 
        scheduleDT = datetime.strptime(schedule.replace('+01:00','').replace('+02:00',''), '%Y-%m-%dT%H:%M:%S')
        #print scheduleDT
        #print scheduleDT.strftime('%Y-%m-%d %H:%M:%S')
        scheduleDetails = movieInfo.copy()
        scheduleDetails["schedule"] = scheduleDT
        scraperwiki.sqlite.save(unique_keys=["schedule"], data= scheduleDetails)
    import scraperwiki
from datetime import datetime, date
from httplib import IncompleteRead
from lxml.html.soupparser import fromstring
from os import path
from urllib2 import URLError
import os.path
import urllib
import urllib2

def firstValue(array):
    return array[0] if len(array)>0 else ""

def getDetailsFromUrl(address):
    url = 'http://lesvisiteursdusoir.com' + address
    response = urllib2.urlopen(url)
    html = response.read()
    root = fromstring(html)
    titleArray = root.xpath("//h1[@class='title']/text()")
    yearArray = root.xpath("//div[@class='field field-name-field-annee-realisation field-type-date field-label-inline clearfix']//span/text()")
    durationArray = root.xpath("string(//div[@class='field field-name-field-duree-txt field-type-text field-label-inline clearfix']//div[@class='field-item even']/text())")
    countryArray = root.xpath("//div[@class='field field-name-field-pays field-type-text field-label-inline clearfix']//div[@class='field-item even']/text()")
    directorArray = root.xpath("//div[@class='field field-name-field-realisateur field-type-text field-label-inline clearfix']//div[@class='field-item even']/text()")
    synopsisArray = root.xpath("//div[@class='field field-name-field-synopsis field-type-text-long field-label-above']//p/text()");
    imageArray = root.xpath("//div[@class='field field-name-field-affiche field-type-image field-label-hidden']//img/@src");
    allocineShortcutArray = root.xpath("//div[@class='region region-content']//div[@class='content']/a/@href");    
    #print title,  duration, country, director, synopsis, image, allocineShortcut
    details = {"title": firstValue(titleArray), "duration": str(durationArray), "country": firstValue(countryArray), "year":firstValue(yearArray), "synopsis" : firstValue(synopsisArray), "director": firstValue(directorArray), "url": url, "poster":firstValue(imageArray), "allocine":firstValue(allocineShortcutArray)}
    return details

response = urllib2.urlopen('http://lesvisiteursdusoir.com/les-films-a-l-affiche')
html = response.read()
root = fromstring(html)
movies = root.xpath("//div[@class='node node-affiche node-teaser clearfix']")
for movie in movies:
    title = movie.xpath('h2/a/text()')
    #print title
    detailsUrl = movie.xpath('h2/a/@href')
    movieInfo = getDetailsFromUrl(detailsUrl[0])
    schedules = movie.xpath("div/div/div/div/span[@class='date-display-single']/@content")
    for schedule in schedules: 
        scheduleDT = datetime.strptime(schedule.replace('+01:00','').replace('+02:00',''), '%Y-%m-%dT%H:%M:%S')
        #print scheduleDT
        #print scheduleDT.strftime('%Y-%m-%d %H:%M:%S')
        scheduleDetails = movieInfo.copy()
        scheduleDetails["schedule"] = scheduleDT
        scraperwiki.sqlite.save(unique_keys=["schedule"], data= scheduleDetails)
    