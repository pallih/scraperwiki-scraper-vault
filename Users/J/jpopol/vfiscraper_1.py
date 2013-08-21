import scraperwiki

import re
import urllib2
import sys
import json
from BeautifulSoup import BeautifulSoup
import requests

baseUrl = "http://vfi.ie"
queryUrl = baseUrl + "/pub-list.php?"

aspects = ['town', 'region', 'county', 'offer', 'facility']

def GetAspectsMaps(baseUrl):
    rhs = {}
    html = urllib2.urlopen(baseUrl)
    soup = BeautifulSoup(html)
    
    browseList = soup.find("ul" , {"class":"browse"})
    lis = browseList.findAll("li")
    
    rawLists = []
    for liMenu in lis:
        uls = liMenu.findAll("ul")
        for ul in uls:
            rawLists.append(ul.findAll("li"))
    
    for aspect in aspects :       
        rhs[aspect] =  __GetTypeList(rawLists, aspect)
    
    return rhs


def __GetTypeList(rawLists, key):
    rhs = {}
    for rawList in rawLists:
        for item in rawList:
            # the value is what the site understand the page Id
            value = item.a['href'].split(key+'=')
            if len(value) < 2:
                continue
            # the id is what we know as human: town, food, couty
            id = item.a.text.split('(')[0].strip().lower()
            rhs[id] = int(value[1])
    return rhs

def __SpaceItRight(sentence):
    return re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', sentence.strip())

def __ItemsInDiv(div, *items):
    rhs = []
    for item in items:
        if item in div:
            rhs.append(item)
    return rhs
    
def __Extract(key, div, settings):
    
    getIdFromKey = dict(zip(settings, range(len(settings))))
    getKeyFromId = dict(zip(range(len(settings)),settings))

    if key not in settings:
        return "Unknown"
    
    #last key
    if getKeyFromId[len(settings) - 1] is key:
         try:
            return div.text.split(key + ":")[1].lstrip().rstrip()
         except:
            print ("can't find last: " + key +" in \n" + div )
            return "Unknown"
    
    nextKey = getKeyFromId[getIdFromKey[key] + 1]
    try:
        return div.text.split(key + ":")[1].split(nextKey + ":")[0].lstrip().rstrip()
    except:
        print ("can't find: " + key +" in \n" + div.text )
        return "Unknown"

    return "Unknown"

def GetPubsInfo(aspect, pageId, nameOnly = False):
    pubs = []
    # all result in one page
    html = urllib2.urlopen(queryUrl + aspect + '=' + str(pageId) + '&rpp=all');
    soup = BeautifulSoup(html)
    results =  soup.findAll('div', {'class':'result'})
    
    for (counter, result) in enumerate(results) :
        pubs.append({})

        pubs[counter]['name'] = result.find('div', {'class' : 'fm-details-1'}).h3.text
        if nameOnly:
            continue
        pubs[counter]['logo'] = result.img['src']
        pubs[counter]['address'] = __SpaceItRight(result.find('div', {'class' : 'left'}).text)
        
        rightDiv = result.find('div', {'class' : 'right'})
        try:
            pubs[counter]['email'] = rightDiv.a.text
        except:
            pubs[counter]['email'] = 'Unknown'

        settings = __ItemsInDiv(rightDiv.text, 'Tel', 'Fax', 'Proprietor')
        pubs[counter]['phone'] = __Extract("Tel", rightDiv, settings)
        pubs[counter]['fax'] = __Extract("Fax", rightDiv, settings)
        pubs[counter]['proprietor'] = __Extract("Proprietor", rightDiv, settings)      

        pubs[counter]['description'] = result.find('div', {'class' : 'fm-details-3'}).text
    
    return pubs

#def Store(pubs):
    #for pub in pubs:
    #    try :
    #        scraperwiki.sqlite.save(['name'], pub)
    #    except:
    #        print "can't save pub: " + pub['name']


def Main():
    aspectsMap = GetAspectsMaps(baseUrl)
    pubStore = False
    for aspectKey in aspectsMap.keys():
        if aspectKey is 'region':
            pubStore = True
        else:
            pubStore = False
        aspectid = 0
        for aspect in aspectsMap[aspectKey]:
            if pubStore:
                pubs = GetPubsInfo(aspectKey, aspectsMap[aspectKey][aspect])
                scraperwiki.sqlite.save(['name'], pubs, 'pubs')
            else:             
                pubs = GetPubsInfo(aspectKey, aspectsMap[aspectKey][aspect], True)
            for pub in pubs:
                 scraperwiki.sqlite.save(['id', aspectKey],{'id' : aspectid, 'name' :  pub['name'], aspectKey: aspect}, aspectKey)
                 aspectid = aspectid + 1

Main()
                  