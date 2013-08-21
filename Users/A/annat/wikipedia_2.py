# -*- coding: utf-8 -*-
import scraperwiki
import simplejson
import urllib
import urllib2
import time
import re
import requests
import BeautifulSoup



category = "Baudenkmal in Berlin"

urlCategory1 = "http://de.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Baudenkmal%20in%20Berlin&cmlimit=500&format=json"
urlCategory2 = "http://de.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Baudenkmal%20in%20Berlin&cmlimit=500&cmcontinue=%22page|5052494e5a455353494e4e454e50414c4149530a5052494e5a455353494e4e454e50414c414953|1740073&format=json"
#Category

resultsJsonC1 = simplejson.loads(urllib.urlopen(urlCategory1).read())
resultsJsonC2 = simplejson.loads(urllib.urlopen(urlCategory2).read())

categoryMembers = resultsJsonC1['query']['categorymembers']
categoryMembers.extend(resultsJsonC2['query']['categorymembers'])

resultsJson = resultsJsonC1

#response = requests.get(urlCategory, verify = False).text
#resultsJson = simplejson.loads(response)
#categoryMembers = resultsJson['query']['categorymembers']

#print categoryMembers

def clean(data):     
    p = re.compile('//')     
    return p.sub('', data)

def image(title,id):
    print title
    titleUrl = "http://de.wikipedia.org/w/api.php?action=query&titles="+title+"&prop=images&format=json"
    imgJson = simplejson.loads(urllib.urlopen(titleUrl).read())

    imageUrl = None
    
    if imgJson['query']['pages'].has_key(id):
        if imgJson['query']['pages'][id].has_key('images'):
            if imgJson['query']['pages'][id]['images'][0]:
                imageTitle = imgJson['query']['pages'][id]['images'][0]['title']
                
                imageTitle = imageTitle.encode('utf-8')
                imageTitleUrl = "http://de.wikipedia.org/w/api.php?action=query&titles="+imageTitle+"&prop=imageinfo&iiprop=url&iiurlwidth=640&format=json"
     
                imgTitleJson = simplejson.loads(urllib.urlopen(imageTitleUrl).read())
                
            
                if imgTitleJson['query']['pages'].has_key("-1"):
                    if imgTitleJson['query']['pages']['-1'].has_key('imageinfo') :
                        imageUrl = imgTitleJson['query']['pages']['-1']['imageinfo'][0]['thumburl']
        
                elif imgTitleJson['query']['pages'].has_key('id'):
                     if imgTitleJson['query']['pages']['id'].has_key('imageinfo'):
                        imageUrl = imgTitleJson['query']['pages']['id']['imageinfo'][0]['thumburl']
    
        
    return imageUrl

def introduction(name, id):
    print name
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


def coords(urlWiki):
    #print urlWiki
    response = requests.get(urlWiki, verify = False).text
    soup = BeautifulSoup.BeautifulSoup(response)
    coordLink = soup.findAll('a', {'class':'external text'})
    
    lat = None  
    lng = None

    for i in range(len(coordLink)):
        if coordLink[i]['href'].startswith("//toolserver"):
            coordUrl = "http:" + coordLink[i]['href']
            resp = requests.get(coordUrl, verify = False).text
            coordSoup = BeautifulSoup.BeautifulSoup(resp)
            try:
                 lat = coordSoup.findAll('span', {'class':'latitude'})[0].text
                 lng = coordSoup.findAll('span', {'class':'longitude'})[0].text
            except IndexError:
                lat = None
                lng = None
       

           
       

    return [lat, lng]

def urlWiki(name,id):
    print name
   
    url = "http://de.wikipedia.org/w/api.php?action=query&titles="+name+"&prop=info&inprop=url&format=json"
    urlJson = simplejson.loads(urllib.urlopen(url).read())
    nr = urlJson['query']['pages'].keys()[0]
    
    if urlJson['query']['pages'].has_key("-1"):
        
        urlW = urlJson['query']['pages']['-1']['fullurl']
        
    else:
        urlW = urlJson['query']['pages'][nr]['fullurl']
        
    return urlW

for i in range(574,len(categoryMembers)):
    id = str(resultsJson['query']['categorymembers'][i]['pageid'])
    name = resultsJson['query']['categorymembers'][i]['title']
  
                
    #name = resultsJson['query']['categorymembers'][i]['title']
    name = name.encode('utf-8')
        
            
    urlW = urlWiki(name,id)
    
    [lat, lng] = coords(str(urlW)) 
    
    imageUrl = image(name, id)
                
    infoText = introduction(name, id)
              
    data = {'id' : id,
        'name' : name,
        'lat' : lat,
        'lng' : lng,
        'url' : urlW,
        'category' : category,
        'imageUrl' : imageUrl,
        'infoText': infoText}  

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    time.sleep(10)   
    
   





