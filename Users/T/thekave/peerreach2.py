import scraperwiki
import simplejson

##vul hier de schermnamen in van de personen die je wil scrapen. De namen moeten gescheiden worden met een comma (zonder spaties)

peer_handle = 'tijevlam'
base_url = 'http://api.peerreach.com/v1/multi-user/lookup.json?screen_name=' + peer_handle 

results_json = simplejson.loads(scraperwiki.scrape(base_url))

for result in results_json:
    data = {}
    data['user_id'] = result['user_id']
    data['profile'] = result['profile']
    data['lastupdate'] = result['lastupdate']
    data['screen_name'] = result['screen_name']
    data['followers'] = result['followers']
    data['country'] = result['country']
    data['gender'] = result['gender']
    ##peergroups = result['peergroups']
    
    ##data2 = {}
    ##data2['topic'] = result['topic']
    ##data2['region'] = result['region']
    ##data2['rank'] = result['rank']
    ##data['peergroups'] = data2
        

scraperwiki.sqlite.save(["screen_name"], data)



##data['peergroups'] = 

##nog te doen: Peergroups opsplitsen in database, topic, region, rank


    ##scraperwiki.sqlite.save(["screen_name"], data)       
                              
##print data['screen_name']import scraperwiki
import simplejson

##vul hier de schermnamen in van de personen die je wil scrapen. De namen moeten gescheiden worden met een comma (zonder spaties)

peer_handle = 'tijevlam'
base_url = 'http://api.peerreach.com/v1/multi-user/lookup.json?screen_name=' + peer_handle 

results_json = simplejson.loads(scraperwiki.scrape(base_url))

for result in results_json:
    data = {}
    data['user_id'] = result['user_id']
    data['profile'] = result['profile']
    data['lastupdate'] = result['lastupdate']
    data['screen_name'] = result['screen_name']
    data['followers'] = result['followers']
    data['country'] = result['country']
    data['gender'] = result['gender']
    ##peergroups = result['peergroups']
    
    ##data2 = {}
    ##data2['topic'] = result['topic']
    ##data2['region'] = result['region']
    ##data2['rank'] = result['rank']
    ##data['peergroups'] = data2
        

scraperwiki.sqlite.save(["screen_name"], data)



##data['peergroups'] = 

##nog te doen: Peergroups opsplitsen in database, topic, region, rank


    ##scraperwiki.sqlite.save(["screen_name"], data)       
                              
##print data['screen_name']