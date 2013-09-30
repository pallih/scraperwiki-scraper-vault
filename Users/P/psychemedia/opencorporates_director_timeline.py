import scraperwiki,json
from datetime import datetime
from datetime import date
from time import *

import cgi, os
qstring=os.getenv("QUERY_STRING")

key='MARTIN_STUART_SORRELL'
headline=key.replace('_',' ')
text=''

output='similejson'  #also timelinerjs similejson

if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'key' in get: key=get['key'].lower()
    if 'output' in get: output=get['output']
    if 'headline' in get: headline=get['headline']
    else: headline=key.replace('_',' ')
    if 'text' in get: text=get['text']
    else: text=''
    if 'scraper' in get: scraperpath=get['scraper']
    else: scraperpath='opencorporates_director_history'

table='dir_'+key.lower()

scraperwiki.sqlite.attach( scraperpath )
q = '* FROM `'+table+'`'
data = scraperwiki.sqlite.select(q)

'''
       "date": [
            {
                "startDate":"2012,1,26",
                "endDate":"2012,1,27",
                "headline":"Sh*t Politicians Say",
                "text":"<p>In true political fashion, his character rattles off common jargon heard from people running for office.</p>",
                "asset":
                {
                    "media":"http://youtu.be/u4XpeU9erbg",
                    "credit":"",
                    "caption":""
                }
            },
'''
def dateformatter(dt):
    dt= datetime.strptime(dt, '%Y-%m-%d')
    return ",".join( [ str(dt.strftime("%Y")), dt.strftime("%m"), dt.strftime("%d") ] )

today= date.today().strftime('%Y-%m-%d')
startDate = today

if output=='timelinerjs':
    scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
    
    
    jdata={"headline":headline, "type":"default", "text":text, "date":[] }
    dates=[]

    for d in data:
        dateRecord={ 'asset':{'media':'','credit':'','caption':''} }
        dateRecord['startDate']=dateformatter( d['start_date'] )
        if d['inactive']==0: dateRecord['endDate'] = dateformatter( d['end_date'] )
        else: dateRecord['endDate']= dateformatter( today )
        
        if startDate < today: startDate= today

        dateRecord['headline']=d['cname']
        dateRecord['text']=d['dirPos']
        
        jdata['date'].append(dateRecord.copy())

    jdata["startDate"]=dateformatter(startDate) 
    tdata={'timeline':jdata}
    print json.dumps(tdata)

elif output=='similejson':
    scraperwiki.utils.httpresponseheader("Content-Type", "text/plain")

    jdata=[]
    for d in data:
        dateRecord={}
        dateRecord['start']=dateformatter( d['start_date'] )
        if d['inactive']==0: dateRecord['end'] = dateformatter( d['end_date'] )
        else: dateRecord['end']= dateformatter( today )
        
        if startDate < today: startDate= today

        dateRecord['title']=d['cname']
        dateRecord['description']=d['dirPos']
        
        jdata.append(dateRecord.copy())
    print json.dumps(jdata)

elif output=='logfile':
    scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
    for d in data:
        dt=int(mktime(strptime(d['start_date'],"%Y-%m-%d")))
        #1301612404|687369|A|www.isinet.com/WoK/UA
        print '|'.join([ str(dt),d['dirPos'], 'A', d['cname'].replace(' ','_') ])
        if d['inactive']==0:
            dt=int(mktime(strptime(d['end_date'],"%Y-%m-%d")))
            print '|'.join([ str(dt) ,d['dirPos'], 'D', d['cname'].replace(' ','_') ])import scraperwiki,json
from datetime import datetime
from datetime import date
from time import *

import cgi, os
qstring=os.getenv("QUERY_STRING")

key='MARTIN_STUART_SORRELL'
headline=key.replace('_',' ')
text=''

output='similejson'  #also timelinerjs similejson

if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'key' in get: key=get['key'].lower()
    if 'output' in get: output=get['output']
    if 'headline' in get: headline=get['headline']
    else: headline=key.replace('_',' ')
    if 'text' in get: text=get['text']
    else: text=''
    if 'scraper' in get: scraperpath=get['scraper']
    else: scraperpath='opencorporates_director_history'

table='dir_'+key.lower()

scraperwiki.sqlite.attach( scraperpath )
q = '* FROM `'+table+'`'
data = scraperwiki.sqlite.select(q)

'''
       "date": [
            {
                "startDate":"2012,1,26",
                "endDate":"2012,1,27",
                "headline":"Sh*t Politicians Say",
                "text":"<p>In true political fashion, his character rattles off common jargon heard from people running for office.</p>",
                "asset":
                {
                    "media":"http://youtu.be/u4XpeU9erbg",
                    "credit":"",
                    "caption":""
                }
            },
'''
def dateformatter(dt):
    dt= datetime.strptime(dt, '%Y-%m-%d')
    return ",".join( [ str(dt.strftime("%Y")), dt.strftime("%m"), dt.strftime("%d") ] )

today= date.today().strftime('%Y-%m-%d')
startDate = today

if output=='timelinerjs':
    scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
    
    
    jdata={"headline":headline, "type":"default", "text":text, "date":[] }
    dates=[]

    for d in data:
        dateRecord={ 'asset':{'media':'','credit':'','caption':''} }
        dateRecord['startDate']=dateformatter( d['start_date'] )
        if d['inactive']==0: dateRecord['endDate'] = dateformatter( d['end_date'] )
        else: dateRecord['endDate']= dateformatter( today )
        
        if startDate < today: startDate= today

        dateRecord['headline']=d['cname']
        dateRecord['text']=d['dirPos']
        
        jdata['date'].append(dateRecord.copy())

    jdata["startDate"]=dateformatter(startDate) 
    tdata={'timeline':jdata}
    print json.dumps(tdata)

elif output=='similejson':
    scraperwiki.utils.httpresponseheader("Content-Type", "text/plain")

    jdata=[]
    for d in data:
        dateRecord={}
        dateRecord['start']=dateformatter( d['start_date'] )
        if d['inactive']==0: dateRecord['end'] = dateformatter( d['end_date'] )
        else: dateRecord['end']= dateformatter( today )
        
        if startDate < today: startDate= today

        dateRecord['title']=d['cname']
        dateRecord['description']=d['dirPos']
        
        jdata.append(dateRecord.copy())
    print json.dumps(jdata)

elif output=='logfile':
    scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
    for d in data:
        dt=int(mktime(strptime(d['start_date'],"%Y-%m-%d")))
        #1301612404|687369|A|www.isinet.com/WoK/UA
        print '|'.join([ str(dt),d['dirPos'], 'A', d['cname'].replace(' ','_') ])
        if d['inactive']==0:
            dt=int(mktime(strptime(d['end_date'],"%Y-%m-%d")))
            print '|'.join([ str(dt) ,d['dirPos'], 'D', d['cname'].replace(' ','_') ])