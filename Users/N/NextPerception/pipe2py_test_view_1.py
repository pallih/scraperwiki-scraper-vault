import scraperwiki,json

from pipe2py import compile, Context

import cgi, os
qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'pipeid' in get: pipeid=get['pipeid']
    else: pipeid='2de0e4517ed76082dcddf66f7b218057'
else:
    pipeid='2de0e4517ed76082dcddf66f7b218057'


def getpjsonFromDB(id):
    scraperwiki.sqlite.attach( 'pipe2py_test' )
    q = '* FROM "pipes" WHERE "id"="'+id+'"'
    data = scraperwiki.sqlite.select(q)
    #print data
    pipe_def = json.loads(data[0]['pjson'])
    if not pipe_def['query']['results']:
        print "Pipe not found"
        sys.exit(1)
    pjson = pipe_def['query']['results']['json']['PIPE']['working']
    return pjson

pjson=getpjsonFromDB(pipeid)

p = compile.parse_and_build_pipe(Context(), pjson)
for i in p:
    #print 'as',i
    print '<a href="'+i['link']+'">'+i['title']+'</a><br/>',i['summary_detail']['value']+'<br/><br/>'
