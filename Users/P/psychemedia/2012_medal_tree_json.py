import scraperwiki
import networkx as nx

sourcescraper = 'nbc_olympic_medalscrape'
scraperwiki.sqlite.attach( sourcescraper )
q = '* FROM "medalStandings"'
data = scraperwiki.sqlite.select(q)

medals=["Gold","Silver","Bronze"]


DG=nx.DiGraph()
nc=1

def countryEventMedal(data,DG):
    alist=[]
    rlist=[]
    root=1
    DG.add_node(root,name="Country Event Medal Table")
    for row in data:
        ac=row['cc']
        bc=row['Event']
        for m in medals:
            if row[m]>0:
                bcc=bc+ac
                node=bc+" ("+ac+")"
                if ac not in rlist:
                    rlist.append(ac)
                    nc=rlist.index(ac)+10
                    DG.add_node(nc,name=ac)
                    DG.add_edge(root,nc)
                if bcc not in alist:
                    alist.append(bcc)
                    nc=4*alist.index(bcc)+10000
                    DG.add_node(nc,name=bc)
                    DG.add_edge(rlist.index(ac)+10,nc)
                nce=4*alist.index(bcc)+10000
                ncm=4*alist.index(bcc)+10000+1+medals.index(m)
                DG.add_node(ncm,name=m,value=row[m])
                DG.add_edge(nce,ncm)
    return DG


from networkx.readwrite import json_graph
import json

scraperwiki.utils.httpresponseheader("Content-Type", "text/json")

DG=countryEventMedal(data,DG)

jtdata = json_graph.tree_data(DG,root=1)
print json.dumps(jtdata)
import scraperwiki
import networkx as nx

sourcescraper = 'nbc_olympic_medalscrape'
scraperwiki.sqlite.attach( sourcescraper )
q = '* FROM "medalStandings"'
data = scraperwiki.sqlite.select(q)

medals=["Gold","Silver","Bronze"]


DG=nx.DiGraph()
nc=1

def countryEventMedal(data,DG):
    alist=[]
    rlist=[]
    root=1
    DG.add_node(root,name="Country Event Medal Table")
    for row in data:
        ac=row['cc']
        bc=row['Event']
        for m in medals:
            if row[m]>0:
                bcc=bc+ac
                node=bc+" ("+ac+")"
                if ac not in rlist:
                    rlist.append(ac)
                    nc=rlist.index(ac)+10
                    DG.add_node(nc,name=ac)
                    DG.add_edge(root,nc)
                if bcc not in alist:
                    alist.append(bcc)
                    nc=4*alist.index(bcc)+10000
                    DG.add_node(nc,name=bc)
                    DG.add_edge(rlist.index(ac)+10,nc)
                nce=4*alist.index(bcc)+10000
                ncm=4*alist.index(bcc)+10000+1+medals.index(m)
                DG.add_node(ncm,name=m,value=row[m])
                DG.add_edge(nce,ncm)
    return DG


from networkx.readwrite import json_graph
import json

scraperwiki.utils.httpresponseheader("Content-Type", "text/json")

DG=countryEventMedal(data,DG)

jtdata = json_graph.tree_data(DG,root=1)
print json.dumps(jtdata)
