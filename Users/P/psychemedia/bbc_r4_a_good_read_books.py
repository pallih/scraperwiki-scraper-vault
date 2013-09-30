import simplejson
import urllib,re
import scraperwiki

'''
def bookTitleVicinity(title):
    btv=title
    m=re.search('(?<=book ).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=novel ).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=novel,).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=thriller).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=autobiography).*',title)
    if m:
        return m.group(0)+' Autobiography'
    m=re.search('(?<=biography of).*',title)
    if m:
        return m.group(0)+' Biography'
    m=re.search('(?<=bestseller).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=bestselling).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=discusses).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=discuss).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=author of).*',title)
    if m:
        return m.group(0)

    m=re.search('(?<=about).*',title)
    if m:
        return m.group(0)
    return btv
'''

def getProgDetails(pid):
    #episodes http://www.bbc.co.uk/programmes/b011zms3.json
    purl='http://www.bbc.co.uk/programmes/'+pid+'.json'
    details=simplejson.load(urllib.urlopen(purl))
    print details
    p=details['programme']
    supp=p['supporting_content_items'][0]['content']
    record={'series':p['parent']['programme']['title'],'title':p['title'],'pid':p['pid'], 'shortdesc':p['short_synopsis'],'books':supp}
    scraperwiki.sqlite.save(["pid"], record)

#BBC R4 A Good Read archive
url='http://www.bbc.co.uk/programmes/b006v8jn/episodes/player.json'

data=simplejson.load(urllib.urlopen(url))['episodes']

for d in data:
    p = d['programme']
    print p['pid'],p
    getProgDetails(p['pid'])
    print 'ok...'
import simplejson
import urllib,re
import scraperwiki

'''
def bookTitleVicinity(title):
    btv=title
    m=re.search('(?<=book ).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=novel ).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=novel,).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=thriller).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=autobiography).*',title)
    if m:
        return m.group(0)+' Autobiography'
    m=re.search('(?<=biography of).*',title)
    if m:
        return m.group(0)+' Biography'
    m=re.search('(?<=bestseller).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=bestselling).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=discusses).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=discuss).*',title)
    if m:
        return m.group(0)
    m=re.search('(?<=author of).*',title)
    if m:
        return m.group(0)

    m=re.search('(?<=about).*',title)
    if m:
        return m.group(0)
    return btv
'''

def getProgDetails(pid):
    #episodes http://www.bbc.co.uk/programmes/b011zms3.json
    purl='http://www.bbc.co.uk/programmes/'+pid+'.json'
    details=simplejson.load(urllib.urlopen(purl))
    print details
    p=details['programme']
    supp=p['supporting_content_items'][0]['content']
    record={'series':p['parent']['programme']['title'],'title':p['title'],'pid':p['pid'], 'shortdesc':p['short_synopsis'],'books':supp}
    scraperwiki.sqlite.save(["pid"], record)

#BBC R4 A Good Read archive
url='http://www.bbc.co.uk/programmes/b006v8jn/episodes/player.json'

data=simplejson.load(urllib.urlopen(url))['episodes']

for d in data:
    p = d['programme']
    print p['pid'],p
    getProgDetails(p['pid'])
    print 'ok...'
