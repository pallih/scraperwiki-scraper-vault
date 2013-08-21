import scraperwiki
import networkx as nx
import networkx.readwrite.gexf as gf


#--via @mhawksey
# query string crib https://views.scraperwiki.com/run/python_querystring_cheat_sheet/?
import cgi, os
qstring=os.getenv("QUERY_STRING")

key='sodexo2_2'
output='gexf'  #also json
reduce=-1
modularity=-1
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'key' in get:
        key=get['key']
    if 'output' in get: output=get['output'].lower()
    if 'reduce' in get: reduce=get['reduce'] #companies or officers
    if 'modularity' in get: modularity=1
table='directors_'+key
#---


scraperwiki.sqlite.attach( 'opencorporates_trawler')
q = '* FROM `'+table+'`'
data = scraperwiki.sqlite.select(q)

if reduce==-1:DG=nx.DiGraph()
else:DG=nx.Graph()

directors=[]
companies=[]
for row in data:
    if row['name'] not in directors:
        directors.append(row['name'])
        DG.add_node(directors.index(row['name']),label=row['name'],name=row['name'])
    if row['cname'] not in companies:
        companies.append(row['cname'])
        DG.add_node(row['ocid'],label=row['cname'],name=row['cname'])   
    DG.add_edge(directors.index(row['name']),row['ocid'])


if reduce!=-1:
    from networkx.algorithms import bipartite
    officers,companies=bipartite.sets(DG)
    #print list(officers)
    #print list(companies)

    if reduce=="officers":
        #Collapse the bipartite graph to a graph of journalists connected via a common tag
        OG= bipartite.projected_graph(DG, officers)
    elif reduce=='companies':
        #Collapse the bipartite graph to a set of tags connected via a common journalist
        OG= bipartite.projected_graph(DG, companies)
    else: OG=DG
else: OG=DG

'''
modularity=1
if modularity!=-1:
    import community
    partition = community.best_partition(G)
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()) :
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
        #nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20, node_color = str(count / size))
'''

pos=nx.spring_layout(OG)
#The folloiwng needs a multiplier on x and y; layout is pretty ropey.
for n,(x,y) in pos.items():    
    #DG.node[n]['viz']={'position':{'x':100*x,'y':100*y}}
    OG.node[n]['position']={'x':100*x,'y':100*y}


if output=='json':
    scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
    from networkx.readwrite import json_graph
    import json
    print json.dumps(json_graph.node_link_data(OG))
else:
    from xml.etree.cElementTree import tostring
    scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
    writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
    writer.add_graph(OG)

    print tostring(writer.xml)


