# bibliotecas necessárias

import scraperwiki
import scraperwiki
import simplejson
import urllib2
import sys

# nome precisa ser em letras minúsculas

SCREENNAME = 'marcelo_barrett'

# pulo do gato: API de ajuda: http://dev.twitter.com/docs/api/1/get/following/ids

url = 'http://api.twitter.com/1/following/ids.json?screen_name=%s' % (urllib2.quote(SCREENNAME))
print url
followers_json = simplejson.loads(scraperwiki.scrape(url))
print "Found %d followers of %s" % (len(followers_json), SCREENNAME)
print followers_json
followers_json = followers_json['ids'] # obter os primeiros seguidores primeiro para batching
followers_json.reverse()
print followers_json 

# Grupos de uma lista de blocos de um determinado tamanho

def group(lst, n):
    for i in range(0, len(lst), n):
        val = lst[i:i+n]
        if len(val) == n:
            yield tuple(val)

# Por onde começar? Sobreponha um lote para aumentar a taxa de acerto, se deixar de seguir as pessoas, etc

batchdone = scraperwiki.sqlite.get_var('batchdone', 1)
batchstart = batchdone - 1
if batchstart < 1:
    batchstart = 1

# Pegue 100 por vez e não uma chamada de pesquisa (lookup call) para cada lote batch

c = 0
for follower_list in group(followers_json, 100):
    c = c + 1
    if c < batchstart:
        continue
    print "number", c, "out of", len(followers_json) / 100
    print 'batch of ids:', follower_list
    url = 'http://api.twitter.com/1/users/lookup.json?user_id=%s' % (urllib2.quote(','.join(map(str, follower_list))))
    print 'getting url:', url
    details_json = simplejson.loads(scraperwiki.scrape(url))
    for detail in details_json:
        data = {'screen_name': detail['screen_name'],'id': detail['id'],'location': detail['location'], 'bio': detail['description']}
        print "Found person", data
        scraperwiki.sqlite.save(unique_keys=['id'], data = data)
    scraperwiki.sqlite.save_var('batchdone', c)





