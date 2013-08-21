import scraperwiki
import urllib
''' 
Skeleton code for NetworkX manipulations 
by Lynn Cherny (lynn@ghostweather.com) for 
Boston Predictive Analytics Meetup
Feb 21, 2012
Talk slides at
http://www.ghostweather.com/essays/talks/networkx/NetworkX_LCherny.ppt

A bunch of code examples to do things you might want to do with NetworkX, 
includes reading in edgelists, calculations on networks, adding attributes to nodes, reducing network size in principled way, saving to json...

Does not include any testing for error conditions, use at own risk!
Run on Python 2.7 and NetworkX 1.6
'''

import networkx as nx    # using 1.6, from http://networkx.lanl.gov/ 
#from networkx.readwrite import json_graph
from operator import itemgetter
import json 
import sys
import community   # get this lib from http://perso.crans.org/aynaud/communities/
# import matplotlib.pyplot as plt  -- only needed for a single graph below in draw_partition
import os
import cgi

# query string crib https://views.scraperwiki.com/run/python_querystring_cheat_sheet/?
#get = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
#key=get['key']
#gid=get['gid']
key='0AqGkLMU9sHmLdDd6NTNweFdKM2lnVW9LcVo4ak1CS3c'
gid='13'
stub='https://docs.google.com/spreadsheet/pub?key='+key+'&single=true&output=txt&gid='+gid


def read_in_edges(filename, info=True):
    ''' 
    Read a directed graph by default.  Change from DiGraph to Graph below if you want undirected. 
    Edgelist looks like this:
    node1 node2
    node3 node1
    node1 node3
     ...
     '''
     
    g_orig = nx.read_edgelist(filename, create_using=nx.DiGraph())
    if info:
        print "Read in edgelist file ", filename
        print nx.info(g_orig)
    return g_orig
    
def save_to_jsonfile(filename, graph):
    ''' 
    Save graph object to filename 
    '''
    g = graph
    g_json = json_graph.node_link_data(g) # node-link format to serialize
    json.dump(g_json, open(filename,'w'))

def read_json_file(filename, info=True):
    '''
    Use if you already have a json rep of a graph and want to update/modify it
    '''
    graph = json_graph.load(open(filename))
    if info:
        print "Read in file ", filename
        print nx.info(graph)
    return graph
    
def report_node_data(graph, node=""):
    '''
    Will tell you what attributes exist on nodes in the graph.
    Useful for checking your updates.
    '''
    
    g = graph
    if len(node) == 0:
        print "Found these sample attributes on the nodes:"
        print g.nodes(data=True)[0]
    else:
        print "Values for node " + node
        print [d for n,d in g.nodes_iter(data=True) if n==node]

def calculate_degree(graph):
    '''
    Calculate the degree of a node and save the value as an attribute on the node. Returns the graph and the dict of degrees.
    '''
    g = graph
    deg = nx.degree(g)
    nx.set_node_attributes(g,'degree',deg)
    return g, deg

def calculate_indegree(graph):
    '''Will only work on DiGraph (directed graph)
    Saves the indegree as attribute on the node, and returns graph, dict of indegree
    '''
    g = graph
    indeg = g.in_degree()
    nx.set_node_attributes(g, 'indegree', indeg)
    return g, indeg
    
def calculate_outdegree(graph):
    '''Will only work on DiGraph (directed graph)
    Saves the outdegree as attribute on the node, and returns graph, dict of outdegree
    '''
    g = graph
    outdeg = g.out_degree()
    nx.set_node_attributes(g, 'outdegree', outdeg)
    return g, outdeg

def calculate_betweenness(graph):
    ''' Calculate betweenness centrality of a node, sets value on node as attribute; returns graph, and dict of the betweenness centrality values
    '''
    g = graph
    bc=nx.betweenness_centrality(g)
    nx.set_node_attributes(g,'betweenness',bc)
    return g, bc
    
def calculate_eigenvector_centrality(graph):  
    ''' Calculate eigenvector centrality of a node, sets value on node as attribute; returns graph, and dict of the eigenvector centrality values.
    Also has commented out code to sort by ec value
    '''
    g = graph
    ec = nx.eigenvector_centrality(g)
    nx.set_node_attributes(g,'eigen_cent',ec)
    #ec_sorted = sorted(ec.items(), key=itemgetter(1), reverse=True)
    return g, ec

def calculate_degree_centrality(graph):
    ''' Calculate degree centrality of a node, sets value on node as attribute; returns graph, and dict of the degree centrality values.
    Also has code to print the top 10 nodes by degree centrality to console
    '''
    g = graph
    dc = nx.degree_centrality(g)
    nx.set_node_attributes(g,'degree_cent',dc)
    degcent_sorted = sorted(dc.items(), key=itemgetter(1), reverse=True)
    for key,value in degcent_sorted[0:10]:
        print "Highest degree Centrality:", key, value
    return graph, dc

def find_cliques(graph):
    ''' Calculate cliques and return as sorted list.  Print sizes of cliques found.
    '''
    g = graph
    cl = nx.find_cliques(g)
    cl = sorted(list( cl ), key=len, reverse=True)
    print "Number of cliques:", len(cl)
    cl_sizes = [len(c) for c in cl]
    print "Size of cliques:", cl_sizes
    return cl
    
def find_partition(graph):
    ''' Calculate partition membership, or subcommunities
    Requires code and lib from http://perso.crans.org/aynaud/communities/
    Requires an undirected graph - so convert it first.
    Returns graph, partition which is dict.  Updates the graph nodes with partition membership.
    Has commented out code that will report partition for each node.
    '''
    import community          # download the code from link above and put in same dir.
    g = graph
    partition = community.best_partition( g )
    print "Partitions found: ", len(set(partition.values()))
    # Uncomment this to show members of each partition:
    #for i in set(partition.values()):
        #members = [nodes for nodes in partition.keys() if partition[nodes] == i]
        #for member in members:
            #print member, i
    #print "Partition for node Arnicas: ", partition["arnicas"]
    nx.set_node_attributes(g,'partition',partition)
    return g, partition
     
def add_partitions_to_digraph(graph, partitiondict):
    ''' Add the partition numbers to a graph - in this case, using this to update the digraph, with partitions calc'd off the undirected graph. Yes, it's a bad hack.
    '''
    g = graph
    nx.set_node_attributes(g, 'partition', partitiondict)
    nx.info(g)
    return
        
def draw_partition(graph, partition):
    ''' Requires matplotlib.pyplot, uncomment in the top imports if you want
    to try this, but it's a useless hairy graph for the infovis data.
    Uses community code and sample from http://perso.crans.org/aynaud/communities/ to draw matplotlib graph in shades of gray
    '''
    g = graph
    count = 0
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(g)
    for com in set(partition.values()):
        count = count + 1
        list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
        nx.draw_networkx_nodes(g, pos, list_nodes, node_size = 20,
                                    node_color = str(count / size))
    nx.draw_networkx_edges(g,pos, alpha=0.5)
    plt.show()

 
def trim_nodes_by_attribute_for_remaining_number(graph, attributelist, count):
    '''Reduce the nodes by some attribute to leave only count.
    E.g., remove first 1000 from 1644 nodes by low eigenvector_centrality -- Assumes it's sorted in reverse order!
    '''
    g = graph
    to_remove = len(graph.nodes()) - count - 2
    g.remove_nodes_from([x[0] for x in attributelist[0:to_remove]])
    print "Now graph has node count: ", len(g.nodes())
    return g

def trim_nodes_by_attribute_value(graph, attributedict, threshold):
    ''' Remove nodes by values in an attributedict if lower than threshold
    Returns graph without those nodes.
    '''
    g = graph 
    g.remove_nodes_from([k for k,v in attributedict.iteritems() if v <= threshold])
    return g
    
def write_node_attributes(graph, attributes):
    ''' Print the node + various attributes in a csv format for excel/etc. Give it a series of attributes as args in list form.
    '''
    if type(attributes) is not list:
        attributes = [attributes]
    for node in graph.nodes():
        vals = [str(dict[node]) for dict in [nx.get_node_attributes(graph,x) for x in attributes]]
        print node, ",", ",".join(vals) 
        
def numeric_comp(a,b):
    print a, b, float(b) > float(a)
    return float(b) > float(a)
        
def main():

    path = ''
    inputjsonfile = 'new_json.json'

    edgesfile = urllib.urlopen(stub)
    
    g = read_in_edges(edgesfile) # my func will create a Digraph from node pairs.
    # or read in an already-created json file and modify it.
    #g = read_json_file(path + inputjsonfile)
    
    # this is the series of steps to calculate and modify the graph with node attributes...
    
    g, deg = calculate_degree(g)
    g, bet = calculate_betweenness(g)
    g, eigen = calculate_eigenvector_centrality(g)
    g, degcent = calculate_degree_centrality(g)
    
    # verify that the graph's nodes are carrying the attributes, using me in this case:
    
    report_node_data(g, node='flowingdata')
    report_node_data(g, node='infosthetics')
        
    # to print out values for a scatterplot as csv, for example, do this:
    #write_node_attributes(g, ["betweenness", "eigen_cent"])
    
    
    # to do community partitions, must have undirected graph. Convert it - just to calculate partitions.
    undir_g = g.to_undirected()
    undir_g, part = find_partition(undir_g)  # uses the community lib included about, linked from NetworkX site
    
    # super important - add the partitions found into the directed graph
    add_partitions_to_digraph(g, part)
    
    # show that the partition info is added to the nodes:
    report_node_data(g, node='arnicas')
    report_node_data(g, node='flowingdata')
    report_node_data(g, node='infosthetics')
    
    # Check my dictionary output -- use the dict from calculate_eigenvector_centrality()
    
    eigen_sorted = sorted(eigen.items(), key=lambda(k,v):(float(v),k), reverse=True)
    # just check they look resonable: 
    print len(eigen_sorted)
    for key, val in eigen_sorted[0:5]:
        print "highest eigenvector centrality nodes:", key, val

    # Here I trim what's saved to js file by taking only N nodes, with top values of a certain attribute using the dict I was returned with graph.
    # For trimming the list, you normally want it with low values on top because I cut from the top.
    
    eigen_sorted = sorted(eigen.items(), key=lambda(k,v):(float(v),k), reverse=False)
    # don't overwrite the large graph, put it in a small_graph
    print len(eigen_sorted)
    for key, val in eigen_sorted[0:5]:
        print "lowest eigenvector centrality nodes:", key, val
    
    print nx.info(g)
    
    outputjsonfile = 'full_1644nodes_test.json'
    save_to_jsonfile( path+outputjsonfile, g)
    print "Saved to new file: ", path+outputjsonfile
    
    # this function actually modifies the graph itself - so beware and don't do it before saving the big gaph above.
    small_graph = trim_nodes_by_attribute_for_remaining_number(g, eigen_sorted, 100)
    # verify it's smaller!
    print nx.info(small_graph)
    #Save as json for use in javascript - small graph, and full graph if you want.
    small_filename = "top_100eigen_test.json"
    save_to_jsonfile( path+small_filename,small_graph )
    print "Saved to new file: ", path+small_filename

#if __name__ == '__main__':
main()


''' Hey, let me know if this was useful! lynn@ghostweather.com '''
