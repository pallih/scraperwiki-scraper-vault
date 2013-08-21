import scraperwiki
import json
import networkx as nx
import urllib
from networkx.readwrite import json_graph

#--via @mhawksey - to allow the use of params in querystring
# query string crib https://views.scraperwiki.com/run/python_querystring_cheat_sheet/?
import cgi, os
qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'key' in get:
        key=get['key']
        table='directors_'+key
else:
    key=''
    table='directors'
#---

scraperwiki.sqlite.attach( 'tesco_sprawl_grapher')
q = '* FROM "'+table+'"'
data = scraperwiki.sqlite.select(q)
DG = nx.DiGraph()

directors = []
companies = []
# Each row contains a director name and a company. Add both as a node if they don't
# already exist as a node: always add an edge between the two. 
for row in data:
    if row['fdirector'] not in directors:
        directors.append(row['fdirector'])
        DG.add_node(directors.index(row['fdirector']),label=row['fdirector'],name=row['fdirector'])
    if row['ocname'] not in companies:
        companies.append(row['ocname'])
        DG.add_node(row['ocid'],label=row['ocname'],name=row['ocname'])   
    DG.add_edge(directors.index(row['fdirector']),row['ocid'])

# Make directors red and companies blue.

d = json_graph.node_link_data(DG) # node-link format to serialize
print d

# json.dump(d, open('force/force.json','w'))
