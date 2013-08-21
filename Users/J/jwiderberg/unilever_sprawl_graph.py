import scraperwiki
import urllib
import networkx as nx

import networkx.readwrite.gexf as gf

from xml.etree.cElementTree import tostring

key = 'unilever'
table='directors_'+key


scraperwiki.sqlite.attach( 'unilever_sprawl')
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


writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
writer.add_graph(DG)

print tostring(writer.xml)


