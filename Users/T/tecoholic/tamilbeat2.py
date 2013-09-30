###############################################
#   Scrapper to get album  information
###############################################

import re
import scraperwiki
import sys
#from scraperwiki.apiwrapper import getKeys, getData
from BeautifulSoup import BeautifulSoup

def makeSoup(url):
    ''' This function creates a BeautifulSoup object for the input url'''
    try:
        html = scraperwiki.scrape(url) # For scraperwiki
        #html = open(url,'rb')
    except:
        print 'Unable to find the page at '+url
        sys.exit()
    return BeautifulSoup(html)

def getAlbumData(soup):
    ''' This function takes a BeautifulSoup object as input and returns a
    library containing Album, Composer, and Album Artist'''
    film = {'Album':'Movie',
            'Composer':'Music Director',
            'Album Artist':'Stars'        
           }
    table = soup.find(id='AutoNumber6')
    rows = table.findAll('tr')
    for row in rows:
        txt = row.findAll('td')
        key = re.sub('(&nbsp;)?','',txt[0].text)
        if re.search('Title',key):
            film['Album'] = re.sub('(&nbsp;)?','',txt[1].text)
        elif re.search('Star',key):
            film['Album Artist'] = re.sub('\r?\n? ?(&nbsp;)?','',txt[1].text)
        elif re.search('Music',key):
            film['Composer'] = re.sub('(&nbsp;)?','',txt[1].text)
    return film

def getSongs(soup):
    '''This function takes the soup as input and outputs a list libraries made
    of Track Number, Title and Artist'''
    songList = []
    sa = []
    table = soup.find(id = 'AutoNumber4')
    if table.find('tbody'):
        table = table.find('tbody')
    rows = table.findAll('tr', recursive = False)
    for row in rows:
        if not row.find('table'):
            fonts = row.findAll('font')
            for font in fonts:
                txt = re.sub('\r?\n?( )?(&nbsp;)?','',font.text)
                if len(txt) > 0:
                    sa.append(txt)
    for i in range(len(sa)/2):
        song = {}
        song ['Track Number'] = i+1
        song ['Title'] = sa[i]
        song ['Artist'] = sa[2*i]
        if i==0:
            song ['Artist'] = sa[1]
        songList.append(song)
    print songList
    return songList

class mp3:
    ''' to create the complete tag group'''
    def __init__(self,film,song):
        ''' This function takes a library containg the film data and
        a library of song data to form a complete set of tags '''
        self.tags= {'Track Number':song['Track Number'],
                    'Title':song['Title'],
                    'Album':film['Album'],
                    'Artist':song['Artist'],
                    'Album Artist':film['Album Artist'],
                    'Composer':film['Composer']
                    }
        

srcscrap = 'tamilbeat1'
limit = 5
offset = 0
validity=1



scraperwiki.sqlite.attach('tamilbeat1') 
for row in scraperwiki.sqlite.select('* from `tamilbeat1`.swdata'):
    source = row.get('Url')
    print source
    soup = makeSoup(source)
    album  = getAlbumData(soup)
    songs = getSongs(soup)
    for song in songs:
        data = mp3(album,song)
        scraperwiki.datastore.save(['Track Number'],data.tags)
    #print album
    

###############################################
#   Scrapper to get album  information
###############################################

import re
import scraperwiki
import sys
#from scraperwiki.apiwrapper import getKeys, getData
from BeautifulSoup import BeautifulSoup

def makeSoup(url):
    ''' This function creates a BeautifulSoup object for the input url'''
    try:
        html = scraperwiki.scrape(url) # For scraperwiki
        #html = open(url,'rb')
    except:
        print 'Unable to find the page at '+url
        sys.exit()
    return BeautifulSoup(html)

def getAlbumData(soup):
    ''' This function takes a BeautifulSoup object as input and returns a
    library containing Album, Composer, and Album Artist'''
    film = {'Album':'Movie',
            'Composer':'Music Director',
            'Album Artist':'Stars'        
           }
    table = soup.find(id='AutoNumber6')
    rows = table.findAll('tr')
    for row in rows:
        txt = row.findAll('td')
        key = re.sub('(&nbsp;)?','',txt[0].text)
        if re.search('Title',key):
            film['Album'] = re.sub('(&nbsp;)?','',txt[1].text)
        elif re.search('Star',key):
            film['Album Artist'] = re.sub('\r?\n? ?(&nbsp;)?','',txt[1].text)
        elif re.search('Music',key):
            film['Composer'] = re.sub('(&nbsp;)?','',txt[1].text)
    return film

def getSongs(soup):
    '''This function takes the soup as input and outputs a list libraries made
    of Track Number, Title and Artist'''
    songList = []
    sa = []
    table = soup.find(id = 'AutoNumber4')
    if table.find('tbody'):
        table = table.find('tbody')
    rows = table.findAll('tr', recursive = False)
    for row in rows:
        if not row.find('table'):
            fonts = row.findAll('font')
            for font in fonts:
                txt = re.sub('\r?\n?( )?(&nbsp;)?','',font.text)
                if len(txt) > 0:
                    sa.append(txt)
    for i in range(len(sa)/2):
        song = {}
        song ['Track Number'] = i+1
        song ['Title'] = sa[i]
        song ['Artist'] = sa[2*i]
        if i==0:
            song ['Artist'] = sa[1]
        songList.append(song)
    print songList
    return songList

class mp3:
    ''' to create the complete tag group'''
    def __init__(self,film,song):
        ''' This function takes a library containg the film data and
        a library of song data to form a complete set of tags '''
        self.tags= {'Track Number':song['Track Number'],
                    'Title':song['Title'],
                    'Album':film['Album'],
                    'Artist':song['Artist'],
                    'Album Artist':film['Album Artist'],
                    'Composer':film['Composer']
                    }
        

srcscrap = 'tamilbeat1'
limit = 5
offset = 0
validity=1



scraperwiki.sqlite.attach('tamilbeat1') 
for row in scraperwiki.sqlite.select('* from `tamilbeat1`.swdata'):
    source = row.get('Url')
    print source
    soup = makeSoup(source)
    album  = getAlbumData(soup)
    songs = getSongs(soup)
    for song in songs:
        data = mp3(album,song)
        scraperwiki.datastore.save(['Track Number'],data.tags)
    #print album
    

