import scraperwiki,urllib2,json

import os, cgi,datetime
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    pikey=qsenv["PEERINDEX_KEY"]
    kloutkey=qsenv["KLOUT_KEY"]
except:
    pikey=''
    kloutkey=''



russellListURL='https://api.twitter.com/1/lists/members.json?slug=russell-group-members&owner_screen_name=gigitsui&cursor'
jdata=json.load(urllib2.urlopen(russellListURL))
russellUnis=jdata['users']
#print russellUnis
while jdata['next_cursor']!=0:
    russellListURL='https://api.twitter.com/1/lists/members.json?slug=russell-group-members&owner_screen_name=gigitsui&cursor='+str(jdata['next_cursor'])
    jdata=json.load(urllib2.urlopen(russellListURL))
    russellUnis=russellUnis+jdata['users']

def chunks(l, n):   
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

print len(russellUnis)
unilist=[]
for uni in russellUnis:
    unilist.append(uni['screen_name'])

print len(unilist)

currtime=datetime.datetime.now()

kldata={}
if kloutkey!='':
    uniChunks=chunks(unilist,5)
    for unichunk in uniChunks:
        uniOnelist=','.join(unichunk)
        print uniOnelist
        klURL='http://api.klout.com/1/users/show.json?key='+kloutkey+'&users='+uniOnelist
        kljdata=json.load(urllib2.urlopen(klURL))
        print kldata
        for kl in kljdata['users']:
            #print kl
            kls=kl['score']
            kldata[kl['twitter_screen_name']] = {'kl_kscore':kls['kscore'], 'kl_true_reach':kls['true_reach'],'kl_amplification_score':kls['amplification_score'], 'kl_network_score':kls['network_score']}
            
#{u'score': {u'slope': -0.01, u'kclass_description': u'You broadcast great content that spreads like wildfire. You are an essential information source in your industry. You have a large and diverse audience that values your content.', u'amplification_score': 8, u'kscore': 59.9, u'description': u'creates content that is spread throughout their network and drives discussions', u'true_reach': 1815, u'kscore_description': u'creates content that is spread throughout their network and drives discussions', u'delta_5day': -0.55, u'kclass_id': 7, u'network_score': 29.26, u'delta_1day': -0.1, u'kclass': u'Broadcaster'}, u'twitter_id': u'27035508', u'twitter_screen_name': u'UniOfYork'}

for uni in russellUnis:
    data={'td':currtime}
    data['tw_screen_name']=uni['screen_name']
    data['tw_friends_count']=uni['friends_count']
    data['tw_followers_count']=uni['followers_count']
    data['tw_listed_count']=uni['listed_count']
    data['tw_statuses_count']=uni['statuses_count']
    data['tw_name']=uni['name']
    data['tw_description']=uni['description']

    for x in kldata[uni['screen_name']]:
        data[x]=kldata[uni['screen_name']][x]
        
    if pikey!='':
        piURL='http://api.peerindex.net/v2/profile/profile.json?id='+uni['screen_name']+'&api_key='+pikey
        pijdata=json.load(urllib2.urlopen(piURL))
        #print pijdata
        #peerindex': 61, u'twitter': u'uniofyork', u'authority': 43, u'audience': 71, u'activity': 46
        data['pi_peerindex']=pijdata['peerindex']
        data['pi_authority']=pijdata['authority']
        data['pi_audience']=pijdata['audience']
        data['pi_activity']=pijdata['activity']
    scraperwiki.sqlite.save(unique_keys=[],table_name='smdata', data=data)

import scraperwiki,urllib2,json

import os, cgi,datetime
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    pikey=qsenv["PEERINDEX_KEY"]
    kloutkey=qsenv["KLOUT_KEY"]
except:
    pikey=''
    kloutkey=''



russellListURL='https://api.twitter.com/1/lists/members.json?slug=russell-group-members&owner_screen_name=gigitsui&cursor'
jdata=json.load(urllib2.urlopen(russellListURL))
russellUnis=jdata['users']
#print russellUnis
while jdata['next_cursor']!=0:
    russellListURL='https://api.twitter.com/1/lists/members.json?slug=russell-group-members&owner_screen_name=gigitsui&cursor='+str(jdata['next_cursor'])
    jdata=json.load(urllib2.urlopen(russellListURL))
    russellUnis=russellUnis+jdata['users']

def chunks(l, n):   
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

print len(russellUnis)
unilist=[]
for uni in russellUnis:
    unilist.append(uni['screen_name'])

print len(unilist)

currtime=datetime.datetime.now()

kldata={}
if kloutkey!='':
    uniChunks=chunks(unilist,5)
    for unichunk in uniChunks:
        uniOnelist=','.join(unichunk)
        print uniOnelist
        klURL='http://api.klout.com/1/users/show.json?key='+kloutkey+'&users='+uniOnelist
        kljdata=json.load(urllib2.urlopen(klURL))
        print kldata
        for kl in kljdata['users']:
            #print kl
            kls=kl['score']
            kldata[kl['twitter_screen_name']] = {'kl_kscore':kls['kscore'], 'kl_true_reach':kls['true_reach'],'kl_amplification_score':kls['amplification_score'], 'kl_network_score':kls['network_score']}
            
#{u'score': {u'slope': -0.01, u'kclass_description': u'You broadcast great content that spreads like wildfire. You are an essential information source in your industry. You have a large and diverse audience that values your content.', u'amplification_score': 8, u'kscore': 59.9, u'description': u'creates content that is spread throughout their network and drives discussions', u'true_reach': 1815, u'kscore_description': u'creates content that is spread throughout their network and drives discussions', u'delta_5day': -0.55, u'kclass_id': 7, u'network_score': 29.26, u'delta_1day': -0.1, u'kclass': u'Broadcaster'}, u'twitter_id': u'27035508', u'twitter_screen_name': u'UniOfYork'}

for uni in russellUnis:
    data={'td':currtime}
    data['tw_screen_name']=uni['screen_name']
    data['tw_friends_count']=uni['friends_count']
    data['tw_followers_count']=uni['followers_count']
    data['tw_listed_count']=uni['listed_count']
    data['tw_statuses_count']=uni['statuses_count']
    data['tw_name']=uni['name']
    data['tw_description']=uni['description']

    for x in kldata[uni['screen_name']]:
        data[x]=kldata[uni['screen_name']][x]
        
    if pikey!='':
        piURL='http://api.peerindex.net/v2/profile/profile.json?id='+uni['screen_name']+'&api_key='+pikey
        pijdata=json.load(urllib2.urlopen(piURL))
        #print pijdata
        #peerindex': 61, u'twitter': u'uniofyork', u'authority': 43, u'audience': 71, u'activity': 46
        data['pi_peerindex']=pijdata['peerindex']
        data['pi_authority']=pijdata['authority']
        data['pi_audience']=pijdata['audience']
        data['pi_activity']=pijdata['activity']
    scraperwiki.sqlite.save(unique_keys=[],table_name='smdata', data=data)

