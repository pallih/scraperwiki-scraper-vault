# http://networkx.lanl.gov/

import networkx as nx

G=nx.Graph()
G.add_node("spam")
G.add_edge(1,2)
print(G.nodes())
#[1, 2, 'spam']
print(G.edges())
#[(1, 2)]
