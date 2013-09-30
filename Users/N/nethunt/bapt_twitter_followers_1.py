import scraperwiki
import simplejson
import urllib2
import sys

# This script fetches the amount of tweets, following, followers and lists for Twitter usernames
# 1: Replace 'lista' in line 13 w ur own array of Twitter usernames
# 2: Replace value of x in line 14 w number of ur nicks - not automated yet
# 3: Click 'Run', wait and copy data from "Data" tab
x = 0

#Put target nicks here on the 'lista'
lista = ['AstudioStream', 'FinlandInc', 'nethunt', 'tuija', 'tiinanis', 'anttihirvonen', 'aukia', 'petenlife', 'haloefekti', 'niku_hooli', 'Markotweet', 'apoikola', 'HannaKopra', 'JaanaHuhta', 'LyyliHamara', 'petterij', 'SalovaaraPaula', 'Jarkkosetala', 'mporrassalmi', 'avoimuus', 'heliruots', 'jukrampujut', 'Jussipekka', 'sami_vesanto', 'tosipaksu', 'villepeltola', 'YachtBar', '_harpal', 'ajhalo', 'AriHeinonen', 'CherryRobonaugh', 'ElinaLappalaine', 'JouniM', 'Juhabee', 'JussiPullinen', 'kanteletar', 'KarkkainenAri', 'Lahtius', 'lappamatti', 'MikkoAlaJuusela', 'mikkojhe', 'neppari17', 'NikoKostia', 'Sahtor', 'suomitrendit', 'tuureiko', 'up_tanja', '_kusokasa', '_nippe', 'ajakob', 'anicka2', 'anulah', 'attesakari', 'AvoinMinisterio', 'etanatikku', 'Finnfield', 'HeikkiOjala', 'Heiklap', 'HenriAhti', 'henriholli', 'hesep', 'HessuHei', 'hmhahto', 'Huuhkaja1', 'Huumetietoa', 'ilkkapirttimaa', 'Jaakko', 'JaakkoKarhu', 'jannejuhani', 'jennisofia88', 'jonnujee', 'joonahermanni', 'JoonasAutio', 'jormalohman', 'JoukoSalonen', 'jphei', 'jtennila', 'JuhaniHuhtala', 'Jukka_Piiroinen', 'jussilehto', 'kaaiia', 'kalske', 'katjaronkko', 'kille2012', 'KimmoMatikainen', 'lakineuvoja', 'Lapsellisia', 'LKarppi', 'MaaritPiip', 'Makke93', 'mikamartikainen', 'minnik', 'MoikkaSanni', 'mrusila', 'nikojuntunen', 'OlaviRuohomaa', 'PauliinaTee', 'pierrepetrelli', 'ptonteri', 'rakelliekki', 'Saimurajen', 'samipkoivisto', 'slotte', 'Taneli_Heikka', 'TaruPeltola', 'Vaaliliitto', 'vesailola', 'Viranomainen', 'Virva_', 'VKautto', 'vppekkola']
while x <100:
 
    x = x + 1
    SCREENNAME = lista[x]

    url = 'http://api.twitter.com/1/users/lookup.json?screen_name=%s' % (urllib2.quote(SCREENNAME))
    print 'getting url:', url
    details_json = simplejson.loads(scraperwiki.scrape(url))
    print details_json
    for detail in details_json:
        data = {'screen_name': detail['screen_name'],
        'id': detail['id'],
        'followers_count': detail['followers_count'],
        'friends_count': detail['friends_count'],
        'statuses_count': detail['statuses_count'],
        'listed_count': detail['listed_count']}
        scraperwiki.sqlite.save(unique_keys=['id'], data = data)
import scraperwiki
import simplejson
import urllib2
import sys

# This script fetches the amount of tweets, following, followers and lists for Twitter usernames
# 1: Replace 'lista' in line 13 w ur own array of Twitter usernames
# 2: Replace value of x in line 14 w number of ur nicks - not automated yet
# 3: Click 'Run', wait and copy data from "Data" tab
x = 0

#Put target nicks here on the 'lista'
lista = ['AstudioStream', 'FinlandInc', 'nethunt', 'tuija', 'tiinanis', 'anttihirvonen', 'aukia', 'petenlife', 'haloefekti', 'niku_hooli', 'Markotweet', 'apoikola', 'HannaKopra', 'JaanaHuhta', 'LyyliHamara', 'petterij', 'SalovaaraPaula', 'Jarkkosetala', 'mporrassalmi', 'avoimuus', 'heliruots', 'jukrampujut', 'Jussipekka', 'sami_vesanto', 'tosipaksu', 'villepeltola', 'YachtBar', '_harpal', 'ajhalo', 'AriHeinonen', 'CherryRobonaugh', 'ElinaLappalaine', 'JouniM', 'Juhabee', 'JussiPullinen', 'kanteletar', 'KarkkainenAri', 'Lahtius', 'lappamatti', 'MikkoAlaJuusela', 'mikkojhe', 'neppari17', 'NikoKostia', 'Sahtor', 'suomitrendit', 'tuureiko', 'up_tanja', '_kusokasa', '_nippe', 'ajakob', 'anicka2', 'anulah', 'attesakari', 'AvoinMinisterio', 'etanatikku', 'Finnfield', 'HeikkiOjala', 'Heiklap', 'HenriAhti', 'henriholli', 'hesep', 'HessuHei', 'hmhahto', 'Huuhkaja1', 'Huumetietoa', 'ilkkapirttimaa', 'Jaakko', 'JaakkoKarhu', 'jannejuhani', 'jennisofia88', 'jonnujee', 'joonahermanni', 'JoonasAutio', 'jormalohman', 'JoukoSalonen', 'jphei', 'jtennila', 'JuhaniHuhtala', 'Jukka_Piiroinen', 'jussilehto', 'kaaiia', 'kalske', 'katjaronkko', 'kille2012', 'KimmoMatikainen', 'lakineuvoja', 'Lapsellisia', 'LKarppi', 'MaaritPiip', 'Makke93', 'mikamartikainen', 'minnik', 'MoikkaSanni', 'mrusila', 'nikojuntunen', 'OlaviRuohomaa', 'PauliinaTee', 'pierrepetrelli', 'ptonteri', 'rakelliekki', 'Saimurajen', 'samipkoivisto', 'slotte', 'Taneli_Heikka', 'TaruPeltola', 'Vaaliliitto', 'vesailola', 'Viranomainen', 'Virva_', 'VKautto', 'vppekkola']
while x <100:
 
    x = x + 1
    SCREENNAME = lista[x]

    url = 'http://api.twitter.com/1/users/lookup.json?screen_name=%s' % (urllib2.quote(SCREENNAME))
    print 'getting url:', url
    details_json = simplejson.loads(scraperwiki.scrape(url))
    print details_json
    for detail in details_json:
        data = {'screen_name': detail['screen_name'],
        'id': detail['id'],
        'followers_count': detail['followers_count'],
        'friends_count': detail['friends_count'],
        'statuses_count': detail['statuses_count'],
        'listed_count': detail['listed_count']}
        scraperwiki.sqlite.save(unique_keys=['id'], data = data)
