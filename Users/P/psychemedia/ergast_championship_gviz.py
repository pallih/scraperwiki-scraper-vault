import urllib,simplejson,gviz_api,scraperwiki

import cgi, os
qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'year' in get: year=get['year']
    else: year='2012'
    if 'callback' in get: callback=get['callback']
    else: callback=''
    if 'typ' in get: typ=get['typ']
    else: typ='driver'
else:
    year='2012'
    callback=''
    typ=''

url='http://ergast.com/api/f1/'+str(year)+'/results.json?limit=1000'

ejson=simplejson.load(urllib.urlopen(url))
rdata=ejson['MRData']['RaceTable']['Races']


description={"item":('string','item'),"parent":('string','parent'),"points":('number','points')}

def itemise(item,parent,points):
    item={'item':item,'parent':parent,'points':int(points)}
    return item


ddata=[]
cdata=[]
c2data=[]
constructors=[]

season=rdata[0]['season']
drivers=[]
rns={}
ddata.append(itemise(season,'',0))
cdata.append(itemise(season,'',0))
c2data.append(itemise(season,'',0))
for round in rdata:
    race=round['raceName']
    for driver in round['Results']:
        dname=" ".join([ driver['Driver']['givenName'], driver['Driver']['familyName'] ])
        constructor=driver['Constructor']['name']
        if constructor not in constructors:
            rns[constructor]=[]
            constructors.append(constructor)
            cdata.append(itemise(constructor,season,0))
            c2data.append(itemise(constructor,season,0))
        points=int(driver['points'])
        rn=race+' ['+constructor+']'
        if rn not in rns[constructor]:
            rns[constructor].append(rn)
            c2data.append(itemise(rn,constructor,0))
        if dname not in drivers:
            drivers.append(dname)
            ddata.append(itemise(dname,season,0))
            #make a bad assumption for now - that driver will stick with a team throughout the season
            cdata.append(itemise(dname,constructor,0))
        c2data.append(itemise(dname+' ['+str(points)+' points, ('+race+')',rn,points))
        ddata.append(itemise(race+' ['+str(points)+' points, ('+driver['number']+')]',dname,points))
        cdata.append(itemise(race+' ['+str(points)+' points, ('+driver['Driver']['driverId']+')]',dname,points))
        




if typ=='condriver':
    cdata_table = gviz_api.DataTable(description)
    cdata_table.LoadData(cdata)
    json = cdata_table.ToJSon(columns_order=("item", "parent","points"))
elif typ=='conrace':
    c2data_table = gviz_api.DataTable(description)
    c2data_table.LoadData(c2data)
    json = c2data_table.ToJSon(columns_order=("item", "parent","points"))
else:
    ddata_table = gviz_api.DataTable(description)
    ddata_table.LoadData(ddata)
    json = ddata_table.ToJSon(columns_order=("item", "parent","points"))

scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
if callback!='':
    print callback+'(',json,')'
else: print jsonimport urllib,simplejson,gviz_api,scraperwiki

import cgi, os
qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'year' in get: year=get['year']
    else: year='2012'
    if 'callback' in get: callback=get['callback']
    else: callback=''
    if 'typ' in get: typ=get['typ']
    else: typ='driver'
else:
    year='2012'
    callback=''
    typ=''

url='http://ergast.com/api/f1/'+str(year)+'/results.json?limit=1000'

ejson=simplejson.load(urllib.urlopen(url))
rdata=ejson['MRData']['RaceTable']['Races']


description={"item":('string','item'),"parent":('string','parent'),"points":('number','points')}

def itemise(item,parent,points):
    item={'item':item,'parent':parent,'points':int(points)}
    return item


ddata=[]
cdata=[]
c2data=[]
constructors=[]

season=rdata[0]['season']
drivers=[]
rns={}
ddata.append(itemise(season,'',0))
cdata.append(itemise(season,'',0))
c2data.append(itemise(season,'',0))
for round in rdata:
    race=round['raceName']
    for driver in round['Results']:
        dname=" ".join([ driver['Driver']['givenName'], driver['Driver']['familyName'] ])
        constructor=driver['Constructor']['name']
        if constructor not in constructors:
            rns[constructor]=[]
            constructors.append(constructor)
            cdata.append(itemise(constructor,season,0))
            c2data.append(itemise(constructor,season,0))
        points=int(driver['points'])
        rn=race+' ['+constructor+']'
        if rn not in rns[constructor]:
            rns[constructor].append(rn)
            c2data.append(itemise(rn,constructor,0))
        if dname not in drivers:
            drivers.append(dname)
            ddata.append(itemise(dname,season,0))
            #make a bad assumption for now - that driver will stick with a team throughout the season
            cdata.append(itemise(dname,constructor,0))
        c2data.append(itemise(dname+' ['+str(points)+' points, ('+race+')',rn,points))
        ddata.append(itemise(race+' ['+str(points)+' points, ('+driver['number']+')]',dname,points))
        cdata.append(itemise(race+' ['+str(points)+' points, ('+driver['Driver']['driverId']+')]',dname,points))
        




if typ=='condriver':
    cdata_table = gviz_api.DataTable(description)
    cdata_table.LoadData(cdata)
    json = cdata_table.ToJSon(columns_order=("item", "parent","points"))
elif typ=='conrace':
    c2data_table = gviz_api.DataTable(description)
    c2data_table.LoadData(c2data)
    json = c2data_table.ToJSon(columns_order=("item", "parent","points"))
else:
    ddata_table = gviz_api.DataTable(description)
    ddata_table.LoadData(ddata)
    json = ddata_table.ToJSon(columns_order=("item", "parent","points"))

scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
if callback!='':
    print callback+'(',json,')'
else: print json