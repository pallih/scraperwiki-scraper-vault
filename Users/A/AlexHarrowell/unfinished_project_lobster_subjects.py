import scraperwiki
import networkx
import time
import cPickle
from itertools import groupby
from operator import itemgetter

scraperwiki.sqlite.attach('sql_api_for_whoslobbying', 'safw')
scraperwiki.sqlite.attach('project_lobster_constants', 'constants')
lms = scraperwiki.sqlite.get_var('last_month_scraped')
calendar = scraperwiki.sqlite.select('DISTINCT Date from safw.swdata')
r = scraperwiki.sqlite.get_var('rankings')

if r:
    rankings = cPickle.loads(r)  #bucket for caching ministerial weightings. after each month, the cache is written to the db
else: # retrieved at startup. if nothing there (i.e. a cold start) it is set to an empty dictionary
    rankings = {}

average_weight = None
nodes = None

# function for setting ministers' weightings
def utr(minister, department, rankings): #it was called uptown_top_ranking in the proof of concept
    k = minister + department
    if k in rankings:
        return rankings[(k)] # caching to reduce API traffic
    else:
        m = ((minister.split('('))[0]).rstrip()
        d = scraperwiki.sqlite.select('weight from constants.departments where department = ?', [department])
        department_rank = d[0]['weight']
        p = scraperwiki.sqlite.select('weight from constants.ministers where minister like ?', [('%'+(m)+'%')])
        personal_rank = p[0]['weight']
    # a minister's weighting is determined by their department's importance and their personal importance
        ranking = department_rank/personal_rank
        rankings[(k)] = ranking # i.e store the result under this job/department combination
        return ranking

def get_ministers_by_meeting(mo_data):
    return groupby(mo_data, itemgetter('meeting_hash'))
        
        
def process_month(mo_data, rankings):
    mgraph = networkx.MultiGraph(weighted=True)
    meetings = get_ministers_by_meeting(mo_data)
    for k, v in meetings:
        meeting_id = k
        vals = list(v)
        item = vals[0]
        mini = item['Minister']
        l = [value['Purpose of meeting'] if value['Purpose of meeting'] is not None else 'NOTSTATED' for value in vals]
        lobb = [(mini)] + l
        ranking = utr(item['Title'], item['Department'], rankings)
    # maybe need to look at the utr function in performance terms - grab all the ministers in a one-er and then apply the weights?
    # decided to memoise it
        weight = ranking/float(len(l))
        mgraph.add_star(lobb, weight=weight, lobby=item['lobby'], date=item['Date'], meeting_id=item['meeting_hash'])
        mgraph.node[(mini)]['nodetype'] = 'minister'
        mgraph.node[(mini)]['minister_weight'] = ranking
        mgraph.node[(mini)]['Department'] = item['Department']
        mgraph.node[(mini)]['Title'] = item['Title']
        mgraph.add_nodes_from(l, nodetype='subject')
    return mgraph

def subject(mgraph):
    subjects = [node for node in mgraph.nodes(data=True) if node[1]['nodetype'] == 'subject']
    return subjects

def meeting_count(mgraph, month, node):
    v = (mgraph[node[0]]).values()
    list_of_edges = sorted(v[0].values(), key=itemgetter('meeting_id'))
    mc = len([k for k in groupby(list_of_edges, itemgetter('meeting_id'))])
    meeting_count = {'Subject': node[0], 'Date': month, 'Meetings': mc}
    return meeting_count

def network_degree(mgraph, month, node):
    degrees = {'Subject': node[0], 'Date': month, 'Network Degree': mgraph.degree(node[0], weight='weight')}
    return degrees

def centrality_nodes(mgraph, tm):
    def cn(mgraph):
        cn = networkx.algorithms.centrality.betweenness_centrality(mgraph, normalized=True, weight='weight')
        centrality_nodes.nodes = cn
        centrality_nodes.tm = tm
        return cn
    if not hasattr(centrality_nodes, 'tm'):
           return cn(mgraph)
    else:
           if centrality_nodes.tm >= tm:
               centrality_nodes.tm = tm
               return centrality_nodes.nodes
           else:
               return cn(mgraph)

def centrality(mgraph, month, mini, nodes):
    central = [{'Subject': k, 'Date': month, 'Centrality': v} for k,v in nodes.iteritems() if k == mini[0]]
    return central[0]

def greedy_fragile(mgraph, month, mini, nwc, order, nodes):
    total_centrality = order * nwc
    neigh = [n for n in mgraph.neighbors(mini[0]) if len(mgraph.neighbors(n)) == 1]
    neigh_central = sum([v for k,v in nodes.iteritems() if k in neigh])  
    order = order - (1 + len(neigh))
    mc = nodes[(mini[0])] + neigh_central
    gf = nwc - ((total_centrality - mc)/order)
    return {'Subject': mini[0], 'Date': month, 'Greedy_Fragile': gf}

def time_munger(month): # the agonising pain of not having got the time format canonical first time around
    if isinstance(month, dict):
        month = month['Date']
    st = time.strptime(month, '%B %Y')
    return time.mktime(st)

def control_loop(lms, rankings, average_weight, nodes):
    calendar.sort(key=time_munger)
    for month in calendar:
        if time_munger(month) >= time_munger(lms):
            tm = time_munger(month)
            mo_data = scraperwiki.sqlite.select('* from safw.swdata inner join safw.lobbies on safw.swdata.meeting_hash = safw.lobbies.meeting_hash where date = ?', month['Date'])
            #mo_lobbies = scraperwiki.sqlite.select('meeting_hash, lobby from lobbies where meeting_hash in (select distinct meeting_hash from swdata where Date = ?)', month['Date']) # get corresponding lobbies
            graph = process_month(mo_data, rankings)
            subjects = subject(graph)
            nodes = centrality_nodes(graph, tm)
            network_wide_centrality = float(sum(nodes.values())/len(nodes.values()))
            order = graph.order()
            output = []
            for m in subjects:
                op = meeting_count(graph, month['Date'], m)
                op.update(network_degree(graph, month['Date'], m))
                op.update(centrality(graph, month['Date'], m, nodes))
                op.update(greedy_fragile(graph, month['Date'], m, network_wide_centrality, order, nodes))
                output.append(op)
            scraperwiki.sqlite.save(unique_keys=['Subject', 'Date'], data=output, verbose=0)
            rs = cPickle.dumps(rankings)
            scraperwiki.sqlite.save_var('last_month_scraped', month['Date']) # log how far we got
            scraperwiki.sqlite.save_var('rankings', rs) # store the lookup table of rankings, for further saving of API calls
            nodes = None
            average_weight = None
if lms:
    control_loop(lms, rankings, average_weight, nodes)
else:
    lms = 'March 2010' # this horses' birthday is needed for the first run only
    control_loop(lms, rankings, average_weight, nodes)
