import scraperwiki
import networkx

# Blank Python
sourcescraper = 'itunes_collaborations'

scraperwiki.sqlite.attach(sourcescraper)

relevant_artists = set([x['collaborator'] for x in scraperwiki.sqlite.select("collaborator FROM 'swdata' where artist='David Byrne'")])

G = networkx.Graph()

for artist in relevant_artists:
    G.add_node(artist, name=artist, label=artist)


for artist in relevant_artists:
    collaborators = [x['collaborator'] for x in scraperwiki.sqlite.select("collaborator FROM 'swdata' where artist=?", [artist])]
    for collaborator in collaborators:
        
        if collaborator not in relevant_artists: 
            continue
        G.add_edge(artist, collaborator)


# Code (very closely) adapted from Tony Hirst @ http://blog.ouseful.info/2012/04/03/visualising-networks-in-gephi-via-a-scraperwiki-exported-gexf-file/?utm_source=dlvr.it&utm_medium=twitter -- CC Attribution

import networkx.readwrite.gexf as gexf

writer=gexf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
writer.add_graph(G)

scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")

from xml.etree.cElementTree import tostring
print tostring(writer.xml)           

    