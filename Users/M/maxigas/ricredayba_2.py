#!/usr/bin/python
# scrape ric.redah.ba
# Sample URL: http://80.71.144.22/english/index.php?str=13&lotID=RICMoPod-04303-2007&TIP=0

import scraperwiki
from urllib2 import urlopen
from itertools import product
import re, htmlentitydefs

# from http://effbot.org/zone/re-sub.htm#unescape-html
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

# 22 area codes:
areas=('Mo','Ca','Ci','Ja','Ko','Ne','Pr','Ra','St','Gr','Lj','Po','Si','Ku','Li','To','Be','Bi','Ga','Im','Nv','Tr')
years=range(2000,2012)
numbers = map(lambda x: '%0*d' % (5, x), range(0,999)) # 5 digits: 00000-99999
urls = [ "http://ric.redah.ba/english/index.php?str=13&lotID=RIC%sPod-%s-%s&TIP=0" % (a, n, y) for a, n, y in product(areas, years, numbers) ]
surls = {}
re_html = re.compile('<.*?>')
try:
    n = scraperwiki.sqlite.get_var('n')
except:
    n = 0
try:
    laps = scraperwiki.sqlite.get_var('laps')
except:
    laps = 0

def parse(url):
    "The idea is to set a variable on key name and find the value in the next line."
    global n
    retry = 3
    while retry:
        if retry == 3:
            n += 1
#        try:
            x,r = ['',{}]
            scraperwiki.sqlite.save_var('n', n)
            print '#'+str(n)+':', url
            for l in  urlopen(url).readlines():
                if not x:
                    if 'Short name' in l:
                        x = 'short_name'
                    elif 'ID num' in l:
                        x = 'id'
                    elif 'Organizational form' in l:
                        x = 'form'
                    elif 'Ownership type' in l:
                        x = 'type'
                    elif 'Line of business' in l:
                        x = 'line'
                    elif 'Num. of employees' in l:
                        x = 'employees'
                    elif 'Address' in l:
                        x = 'address'
                    elif 'City' in l:
                        x = 'city'
                    elif 'Zip code' in l:
                        x = 'zip'
                    elif 'Canton' in l:
                        x = 'canton'
                    elif 'Telephone' in l:
                        x = 'telephone'
                    elif 'Fax' in l:
                        x = 'fax'
                    elif 'E-mail' in l:
                        x = 'email'
                    elif 'Web' in l:
                        x = 'web'
                    elif 'Contact person:' in l: #the double colon at the end is crucial!
                        x = 'person'
                else:
                    #r[x] = unescape(re_html.sub('', l).strip(' \n').decode('windows-1250'))
                    r[key] = unescape(r[key]).encode('utf8'
                    x = ''
            if r.has_key('short_name'):
                r['url'] = url
                r['uid'] = base64.b16encode(url)
                print r
                scraperwiki.sqlite.save(['uid'], r)
            retry = 0
#        except:
#            print '!!!/\/\/\!!! UNKNOWN ERROR !!!/\/\/\!!!'
#            print 'Retrying.....'
#            retry -= 1

def search_pages():
    links = []
    vowels = ['a', 'e', 'i', 'o', 'u']
    lastpage = {'a': 1996, 'e': 1990, 'i': 1996, 'o': 1993, 'u': 1778}
    totalrows = {'a': 19964, 'e': 19901, 'i': 19964, 'o': 19937, 'u': 17781}
    for vowel in vowels[:2]:
        print '\nGenerating urls for:', vowel
        surls[vowel] = [ 'http://ric.redah.ba/english/index.php?pageNum_poduzetnici=%s&totalRows_poduzetnici=%s&Search=%s&submit=Search&str=7&TIP=0' % (page, totalrows[vowel], vowel) for page in range(0, lastpage[vowel] - 1899) ]
        print 'Looping...'
        for surl in surls[vowel]:
            print '.',
            link_lines = filter(lambda x: 't1tableNazivBold' in x, urlopen(surl).readlines())
            print ':',
            map(lambda x: links.append(x[88:145]), link_lines)
    links = [ 'http://ric.redah.ba' + x for x in links ]
    print "\n\n=> URL COUNT:", len(links)
    return links

urls = [ "http://ric.redah.ba/english/index.php?str=13&lotID=RIC%sPod-%s-%s&TIP=0" % (a, n, y) for a, n, y in product(areas, years, numbers) ]
    
for url in search_pages():
    parse(url)



#!/usr/bin/python
# scrape ric.redah.ba
# Sample URL: http://80.71.144.22/english/index.php?str=13&lotID=RICMoPod-04303-2007&TIP=0

import scraperwiki
from urllib2 import urlopen
from itertools import product
import re, htmlentitydefs

# from http://effbot.org/zone/re-sub.htm#unescape-html
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

# 22 area codes:
areas=('Mo','Ca','Ci','Ja','Ko','Ne','Pr','Ra','St','Gr','Lj','Po','Si','Ku','Li','To','Be','Bi','Ga','Im','Nv','Tr')
years=range(2000,2012)
numbers = map(lambda x: '%0*d' % (5, x), range(0,999)) # 5 digits: 00000-99999
urls = [ "http://ric.redah.ba/english/index.php?str=13&lotID=RIC%sPod-%s-%s&TIP=0" % (a, n, y) for a, n, y in product(areas, years, numbers) ]
surls = {}
re_html = re.compile('<.*?>')
try:
    n = scraperwiki.sqlite.get_var('n')
except:
    n = 0
try:
    laps = scraperwiki.sqlite.get_var('laps')
except:
    laps = 0

def parse(url):
    "The idea is to set a variable on key name and find the value in the next line."
    global n
    retry = 3
    while retry:
        if retry == 3:
            n += 1
#        try:
            x,r = ['',{}]
            scraperwiki.sqlite.save_var('n', n)
            print '#'+str(n)+':', url
            for l in  urlopen(url).readlines():
                if not x:
                    if 'Short name' in l:
                        x = 'short_name'
                    elif 'ID num' in l:
                        x = 'id'
                    elif 'Organizational form' in l:
                        x = 'form'
                    elif 'Ownership type' in l:
                        x = 'type'
                    elif 'Line of business' in l:
                        x = 'line'
                    elif 'Num. of employees' in l:
                        x = 'employees'
                    elif 'Address' in l:
                        x = 'address'
                    elif 'City' in l:
                        x = 'city'
                    elif 'Zip code' in l:
                        x = 'zip'
                    elif 'Canton' in l:
                        x = 'canton'
                    elif 'Telephone' in l:
                        x = 'telephone'
                    elif 'Fax' in l:
                        x = 'fax'
                    elif 'E-mail' in l:
                        x = 'email'
                    elif 'Web' in l:
                        x = 'web'
                    elif 'Contact person:' in l: #the double colon at the end is crucial!
                        x = 'person'
                else:
                    #r[x] = unescape(re_html.sub('', l).strip(' \n').decode('windows-1250'))
                    r[key] = unescape(r[key]).encode('utf8'
                    x = ''
            if r.has_key('short_name'):
                r['url'] = url
                r['uid'] = base64.b16encode(url)
                print r
                scraperwiki.sqlite.save(['uid'], r)
            retry = 0
#        except:
#            print '!!!/\/\/\!!! UNKNOWN ERROR !!!/\/\/\!!!'
#            print 'Retrying.....'
#            retry -= 1

def search_pages():
    links = []
    vowels = ['a', 'e', 'i', 'o', 'u']
    lastpage = {'a': 1996, 'e': 1990, 'i': 1996, 'o': 1993, 'u': 1778}
    totalrows = {'a': 19964, 'e': 19901, 'i': 19964, 'o': 19937, 'u': 17781}
    for vowel in vowels[:2]:
        print '\nGenerating urls for:', vowel
        surls[vowel] = [ 'http://ric.redah.ba/english/index.php?pageNum_poduzetnici=%s&totalRows_poduzetnici=%s&Search=%s&submit=Search&str=7&TIP=0' % (page, totalrows[vowel], vowel) for page in range(0, lastpage[vowel] - 1899) ]
        print 'Looping...'
        for surl in surls[vowel]:
            print '.',
            link_lines = filter(lambda x: 't1tableNazivBold' in x, urlopen(surl).readlines())
            print ':',
            map(lambda x: links.append(x[88:145]), link_lines)
    links = [ 'http://ric.redah.ba' + x for x in links ]
    print "\n\n=> URL COUNT:", len(links)
    return links

urls = [ "http://ric.redah.ba/english/index.php?str=13&lotID=RIC%sPod-%s-%s&TIP=0" % (a, n, y) for a, n, y in product(areas, years, numbers) ]
    
for url in search_pages():
    parse(url)



