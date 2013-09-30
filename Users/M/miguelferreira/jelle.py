import scraperwiki
import lxml.html
import json

def printHtml(html):
    print lxml.html.tostring(html)

def getTitle(root):
    return root.cssselect("div#t_col1 div#chunk p b")[0].text_content()          

def getReleaseDate(root):
    results = []
    for a in root.cssselect("div#t_col1 div#chunk p a"):           
        results.append(a.text_content())
    if len(results) >= 2:
        return results[1]
    else:
        return ""

def getSources(root):
    sources = []
    for div in root.cssselect("div#t_col1 div#chunk"):
        for h2 in div.cssselect("h2.green"):
            if h2.text_content() == "Music From":
                for a in div.cssselect("ul li a"):
                    sources.append(a.text_content())
    return sources

def getAuthors(root):
    authors = []
    for div in root.cssselect("div#t_col1 div#chunk"):
        for h2 in div.cssselect("h2.green"):
            if h2.text_content() == "Music By":
                links = div.cssselect("ul li a")
                if links != []:
                    for a in links:
                        authors.append(a.text_content())
                else:
                    for li in div.cssselect("ul li"):
                        authors.append(li.text_content())
    return authors

def getDisks(root):
    for div in root.cssselect("div#t_col2 div#chunk"):           
        for h2 in div.cssselect("h2"):
            if h2.text_content() == "Track Listing":
                try:
                    if 'class' not in div.cssselect("tr")[0].attrib:
                        return getMultiDisk(root)
                    else:
                        return getSingleDisk(root)
                except IndexError as e:
                    print e
                    return {}

def getMultiDisk(root):
    disks = {}
    tracks = []
    diskLabel = ""
    for div in root.cssselect("div#t_col2 div#chunk"):           
        for h2 in div.cssselect("h2"):
            if h2.text_content() == "Track Listing": 
                for tr in div.cssselect("tr"):
                    if 'class' not in tr.attrib:
                        b = tr.cssselect("td b")
                        if b != [] and diskLabel == "":
                            diskLabel = b[0].text_content()
                        elif b != []:
                            disks[diskLabel] = tracks
                            tracks = []
                            diskLabel = b[0].text_content()
                    if 'class' in tr.attrib and tr.attrib['class'] != "track-time":
                        tracks.append(getTrack(tr))
    disks[diskLabel] = tracks
    return disks

def getSingleDisk(root):
    disks = {}
    tracks = []
    for div in root.cssselect("div#t_col2 div#chunk"):           
        for h2 in div.cssselect("h2"):
            if h2.text_content() == "Track Listing":
                for tr in div.cssselect("tr"):
                    if 'class' in tr.attrib and tr.attrib['class'] != "track-time":
                        tracks.append(getTrack(tr))
    disks['Disk 1'] = tracks
    return disks

def getTrack(tr):
    trackNumber = tr.cssselect("td")[0].cssselect("b")[0].text_content()
    trackName = tr.cssselect("td")[1].text_content()
    trackDuration = tr.cssselect("td")[2].text_content()
    return {"trackNumber" : trackNumber, "trackName" : trackName, "trackDuration" : trackDuration}

def getArtWork(root):
    albumart = root.cssselect("div#t_col1 div#chunk div.albumart img")
    if albumart != []:
        return albumart[0].attrib['src']
    else:
        return root.cssselect("div#t_col1 div#chunk div.soundtrackphoto img")[0].attrib['src']

def getSoundTrack(root):
    title = getTitle(root)
    releaseDate = getReleaseDate(root)
    artWorkUrl = "{0}{1}".format(rootUrl, getArtWork(root))
    sources = getSources(root)
    authors = getAuthors(root)
    disks = getDisks(root)
    soundTrack = { "title": title, 
                   "releaseDate": releaseDate, 
                   "artWorkUrl": artWorkUrl, 
                   "sources": sources, 
                   "authors": authors, 
                   "disks": disks }
    return soundTrack

def scrapeSoundTrack(rootUrl, id):
    html = scraperwiki.scrape("{0}/albums/database/?id={1}".format(rootUrl, id))
    root = lxml.html.fromstring(html)
    try:
        getTitle(root)
    except IndexError as e:
        print "Id {0} has no content".format(id)
        return {}
    soundTrack = getSoundTrack(root)
    return soundTrack


rootUrl = "http://www.soundtrack.net"

soundTracks = {}
#for id in range(1, 8498):
start = 6001
end = 8498
for id in range(start, end):
    soundTracks[id] = scrapeSoundTrack(rootUrl, id)
    

#id = 38
#scrapeSoundTrack(rootUrl, id)
#soundTracks[id] = soundTrack

jsonText = json.dumps(soundTracks)
print jsonText
key ="jsonText-{0}-{1}".format(start, (end - 1))
scraperwiki.sqlite.save(unique_keys=[key], data={key: jsonText})


import scraperwiki
import lxml.html
import json

def printHtml(html):
    print lxml.html.tostring(html)

def getTitle(root):
    return root.cssselect("div#t_col1 div#chunk p b")[0].text_content()          

def getReleaseDate(root):
    results = []
    for a in root.cssselect("div#t_col1 div#chunk p a"):           
        results.append(a.text_content())
    if len(results) >= 2:
        return results[1]
    else:
        return ""

def getSources(root):
    sources = []
    for div in root.cssselect("div#t_col1 div#chunk"):
        for h2 in div.cssselect("h2.green"):
            if h2.text_content() == "Music From":
                for a in div.cssselect("ul li a"):
                    sources.append(a.text_content())
    return sources

def getAuthors(root):
    authors = []
    for div in root.cssselect("div#t_col1 div#chunk"):
        for h2 in div.cssselect("h2.green"):
            if h2.text_content() == "Music By":
                links = div.cssselect("ul li a")
                if links != []:
                    for a in links:
                        authors.append(a.text_content())
                else:
                    for li in div.cssselect("ul li"):
                        authors.append(li.text_content())
    return authors

def getDisks(root):
    for div in root.cssselect("div#t_col2 div#chunk"):           
        for h2 in div.cssselect("h2"):
            if h2.text_content() == "Track Listing":
                try:
                    if 'class' not in div.cssselect("tr")[0].attrib:
                        return getMultiDisk(root)
                    else:
                        return getSingleDisk(root)
                except IndexError as e:
                    print e
                    return {}

def getMultiDisk(root):
    disks = {}
    tracks = []
    diskLabel = ""
    for div in root.cssselect("div#t_col2 div#chunk"):           
        for h2 in div.cssselect("h2"):
            if h2.text_content() == "Track Listing": 
                for tr in div.cssselect("tr"):
                    if 'class' not in tr.attrib:
                        b = tr.cssselect("td b")
                        if b != [] and diskLabel == "":
                            diskLabel = b[0].text_content()
                        elif b != []:
                            disks[diskLabel] = tracks
                            tracks = []
                            diskLabel = b[0].text_content()
                    if 'class' in tr.attrib and tr.attrib['class'] != "track-time":
                        tracks.append(getTrack(tr))
    disks[diskLabel] = tracks
    return disks

def getSingleDisk(root):
    disks = {}
    tracks = []
    for div in root.cssselect("div#t_col2 div#chunk"):           
        for h2 in div.cssselect("h2"):
            if h2.text_content() == "Track Listing":
                for tr in div.cssselect("tr"):
                    if 'class' in tr.attrib and tr.attrib['class'] != "track-time":
                        tracks.append(getTrack(tr))
    disks['Disk 1'] = tracks
    return disks

def getTrack(tr):
    trackNumber = tr.cssselect("td")[0].cssselect("b")[0].text_content()
    trackName = tr.cssselect("td")[1].text_content()
    trackDuration = tr.cssselect("td")[2].text_content()
    return {"trackNumber" : trackNumber, "trackName" : trackName, "trackDuration" : trackDuration}

def getArtWork(root):
    albumart = root.cssselect("div#t_col1 div#chunk div.albumart img")
    if albumart != []:
        return albumart[0].attrib['src']
    else:
        return root.cssselect("div#t_col1 div#chunk div.soundtrackphoto img")[0].attrib['src']

def getSoundTrack(root):
    title = getTitle(root)
    releaseDate = getReleaseDate(root)
    artWorkUrl = "{0}{1}".format(rootUrl, getArtWork(root))
    sources = getSources(root)
    authors = getAuthors(root)
    disks = getDisks(root)
    soundTrack = { "title": title, 
                   "releaseDate": releaseDate, 
                   "artWorkUrl": artWorkUrl, 
                   "sources": sources, 
                   "authors": authors, 
                   "disks": disks }
    return soundTrack

def scrapeSoundTrack(rootUrl, id):
    html = scraperwiki.scrape("{0}/albums/database/?id={1}".format(rootUrl, id))
    root = lxml.html.fromstring(html)
    try:
        getTitle(root)
    except IndexError as e:
        print "Id {0} has no content".format(id)
        return {}
    soundTrack = getSoundTrack(root)
    return soundTrack


rootUrl = "http://www.soundtrack.net"

soundTracks = {}
#for id in range(1, 8498):
start = 6001
end = 8498
for id in range(start, end):
    soundTracks[id] = scrapeSoundTrack(rootUrl, id)
    

#id = 38
#scrapeSoundTrack(rootUrl, id)
#soundTracks[id] = soundTrack

jsonText = json.dumps(soundTracks)
print jsonText
key ="jsonText-{0}-{1}".format(start, (end - 1))
scraperwiki.sqlite.save(unique_keys=[key], data={key: jsonText})


