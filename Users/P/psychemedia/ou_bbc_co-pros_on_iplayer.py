import scraperwiki, simplejson,urllib,string


def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass


def checkForNewOUContent(seriesData):
    ouItems=[]
    if 'supporting_content_items' in seriesData['programme']:
        for suppItem in seriesData['programme']['supporting_content_items']:
            print suppItem
            grabbed=0
            if suppItem['link_title'] != None:
                if string.find(suppItem['link_title'],"Open University")>-1 or string.find(suppItem['link_title'],"OpenLearn")>-1:
                    ouItems=suppItem
                    grabbed=1
            if grabbed==0 and suppItem['title']!=None:
                if string.find(suppItem['title'],"Open University")>-1 or string.find(suppItem['title'],"OpenLearn")>-1:
                    ouItems=suppItem
                    grabbed=1
            if grabbed==0 and 'link_uri' in suppItem:
                if suppItem['link_uri']!=None:
                    if string.find(suppItem['link_uri'],'open.edu')>-1:
                        ouItems=suppItem
                        grabbed=1
    seriesID=seriesData['programme']['pid']
    if len(ouItems)>0:
        print ouItems['link_title'], ouItems['title'],ouItems['published_image_uri'],ouItems['link_uri'],ouItems['content']
        data=ouItems
        data['ouTitle']=data['title']
        data['seriesID']=seriesID
        ouSeriesDetails[seriesID]=data
        scraperwiki.sqlite.save(unique_keys=['seriesID'], table_name='ouProgData', data=data)
    else:
        print 'no OU items for ',seriesData['programme']['title']
        ouItems={'link_title':'','ouTitle':'','published_image_uri':'','link_uri':'','content':''}
        data=ouItems
        data['seriesID']=seriesData['programme']['pid']
        scraperwiki.sqlite.save(unique_keys=['seriesID'], table_name='ouProgData', data=data)  
        ouSeriesDetails[seriesID]=data
    return ouItems

def checkForOUContent(seriesData):
    seriesID=seriesData['programme']['pid']
    if seriesID not in ouSeries:
        print 'new to me... looking for OU details'
        return checkForNewOUContent(seriesData)
    return ouSeriesDetails[seriesID]

def parseEpisodesData(seriesData,episodesData):
    print seriesData,episodesData
    ouItems=checkForOUContent(seriesData)
    print 'ou',ouItems
    for programme in episodesData['episodes']:
        episode=programme['programme']
        print episode
        print episode['title'],episode['short_synopsis'],episode['media']['availability'],episode['media']['format'],episode['pid'],seriesData['programme']['title'],seriesData['programme']['short_synopsis']
        scraperwiki.sqlite.save(unique_keys=['progID'], table_name='bbcOUcoPros', data={ 'progID':episode['pid'], 'seriesID':seriesData['programme']['pid'],'seriesTitle':seriesData['programme']['title'],'short_synopsis':episode['short_synopsis'],'expires':episode['media']['expires'],'availability':episode['media']['availability'],'format':episode['media']['format'], 'title':episode['title'],'image':'http://static.bbc.co.uk/programmeimages/272x153/episode/'+episode['pid']+'.jpg', 'ouLinkTitle':ouItems['link_title'],'ouTitle':ouItems['ouTitle'],'ouImage':ouItems['published_image_uri'],'ouURI':ouItems['link_uri'],'ouContent':ouItems['content']})

def getSeriesData(seriesID):
    episodesURL='http://www.bbc.co.uk/programmes/'+seriesID+'/episodes/player.json'
    try:
        episodesData=simplejson.load(urllib.urlopen(episodesURL))
    except:
        episodesData=''
    if debug==1:print episodesURL,episodesData
    if episodesData!='':
        seriesURL='http://www.bbc.co.uk/programmes/'+seriesID+'.json'
        seriesData=simplejson.load(urllib.urlopen(seriesURL))
        parseEpisodesData(seriesData,episodesData)

def getSeriesUpcoming(seriesID):
    upcomingURL='http://www.bbc.co.uk/programmes/'+seriesID+'/episodes/upcoming.json'
    print upcomingURL
    try:
        upcomingData=simplejson.load(urllib.urlopen(upcomingURL))
    except: return
    print 'got upcoming...'
    for item in upcomingData['broadcasts']:
        data={}
        data=ouSeriesDetails[seriesID]
        data['date']=item['schedule_date']
        data['startTime']=item['start']
        data['endTime']=item['end']
        data['duration']=item['duration']
        data['service']=item['service']['title']
        prog=item['programme']
        data['progID']=prog['pid']
        data['title']=prog['title']
        data['short_synopsis']=prog['short_synopsis']
        if prog['programme']['pid']!=data['seriesID']:
            print 'oops',prog['programme']['pid'],data['seriesID']
            exit(-1)
        else:
            data['seriesID']=prog['programme']['pid']
            data['seriesTitle']=prog['programme']['title']
            print data
            scraperwiki.sqlite.save( unique_keys=[],table_name='upcomingOUBBC', data=data)


'''{"programme":{"type":"episode","pid":"p00kjq6h","position":1,"title":"Spark","short_synopsis":"How pioneers unlocked electricity's mysteries and built strange instruments to create it.","media_type":"audio_video","duration":3600,"display_titles":{"title":"Shock and Awe: The Story of Electricity","subtitle":"Spark"},"first_broadcast_date":"2011-10-06T21:00:00+01:00","programme":{"type":"series","pid":"p00kjq6d","title":"Shock and Awe: The Story of Electricity","position":null,"expected_child_count":3,"first_broadcast_date":"2011-10-06T21:00:00+01:00","ownership":{"service":{"type":"tv","id":"bbc_four","key":"bbcfour","title":"BBC Four"}}},"is_available_mediaset_pc_sd":false,"is_legacy_media":false}}'''

def parseSeriesListing(seriesListing):
    for series in seriesListing:
        seriesID=series['u'].split('/')[-1]
        if seriesID !='':
            getSeriesData(seriesID)
            getSeriesUpcoming(seriesID)


def getSeriesList():
    seriesFeed='http://feeds.delicious.com/v2/json/psychemedia/oubbccopro?count=100'
    feed=simplejson.load(urllib.urlopen(seriesFeed))
    return feed

#try:
#    scraperwiki.sqlite.execute('drop table "bbcOUcoPros"')
#except:
#    pass

debug=0

if debug==0:
    dropper('upcomingOUBBC')
    #dropper('ouProgData')
    try:
        q = '* FROM "ouProgData"'
        ouDetails = scraperwiki.sqlite.select(q)
    except: ouDetails=[]
    ouSeriesDetails={}
    ouSeries=[]
    for series in ouDetails:
        ouSeries.append(series['seriesID'])
        ouSeriesDetails[series['seriesID']]=series

seriesListing=getSeriesList()
print seriesListing

if debug==0: parseSeriesListing(seriesListing)

#need a pass that deletes or archives programmes no longer available?import scraperwiki, simplejson,urllib,string


def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass


def checkForNewOUContent(seriesData):
    ouItems=[]
    if 'supporting_content_items' in seriesData['programme']:
        for suppItem in seriesData['programme']['supporting_content_items']:
            print suppItem
            grabbed=0
            if suppItem['link_title'] != None:
                if string.find(suppItem['link_title'],"Open University")>-1 or string.find(suppItem['link_title'],"OpenLearn")>-1:
                    ouItems=suppItem
                    grabbed=1
            if grabbed==0 and suppItem['title']!=None:
                if string.find(suppItem['title'],"Open University")>-1 or string.find(suppItem['title'],"OpenLearn")>-1:
                    ouItems=suppItem
                    grabbed=1
            if grabbed==0 and 'link_uri' in suppItem:
                if suppItem['link_uri']!=None:
                    if string.find(suppItem['link_uri'],'open.edu')>-1:
                        ouItems=suppItem
                        grabbed=1
    seriesID=seriesData['programme']['pid']
    if len(ouItems)>0:
        print ouItems['link_title'], ouItems['title'],ouItems['published_image_uri'],ouItems['link_uri'],ouItems['content']
        data=ouItems
        data['ouTitle']=data['title']
        data['seriesID']=seriesID
        ouSeriesDetails[seriesID]=data
        scraperwiki.sqlite.save(unique_keys=['seriesID'], table_name='ouProgData', data=data)
    else:
        print 'no OU items for ',seriesData['programme']['title']
        ouItems={'link_title':'','ouTitle':'','published_image_uri':'','link_uri':'','content':''}
        data=ouItems
        data['seriesID']=seriesData['programme']['pid']
        scraperwiki.sqlite.save(unique_keys=['seriesID'], table_name='ouProgData', data=data)  
        ouSeriesDetails[seriesID]=data
    return ouItems

def checkForOUContent(seriesData):
    seriesID=seriesData['programme']['pid']
    if seriesID not in ouSeries:
        print 'new to me... looking for OU details'
        return checkForNewOUContent(seriesData)
    return ouSeriesDetails[seriesID]

def parseEpisodesData(seriesData,episodesData):
    print seriesData,episodesData
    ouItems=checkForOUContent(seriesData)
    print 'ou',ouItems
    for programme in episodesData['episodes']:
        episode=programme['programme']
        print episode
        print episode['title'],episode['short_synopsis'],episode['media']['availability'],episode['media']['format'],episode['pid'],seriesData['programme']['title'],seriesData['programme']['short_synopsis']
        scraperwiki.sqlite.save(unique_keys=['progID'], table_name='bbcOUcoPros', data={ 'progID':episode['pid'], 'seriesID':seriesData['programme']['pid'],'seriesTitle':seriesData['programme']['title'],'short_synopsis':episode['short_synopsis'],'expires':episode['media']['expires'],'availability':episode['media']['availability'],'format':episode['media']['format'], 'title':episode['title'],'image':'http://static.bbc.co.uk/programmeimages/272x153/episode/'+episode['pid']+'.jpg', 'ouLinkTitle':ouItems['link_title'],'ouTitle':ouItems['ouTitle'],'ouImage':ouItems['published_image_uri'],'ouURI':ouItems['link_uri'],'ouContent':ouItems['content']})

def getSeriesData(seriesID):
    episodesURL='http://www.bbc.co.uk/programmes/'+seriesID+'/episodes/player.json'
    try:
        episodesData=simplejson.load(urllib.urlopen(episodesURL))
    except:
        episodesData=''
    if debug==1:print episodesURL,episodesData
    if episodesData!='':
        seriesURL='http://www.bbc.co.uk/programmes/'+seriesID+'.json'
        seriesData=simplejson.load(urllib.urlopen(seriesURL))
        parseEpisodesData(seriesData,episodesData)

def getSeriesUpcoming(seriesID):
    upcomingURL='http://www.bbc.co.uk/programmes/'+seriesID+'/episodes/upcoming.json'
    print upcomingURL
    try:
        upcomingData=simplejson.load(urllib.urlopen(upcomingURL))
    except: return
    print 'got upcoming...'
    for item in upcomingData['broadcasts']:
        data={}
        data=ouSeriesDetails[seriesID]
        data['date']=item['schedule_date']
        data['startTime']=item['start']
        data['endTime']=item['end']
        data['duration']=item['duration']
        data['service']=item['service']['title']
        prog=item['programme']
        data['progID']=prog['pid']
        data['title']=prog['title']
        data['short_synopsis']=prog['short_synopsis']
        if prog['programme']['pid']!=data['seriesID']:
            print 'oops',prog['programme']['pid'],data['seriesID']
            exit(-1)
        else:
            data['seriesID']=prog['programme']['pid']
            data['seriesTitle']=prog['programme']['title']
            print data
            scraperwiki.sqlite.save( unique_keys=[],table_name='upcomingOUBBC', data=data)


'''{"programme":{"type":"episode","pid":"p00kjq6h","position":1,"title":"Spark","short_synopsis":"How pioneers unlocked electricity's mysteries and built strange instruments to create it.","media_type":"audio_video","duration":3600,"display_titles":{"title":"Shock and Awe: The Story of Electricity","subtitle":"Spark"},"first_broadcast_date":"2011-10-06T21:00:00+01:00","programme":{"type":"series","pid":"p00kjq6d","title":"Shock and Awe: The Story of Electricity","position":null,"expected_child_count":3,"first_broadcast_date":"2011-10-06T21:00:00+01:00","ownership":{"service":{"type":"tv","id":"bbc_four","key":"bbcfour","title":"BBC Four"}}},"is_available_mediaset_pc_sd":false,"is_legacy_media":false}}'''

def parseSeriesListing(seriesListing):
    for series in seriesListing:
        seriesID=series['u'].split('/')[-1]
        if seriesID !='':
            getSeriesData(seriesID)
            getSeriesUpcoming(seriesID)


def getSeriesList():
    seriesFeed='http://feeds.delicious.com/v2/json/psychemedia/oubbccopro?count=100'
    feed=simplejson.load(urllib.urlopen(seriesFeed))
    return feed

#try:
#    scraperwiki.sqlite.execute('drop table "bbcOUcoPros"')
#except:
#    pass

debug=0

if debug==0:
    dropper('upcomingOUBBC')
    #dropper('ouProgData')
    try:
        q = '* FROM "ouProgData"'
        ouDetails = scraperwiki.sqlite.select(q)
    except: ouDetails=[]
    ouSeriesDetails={}
    ouSeries=[]
    for series in ouDetails:
        ouSeries.append(series['seriesID'])
        ouSeriesDetails[series['seriesID']]=series

seriesListing=getSeriesList()
print seriesListing

if debug==0: parseSeriesListing(seriesListing)

#need a pass that deletes or archives programmes no longer available?