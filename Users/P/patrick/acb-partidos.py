# Blank Python
sourcescraper = 'acbcom_-_partidos_detailed'
import scraperwiki
scraperwiki.sqlite.attach(sourcescraper,'partidos')
#'GameId', 'LeagueCod', 'Season', 'GameNum', 'HomeTeam', 'HomeScore', 'HomeScoreP', 'VisTeam', 'VisScore', 'VisScoreP'
data = scraperwiki.sqlite.select(           
    '''GameId,LeagueCod,Season,GameNum,HomeTeam,HomeScore,VisTeam,VisScore,HomeScoreP,VisScoreP from partidos.swdata 
    order by Season desc limit 10 '''
)
#print data
for d in data:
    #print d.viewvalues()
    print d["GameId"]+','+d["LeagueCod"]+','+d["Season"]+','+d["GameNum"]+','+d["HomeTeam"]+','+d["HomeScore"]+','+d["VisTeam"]+','+d["VisScore"]+','+d["HomeScoreP"]+','+d["VisScoreP"]
#    print "<td>", d["Season"], "</td>"
#    print "<td>", d["HomeTeam"], "</td>"
#    print "</tr>"
#print "</table>"# Blank Python
sourcescraper = 'acbcom_-_partidos_detailed'
import scraperwiki
scraperwiki.sqlite.attach(sourcescraper,'partidos')
#'GameId', 'LeagueCod', 'Season', 'GameNum', 'HomeTeam', 'HomeScore', 'HomeScoreP', 'VisTeam', 'VisScore', 'VisScoreP'
data = scraperwiki.sqlite.select(           
    '''GameId,LeagueCod,Season,GameNum,HomeTeam,HomeScore,VisTeam,VisScore,HomeScoreP,VisScoreP from partidos.swdata 
    order by Season desc limit 10 '''
)
#print data
for d in data:
    #print d.viewvalues()
    print d["GameId"]+','+d["LeagueCod"]+','+d["Season"]+','+d["GameNum"]+','+d["HomeTeam"]+','+d["HomeScore"]+','+d["VisTeam"]+','+d["VisScore"]+','+d["HomeScoreP"]+','+d["VisScoreP"]
#    print "<td>", d["Season"], "</td>"
#    print "<td>", d["HomeTeam"], "</td>"
#    print "</tr>"
#print "</table>"