import scraperwiki
import lxml.html

index_homePlayers = 6
index_awayPlayers = 8
index_homeScorers = 2
index_awayScorers = 3
index_referee     = 4
index_attendance  = 5
index_homeManager = 6
index_awayManager = 7
index_location    = 8

for i in range(1348, 4858):
    html = scraperwiki.scrape("http://www.veikkausliiga.com/ottelutiedot.asp?id=" + str(i))
    root = lxml.html.fromstring(html)
    
    title = root.cssselect("td.joukkue_otsikko font")[0].text
    date = title[:title.index(' ')]
    res = title[title.rfind(' '):]
    
    teams = title[title.index(' ') + 1:title.rfind(' ')]
    sep = teams.index('-')

    if teams.startswith("PK-35") or teams.startswith("TP-47") or teams.startswith("TP-Sein"):
        sep = teams.rfind('-')
        
    team1 = teams[:sep]
    team2 = teams[sep + 1:]

    players = root.cssselect("tr td")
    homePlayers = [x.strip() for x in players[index_homePlayers].text_content()[len(team1) + 3:].split(',')]
    awayPlayers = [x.strip() for x in players[index_awayPlayers].text_content()[len(team2) + 3:].split(',')]

    info = root.cssselect("td.joukkuetiedot")
    homeScorers = [x.strip() for x in info[index_homeScorers].getnext().text[len(team1) + 3:].split(',')]
    awayScorers = [x.strip() for x in info[index_awayScorers].getnext().text[len(team2) + 3:].split(',')]

    referee = info[index_referee].getnext().text
    attendance = info[index_attendance].getnext().text

    homeManager = info[index_homeManager].getnext().text
    awayManager = info[index_awayManager].getnext().text
    location = info[index_location].getnext().text
    
    id = i - 999

    data = {"id":id,
            "date":date,
            "result":res,
            "homeTeam":team1,
            "awayTeam":team2,
            "homeSquad":homePlayers,
            "awaySquad":awayPlayers,   
            "homeScorers":homeScorers,
            "awayScorers":awayScorers,
            "referee":referee,
            "attendance":attendance,
            "homeManager":homeManager,
            "awayManager":awayManager,
            "location":location
    }

    scraperwiki.sqlite.save(unique_keys=["id"], data=data)
    
    #print ", ".join([referee, attendance, homeManager, awayManager, location])
    #print ", ".join([team1, team2])

