import scraperwiki
import networkx
import time
import cPickle
from itertools import groupby
from operator import itemgetter
from time import clock

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

def get_lobbies_by_meeting(mo_data):
    return groupby(mo_data, itemgetter('meeting_hash'))#decided to preload all the lobbies by meeting hash and make a lookup table
        #if k == meeting_hash: # now this should be one query per month
           # return [value['lobby'] for value in v]
        
def process_month(mo_data, rankings):
    mgraph = networkx.MultiGraph(weighted=True)
    meetings = get_lobbies_by_meeting(mo_data)
    for k, v in meetings:
        meeting_id = k
        vals = list(v)
        item = vals[0]
        l = [value['lobby'] for value in vals]
#[row['lobby'] for row in scraperwiki.sqlite.select('lobby from safw.lobbies where meeting_hash = ?', item['meeting_hash'])] # need to do this set-wise instead, or in the original query. probably the biggest performance hit in the whole thing.
        mini = item['Minister']
        lobb = [(mini)] + l
        ranking = utr(item['Title'], item['Department'], rankings)
# maybe need to look at the utr function in performance terms - grab all the ministers in a one-er and then apply the weights?
# decided to memoise it
        weight = ranking/float(len(l))
        mgraph.add_star(lobb, weight=weight, purpose=item['Purpose of meeting'], date=item['Date'], meeting_id=k)
        mgraph.node[(mini)]['nodetype'] = 'minister'
        mgraph.node[(mini)]['minister_weight'] = ranking
        mgraph.node[(mini)]['department'] = item['Department']
        mgraph.node[(mini)]['Title'] = item['Title']
        mgraph.add_nodes_from(l, nodetype='lobby')
    return mgraph

def mini(mgraph):
    lobbies = [node for node in mgraph.nodes(data=True) if node[1]['nodetype'] == 'lobby']
    return lobbies

def meeting_count(mgraph, month, node):
    v = (mgraph[node[0]]).values()
    list_of_edges = sorted(v[0].values(), key=itemgetter('meeting_id'))
    mc = len([k for k in groupby(list_of_edges, itemgetter('meeting_id'))])
    meeting_count = {'Lobby': node[0], 'Date': month, 'Meetings': mc}
    return meeting_count

def network_degree(mgraph, month, node):
    degrees = {'Lobby': node[0], 'Date': month, 'Network Degree': mgraph.degree(node[0], weight='weight')}
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
    central = [{'Lobby': k, 'Date': month, 'Centrality': v} for k, v in nodes.iteritems() if k == mini[0]]
    return central[0]

def greedy_fragile(mgraph, month, mini, nwc, order, nodes):
    total_centrality = order * nwc
    neigh = [n for n in mgraph.neighbors(mini[0]) if len(mgraph.neighbors(n)) == 1]
    neigh_central = sum([v for k,v in nodes.iteritems() if k in neigh]) 
    order = order - (1 + len(neigh))
    mc = nodes[(mini[0])] + neigh_central
    gf = nwc - ((total_centrality - mc)/order)
    return {'Lobby': mini[0], 'Date': month, 'Greedy_Fragile': gf}

def time_munger(month): # the agonising pain of not having got the time format canonical first time around
    if isinstance(month, dict):
        month = month['Date']
    st = time.strptime(month, '%B %Y')
    return time.mktime(st)

def control_loop(lms, rankings, average_weight, nodes):
    calendar.sort(key=time_munger)
    gotdatatimer = 0
    nxtimer = 0
    lobbytimer = 0
    centralitylisttimer = 0
    nwctimer = 0
    meetingcounttimer = 0
    netdegreetimer = 0
    centralitymetricstimer = 0
    greedyfragiletimer = 0
    datawritetimer = 0
    metadatatimer = 0
    for month in calendar:
        if time_munger(month) >= time_munger(lms):
            tm = time_munger(month)
            t = clock()
            mo_data = scraperwiki.sqlite.select('* from safw.swdata inner join safw.lobbies on safw.swdata.meeting_hash = safw.lobbies.meeting_hash where date = ?', month['Date']) # get monthly meetings
            #mo_lobbies = scraperwiki.sqlite.select('meeting_hash, lobby from lobbies where meeting_hash in (select distinct meeting_hash from swdata where Date = ?)', month['Date']) # get corresponding lobbies
            gotdatatimer = gotdatatimer + clock() - t
            t = clock()
            graph = process_month(mo_data, rankings)
            nxtimer = nxtimer + clock() - t
            t = clock()
            lobbies = mini(graph)
            lobbytimer = lobbytimer + clock() - t
            t = clock()
            nodes = centrality_nodes(graph, tm)
            centralitylisttimer = centralitylisttimer + clock() - t
            t = clock()
            network_wide_centrality = float(sum(nodes.values())/len(nodes.values()))
            order = graph.order()
            nwctimer = nwctimer + clock() - t
            output = []
            for l in lobbies:
                t = clock()
                op = meeting_count(graph, month['Date'], l)
                meetingcounttimer = meetingcounttimer + clock() - t
                t = clock()
                op.update(network_degree(graph, month['Date'], l))
                netdegreetimer = netdegreetimer + clock() - t
                t = clock()
                op.update(centrality(graph, month['Date'], l, nodes))
                centralitymetricstimer = centralitymetricstimer + clock() - t
                t = clock()
                op.update(greedy_fragile(graph, month['Date'], l, network_wide_centrality, order, nodes))
                greedyfragiletimer = greedyfragiletimer + clock() - t
                output.append(op)
            t = clock()
            scraperwiki.sqlite.save(unique_keys=['Lobby', 'Date'], data=output, verbose=0)
            datawritetimer = datawritetimer + clock() - t
            t = clock()
            rs = cPickle.dumps(rankings)
            scraperwiki.sqlite.save_var('last_month_scraped', month['Date']) # log how far we got
            scraperwiki.sqlite.save_var('rankings', rs) # store the lookup table of rankings, for further saving of API calls
            metadatatimer = metadatatimer + clock() - t
            average_weight = None
            centrality.nodes = None
    print gotdatatimer, ' CPU seconds'
    print nxtimer
    print lobbytimer
    print centralitylisttimer
    print nwctimer
    print meetingcounttimer
    print netdegreetimer
    print centralitymetricstimer
    print greedyfragiletimer
    print datawritetimer
    print metadatatimer

if lms:
    control_loop(lms, rankings, average_weight, nodes)
else:
    lms = 'March 2010' # this horses' birthday is needed for the first run only
    control_loop(lms, rankings, average_weight, nodes)
