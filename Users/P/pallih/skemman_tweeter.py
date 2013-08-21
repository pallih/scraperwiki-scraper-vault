# -*- coding: utf-8 -*-
import json
import requests
from datetime import *
import tweepy

CONSUMER_KEY = 'mLlNaphI1faUJuaq4kq3ag'
CONSUMER_SECRET = 'WwzXiRit8QG48XGHkkZK8Jz0bWTcKgkAndafmfsU'
ACCESS_TOKEN = '840402775-eMqTyRuCUU1jjpa4nGKtvEKrexONudKVZTLKUEd5'
ACCESS_SECRET = 'kiT0E9Aw3tNmFyvra9Ek2vyKLuGX3vKPVgcUci7ioE'


def smart_truncate(content, length=99, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return content[:length].rsplit(' ', 1)[0]+suffix

today_string = datetime.today().strftime("%d.%m.%Y")
today_string = '1.1.2013'

url = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=skemman&query=select%20title%2Curl%2Cfile_1_locked_until%20from%20%22publications_details%22%20where%20%22file_1_locked_until%22%20%20%3D%20%22'+today_string+'%22%20ORDER%20BY%20file_1_locked_until'
print url
jsonlist = requests.get(url,verify=False)
stuff =  json.loads(jsonlist.text)

if stuff:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)  
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    expanded_old_list = []
    for status in tweepy.Cursor(api.user_timeline,include_entities=True).items(100):
        length = len(status.text)
        expanded_old_list.append(status.text[0:int(status.entities['urls'][0]['indices'][0])]+status.entities['urls'][0]['expanded_url'] )
    new_list = []
    for x in stuff:
        prefix = 'Opið: "'.decode('utf-8')
        tweet = smart_truncate(prefix + x['title']) +'" '+ x['url']
        #tweet = tweet.encode('iso-8859-1')
        print len(tweet)
        new_list.append(tweet)
        
        #try:
        #    #api.update_status(tweet)
        #    print 'tweet'
        #except:
        #    pass
        #print len(x['url'])
    try:
        for x in expanded_old_list:
            new_list.remove(x)
    except:
        pass
    if len(new_list)>0:
        print len(new_list), new_list
        for x in new_list:
            try:
                api.update_status(x)
            except:
                pass
        

