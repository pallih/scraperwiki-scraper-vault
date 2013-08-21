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

def getEpisodeMetadata(episode):
    episodeMetadataURL='http://www.bbc.co.uk/programmes/'+episode+'.json'
    try:
        episodeMetaData=simplejson.load(urllib.urlopen(episodeMetadataURL))
    except:
        episodeMetaData={programme:{}}
    #print episodeMetaData
    return episodeMetaData

def addDBrecord(record):
    #scraperwiki.sqlite.save(unique_keys=['progID'], table_name=dataTable, data={ 'progID':episode['pid'], 'seriesID':seriesData['programme']['pid'],'seriesTitle':seriesData['programme']['title'],'short_synopsis':episode['short_synopsis'],'expires':episode['media']['expires'],'availability':episode['media']['availability'],'format':episode['media']['format'], 'title':episode['title'],'image':'http://static.bbc.co.uk/programmeimages/272x153/episode/'+episode['pid']+'.jpg', 'ouLinkTitle':ouItems[0]['link_title'],'ouTitle':ouItems[0]['title'],'ouImage':ouItems[0]['published_image_uri'],'ouURI':ouItems[0]['link_uri'],'ouContent':ouItems[0]['content']})
    
    scraperwiki.sqlite.save(unique_keys=['progID'], table_name=dataTable, data= record )


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
        episodemetadata=getEpisodeMetadata(episode['pid'])
        record={}
        record['progID']=episode['pid']
        record['seriesID']=seriesData['programme']['pid']
        record['seriesTitle']=seriesData['programme']['title']
        record['short_synopsis']=episode['short_synopsis']
        if 'medium_synopsis' in episodemetadata['programme']:
            record['medium_synopsis']=episodemetadata['programme']['medium_synopsis']
        else: record['medium_synopsis']=''
        record['expires']=episode['media']['expires']
        record['availability']=episode['media']['availability']
        record['format']=episode['media']['format']
        record['title']=episode['title']
        record['image']='http://static.bbc.co.uk/programmeimages/272x153/episode/'+episode['pid']+'.jpg'
        record['ouLinkTitle']=ouItems[0]['link_title']
        record['ouTitle']=ouItems[0]['title']
        record['ouImage']=ouItems[0]['published_image_uri']
        record['ouURI']=ouItems[0]['link_uri']
        record['ouContent']=ouItems[0]['content']
        if 'long_synopsis' in episodemetadata['programme']:
            record['long_synopsis']=episodemetadata['programme']['long_synopsis']
        else:
            record['long_synopsis']=''
        '''
        if 'long_synopsis' in episodemetadata['programme']:
            record['long_synopsis']=string.replace(episodemetadata['programme']['long_synopsis'],'The view from the top of business. Presented by Evan Davis, The Bottom Line cuts through confusion, statistics and spin to present a clearer view of the business world, through discussion with people running leading and emerging companies.','')
            record['long_synopsis']=record['long_synopsis'].lstrip()
            record['long_synopsis']=string.replace(record['long_synopsis'],'The programme is broadcast first on BBC Radio 4 and later on BBC World Service Radio, BBC World News TV and BBC News Channel TV.','')
            record['long_synopsis']=record['long_synopsis'].lstrip()
        else: record['long_synopsis']=''
        done=False

        if 'supporting_content_items' in episodemetadata['programme']:
            if episodemetadata['programme']['supporting_content_items']!='':
                print 'metadata',episodemetadata['programme']['supporting_content_items']
                i=0
                for suppitem in episodemetadata['programme']['supporting_content_items']:
                    if suppitem['link_title']!='' and suppitem['content']!='':
                        record['person']=suppitem['title']
                        record['company']=suppitem['link_title']
                        record['companyLink']=suppitem['link_uri']
                        record['role']=suppitem['content']
                        record['photo']=suppitem['published_image_uri']
                        record['key']=str(record['progID'])+str(i)
                        i=i+1
                        ocrecURL='http://opencorporates.com/reconcile?query='+urllib.quote_plus("".join(i for i in record['company'] if ord(i)<128))
                        try:
                            recData=simplejson.load(urllib.urlopen(ocrecURL))
                        except:
                            recData={'result':[]}
                        print ocrecURL,[recData]
                        if len(recData['result'])>0:
                            if recData['result'][0]['score']>=0.7:
                                record['ocData']=recData['result'][0]
                                record['ocID']=recData['result'][0]['uri']
                                record['ocName']=recData['result'][0]['name']
                            else:
                                record['ocData']=''
                                record['ocID']=''
                                record['ocName']=''
                        else:
                            record['ocData']=''
                            record['ocID']=''
                            record['ocName']=''
                        print record
                        addDBrecord(record)
                        done=True
        if done is False:
            print record
            #addDBrecord(record)
        '''
        addDBrecord(record)

#{'link_title': '', 'emp_playlist_uri': None, 'title': 'EVAN DAVIS', 'published_image_uri': 'http://www.bbc.co.uk/programmes/i/b9/7c/3426dbf695cb63c4522a483664c93ffbe6dc.jpg', 'emp_type': 'video', 'link_uri': '', 'content': '', 'layout_arrangement': 'image', 'position': 0}, {'link_title': 'Aberdeen Asset Management', 'emp_playlist_uri': None, 'title': 'MARTIN GILBERT', 'published_image_uri': 'http://www.bbc.co.uk/programmes/i/76/0c/782c71736dfd900c1e14e781893fd5fd3f3e.jpg', 'emp_type': 'video', 'link_uri': 'http://www.aberdeen-asset.com/aam.nsf/aboutus/home', 'content': 'Martin Gilbert is the chief executive of fund manager Aberdeen Asset Management.', 'layout_arrangement': 'image', 'position': 0}, {'link_title': 'PACE', 'emp_playlist_uri': None, 'title': 'ALLAN LEIGHTON', 'published_image_uri': 'http://www.bbc.co.uk/programmes/i/b6/93/3a2db74d0c974981b155feb4675bfb612a17.jpg', 'emp_type': 'video', 'link_uri': 'http://www.pace.com/global/about-pace/', 'content': 'Allan Leighton is the chairman of set top box maker PACE.', 'layout_arrangement': 'image', 'position': 0}

def getSeriesData(seriesID,typ='player'):
    episodesURL='http://www.bbc.co.uk/programmes/'+seriesID+'/episodes/'+typ+'.json'
    try:
        episodesData=simplejson.load(urllib.urlopen(episodesURL))
    except:
        episodesData=''

    if episodesData!='':
        seriesURL='http://www.bbc.co.uk/programmes/'+seriesID+'.json'
        seriesData=simplejson.load(urllib.urlopen(seriesURL))
        parseEpisodesData(seriesData,episodesData)

def parseSeriesListing(seriesListing):
    for series in seriesListing:
        seriesID=series['u'].split('/')[-1]
        if seriesID !='':
            getSeriesData(seriesID)


def getSeriesList():
    seriesFeed='http://feeds.delicious.com/v2/json/psychemedia/oubbccopro?count=100'
    feed=simplejson.load(urllib.urlopen(seriesFeed))
    return feed

#bottomLineSeriesID='b006sz6t'
#dataTable="bottomLine"

seriesIDs=['b006tht9','p002w6r2','b006m9ry']
dataTable="clickz"

try:
    drop='drop table "'+dataTable+'"'
    scraperwiki.sqlite.execute(drop)
except:
    pass

for id in seriesIDs:
    getSeriesData(id)