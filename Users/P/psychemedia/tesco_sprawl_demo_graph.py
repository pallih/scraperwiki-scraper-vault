import scraperwiki
import urllib
import networkx as nx

import networkx.readwrite.gexf as gf

from xml.etree.cElementTree import tostring

####TO DO
##Need to do a demo view showing how to use the gexf file with http://sigmajs.org/examples.html
#it looks like it should be (almost as) easy as)
#// (requires "sigma.parseGexf.js" to be included)
#sigInst.parseGexf('/data/arctic.gexf');
#// (requires "sigma.forceatlas2.js" to be included)
#sigInst.startForceAtlas2();
#// Draw the graph :
####sigInst.draw();


#--via @mhawksey
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

DG=nx.DiGraph()

directors=[]
companies=[]
for row in data:
    if row['fdirector'] not in directors:
        directors.append(row['fdirector'])
        DG.add_node(directors.index(row['fdirector']),label=row['fdirector'],name=row['fdirector'])
    if row['ocname'] not in companies:
        companies.append(row['ocname'])
        DG.add_node(row['ocid'],label=row['ocname'],name=row['ocname'])   
    DG.add_edge(directors.index(row['fdirector']),row['ocid'])

scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")

#pos=nx.spring_layout(DG)
#pos=nx.spectral_layout(DG)
pos=nx.spring_layout(DG)
#The folloiwng needs a multiplier on x and y; layout is pretty ropey.
for n,(x,y) in pos.items():    
    DG.node[n]['viz']={'position':{'x':100*x,'y':100*y}}

writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
writer.add_graph(DG)

print tostring(writer.xml)


