import scraperwiki
import urllib
import networkx as nx

import networkx.readwrite.gexf as gf

from xml.etree.cElementTree import tostring

scraperwiki.sqlite.attach( 'tesco_sprawl_grapher')
q = '* FROM "companydetails"'
data = scraperwiki.sqlite.select(q)

DG=nx.DiGraph()

address=[]
companies=[]
for row in data:
    if row['address'] != None:
        if row['address'] not in address:
            address.append(row['address'])
            DG.add_node(address.index(row['address']),label=row['address'],name=row['address'])
        if row['ocid'] not in companies:
            companies.append(row['name'])
            DG.add_node(row['ocid'],label=row['name'],name=row['name'])   
        DG.add_edge(address.index(row['address']),row['ocid'])

scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")


writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
writer.add_graph(DG)

print tostring(writer.xml)


