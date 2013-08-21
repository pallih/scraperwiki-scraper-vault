import scraperwiki
scraperwiki.sqlite.attach('profcoachscraper_1','data')
# Blank Python

aSyst = ['4-4-3', '4-4-2', '3-4-3', '3-5-2']

def getmax(players, playertype, number=4):
    scores = [x['player_pntscor'] for x in players if x['player_type']==playertype]
    scores.sort()
    return sum(scores[-number:])

def index_max(values):
    return max(xrange(len(values)),key=values.__getitem__)

rawteams = scraperwiki.sqlite.select("team_name from data.pcteams")
for team in rawteams:
    teamstr = team['team_name']
    rawplayers = scraperwiki.sqlite.select("* from pcteamplayers where player_team = ?",teamstr)
    rawbestplayer = scraperwiki.sqlite.select("max(player_pntscor) as best from pcteamplayers where player_team = ?",teamstr)
#    print rawbestplayer[0]['best']
    i443 = (((getmax(rawplayers, 'Keeper', 1)+getmax(rawplayers, 'Verdediger', 4)+getmax(rawplayers, 'Middenvelder', 3)+getmax(rawplayers, 'Aanvaller', 3))-rawbestplayer[0]['best'])+(2*rawbestplayer[0]['best']))
    i442 = (((getmax(rawplayers, 'Keeper', 1)+getmax(rawplayers, 'Verdediger', 4)+getmax(rawplayers, 'Middenvelder', 4)+getmax(rawplayers, 'Aanvaller', 2))-rawbestplayer[0]['best'])+(2*rawbestplayer[0]['best']))
    i343 = (((getmax(rawplayers, 'Keeper', 1)+getmax(rawplayers, 'Verdediger', 3)+getmax(rawplayers, 'Middenvelder', 4)+getmax(rawplayers, 'Aanvaller', 3))-rawbestplayer[0]['best'])+(2*rawbestplayer[0]['best']))
    i352 = (((getmax(rawplayers, 'Keeper', 1)+getmax(rawplayers, 'Verdediger', 3)+getmax(rawplayers, 'Middenvelder', 5)+getmax(rawplayers, 'Aanvaller', 2))-rawbestplayer[0]['best'])+(2*rawbestplayer[0]['best']))
    print 'Maximaal haalbare score voor ', teamstr, 'is: ', max((i443), (i442), (i343), (i352))
    print 'Beste systeem voor ', teamstr, 'is: ', aSyst[index_max([i443, i442, i343, i352])]