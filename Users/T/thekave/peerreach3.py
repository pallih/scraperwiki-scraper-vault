import scraperwiki
import simplejson

##vul hier de schermnamen in van de personen die je wil scrapen. De namen moeten gescheiden worden met een comma (zonder spaties)

peer_handle ='_Zero_e,AlexAgNL,ArnoPeels,BasHilckmann,Binnenvaartfan,connektnico,delaatstemeter,joosthelmsVVD,martiendas,martijnvdleur,unlimitdreams'

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
    result_extra = result['peergroups']
    
    for result in result_extra:
            data['topic'] = result['topic']
            data['region'] = result['region']
            data['rank'] = result['rank']
            scraperwiki.sqlite.save(["screen_name"], data)
            print data['user_id']
                              