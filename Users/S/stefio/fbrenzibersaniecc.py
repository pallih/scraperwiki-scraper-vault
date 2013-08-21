# Blank Python
import simplejson, urllib, scraperwiki, datetime

sourcescraper = ''

pages =['matteorenziufficiale',
'PierLuigiBersani.PaginaUfficiale',
'MarioMonti.ufficiale',
'SilvioBerlusconi','beppegrillo.it']

names = ['Renzi', 'Bersani', 'Monti', 'Berlusconi','Beppegrillo.it'] 
counter = 0

for politico in pages:


    url="https://graph.facebook.com/" + politico
    data=simplejson.load(urllib.urlopen(url))


    temp = data['likes']
    temp2 = data['talking_about_count']
    data = {"Nome": names[counter], "Likes": temp, "Time": str(datetime.datetime.now()), "Talking About": temp2}
    
    scraperwiki.sqlite.save(['Time'], data)
    
    counter = counter + 1
