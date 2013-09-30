import scraperwiki,urllib,json,simplejson
 
def getPipesJSON(id,name):
    url = ("""http://query.yahooapis.com/v1/public/yql"""
               """?q=select%20PIPE.working%20from%20json%20"""
               """where%20url%3D%22http%3A%2F%2Fpipes.yahoo.com%2Fpipes%2Fpipe.info%3F_out%3Djson%26_id%3D"""
               + id +
               """%22&format=json""")
    pjson = urllib.urlopen(url).readlines()
    pjson = "".join(pjson)
    pipe_def = json.loads(pjson)
    scraperwiki.sqlite.save(unique_keys=['id'], table_name='pipes', data={'id':id,'pjson':pjson,'title':name})
    if not pipe_def['query']['results']:
        print "Pipe not found"
        sys.exit(1)
    pjson = pipe_def['query']['results']['json']['PIPE']['working']
    return pjson
 
#-------
def getPipesPage(uid,pageNum):
    print 'getting',uid,pageNum
    pipesFeed='http://pipes.yahoo.com/pipes/person.info?_out=json&display=pipes&guid='+uid+'&page='+str(pageNum)
    feed=simplejson.load(urllib.urlopen(pipesFeed))
    return feed
 
def userPipesExport(uid):
    page=1
    scrapeit=True

    while (scrapeit):
        feeds= getPipesPage(uid,page)
        print feeds
        if feeds['value']['hits']==0:
            scrapeit=False
        else:
            for pipe in feeds['value']['items']:
                id=pipe['id']
                tmp=getPipesJSON(id,pipe['title'])
            page=page+1

#Yahoo pipes user ID
uid='SZHKUPNX6A6I2BXPKK7JWAAZXU'
 
userPipesExport(uid)import scraperwiki,urllib,json,simplejson
 
def getPipesJSON(id,name):
    url = ("""http://query.yahooapis.com/v1/public/yql"""
               """?q=select%20PIPE.working%20from%20json%20"""
               """where%20url%3D%22http%3A%2F%2Fpipes.yahoo.com%2Fpipes%2Fpipe.info%3F_out%3Djson%26_id%3D"""
               + id +
               """%22&format=json""")
    pjson = urllib.urlopen(url).readlines()
    pjson = "".join(pjson)
    pipe_def = json.loads(pjson)
    scraperwiki.sqlite.save(unique_keys=['id'], table_name='pipes', data={'id':id,'pjson':pjson,'title':name})
    if not pipe_def['query']['results']:
        print "Pipe not found"
        sys.exit(1)
    pjson = pipe_def['query']['results']['json']['PIPE']['working']
    return pjson
 
#-------
def getPipesPage(uid,pageNum):
    print 'getting',uid,pageNum
    pipesFeed='http://pipes.yahoo.com/pipes/person.info?_out=json&display=pipes&guid='+uid+'&page='+str(pageNum)
    feed=simplejson.load(urllib.urlopen(pipesFeed))
    return feed
 
def userPipesExport(uid):
    page=1
    scrapeit=True

    while (scrapeit):
        feeds= getPipesPage(uid,page)
        print feeds
        if feeds['value']['hits']==0:
            scrapeit=False
        else:
            for pipe in feeds['value']['items']:
                id=pipe['id']
                tmp=getPipesJSON(id,pipe['title'])
            page=page+1

#Yahoo pipes user ID
uid='SZHKUPNX6A6I2BXPKK7JWAAZXU'
 
userPipesExport(uid)