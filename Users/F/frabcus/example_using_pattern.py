# Example of pattern: http://www.clips.ua.ac.be/pages/pattern

from pattern.web    import Bing, plaintext
from pattern.en     import Sentence, Chunk, parse
from pattern.search import Pattern
from pattern.graph  import Graph, Node, Edge, export
 
g = Graph()
for i in range(1):
    print "--------------", i
    for r in Bing().search('"more important than"', start=i+1, count=50):
        s = plaintext(r.description.lower())
        print s
        s = Sentence(parse(s))
        print s    
        p = Pattern.fromstring('NP (VP) more important than NP')
        for m in p.search(s):
            a = m.constituents(p[+0])[-1] # Left NP.
            b = m.constituents(p[-1])[+0] # Right NP.
            a = (isinstance(a, Chunk) and a.head or a).string
            b = (isinstance(b, Chunk) and b.head or b).string
            if a and b:
                if a not in g:
                    g.add_node(a, radius=5, stroke=(0,0,0,0.8))
                if b not in g:
                    g.add_node(b, radius=5, stroke=(0,0,0,0.8))
                g.add_edge(g[b], g[a], stroke=(0,0,0,0.6))

g = g.split()[0] # Largest subgraph.
 
for n in g.sorted()[:40]: # Sorted by Node.weight.
    n.fill = (0.0, 0.5, 1.0, 0.7 * n.weight)

export(g, 'test', directed=True, weighted=0.6, distance=6, force=0.05, repulsion=150)
import os
os.system('ls -lR test/')


