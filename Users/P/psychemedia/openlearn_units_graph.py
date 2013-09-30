import scraperwiki
import urllib
import networkx as nx

import networkx.readwrite.gexf as gf

from xml.etree.cElementTree import tostring

scraperwiki.sqlite.attach( 'openlearn-units' )
q = '* FROM "swdata"'
data = scraperwiki.sqlite.select(q)

G=nx.Graph()

topics=[]
for row in data:
    G.add_node(row['unitcode'],label=row['unitcode'],name=row['name'],parentCC=row['parentCourseCode'])
    topic=row['topic']
    if topic not in topics:
        topics.append(topic)
    tID=topics.index(topic)
    topicID='topic_'+str(tID)
    G.add_node(topicID,label=topic,name=topic)     
    G.add_edge(topicID,row['parentCourseCode'])
    G.add_edge(row['unitcode'],row['parentCourseCode'])

scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")


writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
writer.add_graph(G)

print tostring(writer.xml)


import scraperwiki
import urllib
import networkx as nx

import networkx.readwrite.gexf as gf

from xml.etree.cElementTree import tostring

scraperwiki.sqlite.attach( 'openlearn-units' )
q = '* FROM "swdata"'
data = scraperwiki.sqlite.select(q)

G=nx.Graph()

topics=[]
for row in data:
    G.add_node(row['unitcode'],label=row['unitcode'],name=row['name'],parentCC=row['parentCourseCode'])
    topic=row['topic']
    if topic not in topics:
        topics.append(topic)
    tID=topics.index(topic)
    topicID='topic_'+str(tID)
    G.add_node(topicID,label=topic,name=topic)     
    G.add_edge(topicID,row['parentCourseCode'])
    G.add_edge(row['unitcode'],row['parentCourseCode'])

scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")


writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
writer.add_graph(G)

print tostring(writer.xml)


