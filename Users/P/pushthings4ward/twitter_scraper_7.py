import urllib
import json
import scraperwiki

def getUser(pushthings4ward):
    url = 'http://api.twitter.com/1/users/show.json?screen_name=' + pushthings4ward
    user = urllib.urlopen(url).read()
    user = json.loads(user)
    data = {}
    data['id'] = user['id']
    data['name'] = user['name']
    data['screen_name'] = user['screen_name']
    data['url'] = u'http://www.twitter.com/#!/' + user['screen_name']
    data['created_at'] = user['created_at']
    data['followers'] = user['followers_count']
    data['following'] = user['friends_count']
    data['tweets'] = user['statuses_count']
    data['time_zone'] = user['time_zone']
    data['description'] = user['description']
    data['listed'] = user['listed_count']
    #mentions_url = 'http://search.twitter.com/search.json?&rpp=100&ref=' + pushthings4ward
    #mentions = urllib.urlopen(mentions_url).read()
    #mentions = json.loads(user)
    scraperwiki.sqlite.save(['id'], data, table_name='pushthings4wards')
    
    #inicializa tabela
    void = {'id': 0}
    scraperwiki.sqlite.save(['id'], void, table_name=pushthings4ward)
    

def getStatus(pushthings4ward):
    options = '&include_entities=true&include_rts=true&count=200&page='
    page = 1
    while page > 0:
        url = 'http://api.twitter.com/1/statuses/user_timeline.json?screen_name=' + pushthings4ward + options + str(page)
        full_timeline = urllib.urlopen(url).read()
        full_timeline = json.loads(full_timeline)

        if full_timeline == []:
            print 'Baixou ' + str(page) + ' paginas de ' + pushthings4ward
            page = -1
        elif 'error' in full_timeline:
            print 'Erro encontrado: ' + full_timeline['error']
            print 'Na url: ' + url
        elif scraperwiki.sqlite.select('id from %(o)s where id==%(a)s' % {'o': pushthings4ward, 'a': full_timeline[len(full_timeline)-1]['id']}):
            print 'Tweets dessa pagina ' + pushthings4ward + ' atualizados!'
            pass
        else:
            for status in full_timeline:
                timeline = {}
                timeline['id'] = str(status['id'])
                timeline['url'] = u'http://www.twitter.com/#!/' + status['user']['screen_name'] + u'/status/' + unicode(status['id'])
                timeline['texto'] = status['text']
                timeline['data'] = status['created_at']
                
                if status['retweeted'] == False:
                    timeline['retweet'] = 0
                else:
                    timeline['retweet'] = 1
                
                timeline['retweeted'] = status['retweet_count']
                
                if status['in_reply_to_screen_name'] != None:
                    timeline['reply'] = 1
                    timeline['reply_to'] = status['in_reply_to_screen_name']
                else:
                    timeline['reply'] = 0
                    timeline['reply_to'] = ''

                timeline['source'] = status['source']
                #entities
                timeline['hashtags'] = []
                for h in status['entities']['hashtags']:
                    timeline['hashtags'].append(h['text'])            
                timeline['urls'] = []
                for u in status['entities']['urls']:
                    timeline['urls'].append(u['url'])
                scraperwiki.sqlite.save(['id'], timeline, table_name=pushthings4ward)
        page += 1

pushthings4wards_done = [u'pushthings4ward']
pushthings4wards = [u'pushthings4ward']


for pushthings4ward in pushthings4wards:
    screenname = pushthings4ward
    getUser(pushthings4ward)
    getStatus(pushthings4ward)