#Example of how to grab a pipe definition from Yahoo pipes, compile and execute it, and preview its (locally obtained) output

import scraperwiki,json,urllib

from pipe2py import compile, Context

pipeid='4047c89fe888a2f21ca44fc1d62da245'

def getPipesJSON(id):
    url = ("""http://query.yahooapis.com/v1/public/yql"""
               """?q=select%20PIPE.working%20from%20json%20"""
               """where%20url%3D%22http%3A%2F%2Fpipes.yahoo.com%2Fpipes%2Fpipe.info%3F_out%3Djson%26_id%3D"""
               + id + 
               """%22&format=json""")
    pjson = urllib.urlopen(url).readlines()
    pjson = "".join(pjson)
    pipe_def = json.loads(pjson)
    if not pipe_def['query']['results']:
        print "Pipe not found"
        sys.exit(1)
    pjson = pipe_def['query']['results']['json']['PIPE']['working']
    return pjson


pjson=getPipesJSON(pipeid)

p = compile.parse_and_build_pipe(Context(), pjson)
for i in p:
    #print 'as',i
    print '<a href="'+i['link']+'">'+i['title']+'</a><br/>',i['summary_detail']['value']+'<br/><br/>'
