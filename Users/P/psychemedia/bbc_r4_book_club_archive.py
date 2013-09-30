import simplejson
import urllib,re
import scraperwiki

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

#BBC R4 Bookclub archive
url='http://www.bbc.co.uk/programmes/b006s5sf/episodes/player.json'

data=simplejson.load(urllib.urlopen(url))['episodes']

for d in data:
    print d
    p = d['programme']
    btg=bookTitleVicinity(p['short_synopsis'])
    btg=btg.strip(',')
    btg=btg.strip()
    btg=btg.strip('.')
    #print 'Guessing',btg
    #print p['title'],p['pid'],p['programme']['title'],p['short_synopsis']
    record={'series':p['programme']['title'],'title':p['title'],'pid':p['pid'], 'shortdesc':p['short_synopsis'],'bookTitleGuess':btg}
    #print record
    scraperwiki.datastore.save(["pid"], record)
    print 'ok...'import simplejson
import urllib,re
import scraperwiki

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

#BBC R4 Bookclub archive
url='http://www.bbc.co.uk/programmes/b006s5sf/episodes/player.json'

data=simplejson.load(urllib.urlopen(url))['episodes']

for d in data:
    print d
    p = d['programme']
    btg=bookTitleVicinity(p['short_synopsis'])
    btg=btg.strip(',')
    btg=btg.strip()
    btg=btg.strip('.')
    #print 'Guessing',btg
    #print p['title'],p['pid'],p['programme']['title'],p['short_synopsis']
    record={'series':p['programme']['title'],'title':p['title'],'pid':p['pid'], 'shortdesc':p['short_synopsis'],'bookTitleGuess':btg}
    #print record
    scraperwiki.datastore.save(["pid"], record)
    print 'ok...'