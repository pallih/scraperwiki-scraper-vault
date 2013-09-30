# Blank Python
# zakaro voorbeeld

import scraperwiki
import lxml.html
import requests
import base64
import re
import os
import sqlite3 as lite


# haal foto 's url van kapaza class = 

html = scraperwiki.scrape("http://nl.kapaza.be/belgie/agrarisch/")
root = lxml.html.fromstring(html) 
lijstfoto = root.cssselect('.inner_image_div')
print type(lijstfoto)
deelstring = ''
totaalstring = ''

#scraperwiki.sqlite.execute("CREATE  TABLE IF NOT EXISTS `fotos` (`id` INTEGER PRIMARY KEY,    `url` TEXT,  `bin` BLOB);")
print scraperwiki.sqlite.show_tables()

scraperwiki.sqlite.execute("drop table if exists  'fotostxt'")
scraperwiki.sqlite.execute("drop table if exists  'foto'")

print scraperwiki.sqlite.show_tables()
scraperwiki.sqlite.execute("CREATE  TABLE IF NOT EXISTS `fotostxt` (`id` INTEGER PRIMARY KEY,    `url` TEXT,  `bin` TEXT);")
print scraperwiki.sqlite.show_tables()



tel = 1

for   el in  lijstfoto:
        print type(el)
        for le in el:
             print type(le)
             print le.get('src')
             fotourl = le.get('src')  # in dic-v class  is er subelement img 
             foto  = requests.get(fotourl)
        binary = lite.Binary(foto.content)
        bintxt = base64.b64encode(foto.content)
        scraperwiki.sqlite.save(unique_keys =['id'] , data={'id' : tel ,'url':fotourl,'bin':bintxt},table_name = 'fotostext',verbose = 2)
        tel = tel + 1
        if tel == 4:
               break 


#print  lxml.html.tostring(el)
#          fotourl = el.get('url')  
#          print fotourl
#          deelstring = str(lxml.html.tostring(el))   
#          deelstring = lxml.html.tostring(el) 
#          print deelstring  , len(deelstring)
#          print deelstring.find('img src=')
#          print deelstring[35:] 
             
#          print el.find('img src') 
#          print el.attrib
#          print el.keys()  # class 
#          print el.items()
#          print el.values()    
#          print deelstring  , 'url' , fotourl 
#          totaalstring += deelstring   

           
#print totaalstring



#print foto.content
#scraperwiki.sqlite.save(unique_keys=["id"],data={"id" : teller,"fotoref":foto,"omschrijving":beschrijving},table_name="tweedehands",verbose=2)    


#scraperwiki.sqlite.save(unique_keys =['id'] , data={'id' : tel ,'url':fotourl,'bin':binary},table_name = 'fotos',verbose = 2)


#scraperwiki.sqlite.execute("insert into fotos(id , url , bin) VALUES (?,?,?)",( tel , fotourl ,binary))

# encoderen en als text opslaan

result =    scraperwiki.sqlite.select(" count(url) from fotostext")
print result

'''

def get_image_from_brick(lxml_brick):
    thumb_url = a.cssselect('img')[1].get('src')
    url = thumb_url.replace('_250', '_500') 
    r = requests.get(url)
    if r.status_code == 200:
        bin = base64.b64encode(r.content)
    elif r.status_code == 403:
        url = thumb_url.replace('_250', '_400')
        bin = base64.b64encode(requests.get(url).content)
    else:
        url = None
        bin = None
    return {
        'post_id': re.sub(r'[^0-9]+', '', a.get('href')),
        'timestamp': re.sub(r'[^0-9]+', '', a.get('class')),
        'post_url': a.get('href'),
        'url': url, 
        'thumb_url': thumb_url,
        'bin': bin
    }

base_url = 'http://zarinozappia.tumblr.com'
html = requests.get(base_url + '/archive')
dom = lxml.html.fromstring(html.text)

scraperwiki.sqlite.execute('CREATE  TABLE IF NOT EXISTS `photos` ( `post_id` INT PRIMARY KEY, `timestamp`  INT, `post_url` TEXT, `url` TEXT, `thumb_url` TEXT, `bin` TEXT)')

months = []
photos = []
carryon = True

for month in dom.cssselect('#browse_months_widget .month.active'):
    months.append(month.cssselect('a')[0].get('href'))

for month_url in months:
    # get first page of this month's photos
    html = requests.get(base_url + month_url)
    dom = lxml.html.fromstring(html.text)
    
    for a in dom.cssselect('a.brick.photo'):
        photos.append(get_image_from_brick(a))

    # save first page of this month's photos
    scraperwiki.sqlite.save(['post_id'], photos, 'photos')
    last_timestamp = photos[-1]['timestamp']
    photos = []

'''
'''

def ls(dir=''):
     print '$ ls ' + os.getcwd() + '/' + dir
     print os.system('ls -lAh ' + os.getcwd() + '/' + dir)
 
 def rm(f):
     os.remove(os.getcwd() + '/' + f)

'''
# Blank Python
# zakaro voorbeeld

import scraperwiki
import lxml.html
import requests
import base64
import re
import os
import sqlite3 as lite


# haal foto 's url van kapaza class = 

html = scraperwiki.scrape("http://nl.kapaza.be/belgie/agrarisch/")
root = lxml.html.fromstring(html) 
lijstfoto = root.cssselect('.inner_image_div')
print type(lijstfoto)
deelstring = ''
totaalstring = ''

#scraperwiki.sqlite.execute("CREATE  TABLE IF NOT EXISTS `fotos` (`id` INTEGER PRIMARY KEY,    `url` TEXT,  `bin` BLOB);")
print scraperwiki.sqlite.show_tables()

scraperwiki.sqlite.execute("drop table if exists  'fotostxt'")
scraperwiki.sqlite.execute("drop table if exists  'foto'")

print scraperwiki.sqlite.show_tables()
scraperwiki.sqlite.execute("CREATE  TABLE IF NOT EXISTS `fotostxt` (`id` INTEGER PRIMARY KEY,    `url` TEXT,  `bin` TEXT);")
print scraperwiki.sqlite.show_tables()



tel = 1

for   el in  lijstfoto:
        print type(el)
        for le in el:
             print type(le)
             print le.get('src')
             fotourl = le.get('src')  # in dic-v class  is er subelement img 
             foto  = requests.get(fotourl)
        binary = lite.Binary(foto.content)
        bintxt = base64.b64encode(foto.content)
        scraperwiki.sqlite.save(unique_keys =['id'] , data={'id' : tel ,'url':fotourl,'bin':bintxt},table_name = 'fotostext',verbose = 2)
        tel = tel + 1
        if tel == 4:
               break 


#print  lxml.html.tostring(el)
#          fotourl = el.get('url')  
#          print fotourl
#          deelstring = str(lxml.html.tostring(el))   
#          deelstring = lxml.html.tostring(el) 
#          print deelstring  , len(deelstring)
#          print deelstring.find('img src=')
#          print deelstring[35:] 
             
#          print el.find('img src') 
#          print el.attrib
#          print el.keys()  # class 
#          print el.items()
#          print el.values()    
#          print deelstring  , 'url' , fotourl 
#          totaalstring += deelstring   

           
#print totaalstring



#print foto.content
#scraperwiki.sqlite.save(unique_keys=["id"],data={"id" : teller,"fotoref":foto,"omschrijving":beschrijving},table_name="tweedehands",verbose=2)    


#scraperwiki.sqlite.save(unique_keys =['id'] , data={'id' : tel ,'url':fotourl,'bin':binary},table_name = 'fotos',verbose = 2)


#scraperwiki.sqlite.execute("insert into fotos(id , url , bin) VALUES (?,?,?)",( tel , fotourl ,binary))

# encoderen en als text opslaan

result =    scraperwiki.sqlite.select(" count(url) from fotostext")
print result

'''

def get_image_from_brick(lxml_brick):
    thumb_url = a.cssselect('img')[1].get('src')
    url = thumb_url.replace('_250', '_500') 
    r = requests.get(url)
    if r.status_code == 200:
        bin = base64.b64encode(r.content)
    elif r.status_code == 403:
        url = thumb_url.replace('_250', '_400')
        bin = base64.b64encode(requests.get(url).content)
    else:
        url = None
        bin = None
    return {
        'post_id': re.sub(r'[^0-9]+', '', a.get('href')),
        'timestamp': re.sub(r'[^0-9]+', '', a.get('class')),
        'post_url': a.get('href'),
        'url': url, 
        'thumb_url': thumb_url,
        'bin': bin
    }

base_url = 'http://zarinozappia.tumblr.com'
html = requests.get(base_url + '/archive')
dom = lxml.html.fromstring(html.text)

scraperwiki.sqlite.execute('CREATE  TABLE IF NOT EXISTS `photos` ( `post_id` INT PRIMARY KEY, `timestamp`  INT, `post_url` TEXT, `url` TEXT, `thumb_url` TEXT, `bin` TEXT)')

months = []
photos = []
carryon = True

for month in dom.cssselect('#browse_months_widget .month.active'):
    months.append(month.cssselect('a')[0].get('href'))

for month_url in months:
    # get first page of this month's photos
    html = requests.get(base_url + month_url)
    dom = lxml.html.fromstring(html.text)
    
    for a in dom.cssselect('a.brick.photo'):
        photos.append(get_image_from_brick(a))

    # save first page of this month's photos
    scraperwiki.sqlite.save(['post_id'], photos, 'photos')
    last_timestamp = photos[-1]['timestamp']
    photos = []

'''
'''

def ls(dir=''):
     print '$ ls ' + os.getcwd() + '/' + dir
     print os.system('ls -lAh ' + os.getcwd() + '/' + dir)
 
 def rm(f):
     os.remove(os.getcwd() + '/' + f)

'''
