import scraperwiki,urllib,json,simplejson


# pipe2py test
# This minimal example shows how to grab a Yahoo pipe json definition, then compile and run the pipe in process
#(example lifted more or less from https://github.com/ggaughan/pipe2py/blob/master/compile.py )

# Thoughts:
##1) populate a scraperwiki table with pipe IDs and pipe definitions
##2) allow user to grab look up the pipe definition via a SELECT onto the table using ID, compile and run pipe and pop result into a table?


'''
>>>I posted a related issue on the pipe2py github site [ https://github.com/ggaughan/pipe2py/issues/16 ]:

I'm not sure about what the best way of thinking about pipes on scraperwiki is? My first thought is that a scraper db could be used to hold a pipe definition (or set of pipe definitions where there are pipes embedded in pipes) (which would require a one off 'configuration scrape'/pipe export phase to get hold of the data from Yahoo pipes) then the scraper could be scheduled to compile and run the pipe and drop the output from executing the pipe into a second dbtable?'''

'''I don't think this scraper handles nested pipes?'''

from pipe2py import compile, Context


def getPipesJSON(id,name=''):
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

def examplePipeOutput(pipeid):
    pjson=getPipesJSON(pipeid)
    print pjson

    p = compile.parse_and_build_pipe(Context(), pjson)
    for i in p:
        print 'as',i


# Simple exporter for published Yahoo Pipes

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

pipeid='53813bf4f427986802da941cc4338b65'
#examplePipeOutput(pipeid)

#getPipesJSON('975789b47f17690a21e89b10a702bcbd','Hashtag tokeniser')import scraperwiki,urllib,json,simplejson


# pipe2py test
# This minimal example shows how to grab a Yahoo pipe json definition, then compile and run the pipe in process
#(example lifted more or less from https://github.com/ggaughan/pipe2py/blob/master/compile.py )

# Thoughts:
##1) populate a scraperwiki table with pipe IDs and pipe definitions
##2) allow user to grab look up the pipe definition via a SELECT onto the table using ID, compile and run pipe and pop result into a table?


'''
>>>I posted a related issue on the pipe2py github site [ https://github.com/ggaughan/pipe2py/issues/16 ]:

I'm not sure about what the best way of thinking about pipes on scraperwiki is? My first thought is that a scraper db could be used to hold a pipe definition (or set of pipe definitions where there are pipes embedded in pipes) (which would require a one off 'configuration scrape'/pipe export phase to get hold of the data from Yahoo pipes) then the scraper could be scheduled to compile and run the pipe and drop the output from executing the pipe into a second dbtable?'''

'''I don't think this scraper handles nested pipes?'''

from pipe2py import compile, Context


def getPipesJSON(id,name=''):
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

def examplePipeOutput(pipeid):
    pjson=getPipesJSON(pipeid)
    print pjson

    p = compile.parse_and_build_pipe(Context(), pjson)
    for i in p:
        print 'as',i


# Simple exporter for published Yahoo Pipes

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

pipeid='53813bf4f427986802da941cc4338b65'
#examplePipeOutput(pipeid)

#getPipesJSON('975789b47f17690a21e89b10a702bcbd','Hashtag tokeniser')