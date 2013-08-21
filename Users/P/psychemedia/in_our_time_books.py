# http://www.bbc.co.uk/programmes/b00xhz8d.json

import simplejson
import urllib
import scraperwiki

#BBC R4 In Our Time referenced books archive
url='http://www.bbc.co.uk/programmes/b006qykl/episodes/player.json'

data=simplejson.load(urllib.urlopen(url))['episodes']
#db=urllib.urlopen('http://api.scraperwiki.com/api/1.0/datastore/getdata?format=jsondict&name=in_our_time_books&limit=500')
#currdb=eval(db.read())

def getProgDetails(id):
    books=''
    long_synopsis=''
    cats=[]
    progurl='http://www.bbc.co.uk/programmes/'+id+'.json'
    progdata=simplejson.load(urllib.urlopen(progurl))['programme']
    if 'supporting_content_items' in progdata:
        for supp in progdata['supporting_content_items']:
            if 'title' in supp:
                print supp['title']
                if supp['title'].upper()=='FURTHER READING':
                    print supp['content']
                    books=supp['content']
    else:
        print 'nope',progdata
    if 'long_synopsis' in progdata:
        long_synopsis=progdata['long_synopsis']
        print 'desc',progdata['long_synopsis']
    for item in progdata['categories']:
        if item['type']=='subject':  
            cats.append(item['title'])
    return books,long_synopsis,cats

currids=[]
#for prog in currdb:
#    currids.append(prog['pid'])
#print currids

for d in data:
    print d
    p = d['programme']
#    if p['pid'] in currids:
#        print 'Already got',p['pid']
#    else:
    if True:
        print p['title'],p['pid'],p['programme']['title'],p['short_synopsis']
        books,long_synopsis,cats=getProgDetails(p['pid'])
        record={'series':p['programme']['title'],'title':p['title'],'pid':p['pid'], 'shortdesc':p['short_synopsis'],'long_synopsis':long_synopsis,'books':books,'categories':cats}
        print record
        scraperwiki.datastore.save(["pid"], record)
        print 'ok...'
        
