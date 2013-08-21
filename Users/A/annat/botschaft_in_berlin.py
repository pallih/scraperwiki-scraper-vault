# -*- coding: utf-8 -*-
import scraperwiki
import simplejson
import urllib
import urllib2
import time
import re

center = 52.527919,13.404465


#Location

coords = ["lat=52.527919&lng=13.404465"]#["lat=52.666389&lng=13.281555" ]#, ""lat=52.476089&lng=13.545227"", "lat=52.472743&lng=13.226623"]
locationDict = {}
for j in range(1):

    offset = 0
    offsetStart = 0

    for k in range(10):

        offset = offsetStart
        for i in range(50):

            offset = str(offset)
            urlLocation = "http://api.wikilocation.org/articles?&"+coords[j]+"&radius=20000&offset="+offset+"&locale=de&format=json"
            resultsJsonL = simplejson.loads(urllib.urlopen(urlLocation).read())

            for i in range(len(resultsJsonL['articles'])):
                id = resultsJsonL['articles'][i]['id']
                lat = resultsJsonL['articles'][i]['lat']
                lng = resultsJsonL['articles'][i]['lng']
                locationDict[id] = lat,lng

            offset = int(offset)
            offset += 50
            #time.sleep(2)
        
        #time.sleep(5)
        offsetStart += 2500
    time.sleep(2)


category = "Botschaft in Berlin"

urlCategory1 = "http://de.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Botschaft_in_Berlin&cmlimit=500&format=json"


resultsJsonC1 = simplejson.loads(urllib.urlopen(urlCategory1).read())

categoryMembers = resultsJsonC1['query']['categorymembers']



countList = []


def image(title,id):
    
    titleUrl = "http://de.wikipedia.org/w/api.php?action=query&titles="+title+"&prop=images&format=json"
    imgJson = simplejson.loads(urllib.urlopen(titleUrl).read())

    imageUrl = None
    
    if imgJson['query']['pages'].has_key(id):
        if imgJson['query']['pages'][id].has_key('images'):
            if imgJson['query']['pages'][id]['images'][0]:
                imageTitle = imgJson['query']['pages'][id]['images'][0]['title']
                imageTitle = imageTitle.encode('utf-8')
                imageTitleUrl = "http://de.wikipedia.org/w/api.php?action=query&titles="+imageTitle+"&prop=imageinfo&iiprop=url&format=json"
     
                imgTitleJson = simplejson.loads(urllib.urlopen(imageTitleUrl).read())
                
            
                if imgTitleJson['query']['pages'].has_key("-1"):
                    if imgTitleJson['query']['pages']['-1'].has_key('imageinfo') :
                        imageUrl = imgTitleJson['query']['pages']['-1']['imageinfo'][0]['url']
        
                elif imgTitleJson['query']['pages'].has_key('id'):
                     if imgTitleJson['query']['pages']['id'].has_key('imageinfo'):
                        imageUrl = imgTitleJson['query']['pages']['id']['imageinfo'][0]['url']
    
        
    return imageUrl

def introduction(name, id): 
    
    introUrl = "http://de.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&titles="+name+"&format=json"
    
    introJson = simplejson.loads(urllib.urlopen(introUrl).read())
    introText = None
    if introJson['query']['pages'].has_key(id):
        introText = introJson['query']['pages'][id]['extract']
    
    if introText != None:
        introText = remove_html_tags(introText)
   
    return introText

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


resultList = []
def urlWiki(name,id):
   
    url = "http://de.wikipedia.org/w/api.php?action=query&titles="+name+"&prop=info&inprop=url&format=json"
    urlJson = simplejson.loads(urllib.urlopen(url).read())
    nr = urlJson['query']['pages'].keys()[0]
    
    if urlJson['query']['pages'].has_key("-1"):
        
        urlW = urlJson['query']['pages']['-1']['fullurl']
       
    else: 
        urlW = urlJson['query']['pages'][nr]['fullurl']
       
    return urlW

for i in range(len(categoryMembers)):
    id = str(resultsJsonC1['query']['categorymembers'][i]['pageid'])
    name = resultsJsonC1['query']['categorymembers'][i]['title']
    
    #print name 
    if id in locationDict:
        location = locationDict[id]
        print location
)
        name = resultsJsonC1['query']['categorymembers'][i]['title']
        name = name.encode('utf-8')
        print name   
            
        urlW = urlWiki(name,id)
                
        imageUrl = image(name, id)
                
        infoText = introduction(name, id)
              
        data = {'id' : id,
            'name' : name,
            'lat' : location[0],
            'long' : location[1],
            'url' : urlW,
            'category' : category,
            'imageUrl' : imageUrl,
            'infoText': infoText}  

        scraperwiki.sqlite.save(unique_keys=['id'], data=data) 
        #time.sleep(5)
    time.sleep(2)
   


