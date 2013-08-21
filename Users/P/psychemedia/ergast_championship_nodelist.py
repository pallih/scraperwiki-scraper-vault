import urllib,gviz_api,scraperwiki,json

import networkx as nx
from networkx.readwrite import json_graph

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

ejson=json.load(urllib.urlopen(url))
rdata=ejson['MRData']['RaceTable']['Races']

DG = nx.DiGraph()
#DG=nx.MultiGraph()
#DG.add_node(1,name=ascii(title))def ascii(s): return "".join(i for i in s if ord(i)<128)
def ascii(s): return "".join(i for i in s if ord(i)<128)
def gNodeAdd(DG,nodelist,name):
    node=len(nodelist)
    DG.add_node(node,name=ascii(name))
    #DG.add_node(node,name=name)
    #DG.add_node(node,name='')
    nodelist.append(name)
    return DG,nodelist

#DG.add_edge(root,node)
#DG,root=gNodeAdd(DG,root,node,name)
#Graph depicts flow of points from race to driver and from driver to team
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
nodelist=[]
rns={}
ddata.append(itemise(season,'',0))
cdata.append(itemise(season,'',0))
c2data.append(itemise(season,'',0))
for round in rdata:
    race=round['raceName']
    DG,nodelist=gNodeAdd(DG,nodelist,race)
    for driver in round['Results']:
        dname=" ".join([ driver['Driver']['givenName'], driver['Driver']['familyName'] ])
        points=int(driver['points'])
        constructor=driver['Constructor']['name']
        if constructor not in constructors:
            rns[constructor]=[]
            constructors.append(constructor)
            cdata.append(itemise(constructor,season,0))
            c2data.append(itemise(constructor,season,0))
        if points>0 and constructor not in nodelist: DG,nodelist=gNodeAdd(DG,nodelist,constructor)

        rn=race+' ['+constructor+']'
        if rn not in rns[constructor]:
            rns[constructor].append(rn)
            c2data.append(itemise(rn,constructor,0))
        if dname not in drivers:
            drivers.append(dname)
            ddata.append(itemise(dname,season,0))
            #make a bad assumption for now - that driver will stick with a team throughout the season
            cdata.append(itemise(dname,constructor,0))
        if points>0 and dname not in nodelist: DG,nodelist=gNodeAdd(DG,nodelist,dname)
        c2data.append(itemise(dname+' ['+str(points)+' points, ('+race+')',rn,points))
        ddata.append(itemise(race+' ['+str(points)+' points, ('+driver['number']+')]',dname,points))
        cdata.append(itemise(race+' ['+str(points)+' points, ('+driver['Driver']['driverId']+')]',dname,points))
        if points>0:DG.add_edge(nodelist.index(race),nodelist.index(dname),value=points)
        if points>0:
            if DG.has_edge(nodelist.index(dname),nodelist.index(constructor)):
                DG[nodelist.index(dname)][nodelist.index(constructor)]['value'] += points
            else: DG.add_edge(nodelist.index(dname),nodelist.index(constructor),value=points)


'''
if typ=='condriver':
    cdata_table = gviz_api.DataTable(description)
    cdata_table.LoadData(cdata)
    jsond = cdata_table.ToJSon(columns_order=("item", "parent","points"))
elif typ=='conrace':
    c2data_table = gviz_api.DataTable(description)
    c2data_table.LoadData(c2data)
    jsond = c2data_table.ToJSon(columns_order=("item", "parent","points"))
else:
    ddata_table = gviz_api.DataTable(description)
    ddata_table.LoadData(ddata)
    jsond = ddata_table.ToJSon(columns_order=("item", "parent","points"))
'''
scraperwiki.utils.httpresponseheader("Content-Type", "application/json")

data = json_graph.node_link_data(DG)
jsond=json.dumps(data)
if callback!='':
    print callback+'(',jsond,')'
else: print jsond


