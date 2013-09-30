#coding:utf-8
import sys, codecs, re, time, csv
sys.stdout = codecs.lookup('utf_8')[-1](sys.stdout)
print sys.stdout.encoding

import urllib2
from BeautifulSoup import BeautifulSoup

def main():
    baseUrl = "http://www.animecharactersdatabase.com/character.php?id="
    id = 875
    
    while id <= 45000:
        url = baseUrl + str(id)
        htmlfp = urllib2.urlopen(url)
        html = htmlfp.read().decode("utf-8", "replace")
        htmlfp.close()
    
        writer1 = csv.writer(open('./animecharactersdatabase_20120311.csv', 'ab'), lineterminator="\n")
    
        soup = BeautifulSoup(html)
        if soup.find('h1').string == 'ID not found!':
            continue
        besttable1 = soup.find('div', {'id' : 'besttable'})
        table1 = besttable1.find('table')
        thList = table1.findAll('th')
        tdList = table1.findAll('td')
        
        # init
        i = 0
        appearsIn = ''
        for th in thList:
            #Romaji Name
            if th.string == 'Romaji Name':
                romajiName = tdList[i].string
            #Japanese Name
            if th.string == 'Japanese Name':
                japaneseName = tdList[i].string
                if japaneseName is None:
                    japaneseName = ''
            # Role
            if th.string == 'Role':
                role = tdList[i].string
            # Appears In
            if th.string == 'Appears In':
                aAppearsIn = tdList[i].find('a')
                p = re.compile(r'\/>(.+)<\/a>')
                m = p.search(str(aAppearsIn).decode('utf-8'))
                appearsIn += (m.group(1) + ' // ')
            i += 1 #INCREMENT
        
        writer1.writerow([\
            '%s' % str(id).encode("utf-8"), \
            '%s' % romajiName.encode("utf-8"), \
            '%s' % japaneseName.encode("utf-8"), \
            '%s' % role.encode("utf-8"), \
            '%s' % appearsIn.encode("utf-8"), \
            '%s' % url.encode("utf-8"), \
        ])
        
        id += 1
        #time.sleep(1.0) # gentlemanly crawling

if __name__ == '__main__': main()#coding:utf-8
import sys, codecs, re, time, csv
sys.stdout = codecs.lookup('utf_8')[-1](sys.stdout)
print sys.stdout.encoding

import urllib2
from BeautifulSoup import BeautifulSoup

def main():
    baseUrl = "http://www.animecharactersdatabase.com/character.php?id="
    id = 875
    
    while id <= 45000:
        url = baseUrl + str(id)
        htmlfp = urllib2.urlopen(url)
        html = htmlfp.read().decode("utf-8", "replace")
        htmlfp.close()
    
        writer1 = csv.writer(open('./animecharactersdatabase_20120311.csv', 'ab'), lineterminator="\n")
    
        soup = BeautifulSoup(html)
        if soup.find('h1').string == 'ID not found!':
            continue
        besttable1 = soup.find('div', {'id' : 'besttable'})
        table1 = besttable1.find('table')
        thList = table1.findAll('th')
        tdList = table1.findAll('td')
        
        # init
        i = 0
        appearsIn = ''
        for th in thList:
            #Romaji Name
            if th.string == 'Romaji Name':
                romajiName = tdList[i].string
            #Japanese Name
            if th.string == 'Japanese Name':
                japaneseName = tdList[i].string
                if japaneseName is None:
                    japaneseName = ''
            # Role
            if th.string == 'Role':
                role = tdList[i].string
            # Appears In
            if th.string == 'Appears In':
                aAppearsIn = tdList[i].find('a')
                p = re.compile(r'\/>(.+)<\/a>')
                m = p.search(str(aAppearsIn).decode('utf-8'))
                appearsIn += (m.group(1) + ' // ')
            i += 1 #INCREMENT
        
        writer1.writerow([\
            '%s' % str(id).encode("utf-8"), \
            '%s' % romajiName.encode("utf-8"), \
            '%s' % japaneseName.encode("utf-8"), \
            '%s' % role.encode("utf-8"), \
            '%s' % appearsIn.encode("utf-8"), \
            '%s' % url.encode("utf-8"), \
        ])
        
        id += 1
        #time.sleep(1.0) # gentlemanly crawling

if __name__ == '__main__': main()