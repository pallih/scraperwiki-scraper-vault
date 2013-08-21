import scraperwiki, simplejson,urllib,string

def checkForOUContent(seriesData):
    ouItems=[]
    if 'supporting_content_items' in seriesData['programme']:
        for suppItem in seriesData['programme']['supporting_content_items']:
            print suppItem
            grabbed=0
            if suppItem['link_title'] != None:
                if string.find(suppItem['link_title'],"Open University")>-1 or string.find(suppItem['link_title'],"OpenLearn")>-1:
                    ouItems.append(suppItem)
                    grabbed=1
            if grabbed==0 and suppItem['title']!=None:
                if string.find(suppItem['title'],"Open University")>-1 or string.find(suppItem['title'],"OpenLearn")>-1:
                    ouItems.append(suppItem)
                    grabbed=1
            if grabbed==0 and 'link_uri' in suppItem:
                if suppItem['link_uri']!=None:
                    if string.find(suppItem['link_uri'],'open.edu')>-1:
                        ouItems.append(suppItem)
                        grabbed=1
    return ouItems

def parseEpisodesData(seriesData,episodesData):
    print seriesData,episodesData
    ouItems=checkForOUContent(seriesData)
    if len(ouItems)>0:
        print ouItems[0]['link_title'], ouItems[0]['title'],ouItems[0]['published_image_uri'],ouItems[0]['link_uri'],ouItems[0]['content']
    else:
        print 'no OU items for ',seriesData['programme']['title']
        ouItems.append({'link_title':'','title':'','published_image_uri':'','link_uri':'','content':''})
    for programme in episodesData['episodes']:
        episode=programme['programme']
        print episode
        print episode['title'],episode['short_synopsis'],episode['media']['availability'],episode['media']['format'],episode['pid'],seriesData['programme']['title'],seriesData['programme']['short_synopsis']
        scraperwiki.sqlite.save(unique_keys=['progID'], table_name='bbcOUcoProClips', data={ 'progID':episode['pid'], 'seriesID':seriesData['programme']['pid'],'seriesTitle':seriesData['programme']['title'],'short_synposis':episode['short_synopsis'],'expires':episode['media']['expires'],'availability':episode['media']['availability'],'format':episode['media']['format'], 'title':episode['title'],'image':'http://static.bbc.co.uk/programmeimages/272x153/episode/'+episode['pid']+'.jpg', 'ouLinkTitle':ouItems[0]['link_title'],'ouTitle':ouItems[0]['title'],'ouImage':ouItems[0]['published_image_uri'],'ouURI':ouItems[0]['link_uri'],'ouContent':ouItems[0]['content']})


def getCurrentEpisodes(seriesID):
    episodesURL='http://www.bbc.co.uk/programmes/'+seriesID+'/episodes/player.json'
    try:
        episodesData=simplejson.load(urllib.urlopen(episodesURL))
    except:
        episodesData=''
    if episodesData!='':
        seriesURL='http://www.bbc.co.uk/programmes/'+seriesID+'.json'
        seriesData=simplejson.load(urllib.urlopen(seriesURL))
        parseEpisodesData(seriesData,episodesData)


def parseClipsData(seriesData,clipsData):
    print seriesData,clipsData
    ouItems=checkForOUContent(seriesData)
    if len(ouItems)>0:
        print ouItems[0]['link_title'], ouItems[0]['title'],ouItems[0]['published_image_uri'],ouItems[0]['link_uri'],ouItems[0]['content']
    else:
        print 'no OU items for ',seriesData['programme']['title']
        ouItems.append({'link_title':'','title':'','published_image_uri':'','link_uri':'','content':''})
        #rather than use seriesID, use 'parent' data, and maybe check it against seriesID?
    for clip in clipsData['clips']['programmes']:
        if clip['type']=='clip':
            print clip['pid'],clip['media_type'],clip['title'],clip['short_synopsis'],clip['duration']
            scraperwiki.sqlite.save(unique_keys=['clipID'],table_name='bbcOUcoPros', data={ 'seriesID':seriesData['programme']['pid'],'seriesTitle':seriesData['programme']['title'], 'clipID':clip['pid'],'mediaType':clip['media_type'], 'title':clip['title'],'short_synopsis':clip['short_synopsis'],'duration':clip['duration'], 'ouLinkTitle':ouItems[0]['link_title'], 'ouTitle':ouItems[0]['title'], 'ouImage':ouItems[0]['published_image_uri'], 'ouURI':ouItems[0]['link_uri'], 'ouContent':ouItems[0]['content']  })


#"type":"clip","pid":"p00pxgd0","media_type":"audio_video","title":"Nikka makes waffles for Si and Dave","short_synopsis":"95 year old Nikka rustles up waffles on her 65 year old waffle-iron for the bikers.","duration":222

def getSeriesClips(seriesID): 
    print 'Trying',seriesID
    clipsURL='http://www.bbc.co.uk/programmes/'+seriesID+'/clips.json'
    try:
        clipsData=simplejson.load(urllib.urlopen(clipsURL))
    except:
        clipsData=''
    if clipsData!='':
        seriesURL='http://www.bbc.co.uk/programmes/'+seriesID+'.json'
        seriesData=simplejson.load(urllib.urlopen(seriesURL))
        parseClipsData(seriesData,clipsData)
#if we're grabbing current episodes and clips, need to optimise this so we don't get series data twice


def getSeriesData(seriesID,typ='current'):
    if typ=='current':
        getCurrentEpisodes(seriesID)
    elif typ=='clips':
        getSeriesClips(seriesID)
    else: pass
        
def parseSeriesListing(seriesListing,typ='current'):
    for series in seriesListing:
        seriesID=series['u'].split('/')[-1]
        if seriesID !='':
            getSeriesData(seriesID,typ)


def getSeriesList():
    seriesFeed='http://feeds.delicious.com/v2/json/psychemedia/oubbccopro?count=100'
    feed=simplejson.load(urllib.urlopen(seriesFeed))
    return feed

try:
    scraperwiki.sqlite.execute('drop table "bbcOUcoPros"')
    scraperwiki.sqlite.execute('drop table "bbcOUcoProClips"')
except:
    pass

seriesListing=getSeriesList()
print seriesListing
parseSeriesListing(seriesListing,'clips')